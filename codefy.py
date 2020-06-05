#	Friendly Telegram (telegram userbot)
#	Copyright (C) 2018-2019 The Authors

#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.

#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#	SUBSCRIBE TO t.me/keyzend pls
#	You should have received a copy of the GNU Affero General Public License
#	along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils

import logging
import asyncio

logger = logging.getLogger(__name__)

@loader.tds
class CodefyMod(loader.Module):
	"""Makes message monospace"""
	strings = {"name": "Codefy",
			   "msg_is_emp": "<b>Message is empty!</b>"}
	@loader.ratelimit
	async def codecmd(self, message):
		""".code <text or reply>"""
		if message.is_reply:
			reply = await message.get_reply_message()
			code = reply.raw_text
			code = code.replace("<","&lt;").replace(">","&gt;")
			await message.edit(f"<code>{code}</code>")
		else:
			code = message.raw_text[5:]
			code = code.replace("<","&lt;").replace(">","&gt;")
			try:
				await message.edit(f"<code>{code}</code>")
			except:
				await message.edit(self.strings["msg_is_emp"])
		
		
		
		
		
		
		