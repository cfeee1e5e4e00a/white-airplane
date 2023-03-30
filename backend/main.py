import uvicorn
from fastapi import FastAPI

from src.api.auth import auth_router
from src.api.graphql import graphql_router


app = FastAPI()

if __name__ == "__main__":
    app.include_router(auth_router)
    app.include_router(graphql_router, prefix="/graphql")
    uvicorn.run(app, host="0.0.0.0", port=8000)
