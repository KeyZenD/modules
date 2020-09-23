from .. import loader, utils
from requests import get
import io
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl
import os

class aMod(loader.Module):
	strings = {"name": "UrlDl"}
	
	async def urldlcmd(self, event):
		await downloading(event)
	async def urldlbigcmd(self, event):
		await downloading(event, True)
	
		

async def downloading(event, big=False):
	args = utils.get_args_raw(event)
	reply = await event.get_reply_message()
	if not args:
		if not reply:
			await event.edit("<b>Ссылки нету!</b>")
			return
		message = reply
	else:
		message = event
	
	if not message.entities:
		await event.edit("<b>Ссылки нету!</b>")
		return
	
	urls = []
	for ent in message.entities:
		if type(ent) in [MessageEntityUrl, MessageEntityTextUrl]:
			url_ = True
			if type(ent) == MessageEntityUrl:
				offset = ent.offset
				length = ent.length
				url = message.raw_text[offset:offset+length]
			else:
				url = ent.url
			if not url.startswith("http"):
				url = "http://"+url
			urls.append(url)
			
	if not urls:
		await event.edit("<b>Ссылки нету!</b>")
		return
	for url in urls:
		try:
			await event.edit("<b>Загрузка...</b>\n"+url)
			fname = url.split("/")[-1]
			text = get(url, stream=big)
			if big:
				f = open(fname, "wb")
				for chunk in text.iter_content(1024):
					f.write(chunk)
				f.close()
				await event.edit("<b>Отправка...</b>\n"+url)
				await event.client.send_file(event.to_id, open(fname, "rb"), reply_to=reply)
				os.remove(fname)
			else:
				file = io.BytesIO(text.content)
				file.name = fname
				file.seek(0)
				await event.edit("<b>Отправка...</b>\n"+url)
				await event.client.send_file(event.to_id, file, reply_to=reply)
			
		except Exception as e:
			await event.reply("<b>Ошибка при загрузке!</b>\n"+url+"\n<code>"+str(e)+"</code>")
	
	await event.delete()
	
