from services.balancer import apply_balancer, disconnect_all_relays as balancer
from services.relay_controller import RelayController
from models.commutation_state import *

from json import dumps

def balance_efficiency_default():
    houses = [House() for _ in range(DEFAULT_HOUSE_COUNT)]

    print(
        dumps(
            apply_balancer(balancer, [PowerSupply(houses)] * DEFAULT_SUPPLY_COUNT),
            sort_keys=True, 
            indent=4
        )
    )

def balance_efficiency_simulation():
    def count(i: int):
        return (DEFAULT_RELAY_COUNT * (i + 1)) // DEFAULT_HOUSE_COUNT \
            - (DEFAULT_RELAY_COUNT * i) // DEFAULT_HOUSE_COUNT

    houses = [House([Flat()] * count(i)) for i in range(count(0) + 1)]

    print(
        dumps(
            apply_balancer(balancer, [PowerSupply(houses)] * DEFAULT_SUPPLY_COUNT),
            sort_keys=True, 
            indent=4
        )
    )

def relay_controller_init():
    def count(i: int):
        return (DEFAULT_RELAY_COUNT * (i + 1)) // DEFAULT_HOUSE_COUNT \
            - (DEFAULT_RELAY_COUNT * i) // DEFAULT_HOUSE_COUNT

    houses = [House([Flat()] * count(i)) for i in range(count(0) + 1)]
    supplies = [PowerSupply(houses)] * DEFAULT_SUPPLY_COUNT

    d = RelayController(supplies)

    print(d.publisher)

def relay_controller_publish_scheme():
    def count(i: int):
        return (DEFAULT_RELAY_COUNT * (i + 1)) // DEFAULT_HOUSE_COUNT \
            - (DEFAULT_RELAY_COUNT * i) // DEFAULT_HOUSE_COUNT

    houses = [House([Flat()] * count(i)) for i in range(count(0) + 1)]
    supplies = [PowerSupply(houses)] * DEFAULT_SUPPLY_COUNT

    rc = RelayController(supplies)

    scheme = apply_balancer(balancer, supplies)

    rc.change_relays_state(scheme)


if __name__ == '__main__':
    for i, test in enumerate([
                        balance_efficiency_default, 
                        balance_efficiency_simulation,
                        relay_controller_init,
                        relay_controller_publish_scheme,
                        ], 1):
        print(f'#========# Test {i} #=======#')
        test()