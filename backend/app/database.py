from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)

database = client.user_authentication

users_collection = database.get_collection("users")

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "full_name": user["full_name"],
        "hashed_password": user["hashed_password"],
    }
