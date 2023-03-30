import time
from datetime import datetime, timedelta
from typing import Annotated
import fastapi_login
from fastapi import Depends, HTTPException, APIRouter, Body, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from pymongo.collection import Collection
from pydantic import BaseModel, Field
from src.env import env
from src.db import mongo
from src.schemas.user import find_user_by_login, UserCreate


auth_router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'])

manager = fastapi_login.LoginManager(env['AUTH_SECRET'], '/login')

EXPIRES_AFTER_DAYS = 1

class RegisterRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class LoginRequest(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

@auth_router.post('/login')
def login(data: LoginRequest = Body(...)):
    user = find_user_by_username(data.username)
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')
    if not pwd_context.verify(data.username, user['password']):
        raise HTTPException(status_code=400, detail='Неверный пароль')
    exp = time.mktime((datetime.now() + timedelta(days=EXPIRES_AFTER_DAYS)).timetuple())
    return jwt.encode({'username': user['login'], 'exp': exp}, env['JWT_SECRET'], algorithm='HS256')


@auth_router.post('/reqister')
def create_user(data: RegisterRequest):
    collection: Collection['User'] = mongo.db.users # FIXME
    if check_login_in_db(data.username):
        raise HTTPException(status_code=400, detail='Пользователь c таким логином существует')

    collection.insert_one({'login': data.username, 'password': pwd_context.hash(data.password)})
    return {"username": data.username}


@auth_router.get("/users/me")
async def read_users_me(current_user: User = Authorization()):
    return current_user

