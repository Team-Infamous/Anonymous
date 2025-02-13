from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

@Client.on_callback_query(filters.regex("^add_url_button_"))
async def add_url_buttons(client, callback_query):
    await callback_query.message.reply_text(
        "Send me a list of URL buttons for the message in this format:\n\n"
        "`Button text 1 - http://example.com/ | Button text 2 - http://example2.com/`\n"
        "`Button text 3 - http://example3.com/`\n\nChoose 'Cancel' to go back.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ Cancel", callback_data="cancel")]])
    )

@Client.on_message(filters.text & filters.private)
async def save_url_buttons(client, message: Message):
    buttons = []
    lines = message.text.split("\n")

    for line in lines:
        parts = line.split("|")
        row = []
        for part in parts:
            try:
                text, url = part.strip().split(" - ")
                row.append(InlineKeyboardButton(text.strip(), url=url.strip()))
            except ValueError:
                await message.reply_text("Invalid format! Please follow the correct format.")
                return

        buttons.append(row)

    await message.reply_text("✅ URL buttons added!", reply_markup=InlineKeyboardMarkup(buttons))
