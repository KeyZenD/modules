import io
from .. import loader, utils

@loader.tds
class SavedMod(loader.Module):
	"""Соxранятель в избранное"""
	strings = {"name": "SavedMessages", "to":"me"}
	@loader.unrestricted
	async def savedcmd(self, message):
		""".saved реплай на медиа"""
		await message.delete()
		reply = await message.get_reply_message()
		name = utils.get_args_raw(message)
		if not reply or not reply.file:
			return
		media = reply.media
		if media.ttl_seconds or name: 
			file = await reply.download_media(bytes)
			file = io.BytesIO(file)
			file.name = name or str(reply.sender_id) + reply.file.ext
			file.seek(0)
			await message.client.send_file(self.strings["to"], file)
		else:
			await reply.forward_to(self.strings["to"])
