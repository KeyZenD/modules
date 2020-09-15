from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from .. import loader, utils
import string
import random
from PIL import Image
import io
from asyncio import sleep

def register(cb):
	cb(pic2packMod())


class pic2packMod(loader.Module):
	"""pic2pack"""

	strings = {'name': 'pic2pack'}

	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []

	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()

	async def pic2packcmd(self, message):
		""".pic2pack {packname} + <reply to photo>"""
		
		reply = await message.get_reply_message()
		if not reply:
			await message.edit("<b>Reply to photo❗</b>")
			return
		
		args = utils.get_args_raw(message)
		if not args:
			await message.edit("<b>Packname</b>❓")
			return
		chat = '@Stickers'
		name = "".join([random.choice(list(string.ascii_lowercase+string.ascii_uppercase)) for _ in range(16)])
		emoji = "▫️"
		image = io.BytesIO()
		await message.client.download_file(reply, image)
		image = Image.open(image)
		w, h = image.size 
		www = max(w, h)
		await message.edit("🔪<b>Cropping...</b>")
		img = Image.new("RGBA", (www,www), (0,0,0,0))
		img.paste(image, ((www-w)//2, 0))
		face = img.resize((100,100))
		fface = io.BytesIO()
		fface.name = name+".png" 
		images = await cropping(img)
		face.save(fface)
		fface.seek(0)
		await message.edit("<b>📤Uploading...</b>")
		async with message.client.conversation(chat) as conv:
			try:
				x = await message.client.send_message(chat, "/cancel")
				await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
				await x.delete()
				x = await message.client.send_message(chat, "/newpack")
				await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
				await x.delete()
				x = await message.client.send_message(chat, args)
				await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
				await x.delete()
				
				for im in images:
					blank = io.BytesIO(im)
					blank.name = name+".png"
					blank.seek(0)
					x = await message.client.send_file(chat, blank, force_document=True)
					await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
					await x.delete()
					x = await message.client.send_message(chat, emoji)
					await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
					await x.delete()
					
					
				
				x = await message.client.send_message(chat, "/publish")
				await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
				await x.delete()
				x = await message.client.send_file(chat, fface, force_document=True)
				await (await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))).delete()
				await x.delete()
				x = await message.client.send_message(chat, name)
				ending = await conv.wait_event(events.NewMessage(incoming=True, from_users=chat))
				await x.delete()
				await ending.delete() 
				for part in ending.raw_text.split():
					if part.startswith("https://t.me/"):
						break
				await message.edit('✅<b>Uploaded successful!</b>\n'+part)
				
			except YouBlockedUserError:
				await message.edit('<b>@Stickers BLOCKED⛔</b>')
				return

			
async def cropping(img):
	(x, y) = img.size
	cy = 5
	cx = 5
	sx = x//cx
	sy = y//cy
	if (sx*cx, sy*cy) != (x, y):
		img = img.resize((sx*cx, sy*cy))
	(lx, ly) = (0, 0)
	media = []
	for i in range(1, cy+1):
		for o in range(1, cx+1):
			mimg = img.crop((lx, ly, lx+sx, ly+sy))
			mimg = mimg.resize((512,512))
			bio = io.BytesIO()
			bio.name = 'image.png'
			mimg.save(bio, 'PNG')
			media.append(bio.getvalue())
			lx = lx + sx
		lx = 0
		ly = ly + sy
	return media