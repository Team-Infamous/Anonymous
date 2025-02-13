from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime

@Client.on_callback_query(filters.regex("^schedule_post_"))
async def schedule_post(client, callback_query):
    chat_id = callback_query.data.split("_")[2]
    
    await callback_query.message.reply_text(
        "Send me the date and time in this format:\n\n"
        "**YYYY-MM-DD HH:MM** (24-hour format)",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]])
    )

@Client.on_message(filters.text & filters.private)
async def save_schedule(client, message):
    try:
        schedule_time = datetime.datetime.strptime(message.text, "%Y-%m-%d %H:%M")
        await message.reply_text(f"✅ Post scheduled for {schedule_time}!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Done", callback_data="done")]]))
    except ValueError:
        await message.reply_text("❌ Invalid format! Please use **YYYY-MM-DD HH:MM**.")
