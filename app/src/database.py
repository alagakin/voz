import motor.motor_asyncio
import pymongo
from pymongo import MongoClient

from config import MONGO_HOST, MONGO_PASS, MONGO_PORT, MONGO_USER


async def get_async_client():
    return motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/")


def get_sync_client() -> MongoClient:
    return pymongo.MongoClient(
        f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/"
    )
