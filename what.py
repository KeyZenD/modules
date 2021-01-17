from .. import loader, utils
from PIL import Image, ImageDraw
from random import randint
from io import BytesIO


@loader.tds
class WhatMod(loader.Module):
	"""wow, what is it there?"""
	strings = {"name": "What?"}
	
	async def whatcmd(self, message):
		"""Draw circle in random place"""
		args = utils.get_args_raw(message)
		scale = int(args) if args and args.isdigit() else 50
		scale = 10 if scale < 0 else scale
		scale = 100 if scale > 100 else scale
		reply = await message.get_reply_message()
		if not reply or not reply.file.mime_type.split("/")[0].lower() == "image":
			await message.edit("<b>Reply to img!</b>")
			return
		await message.edit("<b>What is it?</b>")
		im = BytesIO()
		await reply.download_media(im)
		im = Image.open(im)
		w, h = im.size
		f = (min(w,h)//100)*scale
		draw = ImageDraw.Draw(im)
		x, y = randint(0, w-f), randint(0, h-f)
		draw.ellipse((x, y, x+randint(f//2, f), y+randint(f//2, f)), fill=None, outline="red", width=randint(3, 10))
		out = BytesIO()
		out.name = "what.png"
		im.save(out)
		out.seek(0)
		await message.delete()
		return await reply.reply(file=out)
		
