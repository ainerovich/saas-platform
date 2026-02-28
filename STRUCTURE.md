# SaaS Platform - Полная структура проекта

## Обзор

**Название:** AgentHub (рабочее)
**Концепт:** White-label мультимодульная SaaS платформа для автоматизации

**Готовые модули:**
1. ✅ **Avito Parser** - почти готов (нужны прокси)
2. ✅ **VPN Service** - готов (исправлен роутинг)

**В разработке:**
3. 🚧 News Aggregator
4. 🚧 Birthday Bot
5. 🚧 Music Lotto
6. 🚧 VK Quests
7. 🚧 Bot Constructor

---

## Файловая структура

```
/var/www/saas-platform/
├── backend/
│   ├── core/                    # Общее ядро
│   │   ├── __init__.py
│   │   ├── config.py           # Конфигурация платформы
│   │   ├── database.py         # DB connector (PostgreSQL)
│   │   ├── auth.py             # JWT авторизация
│   │   ├── models.py           # Общие модели (User, Tenant, Subscription)
│   │   └── utils.py            # Общие утилиты
│   │
│   ├── proxy_pool/             # Общий пул прокси
│   │   ├── __init__.py
│   │   ├── manager.py          # Управление прокси
│   │   ├── checker.py          # Автопроверка (живой/мёртвый)
│   │   └── api.py              # API для модулей
│   │
│   ├── token_manager/          # Управление токенами VK/TG
│   │   ├── __init__.py
│   │   ├── vk_tokens.py        # VK токены + OAuth flow
│   │   ├── tg_tokens.py        # Telegram токены
│   │   └── api.py              # API для модулей
│   │
│   ├── billing/                # Платежи
│   │   ├── __init__.py
│   │   ├── models.py           # Payment, Invoice, Subscription
│   │   ├── yookassa.py         # ЮKassa интеграция
│   │   ├── webhooks.py         # Webhook обработчики
│   │   └── api.py              # API платежей
│   │
│   ├── modules/                # Модули (изолированные)
│   │   ├── avito_parser/       # Модуль 1: Авито парсер
│   │   │   ├── __init__.py
│   │   │   ├── parser.py       # Парсер (из /var/www/avito-parser)
│   │   │   ├── models.py       # Unit, Source, Ad
│   │   │   ├── api.py          # API endpoints
│   │   │   ├── tasks.py        # Celery tasks
│   │   │   └── config.yaml     # Настройки модуля
│   │   │
│   │   ├── vpn_service/        # Модуль 2: VPN
│   │   │   ├── __init__.py
│   │   │   ├── vpn_manager.py  # Из /var/www/vpn-service
│   │   │   ├── models.py       # VPNKey
│   │   │   ├── api.py          # REST API
│   │   │   ├── bot.py          # Telegram бот
│   │   │   └── config.yaml
│   │   │
│   │   ├── news_aggregator/    # Модуль 3: Новости
│   │   │   ├── __init__.py
│   │   │   ├── aggregator.py   # Сбор из VK/TG
│   │   │   ├── filters.py      # Фильтры по темам
│   │   │   ├── publisher.py    # Публикация
│   │   │   ├── models.py
│   │   │   ├── api.py
│   │   │   └── config.yaml
│   │   │
│   │   ├── birthday_bot/       # Модуль 4: Поздравления
│   │   │   ├── __init__.py
│   │   │   ├── scraper.py      # Парсинг ДР из VK
│   │   │   ├── greeter.py      # Автопоздравления
│   │   │   ├── templates.py    # Шаблоны поздравлений
│   │   │   ├── models.py
│   │   │   ├── api.py
│   │   │   └── config.yaml
│   │   │
│   │   ├── music_lotto/        # Модуль 5: Музлото
│   │   │   ├── __init__.py
│   │   │   ├── game_engine.py  # Игровая логика
│   │   │   ├── stream.py       # VK Live интеграция
│   │   │   ├── tickets.py      # Управление билетами
│   │   │   ├── models.py       # Game, Ticket, Player
│   │   │   ├── api.py
│   │   │   ├── websocket.py    # Real-time sync
│   │   │   └── config.yaml
│   │   │
│   │   ├── vk_quests/          # Модуль 6: Квесты VK
│   │   │   ├── __init__.py
│   │   │   ├── quest_engine.py # Логика квестов
│   │   │   ├── comment_parser.py # Парсинг комментариев
│   │   │   ├── models.py
│   │   │   ├── api.py
│   │   │   └── config.yaml
│   │   │
│   │   └── bot_constructor/    # Модуль 7: Конструктор ботов
│   │       ├── __init__.py
│   │       ├── builder.py      # Drag-and-drop логика
│   │       ├── executor.py     # Исполнение ботов
│   │       ├── templates/      # Шаблоны сценариев
│   │       ├── models.py
│   │       ├── api.py
│   │       └── config.yaml
│   │
│   ├── health/                 # Health monitoring
│   │   ├── __init__.py
│   │   ├── checker.py          # Проверка статуса модулей
│   │   ├── metrics.py          # Prometheus метрики
│   │   └── api.py              # /health endpoints
│   │
│   ├── main.py                 # FastAPI app entry point
│   ├── requirements.txt        # Python зависимости
│   └── alembic/                # DB миграции
│       └── versions/
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   └── assets/
│   │       ├── logo.svg        # White-label лого
│   │       └── favicon.ico
│   │
│   ├── src/
│   │   ├── App.jsx             # Главный компонент
│   │   ├── main.jsx            # Entry point
│   │   │
│   │   ├── pages/              # Страницы
│   │   │   ├── Dashboard.jsx   # Главная (Health Monitor)
│   │   │   ├── Modules.jsx     # Управление модулями
│   │   │   ├── Settings.jsx    # Настройки платформы
│   │   │   ├── Login.jsx       # Авторизация
│   │   │   └── Register.jsx    # Регистрация
│   │   │
│   │   ├── components/         # Компоненты
│   │   │   ├── Header.jsx
│   │   │   ├── Sidebar.jsx
│   │   │   ├── ModuleCard.jsx  # Карточка модуля
│   │   │   ├── HealthWidget.jsx # Виджет статуса
│   │   │   ├── ProxyChecker.jsx # Проверка прокси
│   │   │   └── TokenManager.jsx # Управление токенами
│   │   │
│   │   ├── modules/            # UI модулей
│   │   │   ├── AvitoParser/
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── UnitCard.jsx
│   │   │   │   └── Settings.jsx
│   │   │   │
│   │   │   ├── VPNService/
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── KeysList.jsx
│   │   │   │   └── CreateKey.jsx
│   │   │   │
│   │   │   ├── NewsAggregator/
│   │   │   ├── BirthdayBot/
│   │   │   ├── MusicLotto/
│   │   │   ├── VKQuests/
│   │   │   └── BotConstructor/
│   │   │
│   │   ├── api/                # API клиенты
│   │   │   ├── axios.js        # Axios instance
│   │   │   ├── auth.js
│   │   │   ├── modules.js
│   │   │   └── billing.js
│   │   │
│   │   ├── store/              # Redux/Zustand state
│   │   │   ├── authStore.js
│   │   │   ├── modulesStore.js
│   │   │   └── settingsStore.js
│   │   │
│   │   └── utils/
│   │       ├── theme.js        # White-label темы
│   │       └── constants.js
│   │
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js      # Tailwind CSS
│
├── mobile/                     # React Native (для Музлото)
│   ├── android/
│   ├── ios/
│   ├── src/
│   │   ├── screens/
│   │   │   ├── GameScreen.jsx  # Экран игры
│   │   │   ├── LobbyScreen.jsx # Анонсы
│   │   │   └── ProfileScreen.jsx
│   │   ├── components/
│   │   │   ├── TicketCard.jsx  # Карточка 3×5
│   │   │   └── StreamPlayer.jsx # HLS плеер
│   │   └── api/
│   ├── package.json
│   └── metro.config.js
│
├── database/
│   ├── schema.sql              # PostgreSQL схема
│   ├── seeds/                  # Начальные данные
│   │   ├── tenants.sql
│   │   └── modules.sql
│   └── migrations/             # Alembic миграции
│
├── docker/
│   ├── Dockerfile.backend      # FastAPI + Celery
│   ├── Dockerfile.frontend     # Nginx + React
│   ├── Dockerfile.mobile       # React Native builder
│   ├── docker-compose.yml      # Полный стек
│   └── nginx/
│       ├── nginx.conf          # Main config
│       └── sites/
│           ├── api.conf        # Backend reverse proxy
│           └── frontend.conf   # Frontend static
│
├── scripts/
│   ├── setup.sh                # Первичная установка
│   ├── deploy.sh               # Деплой обновлений
│   ├── backup.sh               # Бэкап БД
│   └── migrate.sh              # Запуск миграций
│
├── docs/
│   ├── API.md                  # API документация
│   ├── MODULES.md              # Описание модулей
│   ├── DEPLOYMENT.md           # Инструкции деплоя
│   └── WHITE_LABEL.md          # Гайд по ребрендингу
│
├── .env.example                # Пример конфигурации
├── .gitignore
├── README.md                   # Главный README
└── LICENSE

```

