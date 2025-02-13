from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["AnonymousBot"]
channels_col = db["channels"]
posts_col = db["posts"]
