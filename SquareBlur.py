from PIL import Image, ImageFilter
import io
from .. import loader, utils
@loader.tds
class SquareBlurMod(loader.Module):
	"""Make image 1:1 ratio"""
	strings = {"name": "SquareBlur"}

	@loader.unrestricted
	async def squareblurcmd(self, message):
		"""make image 1:1 ratio"""
		reply = await message.get_reply_message()
		if not reply or not reply.file or not reply.file.mime_type.split("/")[0].lower() == "image":
			await message.edit("<b>Reply to image!</b>")
			return
		im = io.BytesIO()
		await reply.download_media(im)
		im = Image.open(im)
		w, h = im.size
		if w == h:
			await message.edit("<b>Ты за меня придурка не держи!</b>")
			return
		_min, _max = min(w, h), max(w, h)
		bg = im.crop(((w-_min)//2, (h-_min)//2, (w+_min)//2, (h+_min)//2))
		bg = bg.filter(ImageFilter.GaussianBlur(5))
		bg = bg.resize((_max, _max))
		bg.paste(im, ((_max-w)//2, (_max-h)//2))
		img = io.BytesIO()
		img.name = "im.png"
		bg.save(img)
		img.seek(0) 
		await reply.reply(file=img)
		await message.delete()
