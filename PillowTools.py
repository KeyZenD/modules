import io

from PIL import Image, ImageOps
from telethon.tl.types import DocumentAttributeFilename
from uniborg.util import admin_cmd



@borg.on(admin_cmd(pattern=".new ?(.*)", allow_sudo=True))
async def pilnew(event):
	uinp = event.pattern_match.group(1)

	if not uinp:
		get = await event.get_reply_message()
		if not get:
			await event.delete()
			return
		uinp = get.text
	uinp = uinp.split(" ", 2)
	try:
		x = int(uinp[0])
		y = int(uinp[1])
	except ValueError:
		await event.edit("ERROR INPUT=> X or Y is not int")
		return
	if "(" in uinp[2] and ")" in uinp[2]:
		color = uinp[2].replace("(","").replace(")","").split(", ")
		try:
			a = 255
			r = int(color[0])
			g = int(color[1])
			b = int(color[2])
			if len(color) == 4:
				a = int(color[3])
		except ValueError:
			await event.edit("ERROR INPUT=> R or G or B is not int")
			return
		color = (r, g, b, a)
	else:
		color = uinp[2]
	
	try:
		image = Image.new("RGBA", (x, y), color)
	except Exception as e:
		await event.edit("ERROR IN DRAW\n"+str(e))
		return
	
	await event.delete()
	image_stream = io.BytesIO()
	image_stream.name = "pilnew.png"
	image.save(image_stream, "PNG")
	image_stream.seek(0)

	await event.client.send_file(event.chat_id, image_stream)
	
@borg.on(admin_cmd(pattern=".rotate ?(.*)", allow_sudo=True)) 
async def pilrotate(event):
	try:
		angle = int(event.pattern_match.group(1))
	except ValueError:
		await event.edit("ERROR INPUT=> ANGLE")

	if event.is_reply:
		reply_message = await event.get_reply_message()
		data = await check_media(reply_message)

		if isinstance(data, bool):
			await event.edit("`I can't rotate that!".upper())
			return
	else:
		await event.edit("Reply to an image or sticker to rotate it!".upper())
		return
		
	image = io.BytesIO()
	await event.client.download_media(data, image)
	image = Image.open(image)

	try:
		image = image.rotate(angle, expand=True)
	except Exception as e:
		await event.edit("ERROR IN ROTATE\n"+str(e))
		return
	await event.delete()
	image_stream = io.BytesIO()
	image_stream.name = "pilrotate.png"
	image.save(image_stream, "PNG")
	image_stream.seek(0)
	await event.client.send_file(event.chat_id, image_stream)
	
	
@borg.on(admin_cmd(pattern=".ops ?(.*)", allow_sudo=True)) 
async def pilops(event):
	way = event.pattern_match.group(1)
	if not way:
		return
	if event.is_reply:
		reply_message = await event.get_reply_message()
		data = await check_media(reply_message)

		if isinstance(data, bool):
			await event.edit("`I can't ops that!".upper())
			return
	else:
		await event.edit("Reply to an image or sticker to ops it!".upper())
		return
		
	image = io.BytesIO()
	await event.client.download_media(data, image)
	image = Image.open(image)
	
	if "m" in way:
		try:
			image = ImageOps.mirror(image)
		except Exception as e:
			await event.edit("ERROR IN MIRROR\n"+str(e))
			return
	if "f" in way:
		try:
			image = ImageOps.flip(image)
		except Exception as e:
			await event.edit("ERROR IN FLIP\n"+str(e))
			return
		
	await event.delete()
	image_stream = io.BytesIO()
	image_stream.name = "pilops.png"
	image.save(image_stream, "PNG")
	image_stream.seek(0)
	await event.client.send_file(event.chat_id, image_stream)
	
	

	
@borg.on(admin_cmd(pattern=".resize ?(.*)", allow_sudo=True)) 
async def pilrotate(event):
	if event.is_reply:
		reply_message = await event.get_reply_message()
		data = await check_media(reply_message)

		if isinstance(data, bool):
			await event.edit("`I can't resize that!".upper())
			return
	else:
		await event.edit("Reply to an image or sticker to resize it!".upper())
		return
	uinp = event.pattern_match.group(1)

	if not uinp:
		await event.edit("What's about input".upper())
		return
	uinp = uinp.split()
	image = io.BytesIO()
	await event.client.download_media(data, image)
	image = Image.open(image)
	x, y = image.size
	rx, ry = None, None
	if len(uinp) == 1:
		try:
			rx, ry = int(uinp[0]), int(uinp[0])
		except ValueError:
			if uinp[0] == "x":
				rx, ry = x, x
			if uinp[0] == "y":
				rx, ry = y, y
			else:
				await event.edit("INPUT MUST BE STING")
				return
	else:
		if uinp[0] == "x":
			rx = x
		if uinp[0] == "y":
			rx = y
		if uinp[1] == "x":
			ry = x
		if uinp[1] == "y":
			ry = y
		if not rx:
			try:
				rx = int(uinp[0])
			except:
				await event.edit("ERROR IN INPUT")
				return
		if not ry:
			try:
				ry = int(uinp[1])
			except:
				await event.edit("ERROR IN INPUT")
				return
		
	
	try:
		image = image.resize((rx, ry))
	except Exception as e:
		await event.edit("ERROR IN RESIZE\n"+str(e))
		return
	await event.delete()
	image_stream = io.BytesIO()
	image_stream.name = "pilresize.png"
	image.save(image_stream, "PNG")
	image_stream.seek(0)
	await event.client.send_file(event.chat_id, image_stream)
	
	
	
async def check_media(reply_message):
	if reply_message and reply_message.media:
		if reply_message.photo:
			data = reply_message.photo
		elif reply_message.document:
			if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in reply_message.media.document.attributes:
				return False
			if reply_message.gif or reply_message.video or reply_message.audio or reply_message.voice:
				return False
			data = reply_message.media.document
		else:
			return False
	else:
		return False

	if not data or data is None:
		return False
	else:
		return data

