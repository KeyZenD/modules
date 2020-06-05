# -*- coding: utf-8 -*-

#   Friendly Telegram (telegram userbot)
#   Copyright (C) 2018-2020 The Authors

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#   если не подписан на t.me/keyzend
#   твоя мама шлюха
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils  # pylint: disable=relative-beyond-top-level
import io
from PIL import Image, ImageOps
from telethon.tl.types import DocumentAttributeFilename
import logging
import random

logger = logging.getLogger(__name__)

def register(cb):
	cb(GriderMod())


@loader.tds
class GriderMod(loader.Module):
	"""Гавно залупное"""
	strings = {
		"name": "Griding"
	}

	async def client_ready(self, client, db):
		self.client = client
	
	
	@loader.sudo
	async def gridcmd(self, message):
		""".gird <reply to photo>"""
		if message.is_reply:
			reply_message = await message.get_reply_message()
			data = await check_media(reply_message)
			if isinstance(data, bool):
				await utils.answer(message, "<code>Реплай на пикчу или стикер блять!</code>")
				return
		else:
			await utils.answer(message, "`Реплай на пикчу или стикер блять`")
			return
		
		await message.edit("Режу ебать")
		file = await self.client.download_media(data, bytes)
		media = await griding(file)
		await message.delete()
		await message.client.send_file(message.to_id, media)
		
		
		

	@loader.sudo
	async def revgridcmd(self, message):
		""".gird <reply to photo>"""
		if message.is_reply:
			reply_message = await message.get_reply_message()
			data = await check_media(reply_message)
			if isinstance(data, bool):
				await utils.answer(message, "<code>Реплай на пикчу или стикер блять!</code>")
				return
		else:
			await utils.answer(message, "`Реплай на пикчу или стикер блять`")
			return
		
		await message.edit("Режу ебать")
		file = await self.client.download_media(data, bytes)
		media = await griding(file)
		media = media[::-1]
		await message.delete()
		await message.client.send_file(message.to_id, media)
		
		
	
		

async def griding(file):
	img = Image.open(io.BytesIO(file))
	(x, y) = img.size
	cy = 3
	cx = 3
	sx = x//cx
	sy = y//cy
	if (sx*cx, sy*cy) != (x, y):
		img = img.resize((sx*cx, sy*cy))
	(lx, ly) = (0, 0)
	media = []
	for i in range(1, cy+1):
		for o in range(1, cx+1):
			mimg = img.crop((lx, ly, lx+sx, ly+sy))
			bio = io.BytesIO()
			bio.name = 'image.png'
			mimg.save(bio, 'PNG')
			media.append(bio.getvalue())
			lx = lx + sx
		lx = 0
		ly = ly + sy
	return media
	

async def check_media(reply_message):
	if reply_message and reply_message.media:
		if reply_message.photo:
			data = reply_message.photo
		elif reply_message.document:
			if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in reply_message.media.document.attributes:
				return False
			if reply_message.gif or reply_message.video or reply_message.audio or reply_message.voice:
				return False
			data = reply_message.media.document
		else:
			return False
	else:
		return False

	if not data or data is None:
		return False
	else:
		return data