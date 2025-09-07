from motor.motor_asyncio import AsyncIOMotorClient
from config import config

client = AsyncIOMotorClient(config.MONGO_URL)
db = client[config.DB_NAME]

async def close_db_client():
    client.close()
