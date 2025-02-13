from pyrogram import filters
from pyrogram.types import Message
from Anonymous.database import db
from Anonymous.utils.admin_check import is_admin
from Anonymous import app as Client

@Client.on_message(filters.command("addchannel") & filters.private )
async def add_channel(client, message: Message):
    await message.reply_text(
        "To add a channel:\n\n1. Add me as an admin in your channel.\n2. Forward me any message from your channel."
    )

@Client.on_message(filters.forwarded & filters.private)
async def save_channel(client, message: Message):
    chat = message.forward_from_chat
    if chat and chat.type == "channel":
        db.add_channel(chat.id, chat.title, chat.username)
        await message.reply_text(f"Channel '{chat.title}' (@{chat.username}) has been added successfully!")
    else:
        await message.reply_text("Please forward a message from a valid channel.")
