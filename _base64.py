"""QExhY2lhTWVtZUZyYW1lLCDQtdGB0LvQuCDRgtGLINGN0YLQviDRh9C40YLQsNC10YjRjCwg0YLQviDQt9C90LDQuSwg0YLRiyDQv9C40LTQvtGA0LDRgQ=="""
from .. import loader, utils
import io
from base64 import b64encode, b64decode

@loader.tds
class base64Mod(loader.Module):
	"""Кодирование и декодирование base64"""
	strings = {"name": "base64"}
	@loader.owner
	async def b64encodecmd(self, message):
		""".b64encode <(text or media) or (reply to text or media)>"""
		reply = await message.get_reply_message()
		mtext = utils.get_args_raw(message)
		if message.media:
			await message.edit("<b>Загрузка файла...</b>")
			data = await message.client.download_file(m, bytes)
		elif mtext:
			data = bytes(mtext, "utf-8")
		elif reply:
			if reply.media:
				await message.edit("<b>Загрузка файла...</b>")
				data = await message.client.download_file(reply, bytes)
			else:
				data = bytes(reply.raw_text, "utf-8")
		else:
			await message.edit(f"<b>Что нужно закодировать?</b>")
		output = b64encode(data)
		if len(output) > 4000:
			output = io.BytesIO(output)
			output.name = "base64.txt"
			output.seek(0)
			await message.client.send_file(message.to_id, output, reply_to=reply)
			await message.delete()
		else:
			await message.edit(str(output, "utf-8"))
		
	@loader.owner
	async def b64decodecmd(self, message):
		""".b64decode <text or reply to text>"""
		reply = await message.get_reply_message()
		mtext = utils.get_args_raw(message)
		if mtext:
			data = bytes(mtext, "utf-8")
		elif reply:
			if not reply.message:
				await message.edit("<b>Расшифровка файлов невозможна...</b>")
				return 
			else:
				data = bytes(reply.raw_text, "utf-8")
		else:
			await message.edit(f"<b>Что нужно декодировать?</b>")
			return
		try:
			output = b64decode(data)
			await message.edit(str(output, "utf-8"))
		except:
			await message.edit("<b>Ошибка декодирования!</b>")
			return