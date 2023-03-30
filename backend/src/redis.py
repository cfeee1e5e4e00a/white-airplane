import redis

from src.env import env

REDIS_HOST = env["REDIS_HOST"]
REDIS_PORT = int(env["REDIS_PORT"])
REDIS_PASS = env["REDIS_PASS"]

REDIS = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASS,
    charset="utf-8",
    decode_responses=True
)