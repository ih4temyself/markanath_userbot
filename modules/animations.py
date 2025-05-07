"""
this module provides useless animated things:
  - `.earth <speed>` (config value if none)
      `config:`
        `.earth config` to view the config,
        `.earth config speed=0.4` to update.
  - `.rainbow`: animates the rainbow colors.
  - `.moon`: shows moon phases animation.
  - `.clock`: shows a spinning clock animation.
  - `.wave`: creates a wave animation.
  - `.loading`: shows a loading animation.
  - `.heart`: shows a beating heart animation.
  - `.typing`: shows a typing animation.
  - `.stars`: shows a twinkling stars animation.
"""
import asyncio
import random
from collections import deque
from telethon import events
from telethon.errors import MessageNotModifiedError
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

    @client.on(
        events.NewMessage(
            pattern=r"\.moon(?:\s+config(?:\s+([\w=]+))?)?", outgoing=True
        )
    )
    async def moon_handler(event):
        if event.sender_id != owner_id or event.fwd_from:
            return
        config_manager = ConfigManager("moon")
        config_match = event.pattern_match.group(1)
        if handle_config(event, config_manager, config_match):
            return
        
        speed = config_manager.get("speed", 0.3)
        moon_phases = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"]
        for _ in range(32):
            await asyncio.sleep(speed)
            await event.edit("".join(moon_phases))
            moon_phases = moon_phases[1:] + [moon_phases[0]]
        await event.delete()

    @client.on(
        events.NewMessage(
            pattern=r"\.clock(?:\s+config(?:\s+([\w=]+))?)?", outgoing=True
        )
    )
    async def clock_handler(event):
        if event.sender_id != owner_id or event.fwd_from:
            return
        config_manager = ConfigManager("clock")
        config_match = event.pattern_match.group(1)
        if handle_config(event, config_manager, config_match):
            return
            
        speed = config_manager.get("speed", 0.3)
        clock_faces = ["🕛", "🕐", "🕑", "🕒", "🕓", "🕔", "🕕", "🕖", "🕗", "🕘", "🕙", "🕚"]
        for _ in range(36):
            await asyncio.sleep(speed)
            await event.edit(clock_faces[0])
            clock_faces = clock_faces[1:] + [clock_faces[0]]
        await event.delete()

    @client.on(
        events.NewMessage(
            pattern=r"\.wave(?:\s+config(?:\s+([\w=]+))?)?", outgoing=True
        )
    )
    async def wave_handler(event):
        if event.sender_id != owner_id or event.fwd_from:
            return
        config_manager = ConfigManager("wave")
        config_match = event.pattern_match.group(1)
        if handle_config(event, config_manager, config_match):
            return
            
        speed = config_manager.get("speed", 0.3)
        waves = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█", "▇", "▆", "▅", "▄", "▃", "▂", "▁"]
        last_wave = None
        
        for _ in range(30):
            await asyncio.sleep(speed)
            current_wave = "".join([waves[i % len(waves)] for i in range(10)])
            if current_wave != last_wave:
                try:
                    await event.edit(current_wave)
                except MessageNotModifiedError:
                    pass
            last_wave = current_wave
            waves = waves[1:] + [waves[0]]
        await event.delete()

    @client.on(
        events.NewMessage(
            pattern=r"\.loading(?:\s+config(?:\s+([\w=]+))?)?", outgoing=True
        )
    )
    async def loading_handler(event):
        if event.sender_id != owner_id or event.fwd_from:
            return
        config_manager = ConfigManager("loading")
        config_match = event.pattern_match.group(1)
        if handle_config(event, config_manager, config_match):
            return
            
        speed = config_manager.get("speed", 0.3)
        animations = [
            "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"
        ]
        for _ in range(40):
            await asyncio.sleep(speed)
            await event.edit(f"Loading... {animations[0]}")
            animations = animations[1:] + [animations[0]]
        await event.delete()

    @client.on(
        events.NewMessage(
            pattern=r"\.heart(?:\s+config(?:\s+([\w=]+))?)?", outgoing=True
        )
    )
    async def heart_handler(event):
        if event.sender_id != owner_id or event.fwd_from:
            return
        config_manager = ConfigManager("heart")
        config_match = event.pattern_match.group(1)
        if handle_config(event, config_manager, config_match):
            return
            
        speed = config_manager.get("speed", 0.5)
        heart_animations = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🤎", "🖤", "❤️"]
        last_heart = None
        
        for _ in range(24):
            await asyncio.sleep(speed)
            current_heart = heart_animations[0]
            if current_heart != last_heart: 
                try:
                    await event.edit(current_heart)
                except MessageNotModifiedError:
                    pass 
            last_heart = current_heart
            heart_animations = heart_animations[1:] + [heart_animations[0]]
        await event.delete()
        
    
    @client.on(
        events.NewMessage(
            pattern=r"\.typing(?:\s+config(?:\s+([\w=]+))?)?", outgoing=True
        )
    )
    async def typing_handler(event):
        if event.sender_id != owner_id or event.fwd_from:
            return
        config_manager = ConfigManager("typing")
        config_match = event.pattern_match.group(1)
        if handle_config(event, config_manager, config_match):
            return
            
        speed = config_manager.get("speed", 0.3)
        typing_animation = [
            "▒▒▒▒▒▒▒", "█▒▒▒▒▒▒", "██▒▒▒▒▒", "███▒▒▒▒", "████▒▒▒", "█████▒▒", "██████▒", "███████"
        ]
        typing_text = config_manager.get("text", "Typing...")
        for i in range(3):  # Do the animation 3 times
            for frame in typing_animation:
                await asyncio.sleep(speed)
                await event.edit(f"{typing_text} {frame}")
        await event.delete()
        
    @client.on(
        events.NewMessage(
            pattern=r"\.stars(?:\s+config(?:\s+([\w=]+))?)?", outgoing=True
        )
    )
    async def stars_handler(event):
        if event.sender_id != owner_id or event.fwd_from:
            return
        config_manager = ConfigManager("stars")
        config_match = event.pattern_match.group(1)
        if handle_config(event, config_manager, config_match):
            return
            
        speed = config_manager.get("speed", 0.3)
        
        # Create a more dynamic and larger star field
        star_field = [
            "✨ 　　★　　　　　　　✨　　　　　　★　　　　　　✨　　　　★\n"
            "　　　　✨　　　　★　　　　　✨　　　　★　　　　✨　　　　　　\n"
            "★　　　　　　✨　　　　★　　　　　　　✨　　★　　　　✨　　　\n"
            "　　　★　　　　　　　　　　✨　★　　　　★　　　　✨　　　　　\n"
            "　　　　　✨　　★　　✨　　　　　　　★　　　　✨　　★　　　　\n"
            "★　　　　✨　　　　　　★　　　　✨　　　　★　　　　✨　　　　\n"
            "　　　　★　　　　✨　　　　★　　　　　　✨　　★　　　　✨　　\n"
            "✨　　　　　　★　　　　✨　　　　★　　　　　　✨　　★　　　　\n"
            "　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　　　　　★\n"
            "★　　　　　　✨　　　　★　　　　　　✨　　★　　　　✨　　　　",
            
            "　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　\n"
            "✨　　　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　\n"
            "　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　　　　　★\n"
            "★　　　　　　✨　　　　★　　　　　　✨　　★　　　　✨　　　　\n"
            "　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　\n"
            "✨　　　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　\n"
            "　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　　　　　★\n"
            "★　　　　　　✨　　　　★　　　　　　✨　　★　　　　✨　　　　\n"
            "　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　\n"
            "✨　　　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　",
            
            "★　　　　✨　　　　　　★　　　　✨　　　　★　　　　✨　　　　\n"
            "　　　　★　　　　✨　　　　★　　　　　　✨　　★　　　　✨　　\n"
            "✨　　　　　　★　　　　✨　　　　★　　　　　　✨　　★　　　　\n"
            "　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　　　　　★\n"
            "★　　　　　　✨　　　　★　　　　　　✨　　★　　　　✨　　　　\n"
            "　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　\n"
            "✨　　　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　\n"
            "　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　　　　　★\n"
            "★　　　　　　✨　　　　★　　　　　　✨　　★　　　　✨　　　　\n"
            "　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　",
            
            "　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　　　　　★\n"
            "★　　　　　　✨　　　　★　　　　　　✨　　★　　　　✨　　　　\n"
            "　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　\n"
            "✨　　　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　\n"
            "　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　　　　　★\n"
            "★　　　　　　✨　　　　★　　　　　　✨　　★　　　　✨　　　　\n"
            "　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　\n"
            "✨　　　　　　★　　　　✨　　　　★　　　　✨　　　　★　　　　\n"
            "　　　　✨　　　　★　　　　✨　　　　★　　　　✨　　　　　　★\n"
            "★　　　　　　✨　　　　★　　　　　　✨　　★　　　　✨　　　　"
        ]
        
        last_stars = None
        for _ in range(20):
            await asyncio.sleep(speed)
            current_stars = star_field[0]
            if current_stars != last_stars:
                try:
                    await event.edit(current_stars)
                except MessageNotModifiedError:
                    pass
            last_stars = current_stars
            star_field = star_field[1:] + [star_field[0]]
        await event.delete()

def handle_config(event, config_manager, config_match):
    """Helper function to handle config operations"""
    if config_match:
        if "=" in config_match:
            key, value = config_match.split("=", 1)
            key = key.strip()
            value = value.strip()
            try:
                float_value = float(value)
                config_manager.set_config(key, float_value)
                event.respond(f"config updated: {key} = {value}")
            except ValueError:
                event.respond("value has to be a number")
        else:
            event.respond(f"invalid config command {config_match}")
        return True
    elif event.pattern_match.group(0).endswith("config"):
        event.respond(f"Current Configuration:\n{config_manager.to_string()}")
        return True
    return False