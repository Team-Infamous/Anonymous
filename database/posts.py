from database.mongodb import db

posts_col = db["posts"]

async def save_post(channel_id: int, message_id: int, content: dict):
    await posts_col.update_one(
        {"message_id": message_id},
        {"$set": {"channel_id": channel_id, "content": content}},
        upsert=True
    )

async def get_post(message_id: int):
    return await posts_col.find_one({"message_id": message_id})

async def delete_post(message_id: int):
    await posts_col.delete_one({"message_id": message_id})
