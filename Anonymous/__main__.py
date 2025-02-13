# (©) Anonymous Emperor

from Anonymous import app
import time
from pyrogram.errors import BadMsgNotification

async def start_bot():
    retries = 5
    while retries > 0:
        try:
            await app.start()  # This starts the bot
            break
        except BadMsgNotification as e:
            print(f"Error: {e}. Retrying in 5 seconds...")
            time.sleep(5)
            retries -= 1
    if retries == 0:
        print("Failed to sync time after several retries.")

app.run(start_bot())
