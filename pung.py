from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils
from datetime import datetime


def register(cb):
	cb(PingerMod())


class PingerMod(loader.Module):
	"""более точный пинг"""

	strings = {'name': 'PingerХуингер'}

	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []

	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()

	async def pingcmd(self, message):
		"""пингует"""
		a = 5
		r = utils.get_args(message)
		if r and r[0].isdigit():
			a = int(r[0])
		ping_msg = []
		ping_data = []
		for _ in range(a):
			start = datetime.now()
			msg = await message.client.send_message("me", "ping")
			end = datetime.now()
			duration = (end - start).microseconds / 1000
			ping_data.append(duration)
			ping_msg.append(msg)
		ping = sum(ping_data) / len(ping_data)
		await message.edit(f"[ok] {str(ping)[0:5]}ms")
		for i in ping_msg:
			await i.delete()