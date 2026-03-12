from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from jose import JWTError


class AuthService:
    """
    Бизнес-логика аутентификации.
    Выдаёт и обновляет JWT токены.
    """
    def __init__(self, db: AsyncSession):
        """Создаёт экземпляр репозитория с переданной сессией БД."""
        self.repo = UserRepository(db)

    async def login(self, login_data: LoginRequest) -> TokenResponse:
        """Проверяет email и пароль. Возвращает access и refresh токены."""
        # 1. Ищем пользователя по email
        user = await self.repo.get_by_email(login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )

        # 2. Проверяем пароль
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный email или пароль"
            )

        # 3. Проверяем что пользователь активен
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Аккаунт заблокирован"
            )

        # 4. Выдаём токены
        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id)
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        """Проверяет refresh токен. Возвращает новую пару токенов."""
        try:
            payload = decode_token(refresh_token)

            # Проверяем что это именно refresh токен
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Неверный тип токена"
                )
            user_id = payload.get("sub")

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен недействителен или истёк"
            )

        # Проверяем что пользователь ещё существует
        user = await self.repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Пользователь не найден или заблокирован"
            )

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id)
        )
