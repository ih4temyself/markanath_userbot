from telethon import events


def register(client, owner_id):
    @client.on(events.NewMessage(pattern=r"\.ttd"))
    async def ttdownload_handler(event):
        if event.sender_id != owner_id or event.fwd_from:
            return

        await event.delete()

        if not event.is_reply:
            await event.respond("u need to reply with this message")
            return

        reply_message = await event.get_reply_message()
        if not reply_message or not reply_message.message:
            await event.respond("no link here")
            return

        tiktok_link = reply_message.message.strip()
        if not tiktok_link.startswith("http"):
            await event.respond("no link here")
            return

        status_message = await event.respond("downloading tiktok ...")

        bot_username = "@downloader_tiktok_bot"

        async with client.conversation(bot_username) as conv:
            try:
                await conv.send_message(tiktok_link)
                response = await conv.get_response()

                if response.media:
                    await client.send_file(event.chat_id, response.media)
                else:
                    await event.respond("error (maybe video is to big)")
            except Exception as e:
                await event.respond(f"Failed to process the link: {e}")

        await status_message.delete()
