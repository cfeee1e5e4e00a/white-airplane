import strawberry
from strawberry.types import Info
import asyncio

from src.schemas.user import User
from src.dependencies.auth import IsAuthenticated, AuthGraphQLRouter

counter = 1


@strawberry.type
class State:
    count: int
    username: str
    role: str


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


@strawberry.type
class Subscription:
    @strawberry.subscription(permission_classes=[IsAuthenticated])
    async def get_state(self, info: Info) -> State:
        global counter
        user: User = info.context.get("user")

        while True:
            yield State(
                count=counter, username=user.get("login"), role=user.get("role")
            )
            counter += 1
            await asyncio.sleep(1)


schema = strawberry.Schema(query=Query, subscription=Subscription)
graphql_router = AuthGraphQLRouter(schema, graphiql=True)
