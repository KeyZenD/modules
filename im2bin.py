import asyncio
import logging
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
from requests import get
from string import digits
from random import choice
from .. import loader, utils

logger = logging.getLogger(__name__)

font_ = get("https://github.com/KeyZenD/l/blob/master/mono.otf?raw=true").content

@loader.tds
class Im2BinaryMod(loader.Module):
	"""Картинки в текст. что?"""
	strings = {"name": "Im2Bin"}

	@loader.unrestricted
	async def bincmd(self, message):
		""".bin <картинка  или реплай> + слова (дефолт на рандоме) (не мешает слова)"""
		img, words, me = await prepare(message)
		if not img:
			await message.delete()
			return await message.client.send_file(message.chat.id, get("https://thiscatdoesnotexist.com").content, caption=choice(["<b>Тебе картинок мало?</b>"]+[None]*100))
		await message.edit("<b>Processing...</b>")
		img = await image_to_text(words, img, False)
		[await message.delete(), await (await message.get_reply_message()).reply(file=img)] if not me else await message.edit(file=img, text="")
	@loader.unrestricted
	async def rbincmd(self, message):
		""".rbin <картинка  или реплай> + слова (дефолт на рандоме) (мешает слова)"""
		img, words, me = await prepare(message)
		if not img:
			await message.delete()
			return await message.client.send_file(message.chat.id, get("https://thiscatdoesnotexist.com").content, caption=choice(["<b>Тебе картинок мало?</b>"]+[None]*100))
		await message.edit("<b>Processing...</b>")
		img = await image_to_text(words, img, True)
		[await message.delete(), await (await message.get_reply_message()).reply(file=img)] if not me else await message.edit(file=img, text="")

async def getimg(m):
	if not m.file:
		return False
	if not "image" in m.file.mime_type.lower():
		return False
	return True

async def prepare(message):
	if not await getimg(message):
		reply = await message.get_reply_message()
		if not reply or not await getimg(reply):
			return False, False, False
		else:
			me = False
			img = await reply.download_media(bytes)
	else:
		me = True
		img = await message.download_media(bytes)
	args = utils.get_args(message)
	words = [f"{x} " for x in args] if args else list("01")
	return img, words, me

async def image_to_text(words, img, rand):
	inp = Image.open(io.BytesIO(img))
	img = Image.new("RGBA", inp.size, "#000")
	res = img.copy()
	img.paste(inp, (0, 0), inp if inp.mode == "RGBA" else None)
	w, h = img.size
	font = ImageFont.truetype(io.BytesIO(font_), 15)
	mw = min(map(lambda x: font.getsize(x)[0], "".join(words)))
	mh = min(map(lambda x: font.getsize(x)[1], "".join(words)))
	rand_ = 0
	text = []
	while len(text)*mh <= h:
		row = []
		while len("".join(row))*mw <= w:
			word = choice(words) if rand else words[rand_%len(words)]
			rand_ += 1
			row.append(word)
		rand_ -= 1
		text.append("".join(row))
	text = "\n".join(text)
	wt, ht = ImageDraw.Draw(Image.new("L", (0, 0))).multiline_textsize(font=font, text=text, spacing=0)
	im = Image.new("L", (wt, ht), 0)
	ImageDraw.Draw(im).multiline_text((0, -3), font=font, text=text, spacing=0, fill=255)
	im = im.crop((0, 0, w, h))
	im = Image.frombytes("L", (w, h), bytes([255 if x > 150 else 0 for x in im.tobytes()]))
	img.putalpha(im)
	res.paste(img, (0, 0), img)
	out = io.BytesIO()
	out.name = words[0] + ".png"
	res.save(out)
	out.seek(0)
	return out
