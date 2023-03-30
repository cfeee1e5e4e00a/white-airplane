from bson import ObjectId
from typing import Literal, TypedDict
from pymongo.collection import Collection

from src.db import mongo


Role = Literal["admin", "user", "operator"]


class User(TypedDict):
    _id: ObjectId
    login: str
    password: str
    role: Role


def create_user(username: str, password_hash: str, role: Role):
    collection: Collection["User"] = mongo.db.users
    collection.insert_one(User(login=username, password=password_hash, role=role))


def get_user_by_id(id: str) -> User:
    collection: Collection["User"] = mongo.db.users
    return collection.find_one({"_id": id})


def get_user_by_username(login: str) -> User | None:
    collection: Collection["User"] = mongo.db.users
    return collection.find_one({"login": login})
