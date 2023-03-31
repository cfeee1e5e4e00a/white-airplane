"""
LoadBalancer protocol for API. Using strategy pattern.

Strategies:
1) CancelStrategy   - allways False
2) HumidityBased    - rebalancing for humidity balance
3) TemperatureBased - rebalancing for temperature balance
4) EfficiencyBased  - rebalancing for efficiency balance
"""

from itertools import chain
from typing import Dict, Protocol
from src.models.commutation_state import *

RelayScheme = List[List[int]]

FLAT_RELAY_DISABLED = 3


class LoadBalancer(Protocol):
    """Strategy class for load balancing."""

    def __call__(power_supplies: List[PowerSupply]) -> RelayScheme:
        """
        Analyze topology data and get new relay connections.

        :return:
        2 arrays:
        'flat_relays': connection house_index - flat_idx
        'house_relays': connection supply_idx - house_idx
        """


def apply_balancer(
    load_balancer: LoadBalancer,
    power_supplies: List[PowerSupply],
) -> RelayScheme:
    """Apply balancing Strategy to list of supplies."""
    return load_balancer(power_supplies)


def disconnect_all_relays(power_supplies: List[PowerSupply]) -> RelayScheme:
    """Cancel Strategy. Disables all relays."""
    return [
        [FLAT_RELAY_DISABLED] * len(house.flats)
        for house in power_supplies[0].connections
    ]


def balance_evenly_by_current(power_supplies: List[PowerSupply]) -> RelayScheme:
    """Power Supply Efficiency based load balance strategy."""
    flats = list(chain.from_iterable(h.flats for h in power_supplies[0].connections))

    N = len(power_supplies)

    currents = [f.consumption_current for f in flats]

    x = enumerate(currents)

    n = len(currents)

    x = sorted(x, key=lambda l: l[1])

    thresh = sum(currents) // N

    G = [[] for _ in range(N)]

    while len(x) > n % N:
        index, c = x.pop()

        for i in range(N):
            if sum([g[1] for g in G[i]]) + c <= thresh:
                G[i].append((index, c))
                break

    for i in range(n % N):
        G[i].append(x.pop())

    for i in range(N):
        for index, _ in G[i]:
            flats[index].supply_index = i

    return [
        [flat.supply_index for flat in house.flats]
        for house in power_supplies[0].connections
    ]


def balance_by_humidity(power_supplies: List[PowerSupply]) -> RelayScheme:
    """Flat Humidity based load balance strategy."""
    return disconnect_all_relays(power_supplies)


def balance_by_temperature(power_supplies: List[PowerSupply]) -> RelayScheme:
    """Flat Temperature based load balance strategy."""
    return disconnect_all_relays(power_supplies)
