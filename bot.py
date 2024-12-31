import asyncio
import os
from collections import deque

from dotenv import load_dotenv
from telethon import TelegramClient, events

load_dotenv()
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")
owner_id = int(os.getenv("OWNER_ID"))
bot_username = "@downloader_tiktok_bot"

client = TelegramClient(session_name, api_id, api_hash)


@client.on(events.NewMessage(pattern=r"\.help", outgoing=True))
async def help_handler(event):
    help_messages = []
    for module in os.listdir("modules"):
        if module.endswith(".py") and module != "__init__.py":
            module_name = f"modules.{module[:-3]}"
            imported_module = __import__(module_name, fromlist=["register"])

            description = imported_module.__doc__ or "no description."
            help_messages.append(f"**{module[:-3]}**:\n{description.strip()}")

    await event.respond("\n\n".join(help_messages))


async def load_modules():
    for module in os.listdir("modules"):
        if module.endswith(".py") and module != "__init__.py":
            module_name = f"modules.{module[:-3]}"
            imported_module = __import__(module_name, fromlist=["register"])
            if hasattr(imported_module, "register"):
                imported_module.register(client, owner_id)


async def main():
    print("Loading modules...")
    await load_modules()
    print("Userbot is running...")
    await client.start()
    await client.run_until_disconnected()


asyncio.run(main())
