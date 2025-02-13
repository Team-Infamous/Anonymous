from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Anonymous import app
from database.channels import get_channels

@app.on_message(filters.command("start"))
async def start(client, message):
    # Get all the connected channels from the database
    channels = await get_channels()

    # If no channels are connected, show a message prompting the user to add one
    if not channels:
        await message.reply_text(
            "No channels connected. Please add a channel using /addchannel.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Add Channel", callback_data="add_channel")]
            ])
        )
        return

    # Otherwise, show the Create Post button with a list of connected channels
    channel_buttons = [
        [InlineKeyboardButton(f"📢 {channel['name']} @{channel['username']}", callback_data=f"channel_{channel['id']}")]
        for channel in channels
    ]
    
    # Add the Create Post button at the top
    channel_buttons.insert(0, [InlineKeyboardButton("📝 Create Post", callback_data="create_post")])
    
    # Send the message with the inline buttons
    await message.reply_text(
        "Welcome to the post manager! Choose an option below:",
        reply_markup=InlineKeyboardMarkup(channel_buttons)
    )

@app.on_callback_query(filters.regex(r"^create_post$"))
async def create_post(client, query):
    # Show the list of connected channels again when the user clicks on Create Post
    channels = await get_channels()
    if not channels:
        await query.message.edit_text(
            "No channels connected. Please add a channel using /addchannel.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Add Channel", callback_data="add_channel")]
            ])
        )
        return

    # Show channel selection options
    channel_buttons = [
        [InlineKeyboardButton(f"📢 {channel['name']} @{channel['username']}", callback_data=f"channel_{channel['id']}")]
        for channel in channels
    ]
    
    # Send the message with the inline buttons
    await query.message.edit_text(
        "Here is the list of channels. Choose one to create a post:",
        reply_markup=InlineKeyboardMarkup(channel_buttons)
    )
