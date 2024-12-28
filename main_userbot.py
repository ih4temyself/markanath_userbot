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


@client.on(events.NewMessage(pattern=r"\.ttd"))
async def ttdownload_handler(event):
    if event.sender_id != owner_id or event.fwd_from:
        return

    await event.delete()

    if not event.is_reply:
        await event.respond("Please reply to a message containing the TikTok link.")
        return

    reply_message = await event.get_reply_message()
    if not reply_message or not reply_message.message:
        await event.respond("The replied message does not contain a valid link.")
        return

    tiktok_link = reply_message.message.strip()
    if not tiktok_link.startswith("http"):
        await event.respond("The replied message does not contain a valid TikTok link.")
        return

    status_message = await event.respond("downloading tiktok")

    async with client.conversation(bot_username) as conv:
        try:
            await conv.send_message(tiktok_link)
            response = await conv.get_response()

            if response.media:
                await client.send_file(event.chat_id, response.media)
            else:
                await event.respond("The bot didn't return a valid video or photo.")
        except Exception as e:
            await event.respond(f"Failed to process the link: {e}")

    await status_message.delete()


@client.on(events.NewMessage(pattern=r"\.earth", outgoing=True))
async def _(event):
    if event.sender_id != owner_id or event.fwd_from:
        return

    deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
    for _ in range(48):
        await asyncio.sleep(0.3)
        await event.edit("".join(deq))
        deq.rotate(1)
    await event.delete()


@client.on(events.NewMessage(pattern=r"\.rainbow", outgoing=True))
async def rainbow_animation(event):
    if event.sender_id != owner_id or event.fwd_from:
        return
    await event.edit("🌈 rainbow 🌈")
    await asyncio.sleep(1.5)

    rainbow_colors = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪"]

    color_deque = deque(rainbow_colors)
    for _ in range(30):
        await asyncio.sleep(0.3)
        await event.edit("".join(color_deque))
        color_deque.rotate(1)
    await event.delete()


client.start()
print("Userbot is running...")
client.run_until_disconnected()
