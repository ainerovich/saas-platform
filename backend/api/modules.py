"""
Modules API - Управление модулями
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from core.database import get_db
from core.models import User
from core.auth import get_current_user

router = APIRouter()


# Статичный список модулей
MODULES = [
    {
        "slug": "avito_parser",
        "name": "Avito Parser",
        "description": "Парсинг объявлений с Avito и автопубликация в VK/Telegram",
        "icon": "🔍",
        "price_monthly": 99000,
        "status": "available"
    },
    {
        "slug": "vpn_service",
        "name": "VPN Generator",
        "description": "Генерация WireGuard VPN ключей через Telegram бота",
        "icon": "🔐",
        "price_monthly": 49000,
        "status": "available"
    },
    {
        "slug": "news_aggregator",
        "name": "News Aggregator",
        "description": "Сбор и фильтрация новостей из VK/Telegram",
        "icon": "📰",
        "price_monthly": 69000,
        "status": "coming_soon"
    },
    {
        "slug": "birthday_bot",
        "name": "Birthday Bot",
        "description": "Автоматические поздравления с днём рождения в VK",
        "icon": "🎉",
        "price_monthly": 39000,
        "status": "coming_soon"
    },
    {
        "slug": "music_lotto",
        "name": "Music Lotto",
        "description": "Музыкальное лото с VK трансляцией",
        "icon": "🎵",
        "price_monthly": 149000,
        "status": "coming_soon"
    },
    {
        "slug": "vk_quests",
        "name": "VK Quests",
        "description": "Игровые квесты в комментариях VK",
        "icon": "🎮",
        "price_monthly": 59000,
        "status": "coming_soon"
    },
    {
        "slug": "bot_constructor",
        "name": "Bot Constructor",
        "description": "Конструктор ботов для VK/Telegram без кода",
        "icon": "🤖",
        "price_monthly": 79000,
        "status": "coming_soon"
    }
]


class ModuleResponse(BaseModel):
    slug: str
    name: str
    description: str
    icon: str
    price_monthly: int
    status: str
    is_enabled: bool


@router.get("/", response_model=List[ModuleResponse])
async def list_modules(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Список всех модулей с их статусом
    Супер-админ видит все модули как enabled
    """
    
    from core.models import Subscription
    
    # Супер-админ - все модули доступны
    if current_user.is_super_admin:
        return [
            {
                **module,
                "is_enabled": True
            }
            for module in MODULES
        ]
    
    # Получаем подписку
    subscription = db.query(Subscription).filter(
        Subscription.tenant_id == current_user.tenant_id,
        Subscription.status == "active"
    ).first()
    
    enabled_modules = subscription.modules if subscription else {}
    
    return [
        {
            **module,
            "is_enabled": enabled_modules.get(module["slug"], False)
        }
        for module in MODULES
    ]


@router.get("/{slug}/status")
async def module_status(
    slug: str,
    current_user: User = Depends(get_current_user)
):
    """
    Статус конкретного модуля
    """
    
    module = next((m for m in MODULES if m["slug"] == slug), None)
    if not module:
        return {"error": "Module not found"}
    
    # Супер-админ - всегда healthy
    if current_user.is_super_admin:
        return {
            "module": slug,
            "status": "healthy",
            "is_enabled": True,
            "response_time_ms": 45
        }
    
    return {
        "module": slug,
        "status": "unknown",
        "is_enabled": False
    }
