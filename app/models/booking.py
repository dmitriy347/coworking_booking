from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enum import BookingStatus
import sqlalchemy as sa


class Booking(Base):
    """Модель бронирования."""
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", nullable=False))
    workspace_id: Mapped[int] = mapped_column(ForeignKey("workspaces.id", nullable=False))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        sa.Enum(BookingStatus, name="booking_status"),
        default=BookingStatus.PENDING,
        nullable=False,
    )
    total_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Связи
    user: Mapped["User"] = relationship(back_populates="bookings")
    workspace: Mapped["Workspace"] = relationship(back_populates="workspace")