from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class UserRepository:
    @staticmethod
    async def get_user_by_username(db: AsyncIOMotorDatabase, username: str):
        # Шукаємо в колекції "users"
        user = await db.users.find_one({"username": username})
        if user:
            user["_id"] = str(user["_id"]) # Перетворюємо ObjectId в рядок
        return user

  
@staticmethod
async def create_user(db, username, hashed_password):
    user_dict = {
        "username": username,
        "hashed_password": hashed_password 
    }
    
        result = await db.users.insert_one(user_dict)
        return {"_id": str(result.inserted_id), "username": username}