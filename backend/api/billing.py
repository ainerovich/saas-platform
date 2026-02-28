"""
Billing API - Подписки и платежи
СУПЕР-АДМИН НЕ ПЛАТИТ!
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

from core.database import get_db
from core.models import User, Subscription, Payment
from core.auth import get_current_user

router = APIRouter()


# Schemas
class SubscriptionResponse(BaseModel):
    id: int
    plan: str
    modules: dict
    price_monthly: int
    status: str
    started_at: datetime
    expires_at: Optional[datetime]
    auto_renew: bool
    is_free: bool  # Супер-админ или FREE план


class PaymentResponse(BaseModel):
    id: int
    amount: int
    currency: str
    status: str
    created_at: datetime
    paid_at: Optional[datetime]


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Текущая подписка
    Супер-админ всегда видит "unlimited" план
    """
    
    # Супер-админ не платит
    if current_user.is_super_admin:
        return {
            "id": 0,
            "plan": "unlimited",
            "modules": {},  # Все модули доступны
            "price_monthly": 0,
            "status": "active",
            "started_at": current_user.created_at,
            "expires_at": None,
            "auto_renew": False,
            "is_free": True
        }
    
    # Ищем подписку тенанта
    subscription = db.query(Subscription).filter(
        Subscription.tenant_id == current_user.tenant_id
    ).order_by(Subscription.created_at.desc()).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="No subscription found")
    
    return {
        "id": subscription.id,
        "plan": subscription.plan,
        "modules": subscription.modules,
        "price_monthly": subscription.price_monthly,
        "status": subscription.status,
        "started_at": subscription.started_at,
        "expires_at": subscription.expires_at,
        "auto_renew": subscription.auto_renew,
        "is_free": subscription.plan == "free" or subscription.price_monthly == 0
    }


@router.post("/upgrade")
async def upgrade_plan(
    plan: str,  # basic, pro, enterprise
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Апгрейд тарифа
    Супер-админ не может апгрейдить (у него всё бесплатно)
    """
    
    if current_user.is_super_admin:
        raise HTTPException(
            status_code=400,
            detail="Super admin has unlimited access"
        )
    
    # Тарифы
    plans = {
        "basic": {
            "price": 99000,  # 990₽
            "modules": {"avito_parser": True, "vpn_service": True}
        },
        "pro": {
            "price": 299000,  # 2990₽
            "modules": {
                "avito_parser": True,
                "vpn_service": True,
                "news_aggregator": True,
                "birthday_bot": True
            }
        },
        "enterprise": {
            "price": 999000,  # 9990₽
            "modules": {}  # Все модули
        }
    }
    
    if plan not in plans:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    plan_data = plans[plan]
    
    # Создаём новую подписку
    subscription = Subscription(
        tenant_id=current_user.tenant_id,
        plan=plan,
        modules=plan_data["modules"],
        price_monthly=plan_data["price"],
        status="pending",  # Будет active после оплаты
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(subscription)
    db.flush()
    
    # Создаём платёж (для YooKassa)
    payment = Payment(
        tenant_id=current_user.tenant_id,
        subscription_id=subscription.id,
        amount=plan_data["price"],
        currency="RUB",
        provider="yookassa",
        status="pending"
    )
    db.add(payment)
    db.commit()
    
    # TODO: Интеграция YooKassa - создать платёж и вернуть payment_url
    
    return {
        "payment_id": payment.id,
        "amount": payment.amount,
        "currency": payment.currency,
        "payment_url": f"https://yookassa.ru/pay/{payment.id}",  # Заглушка
        "status": "pending"
    }


@router.get("/payments", response_model=List[PaymentResponse])
async def get_payments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    История платежей
    Супер-админ видит пустой список
    """
    
    if current_user.is_super_admin:
        return []
    
    payments = db.query(Payment).filter(
        Payment.tenant_id == current_user.tenant_id
    ).order_by(Payment.created_at.desc()).all()
    
    return [
        {
            "id": p.id,
            "amount": p.amount,
            "currency": p.currency,
            "status": p.status,
            "created_at": p.created_at,
            "paid_at": p.paid_at
        }
        for p in payments
    ]
