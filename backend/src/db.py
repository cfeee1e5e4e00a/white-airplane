import os
from pymongo import MongoClient
from src.env import env

mongo = MongoClient(env["DB_URI"])
