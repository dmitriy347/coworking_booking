from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Хеширует пароль через bcrypt. Возвращает хеш для сохранения в БД."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Сравнивает введённый пароль с хешем из БД. Возвращает True если совпадают."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: str) ->str:
    """Создает JWT access токен с id пользователя."""
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id: str) ->str:
    """Создает JWT refresh токен с id пользователя."""
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    """Декодирует JWT токен. Выбрасывает JWTError если токен невалидный или истёк."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
