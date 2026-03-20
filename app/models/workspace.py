from sqlalchemy import String, Text, Numeric, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.enum import WorkspaceType
import sqlalchemy as sa


class Workspace(Base):
    """Модель рабочего места."""
    __tablename__ = "workspaces"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    type: Mapped[WorkspaceType] = mapped_column(
        sa.Enum(WorkspaceType, name="workspacetype"),
        nullable=False
    )
    price_per_hour: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)

    # Связь с бронированием
    bookings: Mapped[list["Booking"]] = relationship(back_populates="workspace")