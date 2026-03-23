from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.repositories.workspace import WorkspaceRepository
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse


class WorkspaceService:
    """
    Бизнес-логика для рабочих мест.
    Использует WorkspaceRepository для работы с БД.
    """
    def __init__(self, db: AsyncSession):
        """Создает экземпляр репозитория с переданной сессией БД."""
        self.repo = WorkspaceRepository(db)

    async def create(self, data: WorkspaceCreate) -> WorkspaceResponse:
        """Создает новое рабочее место."""
        workspace = await self.repo.create(
            name=data.name,
            description=data.description,
            type=data.type,
            price_per_hour=float(data.price_per_hour)
        )
        return WorkspaceResponse.model_validate(workspace)

    async def get_by_id(self, workspace_id: int) -> WorkspaceResponse:
        """Возвращает рабочее место по id или 404 если не найдено."""
        workspace = await self.repo.get_workspace_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рабочее место не найдено"
            )
        return WorkspaceResponse.model_validate(workspace)

    async def get_all(self, only_active: bool =True) -> list[WorkspaceResponse]:
        """Возвращает список рабочих мест. По умолчанию только активные."""
        workspaces = await self.repo.get_workspace_all(only_active=only_active)
        return [WorkspaceResponse.model_validate(w) for w in workspaces]

    async def update(self, workspace_id: int, data: WorkspaceUpdate) -> WorkspaceResponse:
        """Обновляет рабочее место. 404 если не найдено."""
        # Сначала получаем рабочее место
        workspace = await self.repo.get_workspace_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рабочее место не найдено"
            )
        # Затем обновляем его поля
        workspace = await self.repo.update(
            workspace,
            **data.model_dump(exclude=True)
        )
        return WorkspaceResponse.model_validate(workspace)

    async def delete(self, workspace_id: int) -> None:
        """Деактивирует рабочее место. 404 если не найдено."""
        workspace = await self.repo.get_workspace_by_id(workspace_id)
        if not workspace:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Рабочее место не найдено"
            )
        await self.repo.delete(workspace)