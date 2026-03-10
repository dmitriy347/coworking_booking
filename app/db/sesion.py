from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from app.core.config import settings

# 1. Engine — соединение с БД
# если DEBUG=True, будет печатать все SQL запросы
engine = create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)

# 2. Сессии
# expire_on_commit=False - объекты не истекают после коммита, что позволяет работать с ними после сохранения
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

# 3. Dependency для роутеров
async def get_db() -> AsyncSession:
    """Dependency для роутеров. Создаёт сессию БД на время запроса и закрывает после."""
    async with AsyncSessionLocal() as session:
        yield session  # именно yield, а не return - FastAPI автоматически закроет сессию сам