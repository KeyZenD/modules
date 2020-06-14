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
	cb(Ебал_я_в_рот_ваш_пеп_8_Mod())


@loader.tds
class Ебал_я_в_рот_ваш_пеп_8_Mod(loader.Module):
	"""Гавно залупное"""
	strings = {
		"name": "Хуификатор"
	}

	async def client_ready(self, client, db):
		self.client = client
	
	
	@loader.sudo
	async def хуйcmd(self, message):
		text = utils.get_args(message)
		if not text:
			reply = await message.get_reply_message()
			if not reply:
				await message.delete()
				return
			text = reply.raw_text.split()
		async def huify(word):
			word = word.lower().strip()
			vowels = 'аеёиоуыэюя'
			rules = {
				'а': 'я',
				'о': 'ё',
				'у': 'ю',
				'ы': 'и',
				'э': 'е',
			}
			for letter in word:
				if letter in vowels:
					if letter in rules:
						word = rules[letter] + word[1:]
					break
				else:
					word = word[1:]
			return 'Ху' + word if word else 'Хуй'
		
		out = []
		for word in text:
			хуй = await huify(word)
			out.append(хуй)
		await message.edit(" ".join(out))
		
	async def хуйняcmd(self, message):
		text = utils.get_args(message)
		if not text:
			reply = await message.get_reply_message()
			if not reply:
				await message.delete()
				return
			text = reply.raw_text.split()
		async def huify(word):
			word = word.lower().strip()
			vowels = 'аеёиоуыэюя'
			rules = {
				'а': 'я',
				'о': 'ё',
				'у': 'ю',
				'ы': 'и',
				'э': 'е',
			}
			for letter in word:
				if letter in vowels:
					if letter in rules:
						word = rules[letter] + word[1:]
					break
				else:
					word = word[1:]
			return 'Ху' + word if word else 'Хуй'
		
		out = []
		for word in text:
			хуй = await huify(word)
			out.append(f"{word}-{хуй}")
		await message.edit(" ".join(out))