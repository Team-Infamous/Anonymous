from pymongo import MongoClient
from Anonymous.config import MONGO_URI, DB_NAME

class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.channels = self.db["channels"]
    
    def add_channel(self, chat_id, name, username):
        self.channels.update_one(
            {"chat_id": chat_id},
            {"$set": {"name": name, "username": username}},
            upsert=True
        )

    def get_channels(self):
        return list(self.channels.find())

    def remove_channel(self, chat_id):
        self.channels.delete_one({"chat_id": chat_id})
