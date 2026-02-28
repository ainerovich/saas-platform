"""
Auth API - Регистрация, логин
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from core.database import get_db
from core.models import User, Tenant, Subscription
from core.auth import (
    hash_password, 
    verify_password, 
    create_access_token,
    get_current_user
)
from core.config import settings

router = APIRouter()


# Schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tenant_name: Optional[str] = None  # Для нового тенанта


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: int
    uuid: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    role: str
    is_super_admin: bool
    tenant_id: int


@router.post("/register", response_model=TokenResponse)
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя
    
    - Создаёт тенанта (если не указан)
    - Создаёт FREE подписку
    - Возвращает JWT токен
    """
    
    # Проверяем email
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создаём тенанта
    tenant = Tenant(
        name=data.tenant_name or f"{data.email}'s workspace",
        domain=None  # Можно добавить автогенерацию
    )
    db.add(tenant)
    db.flush()
    
    # Супер-админ?
    role = "super_admin" if data.email == settings.SUPER_ADMIN_EMAIL else "admin"
    
    # Создаём пользователя
    user = User(
        tenant_id=tenant.id,
        email=data.email,
        password_hash=hash_password(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        role=role
    )
    db.add(user)
    db.flush()
    
    # Создаём FREE подписку (если не супер-админ)
    if not user.is_super_admin:
        subscription = Subscription(
            tenant_id=tenant.id,
            plan="free",
            modules={},  # Нет модулей в FREE
            price_monthly=0,
            status="active"
        )
        db.add(subscription)
    
    db.commit()
    db.refresh(user)
    
    # Генерируем токен
    token = create_access_token(data={"sub": user.id})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "uuid": user.uuid,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_super_admin": user.is_super_admin,
            "tenant_id": user.tenant_id
        }
    }


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Авторизация
    """
    
    # Ищем пользователя
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Проверяем пароль
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Обновляем last_login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Генерируем токен
    token = create_access_token(data={"sub": user.id})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "uuid": user.uuid,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_super_admin": user.is_super_admin,
            "tenant_id": user.tenant_id
        }
    }


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Получить информацию о текущем пользователе
    """
    return {
        "id": current_user.id,
        "uuid": current_user.uuid,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role,
        "is_super_admin": current_user.is_super_admin,
        "tenant_id": current_user.tenant_id
    }
