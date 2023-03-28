
import time
from datetime import datetime, timedelta

import fastapi_login
from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from backend.src.env import env

from backend.src.schemas.user import find_user_by_login

auth_router = APIRouter()

pwd_context = CryptContext(schemes=['bcrypt'])

manager = fastapi_login.LoginManager(env['AUTH_SECRET'], '/login')

EXPIRES_AFTER_DAYS = 1


@auth_router.post('/login')
def login(data: OAuth2PasswordRequestForm = Depends()):
    user = find_user_by_login(data.username)
    if not user:
        raise HTTPException(status_code=400, detail='Пользователь не найден')
    if not pwd_context.verify(data.username, user.password):
        raise HTTPException(status_code=400, detail='Неверный пароль')
    exp = time.mktime(datetime.now() + timedelta(days=EXPIRES_AFTER_DAYS))
    return jwt.encode({'username': user.login, 'role': user.role, 'exp': exp}, env['JWT_SECRET'], algorithm='HS256')
