from .. import loader, utils
import io
import logging
import requests
from textwrap import wrap
from PIL import Image, ImageDraw, ImageFont
bytes_font = requests.get("https://github.com/KeyZenD/l/blob/master/bold.ttf?raw=true").content
logger = logging.getLogger(__name__)

def register(cb):
	cb(Text2stickMod())

@loader.tds
class Text2stickMod(loader.Module):
	"""Text to sticker"""
	strings = {"name": "StickText"}

	async def client_ready(self, client, db):
		self.client = client

	@loader.owner
	async def stextcmd(self, message):
		""".stext <reply to photo>"""
		await message.delete()
		text = utils.get_args_raw(message)
		reply = await message.get_reply_message()
		if not text:
			if not reply:
				text = "#ffffff .stext <text or reply>"
			elif not reply.message:
				text = "#ffffff .stext <text or reply>"
			else:
				text = reply.raw_text
		color = text.split(" ", 1)[0]
		if color.startswith("#") and len(color) == 7:
			for ch in color.lower()[1:]:
				if ch not in "0123456789abcdef":
					break
			if len(text.split(" ", 1)) > 1:
				text = text.split(" ", 1)[1]
			else:
				if reply:
					if reply.message:
						text = reply.raw_text
		else:
			color = "#FFFFFF"
		txt = []
		for line in text.split("\n"):
			txt.append("\n".join(wrap(line, 30)))
		text = "\n".join(txt)
		font = io.BytesIO(bytes_font)
		font = ImageFont.truetype(font, 100)
		image = Image.new("RGBA", (1, 1), (0,0,0,0)) 
		draw = ImageDraw.Draw(image) 
		w, h = draw.multiline_textsize(text=text, font=font)
		image = Image.new("RGBA", (w+100, h+100), (0,0,0,0))
		draw = ImageDraw.Draw(image)
		draw.multiline_text((50,50), text=text, font=font, fill=color, align="center")
		output = io.BytesIO()
		output.name = color+".webp"
		image.save(output, "WEBP")
		output.seek(0)
		await self.client.send_file(message.to_id, output, reply_to=reply)
