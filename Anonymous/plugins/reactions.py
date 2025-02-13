from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from Anonymous import app as Client


@Client.on_callback_query(filters.regex("^add_reaction_"))
async def add_reaction(client, callback_query):
    await callback_query.message.reply_text(
        "Send emojis or text separated by space to add reactions.\n\nExample: 😍 🔥 😂",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]])
    )

@Client.on_message(filters.text & filters.private)
async def save_reactions(client, message: Message):
    # Directly split reactions by space without "/"
    reactions = message.text.split()
    if reactions:
        await message.reply_text(f"Reactions added: {', '.join(reactions)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("✅ Done", callback_data="done")]]))
    else:
        await message.reply_text("Please send some reactions.")
