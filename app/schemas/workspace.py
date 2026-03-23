from decimal import Decimal

from pydantic import BaseModel

from app.models.enums import WorkspaceType


class Workspace(BaseModel):
    """Общие поля рабочего места."""
    name: str
    description: str | None = None
    type: WorkspaceType
    price_per_hour: Decimal


class WorkspaceCreate(Workspace):
    """Схема для создания рабочего места. Только для админов."""
    pass


class WorkspaceUpdate(BaseModel):
    """Схема для обновления рабочего места. Все поля опциональны."""
    name: str | None = None
    description: str | None = None
    type: WorkspaceType | None = None
    price_per_hour: Decimal | None = None
    is_active: bool | None = None


class WorkspaceResponse(Workspace):
    """Схема ответа API."""
    id: int
    is_active: bool

    model_config = {"from_attributes": True}

