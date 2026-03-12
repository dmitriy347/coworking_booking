from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Схема запроса на вход."""
    email: str
    password: str


class TokenResponse(BaseModel):
    """Схема ответа с токенами после успешного входа."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    """Схема запроса на обновление access токена."""
    refresh_token: str