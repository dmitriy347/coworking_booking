from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import hash_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, user_data: UserCreate) -> UserResponse:
        # 1. Проверяем что email свободен
        existing = await self.repo.get_by_email(user_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким email уже существует"
            )

        # 2. Хешируем пароль
        hashed = hash_password(user_data.password)

        # 3. Создаём пользователя
        user = await self.repo.create(
            email=user_data.email,
            hashed_password=hashed,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
        )

        # Возвращаем схему (не объект SQLAlchemy)
        return UserResponse.model_validate(user)

    async def get_by_id(self, user_id: int) -> UserResponse:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return UserResponse.model_validate(user)

    async def get_all(self) -> list[UserResponse]:
        users = await self.repo.get_all()
        return [UserResponse.model_validate(u) for u in users]