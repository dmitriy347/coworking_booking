from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from app.db.sesion import get_db
from app.core.security import decode_token
from app.repositories.user import UserRepository
from app.models.user import User


# HTTPBearer достаёт Bearer токен из заголовка Authorization
# Swagger автоматически добавит кнопку Authorize.
security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency. Декодирует токен и возвращает текущего пользователя.
    Бросает 401 если токен невалидный или истёк.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Токен недействителен или истёк",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload=decode_token(credentials.credentials)

        # Проверяем что это access токен
        if payload.get("type") != "access":
            raise credentials_exception

        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Загружаем пользователя из БД
    repo = UserRepository(db)
    user = await repo.get_by_id(int(user_id))

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Аккаунт заблокирован"
        )
    return user


async def get_current_admin(
        current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency. Проверяет что текущий пользователь является администратором.
    Бросает 403 если не админ.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав"
        )
    return current_user