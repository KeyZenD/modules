from .. import loader, utils
import logging
from PIL import Image, ImageDraw, ImageOps, ImageFont
from textwrap import wrap
import io
import requests
# https://t.me/KeyZenD
# https://t.me/SomeScripts
logger = logging.getLogger(__name__)

@loader.tds
class DeMoTiVaToRsMod(loader.Module):
	"""Демотиваторы на картинки от @SomeScripts by @DneZyeK"""
	strings = {
		"name": "SuperDemotivator"
	}

	async def client_ready(self, client, db):
		self.client = client
	
	
	@loader.owner
	async def demoticmd(self, message):
		"""текст + фото или ответ на фото
           не мнёт фотки"""
		await cmds(message, 0)
		
	async def demotcmd(self, message):
		"""текст + фото или ответ на фото
           мнёт фотки"""
		await cmds(message, 1)
		
	
async def cmds(message, type):
	event, is_reply = await check_media(message)
	if not event:
		await message.edit("<b>Ответ командой на картинку!</b>")
		return
	text = utils.get_args_raw(message)
	
	if not text:
		await message.edit("<b>Команду нужно использовать с текстом!</b>")
		return
	await message.edit("<b>Демотивирую...</b>")
	bytes_image = await event.download_media(bytes)
	demotivator = await demotion(font_bytes, bytes_image, text, type)
	if is_reply:
		a = await event.reply(file=demotivator)
		await message.delete()
		return a
	else:
		return await event.edit(file=demotivator, text="")
	
		
async def check_media(message):
	reply = await message.get_reply_message()
	is_reply = True
	if not reply:
		reply = message
		is_reply = False
	if not reply.file:
		return False, ...
	mime = reply.file.mime_type.split("/")[0].lower()
	if mime != "image":
		return False, ...
	return reply, is_reply
	
async def textwrap(text, length=50, splitter = "\n\n"):
	out = []
	
	lines = text.rsplit(splitter, 1)
	for text in lines:
		txt = []
		parts = text.split("\n")
		for part in parts:
			part = "\n".join(wrap(part, length))
			txt.append(part)
		text = "\n".join(txt)
		out.append(text)
	return out

async def draw_main(
			bytes_image,
			type,
			frame_width_1 = 5,
			frame_fill_1 = (0, 0, 0),
			frame_width_2 = 3,
			frame_fill_2 = (255, 255, 255),
			expand_proc = 10,
			main_fill = (0, 0, 0)
			):
				
	main_ = Image.open(io.BytesIO(bytes_image))
	main = Image.new("RGB", main_.size, "black")
	main.paste(main_, (0, 0))
	if type == 1:
		main = main.resize((700, 550))
	main = ImageOps.expand(main, frame_width_1, frame_fill_1)
	main = ImageOps.expand(main, frame_width_2, frame_fill_2)
	w, h = main.size
	h_up = expand_proc*(h//100)
	im = Image.new("RGB", (w+(h_up*2), h+h_up), main_fill)
	im.paste(main, (h_up, h_up))
	return im

async def _draw_text(
			text,
			font_bytes,
			font_size,
			font_add = 20,
			main_fill = (0, 0, 0),
			text_fill = (255, 255, 255),
			text_align = "center"
			):
				
	font = ImageFont.truetype(io.BytesIO(font_bytes), font_size)
	w_txt, h_txt = ImageDraw.Draw(Image.new("RGB", (1, 1))).multiline_textsize(text=text, font=font)
	txt = Image.new("RGB", (w_txt, h_txt+font_add), main_fill)
	ImageDraw.Draw(txt).text((0, 0), text=text, font=font, fill=text_fill, align=text_align)
	return txt
	
async def text_joiner(text_img_1, text_img_2, main_fill = (0, 0, 0)):
	w_txt_1, h_txt_1 = text_img_1.size
	w_txt_2, h_txt_2 = text_img_2.size
	w = max(w_txt_1, w_txt_2)
	h = h_txt_1 + h_txt_2
	text = Image.new("RGB", (w, h), main_fill)
	text.paste(text_img_1, ((w-w_txt_1)//2, 0))
	text.paste(text_img_2, ((w-w_txt_2)//2, h_txt_1))
	return text
	
async def draw_text(text, font_bytes, font_size):
	text = await textwrap(text)
	if len(text) == 1:
		text = await _draw_text(text[0], font_bytes, font_size[0] )
	else:
		text_img_1 = await _draw_text(text[ 0], font_bytes, font_size[0])
		text_img_2 = await _draw_text(text[-1], font_bytes, font_size[1])
		text = await text_joiner(text_img_1, text_img_2)
	return text
	
async def text_finaller(text, main, expand_width_proc = 25, main_fill = (0, 0, 0)):
	x = min(main.size)
	w_txt, h_txt = text.size
	w_proc = expand_width_proc*(w_txt//100)
	h_proc = expand_width_proc*(h_txt//100)
	back = Image.new("RGB", (w_txt+(w_proc*2), h_txt+(h_proc*2)), main_fill)
	back.paste(text, (w_proc, h_proc))
	back.thumbnail((x, x))
	return back
	
	
async def joiner(text_img, main_img, format_save="JPEG"):
	w_im, h_im = main_img.size
	w_txt, h_txt = text_img.size
	text_img.thumbnail((min(w_im, h_im), min(w_im, h_im)))
	w_txt, h_txt = text_img.size
	main_img = main_img.crop((0, 0, w_im, h_im+h_txt))
	main_img.paste(text_img, ((w_im-w_txt)//2, h_im))
	output = io.BytesIO()
	main_img.save(output, format_save)
	output.seek(0)
	return output.getvalue()
	
async def demotion(font_bytes, bytes_image, text, type):
	main = await draw_main(bytes_image, type)
	font_size = [20*(min(main.size)//100), 15*(min(main.size)//100)]
	text = await draw_text(text, font_bytes, font_size)
	text = await text_finaller(text, main)
	output = await joiner(text, main)
	return output

font_bytes = requests.get("https://raw.githubusercontent.com/KeyZenD/l/master/times.ttf").content
#######################
