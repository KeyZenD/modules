from .. import loader, utils
import logging
import asyncio
from telethon import events
from datetime import datetime
logger = logging.getLogger(__name__)
@loader.tds
class PingerMod(loader.Module):
	strings = {"name": "Pinger"}
	def __init__(self):
		self.name = self.strings['name']
	@loader.tds
	async def pingercmd(self, message):
		"""Пингер"""
		text = ""
		for chat in ["@QuickResponseCodeBot", "@onlineVKtracking_bot", "@StickerpackLinkBot", "@ColoriZatioN_bot", "@BlackLinesBot", "@QuickLinksBot", "@KeyZenD_bot"]:
			async with message.client.conversation(chat) as conv:
				response = conv.wait_event(events.NewMessage(incoming=True, from_users=chat), timeout=1)
				ping = await message.client.send_message(chat, "/ping")
				start = datetime.now()
				try:
					response = await response
					end = datetime.now()
					ok = True
					await response.delete()
				except:
					ok = end = False
				if end:
					duration = (end - start).microseconds / 1000
				text += f"✅{chat}: {duration}ms\n" if ok else f"⛔{chat}\n"
				await ping.delete()
			await message.edit(text)
		
