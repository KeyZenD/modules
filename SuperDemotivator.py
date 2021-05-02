from .. import loader, utils
import logging
from PIL import Image, ImageDraw, ImageOps, ImageFont
from textwrap import wrap
import io
import requests
from random import choice
# https://t.me/KeyZenD
# https://t.me/Govnocodules
# https://t.me/DneZyeK
logger = logging.getLogger(__name__)

@loader.tds
class DeMoTiVaToRsMod(loader.Module):
	"""Демотиваторы на картинки от @GovnoCodules by @DneZyeK"""
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
		text = choice(tttxxx)
		
	await message.edit("<b>Демотивирую...</b>")
	bytes_image = await event.download_media(bytes)
	demotivator = await demotion(font_bytes, bytes_image, text, type)
	if is_reply:
		await message.delete()
		return await event.reply(file=demotivator)
		
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
tttxxx = ['А че', 'заставляет задуматься', 'Жалко пацана', 'ты че сука??', 'ААХАХАХАХХАХА\n\nААХАХААХАХА', 'ГИГАНТ МЫСЛИ\n\nотец русской демократии', 'Он', 'ЧТО БЛЯТЬ?', 'охуенная тема', 'ВОТ ОНИ\n\nтипичные комедиклабовские шутки', 'НУ НЕ БЛЯДИНА?', 'Узнали?', 'Согласны?', 'Вот это мужик', 'ЕГО ИДЕИ\n\nбудут актуальны всегда', '\n\nПРИ СТАЛИНЕ ОН БЫ СИДЕЛ', 'о вадим', '2 месяца на дваче\n\nи это, блядь, нихуя не смешно', 'Что дальше?\n\nЧайник с функцией жопа?', '\n\nИ нахуя мне эта информация?', 'Верхний текст', 'нижний текст', 'Показалось', 'Суды при анкапе', 'Хуйло с района\n\n\n\nтакая шелупонь с одной тычки ляжет', 'Брух', 'Расскажи им\n\nкак ты устал в офисе', 'Окурок блять\n\nесть 2 рубля?', 'Аниме ставшее легендой', 'СМИРИСЬ\n\n\n\nты никогда не станешь настолько же крутым', 'а ведь это идея', '\n\nЕсли не лайкнешь у тебя нет сердца', 'Вместо тысячи слов', 'ШАХ И МАТ!!!', 'Самый большой член в мире\n\nУ этой девушки', 'Немного\n\nперфекционизма', 'кто', '\n\nэта сука уводит чужих мужей', 'Кто он???', '\n\nВы тоже хотели насрать туда в детстве?', '\n\nВся суть современного общества\n\nв одном фото', 'Он обязательно выживет!', '\n\nВы тоже хотите подрочить ему?', '\n\nИ вот этой хуйне поклоняются русские?', 'Вот она суть\n\n\n\nчеловеческого общества в одной картинке', 'Вы думали это рофл?\n\nНет это жопа', '\n\nПри сталине такой хуйни не было\n\nА у вас было?', 'Он грыз провода', 'Назло старухам\n\nна радость онанистам', 'Где-то в Челябинске', 'Агитация за Порошенко', 'ИДЕАЛЬНО', 'Грыз?', 'Ну давай расскажи им\n\nкакая у тебя тяжелая работа', '\n\nЖелаю в каждом доме такого гостя', 'Шкура на вырост', 'НИКОГДА\n\nне сдавайся', 'Оппа гангнам стайл\n\nуууу сэкси лейди оп оп', 'Они сделали это\n\nсукины дети, они справились', 'Эта сука\n\nхочет денег', 'Это говно, а ты?', '\n\nВот она нынешняя молодежь', 'Погладь кота\n\nпогладь кота сука', 'Я обязательно выживу', '\n\nВот она, настоящая мужская дружба\n\nбез политики и лицимерия', '\n\nОБИДНО ЧТО Я ЖИВУ В СТРАНЕ\n\nгде гантели стоят в 20 раз дороже чем бутылка водки', 'Царь, просто царь', '\n\nНахуй вы это в учебники вставили?\n\nИ ещё ебаную контрольную устроили', '\n\nЭТО НАСТОЯЩАЯ КРАСОТА\n\nа не ваши голые бляди', '\n\nТема раскрыта ПОЛНОСТЬЮ', '\n\nРОССИЯ, КОТОРУЮ МЫ ПОТЕРЯЛИ', 'ЭТО - Я\n\nПОДУМАЙ МОЖЕТ ЭТО ТЫ', 'почему\n\nчто почему', 'КУПИТЬ БЫ ДЖЫП\n\nБЛЯТЬ ДА НАХУЙ НАДО', '\n\n\n\nмы не продаём бомбастер лицам старше 12 лет', 'МРАЗЬ', 'Правильная аэрография', 'Вот она русская\n\nСМЕКАЛОЧКА', 'Он взял рехстаг!\n\nА чего добился ты?', 'На аватарку', 'Фотошоп по-деревенски', 'Инструкция в самолете', 'Цирк дю Солей', 'Вкус детства\n\nшколоте не понять', 'Вот оно - СЧАСТЬЕ', 'Он за тебя воевал\n\nа ты даже не знаешь его имени', 'Зато не за компьютером', '\n\nНе трогай это на новый год', 'Мой первый рисунок\n\nмочой на снегу', '\n\nМайские праздники на даче', 'Ваш пиздюк?', 'Тест драйв подгузников', 'Не понимаю\n\nкак это вообще выросло?', 'Супермен в СССР', 'Единственный\n\nкто тебе рад', 'Макдональдс отдыхает', 'Ну че\n\n как дела на работе пацаны?', 'Вся суть отношений', 'Беларусы, спасибо!', '\n\nУ дверей узбекского военкомата', 'Вместо 1000 слов', 'Один вопрос\n\nнахуя?', 'Ответ на санкции\n\nЕВРОПЫ', 'ЦЫГАНСКИЕ ФОКУСЫ', 'Блять!\n\nда он гений!', '\n\nУкраина ищет новые источники газа', 'ВОТ ЭТО\n\nНАСТОЯЩИЕ КАЗАКИ а не ряженные', 'Нового года не будет\n\nСанта принял Ислам', '\n\nОн был против наркотиков\n\nа ты и дальше убивай себя', 'Всем похуй!\n\nВсем похуй!', 'БРАТЬЯ СЛАВЯНЕ\n\nпомните друг о друге', '\n\nОН ПРИДУМАЛ ГОВНО\n\nа ты даже не знаешь его имени', '\n\nкраткий курс истории нацболов', 'Эпоха ренессанса']
font_bytes = requests.get("https://raw.githubusercontent.com/KeyZenD/l/master/times.ttf").content
#######################