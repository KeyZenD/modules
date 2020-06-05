import io, random, glob, os
from PIL import Image
from telethon.tl.types import DocumentAttributeFilename
from uniborg.util import admin_cmd
"""Не подписался без матери остался"""
"""https://t.me/KeyZenD"""
"""автор этого говнокода @DneZyeK"""

@borg.on(admin_cmd(pattern=".d(.*)", allow_sudo=True)) 
async def d(message):
	inp =message.pattern_match.group(1)
	pop = 60
	if inp:
		inp = inp.strip()
		if inp.isdigit():
			if int(inp) > 0:
				pop = inp
	
	if message.is_reply:
		reply_message = await message.get_reply_message()
		data = await check_media(reply_message)
		if isinstance(data, bool):
			await message.edit("‮Reply to image, fucking idiot")
			return
	else:
		await message.edit("‮Reply to image, fucking idiot")
		return
	await message.edit(" ‮`P` `r` `o` `c` `e` `s` `s` `i` `n` `g` `.` `.` `.`")
	for distorted in glob.glob("distorted*"):
		os.remove(distorted)
	for findistorted in glob.glob("*/distorted*"):
		os.remove(findistorted)
	fname = f"distorted{random.randint(1, 100)}.png"
	image = io.BytesIO()
	await message.client.download_media(data, image)
	image = Image.open(image)
	image.save(fname)
	imgdimens = image.width, image.height
	distortcmd = f"convert {fname} -liquid-rescale {pop}%x{pop}%! -resize {imgdimens[0]}x{imgdimens[1]}\! {fname}"
	os.system(distortcmd)
	image = Image.open(f"{fname}")
	buf = io.BytesIO()
	buf.name = f'image.png'
	image.save(buf, 'PNG')
	buf.seek(0)
	await message.edit("‮`S` `e` `n` `d` `i` `n` `g` `.` `.` `.`")
	await message.client.send_file(message.chat_id, buf, reply_to=reply_message.id)
	await message.delete()
	

	
	
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