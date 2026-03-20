import enum


class WorkspaceType(str, enum.Enum):
    """Тип рабочего места."""
    OPEN_SPACE = "open-space"
    MEETING_ROOM = "meeting-room"
    PRIVATE_OFFICE = "private-office"


class BookingStatus(str, enum.Enum):
    """Статус бронирования."""
    PENDING = "pending" # Ожидает подтверждения
    CONFIRMED = "confirmed" # подтверждено
    CANCELED = "canceled" # отменено