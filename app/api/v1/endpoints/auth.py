from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.sesion import get_db
from app.schemas.auth import TokenResponse, RefreshRequest, LoginRequest
from app.services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    """Вход по email и паролю. Выдаёт access + refresh токены."""
    service = AuthService(db)
    return await service.login(login_data)

@router.post("/refresh", response_model=TokenResponse)
async def refresh(refresh_data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    """Обновляет access токен по refresh токену."""
    service = AuthService(db)
    return await service.refresh(refresh_data.refresh_token)