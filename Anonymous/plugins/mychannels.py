from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from Anonymous import app
from database.channels import get_channels

@app.on_message(filters.command("mychannels"))
async def my_channels_handler(client, message: Message):
    channels = await get_channels()

    if not channels:
        return await message.reply_text("No channels found. Add one using /addchannel.")

    keyboard = [
        [InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")]
    ]

    row = []
    for index, channel in enumerate(channels, start=1):
        row.append(InlineKeyboardButton(channel["name"], callback_data=f"channel_{channel['channel_id']}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    await message.reply_text("Choose a channel from the list below:", reply_markup=InlineKeyboardMarkup(keyboard))
