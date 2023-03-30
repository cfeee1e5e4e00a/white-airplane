import time
from datetime import datetime, timedelta
from fastapi import HTTPException, APIRouter, Body
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field

from src.env import env
from src.schemas.user import get_user_by_username, create_user, Role

EXPIRES_AFTER_DAYS = 1

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"])


class LoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)


@auth_router.post("/login")
def login(data: LoginRequest = Body(...)):
    user = get_user_by_username(data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")

    if not pwd_context.verify(data.username, user["password"]):
        raise HTTPException(status_code=400, detail="Неверный пароль")

    exp = time.mktime((datetime.now() + timedelta(days=EXPIRES_AFTER_DAYS)).timetuple())

    return jwt.encode(
        {"username": user["login"], "exp": exp}, env["JWT_SECRET"], algorithm="HS256"
    )


class RegisterRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)
    role: Role = Field(...)


@auth_router.post("/register")
def register(data: RegisterRequest):
    if get_user_by_username(data.username):
        raise HTTPException(
            status_code=400, detail="Пользователь c таким логином существует"
        )

    create_user(data.username, pwd_context.hash(data.password), data.role)
