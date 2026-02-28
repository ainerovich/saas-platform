"""
Tenants API - Управление тенантами (только для супер-админа)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from core.database import get_db
from core.models import User, Tenant
from core.auth import require_super_admin

router = APIRouter()


class TenantResponse(BaseModel):
    id: int
    uuid: str
    name: str
    domain: Optional[str]
    logo_url: Optional[str]
    primary_color: str
    is_active: bool
    users_count: int


@router.get("/", response_model=List[TenantResponse])
async def list_tenants(
    current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db)
):
    """
    Список всех тенантов (только для супер-админа)
    """
    
    tenants = db.query(Tenant).all()
    
    return [
        {
            "id": t.id,
            "uuid": t.uuid,
            "name": t.name,
            "domain": t.domain,
            "logo_url": t.logo_url,
            "primary_color": t.primary_color,
            "is_active": t.is_active,
            "users_count": len(t.users)
        }
        for t in tenants
    ]


@router.get("/{tenant_id}", response_model=TenantResponse)
async def get_tenant(
    tenant_id: int,
    current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db)
):
    """
    Детали тенанта
    """
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {
        "id": tenant.id,
        "uuid": tenant.uuid,
        "name": tenant.name,
        "domain": tenant.domain,
        "logo_url": tenant.logo_url,
        "primary_color": tenant.primary_color,
        "is_active": tenant.is_active,
        "users_count": len(tenant.users)
    }
