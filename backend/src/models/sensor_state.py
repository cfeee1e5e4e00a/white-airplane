"""hui."""
from src.models.commutation_state import *
from json import loads
from dacite import from_dict


@dataclass
class FlatTemperature:
    house: int
    flat: int
    value: Celsius

    def __str__(self):
        return f"{self.__class__.__name__} {{ house: {self.house}, flat: {self.flat} }}"


@dataclass
class FlatHumidity:
    house: int
    flat: int
    value: Density

    def __str__(self):
        return f"{self.__class__.__name__} {{ house: {self.house}, flat: {self.flat} }}"


@dataclass
class FlatCurrent:
    house: int
    flat: int
    value: Amps

    def __str__(self):
        return f"{self.__class__.__name__} {{ house: {self.house}, flat: {self.flat} }}"


@dataclass
class PowerSupplyCurrent:
    supply: int
    position: str
    value: Amps

    def __str__(self):
        return f"{self.__class__.__name__} {{ supply: {self.supply}, position: {self.position} }}"


SensorData = FlatTemperature | FlatHumidity | FlatCurrent | PowerSupplyCurrent


def sensor_data_from_str(cls, data: str) -> SensorData:
    # print(data)
    return cls(**eval(data))
    # parsed = loads(data)
    # return from_dict(data_class=cls, data=parsed)
