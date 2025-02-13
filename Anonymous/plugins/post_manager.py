from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery
from Anonymous import app
from database.posts import save_post, get_post, delete_post

# When receiving a message for the post
@app.on_message(filters.private & ~filters.command("start"))
async def receive_post_content(client, message: Message):
    message_type = message.media if message.media else "text"
    # Save the post content in the database
    await save_post(message.chat.id, message.id, {"type": message_type, "content": message.text or "Media"})
    
    await message.reply_text(
        "Choose an action:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("💬 Add Comments", callback_data="add_comments"),
             InlineKeyboardButton("💬 Add Native Comments", callback_data="add_native_comments")],
            [InlineKeyboardButton("📌 Add Reactions", callback_data="add_reactions"),
             InlineKeyboardButton("🔗 Add URL Buttons", callback_data="add_url_buttons")],
            [InlineKeyboardButton("🗑 Delete Post", callback_data="delete_post"),
             InlineKeyboardButton("🔔 Notify [On|Off]", callback_data="toggle_notify")]
        ])
    )

# Handling delete post
@app.on_callback_query(filters.regex(r"^delete_post$"))
async def delete_post_handler(client, query: CallbackQuery):
    post_id = query.message.reply_to_message.message_id if query.message.reply_to_message else None
    if post_id:
        # Delete the post from the database
        await delete_post(post_id)
        await query.message.edit_text("Post deleted successfully.")
    else:
        await query.message.edit_text("No post to delete.")

# Handling post confirmation (sending post)
@app.on_callback_query(filters.regex(r"^send_post_(\d+)$"))
async def confirm_send_post(client, query: CallbackQuery):
    channel_id = int(query.data.split("_")[1])
    # Fetch post count (Dummy implementation, you can fetch actual post count here)
    post_count = 1  # Replace with actual DB query
    
    await query.message.edit_text(
        f"{post_count} message(s) ready to be sent to Channel {channel_id}.\n\nWhen do you want to send the post?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⏳ Set Self-Destruct Timer", callback_data="set_timer")],
            [InlineKeyboardButton("📤 Send Now", callback_data="send_now"),
             InlineKeyboardButton("📌 Enqueue", callback_data="enqueue")],
            [InlineKeyboardButton("🔙 Back", callback_data="back_to_post")]
        ])
    )

# Editing a post (could be used to edit the content or details of an existing post)
@app.on_callback_query(filters.regex(r"^edit_post_(\d+)$"))
async def edit_post_handler(client, query: CallbackQuery):
    post_id = int(query.data.split("_")[1])
    post = await get_post(post_id)
    
    if post:
        # Ask for new content to edit the post
        await query.message.edit_text(
            "Send me the new content for the post.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Cancel Edit", callback_data="cancel_edit")],
                [InlineKeyboardButton("📝 Edit Content", callback_data="edit_content")]
            ])
        )
    else:
        await query.message.edit_text("Post not found.")

# Save edited post content
@app.on_message(filters.private & filters.reply)
async def save_edited_content(client, message: Message):
    original_post = await get_post(message.reply_to_message.message_id)
    
    if original_post:
        # Save edited content to database
        await save_post(message.chat.id, message.id, {"type": message.media, "content": message.text or "Edited Media"})
        await message.reply_text("Post content updated successfully!")
    else:
        await message.reply_text("No post to edit.")
