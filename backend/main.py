import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.redis import redis_default, REDIS
from src.influx import influx
from src.services.sensors_aggregator import SensorsAggregator
from src.api.auth import auth_router
from src.api.graphql import graphql_router


app = FastAPI()

if __name__ == "__main__":
    SensorsAggregator(REDIS, influx)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(auth_router)
    app.include_router(graphql_router, prefix="/graphql")
    uvicorn.run(app, host="0.0.0.0", port=8000)
