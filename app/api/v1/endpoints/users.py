from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies import get_current_user, get_current_admin
from app.db.sesion import get_db
from app.models import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=201)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Регистрирует нового пользователя. Возвращает созданного пользователя."""
    service = UserService(db)
    return await service.register(user_data)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Возвращает профиль только текущего авторизованного пользователя."""
    return UserResponse.model_validate(current_user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(get_current_admin)):
    """Возвращает пользователя по id только для админов. 404 если не найден."""
    service = UserService(db)
    return await service.get_by_id(user_id)


@router.get("/", response_model=list[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_admin)):
    """Возвращает список всех пользователей только для админов."""
    service = UserService(db)
    return await service.get_all()
