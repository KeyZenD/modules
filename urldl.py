from .. import loader, utils
from requests import get
import io
from telethon.tl.types import MessageEntityUrl, MessageEntityTextUrl

class aMod(loader.Module):
	strings = {"name": "UrlDl"}
	
	async def urldlcmd(self, event):
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
			
		url_ = False
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
				break
				
		if not url_:
			await event.edit("<b>Ссылки нету!</b>")
			return
		await message.edit("<b>Загрузка...</b>")
		try:
			text = get(url).content
			file = io.BytesIO(text)
			file.name = url.split("/")[-1]
			file.seek(0)
			await message.edit("<b>Отправка...</b>")
			await event.client.send_file(event.to_id, file, reply_to=reply)
			await event.delete()
		except Exception as e:
			await event.edit("<b>Ошибка при загрузке!\n</b>"+"<code>"+str(e)+"</code>")
