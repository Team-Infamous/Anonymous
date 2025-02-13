from pyrogram import filters
from pyrogram.types import Message
from Anonymous import app

@app.on_callback_query(filters.regex(r"^add_reactions$"))
async def add_reactions(client, query):
    await query.message.edit_text(
        "Send emojis or a text with `/` as a separator to add reactions.\n\nFor example:\n😊 / 👍 / 🔥",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ])
    )

@app.on_message(filters.text & filters.private)
async def receive_reactions(client, message: Message):
    reactions = message.text.split(" / ")
    await message.reply_text(f"Reactions added: {' '.join(reactions)}")
