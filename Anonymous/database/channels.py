from .mongodb import channels_col

async def add_channel(channel_id: int, channel_name: str, username: str):
    if not await channels_col.find_one({"channel_id": channel_id}):
        await channels_col.insert_one(
            {"channel_id": channel_id, "name": channel_name, "username": username}
        )
        return True
    return False

async def get_channels():
    return await channels_col.find().to_list(None)

async def get_channel(channel_id: int):
    return await channels_col.find_one({"channel_id": channel_id})

async def delete_channel(channel_id: int):
    await channels_col.delete_one({"channel_id": channel_id})
