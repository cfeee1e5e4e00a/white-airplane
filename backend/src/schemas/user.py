from http.client import HTTPException
from typing import Union, Literal, TypedDict

from bson import ObjectId
from pydantic.fields import Field
from pydantic.main import BaseModel
from pymongo.collection import Collection
from fastapi import status

from src.db import mongo


Role = Literal['ADMIN', 'USER', 'OPERATOR']


class User(TypedDict):
    _id: ObjectId
    login: str
    password: str
    role: Role


def get_user(id: str) -> User:
    collection: Collection['User'] = mongo.db.users
    return collection.find_one({'_id': id})


def find_user_by_username(login: str) -> User | None:
    collection: Collection['User'] = mongo.db.users
    return collection.find_one({'login': login})


def check_login_in_db(login: str):
    collection: Collection['User'] = mongo.db.users
    if not collection.find_one({'login': login}):
        return False
    else:
        return True

# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = await users_utils.get_user_by_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     if not user["is_active"]:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
#         )
#     return user
def get_user_by_token(token: str):
    return
