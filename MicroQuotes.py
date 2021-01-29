from .. import loader, utils
import io
from PIL import Image, ImageFont, ImageDraw
import requests
import textwrap

@loader.tds
class MicroQuotesMod(loader.Module):
	"""Микроцитаты"""
	strings = {"name": "MicroQuotes"}
	
	async def mqcmd(self, message):
		""".mq <реплай на текст>"""
		bw = False if utils.get_args(message) else True
		reply = await message.get_reply_message()
		if not reply or not reply.raw_text:
			await message.edit("<b>Ответь командой на умную цитату!</b>")
			return
		sender = reply.sender_id
		
		if not sender:
			sender = message.chat.id
		if sender == 1087968824:
			sender = message.chat.id
		pfp = await message.client.download_profile_photo(sender, bytes)
		await message.edit("<i>И сказал этот гений...</i>")
		if not pfp:
			pfp = b'BM:\x00\x00\x00\x00\x00\x00\x006\x00\x00\x00(\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x18\x00\x00\x00\x00\x00\x04\x00\x00\x00\xc4\x0e\x00\x00\xc4\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\x00'
		text = "\n".join(textwrap.wrap(reply.raw_text, 30))
		text = "“"+text+"„"
		bf = requests.get("https://raw.githubusercontent.com/KeyZenD/l/master/times.ttf").content
		font = ImageFont.truetype(io.BytesIO(bf), 50)
		im = Image.open(io.BytesIO(pfp))
		if bw:
			im = im.convert("L")
		im = im.convert("RGBA").resize((1024, 1024))
		w, h = im.size
		w_, h_ = 20*(w//100), 20*(h//100)
		im_ = Image.new("RGBA", (w-w_, h-h_), (0, 0, 0))
		im_.putalpha(150) 
		im.paste(im_, (w_//2, h_//2), im_)
		draw = ImageDraw.Draw(im)
		_w, _h = draw.textsize(text=text, font=font)
		x, y = (w-_w)//2, (h-_h)//2
		draw.text((x, y), text=text, font=font, fill="#fff", align="center")
		output=io.BytesIO()
		im.save(output, "PNG")
		output.seek(0)
		await reply.reply(file=output)
		await message.delete()
		