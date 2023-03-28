import os
from pymongo import MongoClient
from backend.src.env import env

mongo = MongoClient(env['DB_URI'])
