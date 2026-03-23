from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.workspace import Workspace
from app.models.enums import WorkspaceType


class WorkspaceRepository:
    """Слой доступа к данным для рабочих мест. Только запросы к БД."""
    def __init__(self, db: AsyncSession):
        """Принимает сессию БД снаружи."""
        self.db = db

    async def get_workspace_by_id(self, workspace_id: int) -> Workspace | None:
        """Возвращает рабочее место по id или None если не найдено."""
        result = await self.db.execute(
            select(Workspace).where(Workspace.id == workspace_id)
        )
        return result.scalar_one_or_none()

    async def get_workspace_all(self, only_active: bool =True) -> list[Workspace]:
        """Возвращает список рабочих мест. По умолчанию только активные."""
        query = select(Workspace)
        if only_active:
            query = query.where(Workspace.is_active == True)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def create(self, name: str, description: str | None,
                     type: WorkspaceType, price_per_hour: float) -> Workspace:
        """Создаёт новое рабочее место в БД и возвращает его с заполненным id."""
        workspace = Workspace(
            name=name,
            description=description,
            type=type,
            price_per_hour=price_per_hour,
        )
        self.db.add(workspace)
        await self.db.commit()
        await self.db.refresh(workspace)
        return workspace

    async def update(self, workspace: Workspace, **kwargs) -> Workspace:
        """Обновляет переданные поля рабочего места."""
        for key, value in kwargs.items():
            if value is not None:
                setattr(workspace, key, value)
        await self.db.commit()
        await self.db.refresh(workspace)
        return workspace

    async def delete(self, workspace: Workspace) -> None:
        """Удаление - деактивирование рабочего места."""
        workspace.is_active = False
        await self.db.commit()
