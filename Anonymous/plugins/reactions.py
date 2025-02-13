from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from Anonymous import app as Client


@Client.on_callback_query(filters.regex("^add_reaction_"))
async def add_reaction(client, callback_query):
    await callback_query.message.reply_text(
        "Send emojis or a text with `/` as a separator to add reactions.\n\nExample: 😍/🔥/😂",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]])
    )

