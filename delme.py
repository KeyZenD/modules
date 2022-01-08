from .. import loader, utils

class DelmeMod(loader.Module):
    """Удаляет все сообщения"""
    strings = {'name': 'DelMe'}
    def __init__(self):
        self.name = self.strings['name']
    async def client_ready(self, client, db):
        message.client = client
    
    @loader.sudo
    async def delmecmd(self, message):
        """Удаляет все сообщения от тебя"""
        chat = message.chat
        if chat:
            args = utils.get_args_raw(message)
            if args != str(message.chat.id+message.sender_id):
                await message.edit(f"<b>Если ты точно хочешь это сделать, то напиши:</b>\n<code>.delme {message.chat.id+message.sender_id}</code>")
                return
            await delete(message, chat)
        else:
            await message.edit("<b>В лс не чищу!</b>")
    @loader.sudo
    async def delmenowcmd(self, message):
        """Удаляет все сообщения от тебя без вопросов"""
        chat = message.chat
        if chat:
            await delete(message, chat)
        else:
            await message.edit("<b>В лс не чищу!</b>")
            

async def delete(message, chat):
    all = (await message.client.get_messages(chat, from_user="me")).total
    messages = [msg async for msg in message.client.iter_messages(chat, from_user="me")]
    await message.edit(f"<b>{all} сообщений будет удалено!</b>")
    _ = ""
    async for msg in message.client.iter_messages(chat, from_user="me"):
        if _:
            await msg.delete()
        else:
            _ = "_"
    await message.delete()
