from .. import loader, utils
import os
import urllib.parse
from uuid import uuid4

ztd = 'zip-temp-dir'

@loader.tds
class ZipMod(loader.Module):
	'''Запаковывает/распаковывает файлы'''
	strings = {'name': 'ZIP'}

	@loader.unrestricted
	async def zipaddcmd(self, message):
		""".zipadd <file/reply to file> - сохраняет файл во временную папку"""
		reply = await message.get_reply_message()
		event = reply or message
		
		if not event.file:
			await message.edit('<b>[ZIP]Добавить что?<b>')
			return
		
		if not os.path.exists(ztd):
			os.mkdir(ztd)
		
		fn = _fn = event.file.name
		if not fn:
			date = event.date
			kind = event.file.mime_type.split('/')[0]
			ext =  event.file.ext
			fn = _fn = '{}_{}-{:02}-{:02}_{:02}-{:02}-{:02}{}'.format(kind, date.year, date.month, date.day, date.hour, date.minute, date.second, ext)
			
		files = os.listdir(ztd)
		copy = 1
		while fn in files:
			fn = f"({copy}).{_fn}"
			copy += 1
		await message.edit(f'<b>[ZIP]Загружаю файл \'</b><code>{fn}</code>\'...')
		await event.download_media(f'{ztd}/{fn}')
		await message.edit(f"<b>[ZIP]Файл \"</b><code>{fn}</code><b>\" загружен!</b>")
	
	@loader.unrestricted
	async def ziplistcmd(self, message):
		"""список сохраненных файлов"""
		if not os.path.exists(ztd):
			await message.edit('<b>[ZIP]В папке пусто!</b>')
			return
		files = os.listdir(ztd)
		files = '\n'.join([f'<a href="tg://msg?text=.zipshow+{urllib.parse.quote(fn)}">{num+1})</a> <code>{fn}</code>' for num, fn in enumerate(files)])
		await message.edit('<b>[ZIP]Список файлов:</b>\n'+files)
		
	@loader.unrestricted
	async def zipshowcmd(self, message):
		""".zipshow <name> - показывает сохранённый файл"""
		if not os.path.exists(ztd):
			await message.edit('<b>[ZIP]В папке пусто!</b>')
			return
		files = os.listdir(ztd)
		file = utils.get_args_raw(message)
		if not file:
			await message.edit('<b>[ZIP]Пустой запрос!</b>')
			return
		if file not in files:
			await message.edit('<b>[ZIP]Такого файла нет!</b>')
			return
		await message.edit(f"<b>[ZIP]Отправляю \"</b><code>{file}</code><b>\"...")
		await message.respond(file=ztd+"/"+file)
		await message.delete()
		
	@loader.unrestricted
	async def zipdelcmd(self, message):
		""".zipdel <name> - удаляет сохранённый файл"""
		file = utils.get_args_raw(message)
		try:
			os.remove(ztd+"/"+file)
		except FileNotFoundError:
			await message.edit("<b>[ZIP]Такого файла нет!</b>")
			return
		await message.edit(f"<b>[ZIP]Файл \"</b><code>{file}</code><b>\" удалён!</b>")
		
		
	@loader.unrestricted
	async def zipcmd(self, message):
		""".zip <name> (-s) - пакует в архив name. если есть флаг -s то сохраняет папку с фацлами"""
		if not os.path.exists(ztd):
			await message.edit("<b>[ZIP]Файлов для запаковки не найдено!</b>")
			return
		name = utils.get_args_raw(message)
		save = False
		if "-s" in name:
			save = True
			name = name.replace("-s","").strip()
		if not name:
			name = str(uuid4()).split("-")[-1]+".zip"
			
		name = name + (".zip" if ".zip" not in name else "")
		await message.edit(f'<b>[ZIP]Запаковываю {len(os.listdir(ztd))} файл(ов) в </b>"<code>{name}</code>"')
		os.system(f"zip {name} {ztd}/*")
		await message.edit(f'<b>[ZIP]Отправляю </b>"<code>{name}</code>"')
		await message.respond(file=open(name, "rb"))
		await message.delete()
		os.system("rm -rf {name}")
		if not save:
			os.system("rm -rf zip-temp-dir")
		
	@loader.unrestricted
	async def zipcleancmd(self, message):
		""".zipclear - очищает папку с файлами"""
		os.system("rm -rf zip-temp-dir")
		await message.edit('<b>[ZIP]Очищено!</b>')
		os.mkdir(ztd)
