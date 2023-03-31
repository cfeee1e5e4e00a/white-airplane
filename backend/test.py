from json import dumps
from time import sleep
from typing import Any
import random
import redis
from itertools import chain

from src.services.deserializator import Deserializator
from src.services.balancer import (
    apply_balancer,
    disconnect_all_relays as balancer,
    balance_by_efficiency as efficiency_balancer,
)
from src.services.relay_controller import RelayController
from src.services.sensors_aggregator import (
    SensorsAggregator,
    SENSOR_SCHEMAS,
    SENSOR_TOPICS,
    SENSOR_DATACLASSES,
)
from src.models.commutation_state import *
from src.models.sensor_state import sensor_data_from_str

from src.redis import *
from src.mqtt import *


def balance_efficiency_default():
    houses = [House() for _ in range(DEFAULT_HOUSE_COUNT)]

    return dumps(
        apply_balancer(balancer, [PowerSupply(houses)] * DEFAULT_SUPPLY_COUNT),
        sort_keys=True,
        indent=4,
    )


def balance_efficiency_simulation():
    def count(i: int):
        return (DEFAULT_RELAY_COUNT * (i + 1)) // DEFAULT_HOUSE_COUNT - (
            DEFAULT_RELAY_COUNT * i
        ) // DEFAULT_HOUSE_COUNT

    houses = [House([Flat()] * count(i)) for i in range(count(0) + 1)]

    return dumps(
        apply_balancer(balancer, [PowerSupply(houses)] * DEFAULT_SUPPLY_COUNT),
        sort_keys=True,
        indent=4,
    )


def balance_efficiency_1():
    x = [1, 14, 7, 9, 7, 3, 3, 2, 1, 6, 1, 6, 3, 4]

    houses = [
        House(
            [
                Flat(consumption_current=x.pop(0))
                for j in range(DEFAULT_RELAY_COUNT // DEFAULT_HOUSE_COUNT)
            ]
        )
        for i in range(DEFAULT_HOUSE_COUNT)
    ]

    for i in range(DEFAULT_RELAY_COUNT % DEFAULT_HOUSE_COUNT):
        houses[-(DEFAULT_RELAY_COUNT % DEFAULT_HOUSE_COUNT) + i].flats.append(
            Flat(consumption_current=x.pop(0))
        )

    # print(houses)

    return dumps(
        apply_balancer(
            efficiency_balancer, [PowerSupply(houses)] * DEFAULT_SUPPLY_COUNT
        ),
        sort_keys=True,
        indent=4,
    )


def relay_controller_init():
    d = RelayController(CLIENT)

    return d.client


def relay_controller_publish_scheme():
    def count(i: int):
        return (DEFAULT_RELAY_COUNT * (i + 1)) // DEFAULT_HOUSE_COUNT - (
            DEFAULT_RELAY_COUNT * i
        ) // DEFAULT_HOUSE_COUNT

    houses = [House([Flat()] * count(i)) for i in range(count(0) + 1)]
    supplies = [PowerSupply(houses)] * DEFAULT_SUPPLY_COUNT

    rc = RelayController(CLIENT)

    scheme = apply_balancer(balancer, supplies)

    rc.change_relays_state(scheme, 0)

    return "Done! Check topic!"


def redis_connection_and_set() -> Any:
    REDIS.set("hui", "413N")
    r = REDIS.get("hui")
    REDIS.delete("hui")
    return r


def create_sensor_aggregator():
    rediska = redis.StrictRedis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASS,
        charset="utf-8",
        decode_responses=True,
    )
    SensorsAggregator(rediska)


def sensors_aggregator_init():

    sa = SensorsAggregator(REDIS)

    sleep(1)

    patterns = [f"{c.__name__}*" for c in SENSOR_DATACLASSES]

    for topic, schema in zip(SENSOR_TOPICS, SENSOR_SCHEMAS):
        data = schema.format(
            house_id=random.randint(1000, 1004),
            flat_id=random.randint(1000, 1008),
            supply_id=random.randint(1000, 1003),
            inout=random.choice(["IN", "OUT"]),
            value=random.random() * 30 + 10,
        )
        _, __ = CLIENT.publish(topic, data)

        sensor_key = str(sensor_data_from_str(TOPIC2CLASS[topic], data))

        patterns.append(sensor_key)

    sleep(1)

    sa.stop()

    r = list(chain.from_iterable(REDIS.keys(pattern) for pattern in patterns))

    REDIS.delete(*r)

    return r


def deserializator_call():
    deserializator: Deserializator = Deserializator(REDIS)

    return dumps(
        apply_balancer(balancer, deserializator()),
        sort_keys=True,
        indent=4,
    )


if __name__ == "__main__":
    tests = [
        balance_efficiency_default,
        balance_efficiency_simulation,
        balance_efficiency_1,
        # relay_controller_init,
        # relay_controller_publish_scheme,
        # redis_connection_and_set,
        # sensors_aggregator_init,
        # redis_default,
        # deserializator_call,
    ]

    m = max(len(s.__name__) for s in tests)

    for i, test in enumerate(tests, 1):
        t = f'╔{"═"*(m//2)} Test {i} {"═"*(m//2)}╗'
        print(t)
        n = test.__name__
        d = len(t) - 2
        print(f"║{{n:^{d}s}}║".format(n=n))
        print(f'╠{"═"*d}╣')
        rs = f"{test()}".split("\n")
        for r in rs:
            chunks = len(r)
            chunk_size = m + 5 - d % 2
            k = [
                "║ "
                + r[i : i + chunk_size]
                + f"{' '*(d - (chunk_size if i + chunk_size < chunks else len(r) % chunk_size) - 2)} ║"
                for i in range(0, chunks, chunk_size)
            ]
            print("\n".join(k))
        print(f'╚{"═"*d}╝')
        print()
