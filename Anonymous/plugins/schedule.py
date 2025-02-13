from pyrogram import filters
from pyrogram.types import Message
from Anonymous import app

@app.on_callback_query(filters.regex(r"^schedule_post_(\d+)$"))
async def schedule_post(client, query):
    await query.message.edit_text(
        "Send the time to schedule the post (in YYYY-MM-DD HH:MM format).",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ])
    )

@app.on_message(filters.text & filters.private)
async def receive_schedule_time(client, message: Message):
    # Validate and process scheduling here
    await message.reply_text("Post scheduled successfully!")
