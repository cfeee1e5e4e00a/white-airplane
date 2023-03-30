from json import dumps
from time import sleep
from typing import Any
import random

import redis

from src.services.balancer import apply_balancer, disconnect_all_relays as balancer
from src.services.relay_controller import RelayController
from src.services.sensors_aggregator import SensorsAggregator
from src.models.commutation_state import *

from src.redis import *
from src.mqtt import *

def balance_efficiency_default():
    houses = [House() for _ in range(DEFAULT_HOUSE_COUNT)]

    return dumps(
            apply_balancer(balancer, [PowerSupply(houses)] * DEFAULT_SUPPLY_COUNT),
            sort_keys=True, 
            indent=4
        )

def balance_efficiency_simulation():
    def count(i: int):
        return (DEFAULT_RELAY_COUNT * (i + 1)) // DEFAULT_HOUSE_COUNT \
            - (DEFAULT_RELAY_COUNT * i) // DEFAULT_HOUSE_COUNT

    houses = [House([Flat()] * count(i)) for i in range(count(0) + 1)]

    return dumps(
            apply_balancer(balancer, [PowerSupply(houses)] * DEFAULT_SUPPLY_COUNT),
            sort_keys=True, 
            indent=4
        )

def relay_controller_init():
    d = RelayController(CLIENT)

    return d.client

def relay_controller_publish_scheme():
    def count(i: int):
        return (DEFAULT_RELAY_COUNT * (i + 1)) // DEFAULT_HOUSE_COUNT \
            - (DEFAULT_RELAY_COUNT * i) // DEFAULT_HOUSE_COUNT

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
        decode_responses=True
    )
    SensorsAggregator(rediska)

def sensors_aggregator_init():

    sa = SensorsAggregator(REDIS)

    sleep(1)

    for topic, schema in zip(SensorsAggregator.SENSOR_TOPICS, 
                            SensorsAggregator.SENSOR_SCHEMAS):
        _, __ = CLIENT.publish(
            topic, 
            schema.format(
                id=random.randint(0, 6), 
                inout=random.choice(['IN', 'OUT']),
                value=random.random() * 30 + 10
            ),
        )


    sleep(1)

    sa.stop()

    return list(REDIS.scan_iter('user:*'))

if __name__ == '__main__':
    tests = [
        balance_efficiency_default, 
        balance_efficiency_simulation,
        relay_controller_init,
        relay_controller_publish_scheme,
        redis_connection_and_set,
        sensors_aggregator_init,
    ]

    m = max(len(s.__name__) for s in tests)

    for i, test in enumerate(tests, 1):
        t = f'╔{"═"*(m//2)} Test {i} {"═"*(m//2)}╗'
        print(t)
        n = test.__name__
        d = len(t)-2
        print(f'║{{n:^{d}s}}║'.format(n=n))
        print(f'╠{"═"*d}╣')
        rs = f'{test()}'.split('\n')
        for r in rs:
            chunks = len(r)
            chunk_size = m + 5 - d % 2
            k = [ "║ " + r[i:i+chunk_size] + f"{' '*(d - (chunk_size if i + chunk_size < chunks else len(r) % chunk_size) - 2)} ║" for i in range(0, chunks, chunk_size) ]
            print("\n".join(k))
        print(f'╚{"═"*d}╝')
        print()