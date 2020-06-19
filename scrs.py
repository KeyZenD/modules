
from .. import loader, utils
from telethon import events, errors, functions, types

def register(cb):
	cb(ScrSpamMod())


class ScrSpamMod(loader.Module):
	"""Screenshot Spammer by @KeyZenD"""

	strings = {'name': 'ScrSpam'}

	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []

	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()

	async def scrscmd(self, message):
		""".scrs <amount>"""
		a = 1
		r = utils.get_args(message)
		if r and r[0].isdigit():
			a = int(r[0])
		await message.edit("Screenshoting...")
		for _ in range(a):
			await message.client(functions.messages.SendScreenshotNotificationRequest(peer=message.to_id, reply_to_msg_id=message.id))
		await message.delete()
		
