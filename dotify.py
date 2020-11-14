from PIL import Image, ImageDraw
import io
import asyncio
import logging

from .. import loader, utils

logger = logging.getLogger(__name__)

class DotifyMod(loader.Module):
	"""Image to dot
	   .cmd <count> + reply to img
	   the bigger, the slower and bugger
	   recommended not more 1000"""
	strings = {"name": "[PRIVATE]Dotify"}

	@loader.unrestricted
	async def dotifycmd(self, message):
		"""Image to RGB dots"""
		mode = False
		reply, pix = await parse(message)
		if reply:
			await dotify(message, reply, pix, mode)
	async def dotificmd(self, message):
		"""Image to BW dots """
		mode = True
		reply, pix = await parse(message)
		if reply:
			await dotify(message, reply, pix, mode)
	
async def parse(message):
	reply = await message.get_reply_message()
	if not reply:
		await message.edit("<b>Reply to Image!</b>")
		return None, None
	args = utils.get_args(message)
	pix = 100
	if args:
		args=args[0]
		if args.isdigit():
			pix = int(args) if int(args) > 0 else 100
	return reply, pix

async def dotify(message, reply, pix, mode):
	await message.edit("<b>Putting dots...</b>")
	count = 24
	im_ = Image.open(io.BytesIO(await reply.download_media(bytes)))
	if im_.mode == "RGBA":
		temp = Image.new("RGB", im_.size, "#000")
		temp.paste(im_, (0, 0), im_)
		im_ = temp
		
	im = im_.convert("L")
	im_ = im if mode else im_
	[_.thumbnail((pix, pix)) for _ in[im, im_]]
	w, h = im.size
	img = Image.new(im_.mode, (w*count+(count//2), h*count+(count//2)), 0)
	draw = ImageDraw.Draw(img)
	
	def cirsle(im, x, y, r, fill):
		x += r//2
		y += r//2
		draw = ImageDraw.Draw(im)
		draw.ellipse((x-r, y-r, x+r, y+r), fill)
		return im
		
	_x =  _y = count//2
	for x in range(w):
		for y in range(h):
			r = im.getpixel((x, y))
			fill = im_.getpixel((x, y))
			cirsle(img, _x, _y, r//count, fill)
			_y += count
		_x += count
		_y = count//2
	 
	out = io.BytesIO()
	out.name = "out.png"
	img.save(out)
	out.seek(0)
	await reply.reply(file=out)
	await message.delete()
