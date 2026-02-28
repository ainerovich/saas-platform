"""
FastAPI Main Application
Mobile-first SaaS Platform
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from core.config import settings
from core.database import engine, Base

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI(
    title="SaaS Platform API",
    description="Multi-module automation platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS (для мобильных приложений и фронтенда)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "online",
        "version": "1.0.0",
        "platform": "SaaS Multi-Module"
    }


@app.get("/api/health")
async def health_check():
    """Детальный health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "modules": {
            "avito_parser": "ready",
            "vpn_service": "ready"
        }
    }


# Import routers
from api import auth, tenants, modules, billing

# Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tenants.router, prefix="/api/tenants", tags=["Tenants"])
app.include_router(modules.router, prefix="/api/modules", tags=["Modules"])
app.include_router(billing.router, prefix="/api/billing", tags=["Billing"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
