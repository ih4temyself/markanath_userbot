"""
This module processes animated stickers (TGS files):
  - Usage: `.tgs` (reply to an animated sticker to modify it)
"""

import asyncio
import os
import sys
import subprocess
from random import choice, randint
from pathlib import Path

from telethon import events

def find_lottie_script():
    """Find the lottie_convert.py script in the system."""
    # Common locations for the script
    possible_locations = [
        # Windows locations
        os.path.join(os.path.dirname(sys.executable), 'Scripts', 'lottie_convert.py'),
        os.path.join(os.path.dirname(sys.executable), 'lottie_convert.py'),
        # Linux locations
        '/usr/local/bin/lottie_convert.py',
        '/usr/bin/lottie_convert.py',
        # Virtual environment locations
        os.path.join(sys.prefix, 'bin', 'lottie_convert.py'),
        os.path.join(sys.prefix, 'Scripts', 'lottie_convert.py'),
    ]
    
    for location in possible_locations:
        if os.path.exists(location):
            return location
            
    # If not found in common locations, try to find it in PATH
    try:
        result = subprocess.run(['which', 'lottie_convert.py'], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
        
    return None

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

            # Find lottie_convert.py script
            lottie_script = find_lottie_script()
            if not lottie_script:
                await event.edit("Error: lottie_convert.py not found. Please ensure lottie-tools is installed.")
                return

            # Convert TGS to JSON using lottie
            try:
                result = subprocess.run(
                    [sys.executable, lottie_script, tgs_path, "json.json"],
                    capture_output=True,
                    text=True,
                    check=True
                )
            except subprocess.CalledProcessError as e:
                error_msg = f"Lottie conversion failed: {e.stderr}"
                print(error_msg)  # For debugging
                await event.edit(f"Error converting sticker: {error_msg}")
                return

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

            # Convert JSON back to TGS using lottie
            try:
                result = subprocess.run(
                    [sys.executable, lottie_script, "sticker.json", "sticker_tgs.tgs"],
                    capture_output=True,
                    text=True,
                    check=True
                )
            except subprocess.CalledProcessError as e:
                error_msg = f"Lottie conversion failed: {e.stderr}"
                print(error_msg)  # For debugging
                await event.edit(f"Error converting sticker: {error_msg}")
                return

            await reply.reply(file="sticker_tgs.tgs")
            await event.edit("Sticker processed successfully!")

        except Exception as e:
            await event.edit(f"An error occurred: {e}")

        finally:
            # Clean up temporary files
            for file in ["tgs.tgs", "json.json", "sticker.json", "json1.json", "sticker_tgs.tgs"]:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                    except Exception as e:
                        print(f"Error removing {file}: {e}")
