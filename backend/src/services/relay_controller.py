"""RelayController is additional layer between pure sensor logic and API."""

from typing import Callable, Dict, List
from paho.mqtt.client import Client
from env import env
from models.commutation_state import *

MQTT_BROKER = env["MQTT_BROKER"]
MQTT_PORT   = int(env["MQTT_PORT"])

class RelayController:
    """
    Entity containig all machine electric board operative logic.
    
    RelayController transfers new states for relays through MQTT.
    """

    def __init__(self, power_supplies: List[PowerSupply]) -> None:
        """
        Initialize RelayController for future publishing.

        Initializes Clients for PowerSupplies and Houses.
        """
        self.publisher = RelayController.__init_publisher("driver")

    def change_relays_state(self, schema: Dict[str, List[List[bool]]]) -> None:
        """Publish state messages to supply and house topics."""
        flat_relays  = schema['flat_relays']
        self.__publish_flat_relays(flat_relays)

        house_relays = schema['house_relays']
        self.__publish_house_relays(house_relays)
    
    @staticmethod
    def __init_publisher(name: str) -> Client:
        def on_publish(client, userdata, mid):
            """TODO: Logging."""

        publisher = Client(name)
        publisher.on_publish = on_publish # future logging
        publisher.connect(MQTT_BROKER, MQTT_PORT)
        
        return publisher

    def __publish_flat_relays(self, flat_relays) -> None:
        """Publish new states for relays connected to flats on bread board"""
        for house_index, single_house_relays in enumerate(flat_relays):
            for flat_index, is_relay_connected in enumerate(single_house_relays):
                self.publisher.publish(
                    f"flats/{house_index}/{flat_index}/relays", 
                    int(is_relay_connected)
                )

    def __publish_house_relays(self, house_relays) -> None:
        """Publish new states for relays connected to houses on bread board"""
        for supply_index, single_supply_relays in enumerate(house_relays):
            for house_index, is_house_connected in enumerate(single_supply_relays):
                self.publisher.publish(
                    f"supplies/{house_index}/{supply_index}/relays",
                    int(is_house_connected)
                )
