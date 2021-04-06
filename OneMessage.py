from .. import loader, utils
from telethon.tl.types import Message
		
class OneMessageMod(loader.Module):
	"""@faq lines"""
	strings = {'name': 'OneMessage'}
	def __init__(self):
		self.name = self.strings['name']
	async def client_ready(self, client, db):
		self.client = client
		self._db = db
	
	@loader.sudo
	async def omstartcmd(self, message):
		"""Start OneMessage mode"""
		self._db.set("OneMessage", "status", True)
		self._db.set("OneMessage", "my_id", message.sender_id)
		await message.edit("<b>OneMessage mode activated!</b>")
		
	async def omstopcmd(self, message):
		"""Stop OneMessage mode"""
		self._db.set("OneMessage", "status", False)
		await message.edit("<b>OneMessage mode diactivated!</b>")
			
	async def watcher(self, message):
		if not isinstance(message, Message):
			return
		if message.message:
			if message.raw_text[0] in self._db.get("friendly-telegram.modules.corectrl", "command_prefix", ".") or message.fwd_from:
				return
		if self._db.get("OneMessage", "status", None) and message.sender_id == self._db.get("OneMessage", "my_id", None) and not message.media:
			last_msg = (await self.client.get_messages(message.to_id, limit=2))[-1]
			if last_msg.sender_id == message.sender_id and not last_msg.fwd_from:
				text = last_msg.text 
				text += "\n"*2
				text += message.text
				if message.is_reply:
					message, last_msg = last_msg, message
				try:
					await last_msg.edit(text)
					await message.delete()
				except:
					return
				
		
			
