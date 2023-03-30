"""RelayController is additional layer between pure sensor logic and API."""

from typing import Dict, List
from paho.mqtt.client import Client

from src.models.commutation_state import *


class RelayController:
    """
    Entity containig all machine electric board operative logic.

    RelayController transfers new states for relays through MQTT.
    """

    def __init__(self, client: Client) -> None:
        """
        Initialize RelayController for future publishing.

        Initializes Clients for PowerSupplies and Houses.
        """
        self.client = client

    def change_relays_state(
        self, flat_relays: List[List[int]], supply_relays: int
    ) -> None:
        """Publish state messages to supply and house topics."""
        self.__publish_flat_relays(flat_relays)
        self.__publish_supply_relays(supply_relays)

    def __publish_flat_relays(self, flat_relays: List[List[int]]) -> None:
        """Publish new states for relay connections to flats on bread board"""
        for house_index, single_house_relays in enumerate(flat_relays):
            for flat_index, supply_index in enumerate(single_house_relays):
                self.client.publish(
                    f"flats_relays/{house_index}", f"{flat_index},{int(supply_index)}"
                )

    def __publish_supply_relays(self, reserve_connection_state: int) -> None:
        """Publish new states for relay connections to houses on bread board"""
        self.client.publish("supply_relays", reserve_connection_state)
