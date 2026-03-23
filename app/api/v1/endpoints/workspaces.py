from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.sesion import get_db
from app.models import User
from app.schemas.workspace import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse
from app.services.workspace import WorkspaceService
from app.api.dependencies import get_current_admin, get_current_user


router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("/", response_model=list[WorkspaceResponse])
async def get_all_workspaces(db: AsyncSession = Depends(get_db),
                             current_user: User = Depends(get_current_user)):
    """Возвращает список активных рабочих мест. Для авторизованных пользователей."""
    service = WorkspaceService(db)
    return await service.get_all(only_active=True)


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(workspace_id: int, db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    """Возвращает рабочее место по id."""
    service = WorkspaceService(db)
    return await service.get_by_id(workspace_id)


@router.post("/", response_model=WorkspaceResponse)
async def create_workspace(data: WorkspaceCreate, db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_admin)):
    """Создаёт новое рабочее место. Только для админов."""
    service = WorkspaceService(db)
    return await service.create(data)


@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(workspace_id: int, data: WorkspaceUpdate,
                           db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_admin)):
    """Обновляет рабочее место. Только для админов."""
    service = WorkspaceService(db)
    return await service.update(workspace_id, data)


@router.delete("/{workspace_id}", status_code=204)
async def delete_workspace(workspace_id: int, db: AsyncSession = Depends(get_db),
                           current_user: User = Depends(get_current_admin)):
    """Деактивирует рабочее место. Только для админов."""
    service = WorkspaceService(db)
    return await service.delete(workspace_id)