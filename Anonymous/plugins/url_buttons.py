from pyrogram import filters
from pyrogram.types import Message
from Anonymous import app

@app.on_callback_query(filters.regex(r"^add_url_buttons$"))
async def add_url_buttons(client, query):
    await query.message.edit_text(
        "Send me a list of URL buttons in this format:\n\n"
        "`Button text 1 - http://example.com/ | Button text 2 - http://example2.com/`\n"
        "`Button text 3 - http://example3.com/`\n\n"
        "Choose 'Cancel' to go back to post creation.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]
        ])
    )

@app.on_message(filters.text & filters.private)
async def receive_url_buttons(client, message: Message):
    buttons = message.text.split("|")
    formatted_buttons = [btn.strip().split(" - ") for btn in buttons]
    inline_buttons = [[InlineKeyboardButton(text, url=url)] for text, url in formatted_buttons]
    
    await message.reply_text("URL buttons added.", reply_markup=InlineKeyboardMarkup(inline_buttons))
