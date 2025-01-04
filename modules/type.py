"""
this module provides a typing animation:
  - Usage: `.type <text>` (starts typing animation with the given text)
"""

import asyncio

from telethon import events


def register(client, owner_id):
    @client.on(events.NewMessage(pattern=r"\.type (.+)", outgoing=True))
    async def type_animation(event):
        if event.sender_id != owner_id or event.fwd_from:
            return
        text_to_type = event.pattern_match.group(1)
        await event.delete()  

        typing_message = ""
        message = None
        for i, char in enumerate(text_to_type, start=1):
            typing_message += char
            if i < len(text_to_type):
                animated_message = f"{typing_message}#"
            else:
                animated_message = f"{typing_message}"
            if message is None:
                message = await event.respond(animated_message)
            else:
                await message.edit(animated_message)
            await asyncio.sleep(0.4)
