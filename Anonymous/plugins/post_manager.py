from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from Anonymous.database import db
from Anonymous import app as Client

@Client.on_callback_query(filters.regex("^create_post_"))
async def create_post(client, callback_query):
    chat_id = callback_query.data.split("_")[2]
    channel = db.channels.find_one({"chat_id": int(chat_id)})

    if not channel:
        await callback_query.answer("Channel not found!", show_alert=True)
        return

    await callback_query.message.edit_text(
        f"Here it is: \"{channel['name']}\" (@{channel['username']}).\n\n"
        "Send me one or multiple messages you want to include in the post. It can be anything — a text, photo, video, even a sticker.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🗑 Delete All", callback_data=f"delete_all_{chat_id}"), InlineKeyboardButton("👀 Preview", callback_data=f"preview_{chat_id}")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel"), InlineKeyboardButton("📢 Send", callback_data=f"send_{chat_id}")]
        ])
    )
