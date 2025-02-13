from pyrogram import idle
from Anonymous import app
from plugins import *

if __name__ == "__main__":
    print("Bot is running...")
    app.start()
    idle()
    print("Bot stopped.")
