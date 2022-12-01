import asyncio
import itertools
import logging
import re
import sys
import telethon
import traceback
import types
from meval import meval
from .. import loader, utils

logger = logging.getLogger(__name__)


class ModuleNotForBot(Exception):
    pass


@loader.tds
class PyDraftMod(loader.Module):
    """Выполняет выражение из черновиков (работает 10 минут)
    инструкция на канале @SomeScripts"""
    strings = {
        'name': 'PyDraft',
        'on': 'PyDraft: Включен',
        'off': 'PyDraft: Отключен',
        'isolator': 'pydraft:',
        'timer': 60 * 10,
        'note': '(PyDraft) ExecNote {} не найден!',
        "evaluated": "(PyDratf)Выполненное выражение:\n{}\nВозвращено:\n{}",
        "execute_fail": "(PyDraft)Не удалось выполнить выражение:\n{}\nОшибка:\n{}"}

    def __init__(self):
        self.name = self.strings['name']

    async def client_ready(self, client, db):
        self.client: telethon.client.telegramclient.TelegramClient = client
        self.db = db
        self._db = db

    async def pydraftcmd(self, message):
        """Запустить/Остановить"""
        status = self.db.get(self.name, "status", False)
        if not status:
            self.db.set(self.name, "status", True)
            self.client.loop.create_task(self.check_drafts(message))
            await utils.answer(message, self.strings['on'])
        else:
            self.db.set(self.name, 'status', False)
            await utils.answer(message, self.strings['off'])

    async def pydraft(self, draft):
        show = True if draft.text.startswith('!') else False
        cmd = draft.text[len(self.strings['isolator'])+(1 if show else 0):].strip()
        if cmd.startswith('note:'):
            asset_id = self._db.get("friendly-telegram.modules.notes", "notes", {}).get(cmd.replace('note:', ''), None)
            if asset_id is not None:
                cmd = await self._db.fetch_asset(asset_id)

        await draft.delete()
        try:
            it = await meval(cmd, globals(), **await self.getattrs(draft))
            if show:
                ret = self.strings["evaluated"].format(cmd, utils.escape_html(it))
                await draft.set_message(ret)
        except Exception:
            exc = sys.exc_info()
            exc = "".join(traceback.format_exception(exc[0], exc[1], exc[2].tb_next.tb_next.tb_next))
            await draft.set_message(self.strings["execute_fail"].format(cmd, exc))
            return

    async def check_drafts(self, message):
        msg = await self.client.send_message('me', 'PyDraft')
        timer = 0
        while True:
            await msg.edit(f"PyDraft time left {self.strings['timer']-timer}")
            if not self.db.get(self.name, "status", False):
                await utils.answer(message, self.strings['off'])
                break
            isolator = self.strings['isolator']
            drafts = await self.client.get_drafts()
            for draft in drafts:
                text = draft.text
                if text.startswith(isolator) or text.startswith('!' + isolator):
                    await self.pydraft(draft)
            timer += 1
            await asyncio.sleep(1)
            if timer >= self.strings['timer']:
                self.db.set(self.name, 'status', False)
                await utils.answer(message, self.strings['off'])
                break
        await msg.delete()

    async def getattrs(self, draft):
        data = {'draft':draft, "client": self.client, "self": self, "db": self.db, "chat": draft.entity.id, **self.get_types(), **self.get_functions()}
        if draft.reply_to_msg_id:
            data['message'] = await self.client.get_messages(draft.entity.id, ids=draft.reply_to_msg_id)
            data['reply'] = await data['message'].get_reply_message()
        return data

    def get_types(self):
        return self.get_sub(telethon.tl.types)

    def get_functions(self):
        return self.get_sub(telethon.tl.functions)

    def get_sub(self, it, _depth=1):
        """Get all callable capitalised objects in an object recursively, ignoring _*"""
        return {**dict(filter(lambda x: x[0][0] != "_" and x[0][0].upper() == x[0][0] and callable(x[1]),
                              it.__dict__.items())),
                **dict(itertools.chain.from_iterable([self.get_sub(y[1], _depth + 1).items() for y in
                                                      filter(lambda x: x[0][0] != "_"
                                                                       and isinstance(x[1], types.ModuleType)
                                                                       and x[1] != it
                                                                       and x[1].__package__.rsplit(".", _depth)[0]
                                                                       == "telethon.tl",
                                                             it.__dict__.items())]))}
