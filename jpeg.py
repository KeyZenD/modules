from PIL import Image
from telethon.tl.types import DocumentAttributeFilename
from uniborg.util import admin_cmd
import io

@borg.on(admin_cmd(pattern=".jpeg?(.*)", allow_sudo=True)) 
async def shacal(event):
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
		
	if event.is_reply:
		reply_message = await event.get_reply_message()
		data = await check_media(reply_message)
		if isinstance(data, bool):
			await event.delete()
			return
	else:
		await event.delete()
		return
		
	image = io.BytesIO()
	await event.client.download_media(data, image)
	image = Image.open(image)
	fried_io = io.BytesIO()
	fried_io.name = "image.jpeg"
	image = image.convert("RGB")
	image.save(fried_io, "JPEG", quality=0)
	fried_io.seek(0)
	await event.delete()
	await event.client.send_file(event.chat_id, fried_io, reply_to=reply_message.id)

