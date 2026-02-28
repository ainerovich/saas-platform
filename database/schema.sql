-- SaaS Platform Database Schema
-- PostgreSQL 15+

-- Расширения
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- CORE TABLES (платформа)
-- ============================================

-- Тенанты (клиенты платформы)
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,                    -- Субдомен или свой домен
    logo_url VARCHAR(500),                          -- White-label лого
    primary_color VARCHAR(7) DEFAULT '#FF6B00',    -- HEX цвет бренда
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Пользователи
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'user',                -- admin, user, viewer
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    UNIQUE(tenant_id, email)
);

-- Подписки
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    plan VARCHAR(50) NOT NULL,                      -- basic, pro, enterprise
    modules JSONB DEFAULT '{}',                     -- {"avito_parser": true, "vpn": true}
    price_monthly INTEGER NOT NULL,                 -- Копейки
    status VARCHAR(50) DEFAULT 'active',            -- active, cancelled, expired
    started_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    auto_renew BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Платежи
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    subscription_id INTEGER REFERENCES subscriptions(id),
    amount INTEGER NOT NULL,                        -- Копейки
    currency VARCHAR(3) DEFAULT 'RUB',
    provider VARCHAR(50) DEFAULT 'yookassa',
    provider_payment_id VARCHAR(255),
    status VARCHAR(50) DEFAULT 'pending',           -- pending, succeeded, canceled
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    paid_at TIMESTAMP
);

CREATE INDEX idx_payments_tenant ON payments(tenant_id);
CREATE INDEX idx_payments_status ON payments(status);

-- Модули (метаинформация)
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(50) UNIQUE NOT NULL,               -- avito_parser, vpn_service
    name VARCHAR(255) NOT NULL,
    description TEXT,
    icon VARCHAR(255),                               -- URL иконки
    price_monthly INTEGER DEFAULT 0,                 -- Копейки
    is_available BOOLEAN DEFAULT true,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Начальные модули
INSERT INTO modules (slug, name, description, icon, price_monthly, sort_order) VALUES
('avito_parser', 'Avito Parser', 'Парсинг объявлений с Avito и автопубликация в VK/Telegram', '🔍', 99000, 1),
('vpn_service', 'VPN Generator', 'Генерация WireGuard VPN ключей через Telegram бота', '🔐', 49000, 2),
('news_aggregator', 'News Aggregator', 'Сбор и фильтрация новостей из VK/Telegram', '📰', 69000, 3),
('birthday_bot', 'Birthday Bot', 'Автоматические поздравления с днём рождения в VK', '🎉', 39000, 4),
('music_lotto', 'Music Lotto', 'Музыкальное лото с VK трансляцией', '🎵', 149000, 5),
('vk_quests', 'VK Quests', 'Игровые квесты в комментариях VK', '🎮', 59000, 6),
('bot_constructor', 'Bot Constructor', 'Конструктор ботов для VK/Telegram', '🤖', 79000, 7);

-- Статусы модулей (Health Monitor)
CREATE TABLE module_health (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    module_slug VARCHAR(50) REFERENCES modules(slug),
    status VARCHAR(50) DEFAULT 'unknown',           -- healthy, degraded, down, unknown
    last_check TIMESTAMP DEFAULT NOW(),
    error_message TEXT,
    response_time_ms INTEGER,
    metadata JSONB
);

CREATE INDEX idx_module_health_tenant ON module_health(tenant_id);
CREATE INDEX idx_module_health_module ON module_health(module_slug);

-- ============================================
-- ОБЩИЕ РЕСУРСЫ
-- ============================================

