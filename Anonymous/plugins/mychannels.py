from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Anonymous.database import db
from Anonymous.utils.admin_check import is_admin
from Anonymous import app as Client


@Client.on_message(filters.command("mychannels") & filters.private)
async def my_channels(client, message):
    channels = db.get_channels()
    
    if not channels:
        buttons = [[InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")]]
        await message.reply_text("No channels connected.", reply_markup=InlineKeyboardMarkup(buttons))
        return

    buttons = [[InlineKeyboardButton("➕ Add Channel", callback_data="add_channel")]]
    
    for i in range(0, len(channels), 2):
        row = []
        for j in range(2):
            if i + j < len(channels):
                channel = channels[i + j]
                row.append(InlineKeyboardButton(channel["name"], callback_data=f"manage_{channel['chat_id']}"))
        buttons.append(row)

    await message.reply_text("Choose a channel from the list below:", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex("^manage_"))
async def manage_channel(client, callback_query):
    chat_id = callback_query.data.split("_")[1]
    channel = db.channels.find_one({"chat_id": int(chat_id)})

    if not channel:
        await callback_query.answer("Channel not found!", show_alert=True)
        return

    buttons = [
        [InlineKeyboardButton("📩 Create Post", callback_data=f"create_post_{chat_id}")],
        [InlineKeyboardButton("📅 Schedule Post", callback_data=f"schedule_post_{chat_id}"), InlineKeyboardButton("✏ Edit Post", callback_data=f"edit_post_{chat_id}")],
        [InlineKeyboardButton("📊 Channel Stats", callback_data=f"stats_{chat_id}"), InlineKeyboardButton("⚙ Settings", callback_data=f"settings_{chat_id}")]
    ]
    
    await callback_query.message.edit_text(
        "Here you can create rich posts, view stats and accomplish other tasks.",
        reply_markup=InlineKeyboardMarkup(buttons)
      )
