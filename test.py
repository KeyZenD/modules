#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import logging
import time
from datetime import datetime

from io import BytesIO

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.test(args=None)
async def dumptest(conv):
    m = await conv.send_message("test")
    await conv.send_message(".dump", reply_to=m)
    r = await conv.get_response()
    assert r.message.startswith("Message(") and "test" in r.message, r


@loader.test(args="0")
async def logstest(conv):
    r = await conv.get_response()
    assert r.message == "Loading media...", r
    r2 = await conv.get_response()
    assert r2.document, r2


@loader.tds
class TestMod(loader.Module):
    """Self-tests"""
    strings = {"name": "Tester",
               "pong": ".pong",
               "bad_loglevel": "<b>Не верный уровень логов.</b>",
               "uploading_logs": "<b>Собираю логи...</b>",
               "no_logs": "<b>Логов с уровнем {} нет.</b>",
               "logs_filename": "FTG-Logs[{}].txt",
               "logs_unsafe": ("<b>Если ты точно хочешь показать логи с уровнем {lvl}, то напиши </b><code>.logs {lvl} {force}</code>"),
               "logs_force": "FORCE_INSECURE",
               "suspend_invalid_time": "<b>Invalid time to suspend</b>"}

    @loader.test(resp="Pong")
    @loader.unrestricted
    async def pingcmd(self, message):
        """Does nothing"""
        await utils.answer(message, self.strings("pong", message))
    
    @loader.owner
    async def pungcmd(self, message):
        """Useless pinger"""
        a = 5
        r = utils.get_args(message)
        if r and r[0].isdigit():
            a = int(r[0])
        ping_msg = []
        ping_data = []
        for _ in range(a):
            start = datetime.now()
            msg = await message.client.send_message("me", "ping")
            end = datetime.now()
            duration = (end - start).microseconds / 1000
            ping_data.append(duration)
            ping_msg.append(msg)
        ping = sum(ping_data) / len(ping_data)
        await message.edit(f"<code>[ ping {str(ping)[0:5]}ms ]</code>")
        for i in ping_msg:
            await i.delete()

    @loader.test(func=dumptest)
    async def dumpcmd(self, message):
        """Use in reply to get a dump of a message"""
        if not message.is_reply:
            return
        await utils.answer(message, "<code>"
                           + utils.escape_html((await message.get_reply_message()).stringify()) + "</code>")

    @loader.test(func=logstest)
    async def logscmd(self, message):
        """.logs <level>
           Dumps logs. Loglevels below WARNING may contain personal info."""
        args = utils.get_args(message)
        if not len(args) == 1 and not len(args) == 2:
            args = ["40"]
        try:
            lvl = int(args[0])
        except ValueError:
            # It's not an int. Maybe it's a loglevel
            lvl = getattr(logging, args[0].upper(), None)
        if not isinstance(lvl, int):
            await utils.answer(message, self.strings("bad_loglevel", message))
            return
        if not (lvl >= logging.WARNING or (len(args) == 2 and args[1] == self.strings("logs_force", message))):
            await utils.answer(message,
                               self.strings("logs_unsafe", message).format(lvl=lvl, force=self.strings("logs_force", message)))
            return
        [handler] = logging.getLogger().handlers
        logs = ("\n".join(handler.dumps(lvl))).encode("utf-8")
        if not len(logs) > 0:
            await utils.answer(message, self.strings("no_logs", message).format(lvl))
            return
        logs = BytesIO(logs)
        logs.name = self.strings("logs_filename", message).format(lvl)
        await utils.answer(message, logs)

    @loader.owner
    async def suspendcmd(self, message):
        """.suspend <time>
           Suspends the bot for N seconds"""
        # Blocks asyncio event loop, preventing ANYTHING happening (except multithread ops,
        # but they will be blocked on return).
        try:
            time.sleep(int(utils.get_args_raw(message)))
        except ValueError:
            await utils.answer(message, self.strings("suspend_invalid_time", message))

    async def client_ready(self, client, db):
        self.client = client
