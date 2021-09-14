from asyncio import sleep
from userbot.events import register


@register(outgoing=True, pattern='^.fl ?(.*)')
async def fakeload(e):
	inp = e.pattern_match.group(1)
	load = [" ","▏","▎","▍","▌","▋","▊","▉"]
	bar = ""
	count = 0
	await e.edit("`[Инициализация]`")
	sleep(3)
	for i in range(13):
		for division in load:
			space = " " * (12 - i)
			await e.edit(f"`{bar}{division}{space}[{count}%]`")
			count += 1
			sleep(0.3)
			if count == 101:
				break
		bar += "█"
	sleep(2)
	done = "Загрузка завершена!"
	if inp:
		done = inp
	await e.edit(f"`{done}`")