---

## База данных (PostgreSQL)

### Общие таблицы (core):

```sql
-- Тенанты (клиенты платформы)
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,          -- Субдомен (client1.agenthub.ru)
    logo_url VARCHAR(500),                -- White-label лого
    primary_color VARCHAR(7) DEFAULT '#FF6B00',  -- Цвет бренда
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true
);

-- Пользователи
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',     -- admin, user
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

-- Подписки
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    plan VARCHAR(50) NOT NULL,           -- basic, pro, enterprise
    modules JSONB,                        -- {"avito_parser": true, "vpn": true}
    price_monthly INTEGER,                -- Цена в копейках
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Платежи
CREATE TABLE payments (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    subscription_id INTEGER REFERENCES subscriptions(id),
    amount INTEGER NOT NULL,              -- Копейки
    currency VARCHAR(3) DEFAULT 'RUB',
    provider VARCHAR(50) DEFAULT 'yookassa',
    provider_payment_id VARCHAR(255),
    status VARCHAR(50),                   -- pending, succeeded, canceled
    created_at TIMESTAMP DEFAULT NOW(),
    paid_at TIMESTAMP
);

-- Модули (метаинформация)
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(50) UNIQUE NOT NULL,     -- avito_parser, vpn_service
    name VARCHAR(255) NOT NULL,
    description TEXT,
    icon VARCHAR(255),                     -- URL иконки
    price_monthly INTEGER,                 -- Цена за модуль
    is_available BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Статусы модулей (для Health Monitor)
CREATE TABLE module_health (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    module_slug VARCHAR(50) REFERENCES modules(slug),
    status VARCHAR(50),                    -- healthy, degraded, down
    last_check TIMESTAMP DEFAULT NOW(),
    error_message TEXT,
    response_time_ms INTEGER
);

-- Прокси пул (общий для всех модулей)
CREATE TABLE proxies (
    id SERIAL PRIMARY KEY,
    url VARCHAR(500) NOT NULL,            -- http://user:pass@host:port
    type VARCHAR(50) DEFAULT 'http',      -- http, socks5
    is_alive BOOLEAN DEFAULT true,
    last_check TIMESTAMP,
    fail_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Токены VK/TG (общие)
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    platform VARCHAR(50) NOT NULL,        -- vk, telegram
    token_type VARCHAR(50),                -- user_token, group_token, bot_token
    token_value TEXT NOT NULL,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Таблицы модулей:

**Avito Parser:**
```sql
-- Единицы (units)
CREATE TABLE avito_units (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    city_slug VARCHAR(100) NOT NULL,
    vk_group_id VARCHAR(100),
    telegram_channel_id VARCHAR(100),
    is_enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Источники (категории)
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
    unit_id INTEGER REFERENCES avito_units(id),
    source_id INTEGER REFERENCES avito_sources(id),
    avito_id VARCHAR(100) UNIQUE,
    title TEXT NOT NULL,
    price INTEGER,
    description TEXT,
    url TEXT,
    image_url TEXT,
    published_vk BOOLEAN DEFAULT false,
    published_tg BOOLEAN DEFAULT false,
    scraped_at TIMESTAMP DEFAULT NOW()
);
```

**VPN Service:**
```sql
-- VPN ключи
CREATE TABLE vpn_keys (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    user_id INTEGER REFERENCES users(id),
    config_name VARCHAR(255) NOT NULL,
    public_key VARCHAR(255) NOT NULL,
    ip_address VARCHAR(50) NOT NULL,
    expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    last_handshake TIMESTAMP,
    traffic_rx BIGINT DEFAULT 0,
    traffic_tx BIGINT DEFAULT 0
);
```

**News Aggregator:**
```sql
-- Источники новостей
CREATE TABLE news_sources (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    platform VARCHAR(50),                 -- vk, telegram, rss
    source_id VARCHAR(255),                -- ID группы/канала
    is_enabled BOOLEAN DEFAULT true
);

