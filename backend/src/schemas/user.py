from typing import Union, Literal, TypedDict

from bson import ObjectId
from pydantic.main import BaseModel
from pymongo.collection import Collection

from src.db import mongo

Role = Literal['ADMIN', 'USER', 'OPERATOR']


class User(TypedDict):
    _id: ObjectId
    login: str
    password: str
    role: Role

class UserCreate(BaseModel):
    login: str
    password: str
    role: Role

def get_user(id: str) -> User:
    collection: Collection['User'] = mongo.db.users
    return collection.find_one({'_id': id})


def find_user_by_login(login: str) -> User | None:
    collection: Collection['User'] = mongo.db.users
    return collection.find_one({'login': login})

def create_user():
    pass
