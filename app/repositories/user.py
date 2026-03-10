from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User


class UserRepository:
    """Слой доступа к данным для пользователей. Только запросы к БД, без логики."""
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: int) -> User | None:
        """Возвращает пользователя по id или None если не найден."""
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()  # Вернуть 1 запись или None (если не найдена), если > 1 - упадет с ошибкой

    async def get_by_email(self, email: str) -> User | None:
        """Возвращает пользователя по email или None если не найден."""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def create(self, email: str, hashed_password: str, first_name: str, last_name: str) -> User:
        """Создаёт нового пользователя в БД и возвращает его с заполненным id и датами."""
        user = User(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)  # Подгружает id и created_at из БД
        return user

    async def get_all(self) -> list[User]:
        """Возвращает список всех пользователей из БД."""
        result = await self.db.execute(select(User))
        return list(result.scalars().all())