from itertools import chain
import strawberry
from strawberry.types import Info
import asyncio
from typing import List

from src.schemas.user import User
from src.dependencies.auth import IsAuthenticated, AuthGraphQLRouter
from src.services.deserializator import Deserializator
from src.models.sensor_state import Celsius, Density, Power
from src.redis import REDIS


state_deserializator = Deserializator(REDIS)


@strawberry.type
class Supply:
    consumption_power: Power
    generation_power: Power
    efficiency: float


@strawberry.type
class Flat:
    powered_by: int
    consumption: Power
    temperature: Celsius
    humidity: Density


@strawberry.type
class State:
    supplies: List[Supply]
    flats: List[Flat]


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


@strawberry.type
class Subscription:
    @strawberry.subscription(permission_classes=[IsAuthenticated])
    async def get_state(self, info: Info) -> State:
        user: User = info.context.get("user")

        while True:
            state = state_deserializator()

            power_supplies: List[Supply] = [
                Supply(
                    consumption_power=supply.power,
                    generation_power=supply.ideal_power,
                    efficiency=supply.efficiency,
                )
                for supply in state
            ]

            flats: List[Flat] = [
                Flat(
                    powered_by=flat.supply_index,
                    consumption=flat.consumption_current,
                    temperature=flat.temperature,
                    humidity=flat.humidity,
                )
                for flat in list(
                    chain.from_iterable([house.flats for house in state[0].connections])
                )
            ]

            yield State(supplies=power_supplies, flats=flats)

            await asyncio.sleep(1)


schema = strawberry.Schema(query=Query, subscription=Subscription)
graphql_router = AuthGraphQLRouter(schema, graphiql=True)
