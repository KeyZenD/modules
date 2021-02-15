import asyncio
import logging
from requests import get
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class ValitesMod(loader.Module):
	"""Valute converter"""
	strings = {"name": "Valutes"}

	@loader.unrestricted
	async def valutecmd(self, message):
		""".valute <Valute char code (optional)>"""
		valutes = get("https://www.cbr-xml-daily.ru/daily_json.js").json()
		names = valutes["Valute"].keys()
		args = utils.get_args(message)
		req = []
		
		if args:
			for val in args:
				val = val.upper()
				if val in names:
					req.append(val)
			valutes["Valute"] = {val: valutes["Valute"][val] for val in req}
			
		text = []
		temp = "<b>{}</b>\n{} <code>{}</code>: {}₽ ({}{}₽)"
		for val in valutes["Valute"].values():
			name = val["Name"]
			code = val["CharCode"]
			nom = int(val["Nominal"])
			now = round(float(val["Value"]), 3)
			pre = round(float(val["Previous"]), 3)
			way = "🔹" if now == pre else "🔻" if now < pre else "🔺"
			text.append(temp.format(name, nom, code, now, way, pre))
		if not text:
			return await utils.answer(message, "<b>Запрос неверен - ответ пуст!</b>")
		await utils.answer(message, "\n".join(text))
