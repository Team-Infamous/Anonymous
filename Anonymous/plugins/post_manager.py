from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from Anonymous import app
from database.channels import get_channels
from database.posts import save_post

@app.on_callback_query(filters.regex(r"^channel_(\d+)$"))
async def open_channel_options(client, query):
    channel_id = int(query.data.split("_")[1])
    await query.message.edit_text(
        "Here you can create rich posts, view stats, and accomplish other tasks.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📝 Create Post", callback_data=f"create_post_{channel_id}")],
            [InlineKeyboardButton("📅 Schedule Post", callback_data=f"schedule_post_{channel_id}"),
             InlineKeyboardButton("✏ Edit Post", callback_data=f"edit_post_{channel_id}")],
            [InlineKeyboardButton("📊 Channel Stats", callback_data=f"stats_{channel_id}"),
             InlineKeyboardButton("⚙ Settings", callback_data=f"settings_{channel_id}")]
        ])
    )

@app.on_callback_query(filters.regex(r"^create_post_(\d+)$"))
async def create_post(client, query):
    channel_id = int(query.data.split("_")[1])
    await query.message.edit_text(
        f"Here it is: {channel_id}.\n\nSend me one or multiple messages you want to include in the post.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🗑 Delete All", callback_data="delete_all"),
             InlineKeyboardButton("👁 Preview", callback_data="preview")],
            [InlineKeyboardButton("❌ Cancel", callback_data="cancel"),
             InlineKeyboardButton("📤 Send", callback_data="send_post")]
        ])
    )

@app.on_message(filters.private & ~filters.command("start"))
async def receive_post_content(client, message: Message):
    message_type = message.media if message.media else "text"
    
    # Store message content
    await save_post(message.chat.id, message.id, {
        "type": message_type,
        "content": message.text or "Media"
    })
    
    await message.reply_text(
        "Choose an action:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Add Comments", callback_data="add_comments"),
             InlineKeyboardButton("📌 Add Reactions", callback_data="add_reactions")],
            [InlineKeyboardButton("🔗 Add URL Buttons", callback_data="add_url_buttons"),
             InlineKeyboardButton("🗑 Delete Message", callback_data="delete_message")],
            [InlineKeyboardButton("🔔 Notify [On|Off]", callback_data="toggle_notify")]
        ])
)
