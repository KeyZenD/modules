import asyncio
import logging
from telethon.tl.types import DocumentAttributeFilename
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class filenameMod(loader.Module):
	"""filename changer"""
	strings = {"name": "filename",
			   "wf": "<b>Reply to file?</b>",
			   "wn": "<b>What is the name?</b>",
			   "tnf":"<b>It's not a file!</b>"}

	
	@loader.unrestricted
	async def filenamecmd(self, message):
		""".filename <filename> + reply.file"""
		reply = await message.get_reply_message()
		if not reply or not reply.file:
			await message.edit(self.strings["wf"])
			return
		name = utils.get_args_raw(message)
		if not name:
			await message.edit(self.strings["wn"])
			return
		fn = reply.file.name
		if not fn:
			fn = ""
		fs = reply.file.size
		
		[await message.edit(f"<b>Downloading {fn}</b>") if fs > 500000 else ...]
		file = await reply.download_media(bytes)
		[await message.edit(f"<b>Uploading</b> <code>{name}</code>") if fs > 500000 else ...]
		await message.client.send_file(message.to_id, file, force_document=True, reply_to=reply, attributes=[DocumentAttributeFilename(file_name=name)])
		await message.delete()
