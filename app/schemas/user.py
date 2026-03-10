from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    first_name: str | None = None  # Все опционально
    last_name: str | None = None
    password: str | None = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    # from_attributes: True - нужен только в схемах, которые ты возвращаешь из роутера (Response схемы)
    # Что бы Pydantic умел читать не только ключи словаря, но и атрибуты объекта
    model_config = {"from_attributes": True}