-- Фильтры
CREATE TABLE news_filters (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    keywords JSONB,                        -- ["блокчейн", "AI"]
    exclude_keywords JSONB,
    min_likes INTEGER DEFAULT 0
);

-- Новости
CREATE TABLE news_items (
    id SERIAL PRIMARY KEY,
    source_id INTEGER REFERENCES news_sources(id),
    title TEXT,
    content TEXT,
    url TEXT,
    published_at TIMESTAMP,
    likes INTEGER DEFAULT 0,
    is_published BOOLEAN DEFAULT false
);
```

**Music Lotto:**
```sql
-- Игры
CREATE TABLE lotto_games (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    scheduled_at TIMESTAMP NOT NULL,
    vk_stream_url TEXT,
    status VARCHAR(50) DEFAULT 'scheduled', -- scheduled, live, finished
    winner_user_id INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Билеты
CREATE TABLE lotto_tickets (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES lotto_games(id),
    user_id INTEGER REFERENCES users(id),
    numbers JSONB NOT NULL,                 -- [1,5,12,18,24,...]
    is_winner BOOLEAN DEFAULT false,
    purchased_at TIMESTAMP DEFAULT NOW()
);

-- Числа в игре
CREATE TABLE lotto_drawn_numbers (
    id SERIAL PRIMARY KEY,
    game_id INTEGER REFERENCES lotto_games(id),
    number INTEGER NOT NULL,
    drawn_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Endpoints

### Core (auth, tenants)

```
POST   /api/auth/register          # Регистрация
POST   /api/auth/login             # Авторизация (JWT)
POST   /api/auth/refresh           # Обновление токена
GET    /api/auth/me                # Текущий пользователь

GET    /api/tenants                # Список тенантов (admin)
POST   /api/tenants                # Создать тенанта
GET    /api/tenants/:id            # Инфо о тенанте
PUT    /api/tenants/:id            # Обновить (white-label настройки)
DELETE /api/tenants/:id            # Удалить
```

### Health Monitoring

```
GET    /api/health                 # Общий статус платформы
GET    /api/health/modules         # Статусы всех модулей
GET    /api/health/modules/:slug   # Статус конкретного модуля
```

### Proxy Pool

```
GET    /api/proxies                # Список прокси
POST   /api/proxies                # Добавить прокси
DELETE /api/proxies/:id            # Удалить прокси
POST   /api/proxies/check          # Проверить все прокси
GET    /api/proxies/random         # Получить случайный живой прокси
```

### Token Manager

```
GET    /api/tokens                 # Список токенов
POST   /api/tokens/vk              # Добавить VK токен (OAuth flow)
POST   /api/tokens/telegram        # Добавить TG токен
DELETE /api/tokens/:id             # Удалить токен
```

### Billing

```
GET    /api/subscriptions          # Текущая подписка
POST   /api/subscriptions/upgrade  # Апгрейд тарифа
POST   /api/payments/create        # Создать платёж (ЮKassa)
POST   /api/payments/webhook       # Webhook от ЮKassa
GET    /api/payments/history       # История платежей
```

### Modules

```
GET    /api/modules                # Доступные модули
GET    /api/modules/:slug/status   # Статус модуля (вкл/выкл)
POST   /api/modules/:slug/enable   # Включить модуль
POST   /api/modules/:slug/disable  # Выключить модуль
```

### Avito Parser Module

```
GET    /api/avito/units            # Список единиц
POST   /api/avito/units            # Создать единицу
DELETE /api/avito/units/:id        # Удалить единицу
POST   /api/avito/units/:id/sources # Обновить источники
GET    /api/avito/ads              # Список объявлений
POST   /api/avito/parse            # Запустить парсинг
```

### VPN Module

```
GET    /api/vpn/keys               # Список ключей
POST   /api/vpn/keys               # Создать ключ
DELETE /api/vpn/keys/:id           # Удалить ключ
GET    /api/vpn/keys/:id/qr        # QR код
GET    /api/vpn/stats              # Статистика трафика
```

### News Module

```
GET    /api/news/sources           # Источники
POST   /api/news/sources           # Добавить источник
GET    /api/news/items             # Новости
POST   /api/news/aggregate         # Запустить сбор
```

### Music Lotto Module

```
GET    /api/lotto/games            # Список игр
POST   /api/lotto/games            # Создать игру
GET    /api/lotto/games/:id        # Детали игры
POST   /api/lotto/games/:id/start  # Начать игру
POST   /api/lotto/tickets          # Купить билет
WS     /ws/lotto/:gameId           # WebSocket для real-time
```

---

## Технологии

**Backend:**
- FastAPI (Python 3.11+)
- PostgreSQL 15
- Redis (кэш + Celery broker)
- Celery (фоновые задачи)
- Alembic (миграции)
- JWT (авторизация)

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- Zustand / Redux (state)
- Axios (API клиент)
- React Router

**Mobile:**
- React Native
- Expo (или чистый RN)

**DevOps:**
- Docker + Docker Compose
- Nginx (reverse proxy)
- systemd (сервисы)
- GitHub Actions (CI/CD)

**Мониторинг:**
- Prometheus (метрики)
- Grafana (дашборды)
- Sentry (errors)

---

## White Label

### Ребрендинг за 3 шага:

1. **Logo + Цвета** (в админке тенанта):
   - Загрузить logo.svg
   - Выбрать primary_color (#FF6B00 → #XXXXXX)

2. **Домен**:
   - Указать поддомен: `client1.agenthub.ru`
   - Или свой домен: `vpn.client-domain.com`

3. **Название** (опционально):
   - Изменить в `tenants.name`

Остальное подтягивается автоматически из БД!

---

## Деплой

### Полная установка:

```bash
git clone https://github.com/ainerovich/saas-platform.git
cd saas-platform
cp .env.example .env
# Отредактировать .env (DB, Redis, секреты)

# Запуск через Docker
docker-compose up -d

# Миграции БД
docker-compose exec backend alembic upgrade head

# Создание первого тенанта
docker-compose exec backend python scripts/create_tenant.py \
  --name "Мой Проект" \
  --domain "demo.agenthub.ru" \
  --email "admin@demo.ru"

# Открыть: http://demo.agenthub.ru
```

### Обновление:

```bash
git pull
docker-compose build
docker-compose up -d
docker-compose exec backend alembic upgrade head
```

---

## Roadmap

### Phase 1 (MVP) - 2 недели
- ✅ Авито Parser интеграция
- ✅ VPN Service интеграция
- ✅ Dashboard (Health Monitor)
- ✅ Proxy Pool
- ✅ Token Manager
- ✅ Базовый биллинг

### Phase 2 - 3 недели
- 🚧 News Aggregator
- 🚧 Birthday Bot
- 🚧 VK Quests
- 🚧 ЮKassa полная интеграция

### Phase 3 - 1 месяц
- 🚧 Music Lotto (Web + Mobile)
- 🚧 Bot Constructor
- 🚧 Advanced analytics
- 🚧 Multi-language support

### Phase 4 - Масштабирование
- 🔮 Kubernetes деплой
- 🔮 Load balancing
- 🔮 CDN для статики
- 🔮 White label marketplace

---

## Стоимость разработки (оценка)

**MVP (Phase 1):** 2 недели × 8ч/день = ~100 часов
**Full Platform:** ~300-400 часов

**Монетизация:**
- Базовый тариф: 990₽/мес (1-2 модуля)
- Про тариф: 2990₽/мес (все модули)
- Enterprise: от 9990₽/мес (white label + support)

---

## Следующие шаги

1. ✅ Создать структуру папок
2. ✅ Настроить Docker Compose
3. ✅ Миграция Avito Parser → модуль
4. ✅ Миграция VPN Service → модуль
5. 🚧 Dashboard главная страница
6. 🚧 Proxy Pool MVP
7. 🚧 Token Manager MVP
8. 🚧 Health Monitor
9. 🚧 Базовый биллинг

**Начинаем с пункта 1!** 🚀
