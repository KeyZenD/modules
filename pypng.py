from .. import loader, utils  # pylint: disable=relative-beyond-top-level
import logging
import pygments
from pygments.lexers import Python3Lexer
from pygments.formatters import ImageFormatter
import os


logger = logging.getLogger(__name__)

def register(cb):
	cb(py2pngMod())


@loader.tds
class py2pngMod(loader.Module):
	"""Uploader"""
	strings = {
		"name": "pypng"
	}

	async def client_ready(self, client, db):
		self.client = client
	
	
	@loader.sudo
	async def pypngcmd(self, message):
		"""reply to text code or py file"""
		await message.edit("<b>Py to PNG</b>")
		reply = await message.get_reply_message()
		if not reply:
			await message.edit("<b>reply to file.py</b>")
			return
		media = reply.media
		if not media:
			await message.edit("<b>reply to file.py</b>")
			return
		file = await message.client.download_file(media)
		text = file.decode('utf-8')
		pygments.highlight(text, Python3Lexer(), ImageFormatter(font_name='DejaVu Sans Mono', line_numbers=True), 'out.png')
		await message.client.send_file(message.to_id, 'out.png', force_document=True)
		os.remove("out.png")
		await message.delete()
