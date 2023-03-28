import strawberry
import uvicorn
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from backend.src.api.auth import auth_router


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return 'Hello World'


schema = strawberry.Schema(Query)

graphql_router = GraphQLRouter(schema)

app = FastAPI()

if __name__ == "__main__":
    app.include_router(auth_router)
    app.include_router(graphql_router, prefix='/graphql')
    uvicorn.run(app, host='0.0.0.0', port=8000)
