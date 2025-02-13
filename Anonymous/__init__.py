# (©) Anonymous Emperor

import logging
import importlib
import os
from pyrogram import Client
from Anonymous import config as Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Anonymous")

# Create a new instance of the Pyrogram Client (bot)
app = Client(
    "my_bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
)

# Dynamically load all plugins in the "Anonymous/plugins" directory
PLUGIN_PATH = os.path.join(os.path.dirname(__file__), "plugins")
for file in os.listdir(PLUGIN_PATH):
    if file.endswith(".py") and not file.startswith("__"):
        module_name = f"Anonymous.plugins.{file[:-3]}"
        try:
            importlib.import_module(module_name)
            logger.info(f"✅ Successfully loaded module: {module_name}")
        except Exception as e:
            logger.error(f"❌ Failed to load module: {module_name} - {e}")
