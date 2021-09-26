# @KeyZenD & @D4n13l3k00
# requires: bs4 aiogram

from random import choice
from string import ascii_lowercase

from aiogram import Bot
from bs4 import BeautifulSoup as bs4
from telethon import events, functions, types
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import Channel

from .. import loader, utils


class KickLastMod(loader.Module):
    """Удаляет из чата последних Х зашедших"""

    strings = {
        'name': 'KickLast',
        'pref': '<b>[KickLast]</b> ',
        'cdne': '{}Такого чата не существует',
        'cfju': '{}Не могу обнаружить зашедших...',
        'success': '{}Операция завершена! Кикнуто {} юзеров',
        'found': '{}Найдено {} зашедших юзеров! Кикаю...',
        'howmany': '{}Сколько нужно кикнуть?\n0 если всех зашедших за 48 часов',
        'createerr': '{}Создание бота недоступно.\nПовтори попытку через {}'
        }

    async def botkicklastcmd(self, message):
        """.botkicklst <количество> <юзернейм, если канал> - Кикает при помощи тг бота"""
        await kick(self, message, True)

    async def kicklastcmd(self, message):
        """.kicklst <количество> <юзернейм, если канал> - Кикает юзерботом"""
        await kick(self, message, False)


async def kick(self, message, bot=False):
    client = message.client
    args = utils.get_args(message)
    if not args:
        return await utils.answer(message, self.strings('howmany').format(self.strings('pref')))
    limit = int(args[0])
    limit = limit or 99999
    group = args[-1] if len(args) > 1 else message.chat.id
    try:
        group = await client.get_entity(group)
    except:
        await utils.answer(message, self.strings('cdne').format(self.strings('pref')))
    if not isinstance(group, Channel):
        return await utils.answer(message, self.strings('cdne').format(self.strings('pref')))
    if bot:
        botfather = 93372553
        bantoolbot = "".join(choice(list(ascii_lowercase))
                             for _ in range(29))+"bot"
        async with client.conversation(botfather) as conv:
            await (await client.send_message(botfather, "/newbot")).delete()
            newbot = await conv.wait_event(events.NewMessage(incoming=True, from_users=botfather))
            await newbot.delete()
            if "Sorry" in newbot.text:
                return await utils.answer(message, self.strings('howmany').format(self.strings('pref'), newbot.text[45:]))
            await (await client.send_message(botfather, "BanTool")).delete()
            await (await conv.wait_event(events.NewMessage(incoming=True, from_users=botfather))).delete()
            await (await client.send_message(botfather, bantoolbot)).delete()
            html = await conv.wait_event(events.NewMessage(incoming=True, from_users=botfather))
            await html.delete()
            soup = bs4(html.text, "html.parser")
            token = soup.findAll("code")[0].text
        await client(InviteToChannelRequest(group, [bantoolbot]))
        await client(functions.channels.EditAdminRequest(
            channel=group,
            user_id=bantoolbot,
            admin_rights=types.ChatAdminRights(ban_users=True), rank='BanToolBot'))
    banlist = [x.user_id async for x in client.iter_admin_log(group, join=True, limit=limit)]
    
    message = await utils.answer(message, self.strings('found').format(self.strings('pref'), str(len(banlist))))
    if not banlist:
        return await utils.answer(message, self.strings('cfju').format(self.strings('pref')))
    for banid in banlist:
        if bot:
            await Bot(token).kick_chat_member(f"-100{group}", banid)
        else:
            await client.kick_participant(group, banid)
    if bot:
        await client.kick_participant(group, bantoolbot)
        async with client.conversation(botfather) as conv:
            await client.send_message(botfather, "/deletebot")
            await conv.wait_event(events.NewMessage(incoming=True, from_users=botfather))
            await client.send_message(botfather, "@"+bantoolbot)
            await conv.wait_event(events.NewMessage(incoming=True, from_users=botfather))
            await client.send_message(botfather, "Yes, I am totally sure.")
    return await utils.answer(message, self.strings('success').format(self.strings('pref'), str(len(banlist))))
