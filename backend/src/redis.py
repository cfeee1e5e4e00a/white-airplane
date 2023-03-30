import random
import redis

from src.models.commutation_state import (
    DEFAULT_HOUSE_COUNT,
    DEFAULT_RELAY_COUNT,
    DEFAULT_SUPPLY_COUNT,
)
from src.models.sensor_state import sensor_data_from_str
from src.services.sensors_aggregator import SENSOR_SCHEMAS, SENSOR_TOPICS, TOPIC2CLASS

from src.env import env

REDIS_HOST = env["REDIS_HOST"]
REDIS_PORT = int(env["REDIS_PORT"])
REDIS_PASS = env["REDIS_PASS"]

REDIS = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASS,
    charset="utf-8",
    decode_responses=True,
)


def redis_default():
    for inout in ["IN", "OUT"]:
        for supply_id in range(DEFAULT_SUPPLY_COUNT):
            for house_id in range(DEFAULT_HOUSE_COUNT):
                for flat_id in range(
                    DEFAULT_RELAY_COUNT // DEFAULT_HOUSE_COUNT
                    + (
                        house_id
                        >= DEFAULT_HOUSE_COUNT
                        - DEFAULT_RELAY_COUNT % DEFAULT_HOUSE_COUNT
                    )
                ):
                    for topic, schema in zip(SENSOR_TOPICS, SENSOR_SCHEMAS):
                        msg = schema.format(
                            house_id=house_id,
                            flat_id=flat_id,
                            supply_id=supply_id,
                            inout=inout,
                            value=random.random() * 30 + 10,
                        )
                        sensor_data = sensor_data_from_str(TOPIC2CLASS[topic], msg)

                        REDIS.set(str(sensor_data), sensor_data.value)

    return "Done! Now check Redis database."