-- Прокси пул (общий для всех модулей)
CREATE TABLE proxies (
    id SERIAL PRIMARY KEY,
    url VARCHAR(500) NOT NULL UNIQUE,               -- http://user:pass@host:port
    type VARCHAR(50) DEFAULT 'http',                -- http, https, socks5
    is_alive BOOLEAN DEFAULT true,
    last_check TIMESTAMP,
    fail_count INTEGER DEFAULT 0,
    response_time_ms INTEGER,
    country VARCHAR(2),                              -- Код страны (RU, US)
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_proxies_alive ON proxies(is_alive);

-- Токены VK/TG (общие)
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,                  -- vk, telegram
    token_type VARCHAR(50) NOT NULL,                -- user_token, group_token, bot_token
    token_value TEXT NOT NULL,
    scope TEXT,                                      -- OAuth scope
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tokens_tenant ON tokens(tenant_id);
CREATE INDEX idx_tokens_platform ON tokens(platform);

-- ============================================
-- MODULE: AVITO PARSER
-- ============================================

-- Единицы (units)
CREATE TABLE avito_units (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    city_slug VARCHAR(100) NOT NULL,
    vk_group_id VARCHAR(100),
    telegram_channel_id VARCHAR(100),
    is_enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_avito_units_tenant ON avito_units(tenant_id);

-- Источники (категории Avito)
CREATE TABLE avito_sources (
    id SERIAL PRIMARY KEY,
    unit_id INTEGER REFERENCES avito_units(id) ON DELETE CASCADE,
    category VARCHAR(100) NOT NULL,
    url_path VARCHAR(255),
    signature VARCHAR(50),
    is_enabled BOOLEAN DEFAULT false
);

-- Объявления
CREATE TABLE avito_ads (
    id SERIAL PRIMARY KEY,
    unit_id INTEGER REFERENCES avito_units(id) ON DELETE CASCADE,
    source_id INTEGER REFERENCES avito_sources(id),
    avito_id VARCHAR(100) UNIQUE NOT NULL,
    title TEXT NOT NULL,
    price INTEGER,
    description TEXT,
    url TEXT,
    image_url TEXT,
    published_vk BOOLEAN DEFAULT false,
    published_tg BOOLEAN DEFAULT false,
    scraped_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_avito_ads_unit ON avito_ads(unit_id);
CREATE INDEX idx_avito_ads_avito_id ON avito_ads(avito_id);

-- ============================================
-- MODULE: VPN SERVICE
-- ============================================

-- VPN ключи
CREATE TABLE vpn_keys (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    config_name VARCHAR(255) NOT NULL,
    public_key VARCHAR(255) NOT NULL UNIQUE,
    private_key_encrypted TEXT NOT NULL,           -- Зашифрованный приватный ключ
    ip_address VARCHAR(50) NOT NULL UNIQUE,
    qr_code_url VARCHAR(500),
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    last_handshake TIMESTAMP,
    traffic_rx BIGINT DEFAULT 0,
    traffic_tx BIGINT DEFAULT 0
);

CREATE INDEX idx_vpn_keys_tenant ON vpn_keys(tenant_id);
CREATE INDEX idx_vpn_keys_active ON vpn_keys(is_active);

-- ============================================
-- MODULE: NEWS AGGREGATOR
-- ============================================

-- Источники новостей
CREATE TABLE news_sources (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,                  -- vk, telegram, rss
    source_id VARCHAR(255),                          -- ID группы/канала
    source_url VARCHAR(500),
    is_enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Фильтры
CREATE TABLE news_filters (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    keywords JSONB DEFAULT '[]',                    -- ["блокчейн", "AI"]
    exclude_keywords JSONB DEFAULT '[]',
    min_likes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Новости
CREATE TABLE news_items (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES news_sources(id) ON DELETE CASCADE,
    title TEXT,
    content TEXT,
    url TEXT,
    image_url TEXT,
    published_at TIMESTAMP,
    likes INTEGER DEFAULT 0,
    is_published BOOLEAN DEFAULT false,
    scraped_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_news_items_source ON news_items(source_id);
CREATE INDEX idx_news_items_published ON news_items(is_published);

-- ============================================
-- MODULE: MUSIC LOTTO
-- ============================================

-- Игры
CREATE TABLE lotto_games (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    scheduled_at TIMESTAMP NOT NULL,
    vk_stream_url TEXT,
    status VARCHAR(50) DEFAULT 'scheduled',         -- scheduled, live, finished
    winner_user_id INTEGER REFERENCES users(id),
    ticket_price INTEGER DEFAULT 1000,              -- Копейки
    max_tickets INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Билеты
CREATE TABLE lotto_tickets (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES lotto_games(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    numbers JSONB NOT NULL,                         -- [1, 5, 12, 18, 24, ...]
    is_winner BOOLEAN DEFAULT false,
    purchased_at TIMESTAMP DEFAULT NOW()
);

-- Числа в игре (история розыгрыша)
CREATE TABLE lotto_drawn_numbers (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES lotto_games(id) ON DELETE CASCADE,
    number INTEGER NOT NULL,
    drawn_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_lotto_tickets_game ON lotto_tickets(game_id);
CREATE INDEX idx_lotto_drawn_game ON lotto_drawn_numbers(game_id);

-- ============================================
-- TRIGGERS (автообновление updated_at)
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_tenants_updated_at BEFORE UPDATE ON tenants
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- VIEWS (удобные выборки)
-- ============================================

-- Статус подписок
CREATE VIEW subscription_status AS
SELECT 
    s.*,
    t.name AS tenant_name,
    t.domain,
    CASE 
        WHEN s.expires_at < NOW() THEN 'expired'
        WHEN s.expires_at < NOW() + INTERVAL '7 days' THEN 'expiring_soon'
        ELSE 'active'
    END AS subscription_status
FROM subscriptions s
JOIN tenants t ON s.tenant_id = t.id;

-- Статистика модулей
CREATE VIEW module_stats AS
SELECT 
    m.slug,
    m.name,
    COUNT(DISTINCT mh.tenant_id) AS active_tenants,
    AVG(mh.response_time_ms) AS avg_response_time,
    SUM(CASE WHEN mh.status = 'healthy' THEN 1 ELSE 0 END)::FLOAT / COUNT(*)::FLOAT AS health_percentage
FROM modules m
LEFT JOIN module_health mh ON m.slug = mh.module_slug
WHERE mh.last_check > NOW() - INTERVAL '1 hour'
GROUP BY m.slug, m.name;
