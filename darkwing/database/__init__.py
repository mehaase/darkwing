import os

from motor.motor_asyncio import AsyncIOMotorClient
from trio_asyncio import aio_as_trio


@aio_as_trio
async def connect(host: str, collection: str) -> AsyncIOMotorClient:
    return AsyncIOMotorClient(host or os.getenv("DARKWING_MONGO_HOST"))
