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
	cb(SoaperMod())


@loader.tds
class SoaperMod(loader.Module):
	"""Гавно залупное"""
	strings = {
		"name": "Soaping"
	}

	async def client_ready(self, client, db):
		self.client = client
	
	
	@loader.sudo
	async def soapcmd(self, message):
		""".soap <reply to photo>"""
		soap = 3
		a = utils.get_args(message)
		if a:
			if a[0].isdigit():
				soap = int(a[0])
				if soap <= 0:
					soap = 3
		
		if message.is_reply:
			reply_message = await message.get_reply_message()
			data = await check_media(reply_message)
			if isinstance(data, bool):
				await utils.answer(message, "<code>Reply to pic or stick!</code>")
				return
		else:
			await utils.answer(message, "<code>Reply to pic or stick!</code>")
			return
		
		await message.edit("Soaping...")
		file = await self.client.download_media(data, bytes)
		media = await Soaping(file, soap)
		await message.delete()
		
		await message.client.send_file(message.to_id, media)
		
	
		

async def Soaping(file, soap):
	img = Image.open(io.BytesIO(file))
	(x, y) = img.size
	img = img.resize((x//soap, y//soap), Image.ANTIALIAS)
	img = img.resize((x, y))
	soap_io = io.BytesIO()
	soap_io.name = "image.jpeg"
	img = img.convert("RGB")
	img.save(soap_io, "JPEG", quality=100)
	soap_io.seek(0)
	return soap_io
	

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