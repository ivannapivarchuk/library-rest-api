from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://mongodb_container:27017.")
client = AsyncIOMotorClient(MONGO_URL)
db = client.library_db

async def get_db():
  
    return db