# SaaS Platform - Multi-Module Automation Hub

🚀 **White-label мультимодульная SaaS платформа для автоматизации бизнес-процессов**

## 🎯 Что это?

Единая платформа для управления 7+ модулями автоматизации:
- **Парсинг** (Avito, VK, новости)
- **VPN** (WireGuard генератор)
- **Боты** (автопоздравления, квесты)
- **Развлечения** (музыкальное лото)
- **Конструктор** (создание ботов без кода)

## 📦 Модули

### ✅ Готовые
1. **Avito Parser** - парсинг объявлений + автопубликация VK/TG
2. **VPN Service** - генерация WireGuard ключей через Telegram

### 🚧 В разработке
3. **News Aggregator** - сбор новостей из VK/TG с фильтрами
4. **Birthday Bot** - автопоздравления именинников в VK
5. **Music Lotto** - музлото с VK трансляцией + мобильное приложение
6. **VK Quests** - игровые квесты в комментариях
7. **Bot Constructor** - drag-and-drop создание ботов

## 🏗️ Архитектура

```
Backend:  FastAPI + PostgreSQL + Redis + Celery
Frontend: React + Vite + Tailwind CSS
Mobile:   React Native (для Music Lotto)
Deploy:   Docker Compose + Nginx
```

**Особенности:**
- ✅ Multi-tenant (несколько клиентов на одной инстанции)
- ✅ White Label (легкий ребрендинг)
- ✅ Микросервисы (изолированные модули)
- ✅ Health Monitor (мониторинг всех сервисов)
- ✅ Общий Proxy Pool + Token Manager

## 🚀 Быстрый старт

### Требования
- Docker 20+ + Docker Compose
- 4GB RAM минимум
- PostgreSQL 15
- Redis 7

### Установка

```bash
# Клонировать репозиторий
git clone https://github.com/ainerovich/saas-platform.git
cd saas-platform

# Настроить окружение
cp .env.example .env
nano .env  # Заполнить DB_PASSWORD, JWT_SECRET, etc.

# Запустить через Docker
docker-compose up -d

# Применить миграции
docker-compose exec backend alembic upgrade head

# Создать первого тенанта
docker-compose exec backend python scripts/create_tenant.py \
  --name "Demo Project" \
  --domain "demo.localhost" \
  --email "admin@demo.local"

# Открыть Dashboard
open http://demo.localhost
```

### Разработка (без Docker)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## 📊 Database

PostgreSQL схема с таблицами:
- **Core:** tenants, users, subscriptions, payments
- **Resources:** proxies, tokens, module_health
- **Modules:** avito_*, vpn_*, news_*, lotto_*, ...

Полная схема: [database/schema.sql](database/schema.sql)

## 🔌 API

### Auth
```
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
```

### Health
```
GET /api/health
GET /api/health/modules
```

### Avito Parser
```
GET    /api/avito/units
POST   /api/avito/units
POST   /api/avito/parse
```

### VPN
```
GET    /api/vpn/keys
POST   /api/vpn/keys
GET    /api/vpn/keys/:id/qr
```

Полная документация: [docs/API.md](docs/API.md)

## 🎨 White Label

Ребрендинг за 3 шага:

1. **Logo + Цвета** в админке тенанта
2. **Домен** (субдомен или свой)
3. **Название** в настройках

Всё остальное подтягивается автоматически!

## 💰 Монетизация

**Тарифы:**
- **Basic:** 990₽/мес (1-2 модуля)
- **Pro:** 2990₽/мес (все модули)
- **Enterprise:** от 9990₽/мес (white label + поддержка)

**Биллинг:** ЮKassa интеграция (карты, СБП, ЮMoney)

## 📈 Roadmap

### Phase 1 (MVP) - 2 недели
- [x] Архитектура
- [x] Database schema
- [x] Docker setup
- [ ] Core API (auth, tenants)
- [ ] Dashboard (health monitor)
- [ ] Avito Parser интеграция
- [ ] VPN Service интеграция

### Phase 2 - 3 недели
- [ ] News Aggregator
- [ ] Birthday Bot
- [ ] VK Quests
- [ ] ЮKassa полная интеграция

### Phase 3 - 1 месяц
- [ ] Music Lotto (Web + Mobile)
- [ ] Bot Constructor
- [ ] Advanced analytics

## 🛠️ Tech Stack

**Backend:**
- FastAPI 0.109+
- PostgreSQL 15
- Redis 7
- Celery (задачи)
- Alembic (миграции)

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Zustand (state)

**DevOps:**
- Docker + Compose
- Nginx
- GitHub Actions

## 📝 Лицензия

MIT

## 👥 Контакты

- GitHub: [@ainerovich](https://github.com/ainerovich)
- Telegram: @ainerovich

---

**Сделано с ❤️ в России**
