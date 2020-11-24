from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils


def register(cb):
	cb(BlackLinesMod())


class BlackLinesMod(loader.Module):
	"""Draw line via @BlackLinesBot"""

	strings = {'name': 'BlackLines'}

	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []

	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()

	async def linecmd(self, message):
		""".line <reply to photo>"""
		
		reply = await message.get_reply_message()
		if not reply:
			await message.edit("reply to photo")
			return
		try:
			photo = reply.media.photo
		except:
			await message.edit("reply to photo only")
			return
		
		args = utils.get_args_raw(message)
				
				
		chat = '@BlackLinesBot'
		await message.edit('@BlackLinesBot <code>in process...</code>')
		async with message.client.conversation(chat) as conv:
			try:
				response = conv.wait_event(events.NewMessage(incoming=True, from_users=1051644279))
				await message.client.send_file(chat, photo, caption=args)
				response = await response
			except YouBlockedUserError:
				await message.reply('<code>Unblock</code> @BlackLinesBot')
				return

			await message.delete()
			await message.client.send_file(message.to_id, response.media)
			
