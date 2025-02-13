from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

@Client.on_callback_query(filters.regex("^add_reaction_"))
async def add_reaction(client, callback_query):
    await callback_query.message.reply_text(
        "Send emojis or a text with `/` as a separator to add reactions.\n\nExample: 😍/🔥/😂",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]])
    )

@Client.on_message(filters.text & filters.private)
async def save_reactions(client, message: Message):
    if "/" in message.text:
        reactions = message.text.split("/")
        await message.reply_text(f"Reactions added: {', '.join(reactions)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Done", callback_data="done")]]))
    else:
        await message.reply_text("Invalid format! Use `/` to separate emojis.")
