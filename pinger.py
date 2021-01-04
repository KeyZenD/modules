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
		
	async def pingercmd(self, message):
		"""Пингер"""
		text = ""
		for chat in ['@QuickResponseCodeBot','@StickerpackLinkBot','@ColoriZatioN_bot','@AntiCommentsBot','@BlackLinesBot','@QuickLinksBot','@xClicker_bot','@KeyZenD_bot']:
			async with message.client.conversation(chat) as conv:
				response = conv.wait_event(events.NewMessage(incoming=True, from_users=chat), timeout=1)
				ping = await message.client.send_message(chat, "/start")
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
				text += f"<a href='https://t.me/{chat[1:]}'>✅</a><code>{chat[1:]}:{' '*(22-len(chat))}|</code><a href='https://t.me/{chat[1:]}'>{duration}ms</a>\n" if ok else f"<a href='https://t.me/{chat[1:]}'>⛔</a><code>{chat[1:]}</code>\n"
				await ping.delete()
			await message.edit(text)
		

