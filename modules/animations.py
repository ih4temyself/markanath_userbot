"""
this module provides useless animated things:
  - Usage: `.earth <speed>` (config value if None)
  - Config: 
        `.earth config` to view the config, 
        `.earth config speed=0.4` to update.
- `.rainbow`: Animates the rainbow colors.
"""

import asyncio
from collections import deque

from telethon import events

from config_utils import ConfigManager


def register(client, owner_id):
    @client.on(
        events.NewMessage(
            pattern=r"\.earth(?:\s+config(?:\s+([\w\.=]+))?)?", outgoing=True
        )
    )
    async def earth_handler(event):
        if event.sender_id != owner_id or event.fwd_from:
            return
        config_manager = ConfigManager("earth")

        config_match = event.pattern_match.group(1)
        if config_match:
            if "=" in config_match:
                await event.delete()
                key, value = config_match.split("=", 1)
                key = key.strip()
                value = value.strip()

                try:
                    float_value = float(value)
                    config_manager.set_config(key, float_value)
                    status_message = await event.respond(
                        f"<b>.earth </b>config <b>updated {key}={value}</b>",
                        parse_mode="html",
                    )
                except ValueError:
                    status_message = await event.respond("invalid value")
            else:
                status_message = await event.respond(f"invalid config: {config_match}")
            return
        elif event.pattern_match.group(0).strip() == ".earth config":
            await event.delete()
            await event.respond(f"current config:\n{config_manager.to_string()}")
            return

        speed = config_manager.get("speed", 0.3)
        deq = deque(list("🌏🌍🌎🌎🌍🌏🌍🌎"))
        for _ in range(48):
            await asyncio.sleep(speed)
            await event.edit("".join(deq))
            deq.rotate(1)
        await event.delete()

    @client.on(
        events.NewMessage(
            pattern=r"\.rainbow(?:\s+config(?:\s+([\w=]+))?)?", outgoing=True
        )
    )
    async def rainbow_handler(event):
        if event.sender_id != owner_id or event.fwd_from:
            return
        await event.delete()
        config_manager = ConfigManager("rainbow")

        config_match = event.pattern_match.group(1)
        if config_match:
            if "=" in config_match:
                key, value = config_match.split("=", 1)
                try:
                    config_manager.set_config(key, float(value))
                    status_message = await event.respond(
                        f"config updated: {key} = {value}"
                    )
                except ValueError:
                    status_message = await event.respond("value has to be a number")
            else:
                await event.respond(f"invalid config command {config_match}")
            return
        elif event.pattern_match.group(0).strip() == ".rainbow config":
            await event.respond(f"Current Configuration:\n{config_manager.to_string()}")
            return

        speed = config_manager.get("speed", 0.3)
        rainbow_colors = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪"]
        color_deque = deque(rainbow_colors)
        for _ in range(30):
            await asyncio.sleep(speed)
            await event.edit("".join(color_deque))
            color_deque.rotate(1)
        await event.delete()
