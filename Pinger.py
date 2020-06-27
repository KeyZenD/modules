from .. import loader, utils
import logging
import asyncio
from asyncio import sleep
from telethon import events
logger = logging.getLogger(__name__)
@loader.tds
class PingerMod(loader.Module):
	strings = {"name": "Pinger"}
	@loader.ratelimit
	async def pingercmd(self, message):
		"""Пингер"""
		text = ""
		for chat in ["@QuickResponseCodeBot", "@onlineVKtracking_bot", "@StickerpackLinkBot", "@ColoriZatioN_bot", "@BlackLinesBot", "@QuickLinksBot", "@KeyZenD_bot"]:
			async with message.client.conversation(chat) as conv:
				response = conv.wait_event(events.NewMessage(incoming=True, from_users=chat), timeout=1)
				ping = await message.client.send_message(chat, "/ping")
				try:
					response = await response
					ok = True
					await response.delete()
				except:
					ok = False
				text f"✅{chat}\n" if ok else f"⛔{chat}\n"
				await ping.delete()
			await message.edit(text)
		