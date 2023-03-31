from itertools import chain
import re
from typing import Dict, List, Set
from redis import StrictRedis

from src.models.commutation_state import *
from src.services.sensors_aggregator import SENSOR_DATACLASSES

TOPOLOGY_DATACLASSES = [Flat, House, PowerSupply]

SENSOR_NAMES = [f"{c.__name__}" for c in SENSOR_DATACLASSES]


class Deserializator:
    REDIS_PATTERNS = [f"{n}*" for n in SENSOR_NAMES]

    SENSOR_FIELDS_REGEX = {
        "house": re.compile("(?<=house: )\d+"),
        "flat": re.compile("(?<=flat: )\d+"),
        "supply": re.compile("(?<=supply: )\d+"),
        "position": re.compile("(?<=position: )(IN|OUT)"),
    }

    SENSOR_NAME_REGEX = re.compile(r"\b\w*(?= {)")

    SENSOR2TOPOLOGY = {
        "FlatTemperature": Flat,
        "FlatHumidity": Flat,
        "FlatCurrent": Flat,
        "PowerSupplyCurrent": PowerSupply,
    }

    SENSOR2TOPOLOGY_ARG = {
        "FlatTemperature": "temperature",
        "FlatHumidity": "humidity",
        "FlatCurrent": "consumption_current",
        "PowerSupplyCurrent": {
            "IN": "consumption_current",
            "OUT": "generation_current",
        },
    }

    def __init__(self, redis: StrictRedis) -> None:
        self.redis = redis

    def __call__(self) -> List[PowerSupply]:
        supplies: Dict[str, PowerSupply] = {}
        houses: Dict[str, House] = {}
        houses_list: List[House] = []
        flat_in_house: Set[str] = set()
        flats_list: List[Flat] = []

        redis_keys = self.__redis_get_sensor_keys()
        sensor_keys = [self.__match_fields(key) for key in redis_keys]

        for d in sensor_keys:
            # print(d)
            for id_type, node_id in d.items():
                match id_type:
                    case "house":
                        houses[node_id] = House(flats_list)
                    case "supply":
                        supplies[node_id] = PowerSupply(houses_list)

            match d:
                case {"house": a, "flat": b}:
                    if d["house"] + d["flat"] not in flat_in_house:
                        flat_in_house.add(d["house"] + d["flat"])
                        flats_list.append(Flat())

        supplies_list: List[PowerSupply] = []

        z_d_l = list(zip([supplies, houses], [supplies_list, houses_list]))

        for i in range(len(z_d_l)):
            for j in range(len(list(z_d_l[i][0].keys()))):
                z_d_l[i][1].append(z_d_l[i][0][str(j)])

        houses_count = len(houses_list)
        relays_count = len(flats_list)
        flats_count = relays_count // houses_count
        for i in range(houses_count):
            supplies_list[0].connections[i].flats = flats_list[i : i + flats_count]
        for i in range(relays_count % houses_count):
            supplies_list[0].connections[
                -(relays_count % houses_count) + i
            ].flats.append(flats_list[-(relays_count % houses_count) + i])

        for key, d in zip(redis_keys, sensor_keys):
            data = self.redis.get(key)
            sensor_name = re.findall(Deserializator.SENSOR_NAME_REGEX, key)[0]
            resolved_class = Deserializator.SENSOR2TOPOLOGY[sensor_name].__name__
            match resolved_class:
                case "Flat":
                    flat = (
                        supplies_list[0]
                        .connections[int(d["house"])]
                        .flats[int(d["flat"])]
                    )
                    arg_name = Deserializator.SENSOR2TOPOLOGY_ARG[sensor_name]
                    setattr(flat, arg_name, data)
                    supplies_list[0].connections[int(d["house"])].flats[
                        int(d["flat"])
                    ] = flat
                case "PowerSupply":
                    supply = supplies_list[int(d["supply"])]
                    arg_name = Deserializator.SENSOR2TOPOLOGY_ARG[sensor_name][
                        d["position"]
                    ]
                    setattr(supply, arg_name, data)
                    supplies_list[int(d["supply"])] = supply

        return supplies_list

    def __match_fields(self, key2parse: str):
        # print(key2parse)
        return {
            key: match[0]
            for key, pattern in Deserializator.SENSOR_FIELDS_REGEX.items()
            if not not (match := re.findall(pattern, key2parse))
        }

    def __redis_get_sensor_keys(self) -> List[str]:
        return list(
            chain.from_iterable(
                self.redis.keys(pattern) for pattern in Deserializator.REDIS_PATTERNS
            )
        )
