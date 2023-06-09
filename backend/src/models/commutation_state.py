"""File containing business logic."""

from dataclasses import dataclass, field
from typing import ClassVar, List

Volts = float
Amps = float
Power = float
Density = float
Celsius = float

DEFAULT_SUPPLY_COUNT = 3
DEFAULT_HOUSE_COUNT = 6
DEFAULT_FLAT_COUNT = 2
DEFAULT_RELAY_COUNT = 14
DISCONNECTED_RESERVE_STATE = 3


@dataclass
class Flat:
    """
    Struct containing sensor data.

    Leaf in supply-house-flat topology.
    """

    supply_index: int = DISCONNECTED_RESERVE_STATE
    consumption_current: Amps = 0.0
    humidity: Density = 100.0
    temperature: Celsius = 0.0


@dataclass
class House:
    """
    Commutation Layer between supplies and flats.

    Leaf in supply-house topology and root in house-flat topology.
    """

    flats: List[Flat] = field(default_factory=lambda: [Flat()] * DEFAULT_FLAT_COUNT)

    @property
    def house_consumption_current(self) -> Amps:
        """:return: Integral for house consumption current."""
        return sum(flat.consumption_current for flat in self.flats)


@dataclass
class PowerSupply:
    """
    Struct containing PowerSupply data.

    Root in supply-house-flat topology.
    """

    connections: List[House] = field()
    generation_current: Amps = 0.0
    consumption_current: Amps = 0.0

    SUPPLY_VOLTAGE: ClassVar[Volts] = 12.0
    OUTLET_VOLTAGE: ClassVar[Volts] = 220.0

    @property
    def power(self) -> Power:
        """:return: self power of power supply."""
        return self.SUPPLY_VOLTAGE * self.generation_current

    @property
    def ideal_power(self) -> Power:
        """:return: ideal power of power supply."""
        return self.OUTLET_VOLTAGE * self.consumption_current

    @property
    def efficiency(self) -> float:
        """:return: power supply efficiency."""
        return self.power / self.ideal_power
