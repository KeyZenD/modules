from telethon import events
from .. import loader, utils

#испольуйте только на свой страх и риск
#используя этот модуль вы принимаете то
#что если получите бан, то на мне никакой ответственности



def register(cb):
	cb(MSMod())


class MSMod(loader.Module):
	"""Спаммер медиа(стикер/гиф/фото/видео/войс/видеовойс</code>"""

	strings = {'name': 'МедиаСпам'}

	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []

	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()

	async def mediaspamcmd(self, message):
		""".mediaspam <количество> + реплай на медиа(стикер/гиф/фото/видео/войс/видеовойс)"""
		reply = await message.get_reply_message()
		if not reply:
			await message.edit("<code>.mediaspam <количество> + реплай на медиа(стикер/гиф/фото/видео/войс/видеовойс</code>")
			return
		if not reply.media:
			await message.edit("<code>.mediaspam <количество> + реплай на медиа(стикер/гиф/фото/видео/войс/видеовойс</code>")
			return
		media = reply.media
	
		args = utils.get_args(message)
		if not args:
			await message.edit("<code>.mediaspam <количество> + реплай на медиа(стикер/гиф/фото/видео/войс/видеовойс</code>")
			return
		count = args[0]
		count = count.strip()
		if not count.isdigit():
			await message.edit("<code>.mediaspam <количество> + реплай на медиа(стикер/гиф/фото/видео/войс/видеовойс</code>")
			return
		count = int(count)
		
		await message.delete()
		for _ in range(count):
			await message.client.send_file(message.to_id, media)