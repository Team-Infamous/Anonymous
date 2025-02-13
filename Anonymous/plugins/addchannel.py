from pyrogram import filters
from pyrogram.types import Message, CallbackQuery
from Anonymous import app
from database.channels import add_channel

# Command handler for "/addchannel"
@app.on_message(filters.command("addchannel") & filters.private)
async def add_channel_handler(client, message: Message):
    await message.reply_text(
        "To add a channel, follow these steps:\n\n"
        "1. Add me as an admin in your channel.\n"
        "2. Forward any message from your channel to me, or send its username/ID."
    )

# Handle forwarded messages to add channels
@app.on_message(filters.forwarded & filters.private)
async def save_channel(client, message: Message):
    channel = message.forward_from_chat
    if not channel:
        return await message.reply_text("Invalid forward. Please try again.")

    added = await add_channel(channel.id, channel.title, channel.username or "N/A")
    if added:
        await message.reply_text(f"✅ Channel '{channel.title}' has been added successfully!")
    else:
        await message.reply_text("⚠ This channel is already added.")

# Handle inline "Add Channel" button from My Channels
@app.on_callback_query(filters.regex(r"^add_channel$"))
async def inline_add_channel(client, query: CallbackQuery):
    await query.message.edit_text(
        "To add a channel, follow these steps:\n\n"
        "1. Add me as an admin in your channel.\n"
        "2. Forward any message from your channel to me, or send its username/ID.",
    )
