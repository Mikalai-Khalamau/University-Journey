from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from src.presentation.api.dependencies import auth_service
from src.core.exceptions import ValidationError, UnauthorizedError  # ← ОБЯЗАТЕЛЬНО

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=4)
    confirm_password: str
    email: str | None = None


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(req: RegisterRequest):
    try:
        user = auth_service.register(
            username=req.username,
            password=req.password,
            email=req.email,
            confirm_password=req.confirm_password
        )
        return {"detail": "Регистрация успешна", "user": {"username": user.username}}
    except (ValidationError, UnauthorizedError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")


@router.post("/login")
def login(req: LoginRequest):
    try:
        token, user = auth_service.login(username=req.username, password=req.password)
        return {
            "detail": "Вход успешен",
            "token": token,
            "user": {"id": str(user.id), "username": user.username, "email": user.email}
        }
    except (ValidationError, UnauthorizedError) as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")