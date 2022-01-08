from .. import loader, utils  # pylint: disable=relative-beyond-top-level
from requests import post
import io


@loader.tds
class x0Mod(loader.Module):
	"""Uploader"""
	strings = {
		"name": "x0 Uploader"
	}

	async def client_ready(self, client, db):
		self.client = client
	
	
	@loader.sudo
	async def x0cmd(self, message):
		await message.edit("<b>Uploading...</b>")
		reply = await message.get_reply_message()
		if not reply:
			await message.edit("<b>Reply to message!</b>")
			return
		media = reply.media
		if not media:
			file = io.BytesIO(bytes(reply.raw_text, "utf-8"))
			file.name = "txt.txt"
		else:
			file = io.BytesIO(await self.client.download_file(media))
			file.name = reply.file.name if reply.file.name else  reply.file.id+reply.file.ext
		try:
			x0at = post('https://x0.at', files={'file': file})
		except ConnectionError as e:
			await message.edit(ste(e))
			return
		url = x0at.text
		output = f'<a href="{url}">URL: </a><code>{url}</code>'
		await message.edit(output)
	
