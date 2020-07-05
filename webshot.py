from .. import loader, utils  # pylint: disable=relative-beyond-top-level
import logging
from requests import get
import io
from telethon.tl.types import MessageEntityUrl

logger = logging.getLogger(__name__)

def register(cb):
	cb(WebShotMod())


@loader.tds
class WebShotMod(loader.Module):
	"""link to screen"""
	strings = {
		"name": "WebShot"
	}

	async def client_ready(self, client, db):
		self.client = client
		
	
	@loader.sudo
	async def webshotcmd(self, message):
		reply_id = None
		link = utils.get_args_raw(message)
		if not link:
			reply = await message.get_reply_message()
			if not reply:
				await message.delete()
				return
			reply_id = reply.id
			link = reply.raw_text
		await message.edit("<b>S c r e e n s h o t i n g . . .</b>")
		url = "https://webshot.deam.io/{}/?width=1920&height=1080?type=png"
		file = get(url.format(link))
		if not file.ok:
			await message.edit("<b>Something went wrong...</b>")
			return
		file = io.BytesIO(file.content)
		file.name = "webshot.png"
		file.seek(0)
		await message.client.send_file(message.to_id, file, reply_to=reply_id)
		await message.delete()
