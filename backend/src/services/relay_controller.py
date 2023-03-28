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
        self.supplies = power_supplies
        self.supply_clients = self.__init_supply_clients()

        self.houses = power_supplies[0].connections
        self.house_clients  = self.__init_house_clients()

    def change_relays_state(self, schema: Dict[str, List[List[bool]]]) -> None:
        """Publish state messages to supply and house topics."""
        flat_relays  = schema['flat_relays']
        self.__publish_flat_relays(flat_relays)

        house_relays = schema['house_relays']
        self.__publish_house_relays(house_relays)
    
    def __init_house_clients(self) -> List[Client]:
        """
        Initialize all house clients.
        
        Name all clients, Set callback for publishing, Connect to broker.
        """
        def on_publish(client, userdata, mid):
            """TODO: Logging."""

        def init_client(name: str) -> Client:
            client = Client(name)
            client.on_publish = on_publish # ?? nahuya
            client.connect(MQTT_BROKER, MQTT_PORT)
            return client

        clients = [init_client("house_{i}") for i in range(len(self.houses))]

        return clients
    
    def __init_supply_clients(self) -> List[Client]:
        """
        Initialize all supply clients.
        
        Name all clients, Set callback for publishing, Connect to broker.
        """
        def on_publish(client, userdata, mid):
            """TODO: Logging."""

        def init_client(name: str) -> Client:
            client = Client(name)
            client.on_publish = on_publish # ?? nahuya
            client.connect(MQTT_BROKER, MQTT_PORT)
            return client

        clients = [init_client("supply_{i}") for i in range(len(self.supplies))]

        return clients

    def __publish_flat_relays(self, flat_relays) -> None:
        """Publish new states for relays connected to flats on bread board"""
        for house_index, single_house_relays in enumerate(flat_relays):
            for flat_index, is_relay_connected in enumerate(single_house_relays):
                house_client = self.house_clients[house_index]
                house_client.publish(
                    f"flats/{house_index}/{flat_index}/relays", 
                    int(is_relay_connected)
                )

    def __publish_house_relays(self, house_relays) -> None:
        """Publish new states for relays connected to houses on bread board"""
        for supply_index, single_supply_relays in enumerate(house_relays):
            for house_index, is_house_connected in enumerate(single_supply_relays):
                supply_client = self.supply_clients[supply_index]
                supply_client.publish(
                    f"supplies/{house_index}/{supply_index}/relays",
                    int(is_house_connected)
                )
