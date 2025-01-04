"""
This module processes animated stickers (TGS files):
  - Usage: `.tgs` (reply to an animated sticker to modify it)
"""

import asyncio
import os
from random import choice, randint

from telethon import events


def register(client, owner_id):
    @client.on(events.NewMessage(pattern=r"\.tgs$", outgoing=True))
    async def tgs_handler(event):
        if event.sender_id != owner_id or not event.is_reply:
            await event.edit("Reply to an animated sticker (.tgs file).")
            return

        reply = await event.get_reply_message()
        if not reply.file or not reply.file.name.endswith(".tgs"):
            await event.edit("Reply must be to an animated sticker (.tgs file).")
            return

        await event.edit("Processing the animated sticker...")

        try:
            tgs_path = "tgs.tgs"
            await reply.download_media(tgs_path)

            os.system("lottie_convert.py tgs.tgs json.json")
            with open("json.json", "r") as f:
                stick = f.read()

            for _ in range(randint(6, 10)):
                stick = choice(
                    [stick.replace("[1]", "[99]"), stick.replace(".1", ".10")]
                )

            with open("sticker.json", "w") as f:
                f.write(stick)

            with open("json1.json", "w") as fi:
                fi.write(stick)

            os.system("lottie_convert.py sticker.json sticker_tgs.tgs")
            await reply.reply(file="sticker_tgs.tgs")
            await event.edit("Sticker processed successfully!")

        except Exception as e:
            await event.edit(f"An error occurred: {e}")

        # finally:
        #     for file in ["tgs.tgs", "json.json"]:
        #         if os.path.exists(file):
        #             os.remove(file)
