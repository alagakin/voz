import motor.motor_asyncio
from src.config import MONGO_HOST, MONGO_PASS, MONGO_PORT, MONGO_USER


async def get_client():
    return motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/")
