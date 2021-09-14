from .. import loader
class nullMod(loader.Module):
    strings = {"name": "null"}
    async def nullcmd(self, message):
        await message.edit("null")