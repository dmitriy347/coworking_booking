from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    """Общие поля пользователя. Основа для других схем."""
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    """Схема для регистрации."""
    password: str


class UserUpdate(UserBase):
    """Схема для обновления профиля. Все поля опциональны."""
    first_name: str | None = None  # Все опционально
    last_name: str | None = None
    password: str | None = None


class UserResponse(UserBase):
    """Схема ответа API. Возвращается клиенту без пароля."""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    # from_attributes: True - нужен только в схемах, которые ты возвращаешь из роутера (Response схемы)
    # Что бы Pydantic умел читать не только ключи словаря, но и атрибуты объекта
    model_config = {"from_attributes": True}