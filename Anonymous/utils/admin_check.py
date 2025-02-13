from pyrogram.types import Message, CallbackQuery
from Anonymous.config import ADMINS

def is_admin(func):
    async def wrapper(client, update):
        user_id = update.from_user.id if isinstance(update, (Message, CallbackQuery)) else None
        if user_id not in ADMINS:
            if isinstance(update, Message):
                await update.reply_text("🚫 You are not authorized to use this command.")
            elif isinstance(update, CallbackQuery):
                await update.answer("🚫 You are not authorized!", show_alert=True)
            return
        return await func(client, update)
    return wrapper
