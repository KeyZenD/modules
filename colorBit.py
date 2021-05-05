from .. import loader, utils
from PIL import Image
from io import BytesIO as io

class colorBitMod(loader.Module):
    strings = {"name": "colorBit"}
    async def cbitcmd(self, message):
        """.cbit <число от 0 до 255"""
        reply = await message.get_reply_message()
        if not reply or not reply.file or not "image" in reply.file.mime_type:
            return await message.edit("<b>Reply to image!</b>")
        x = utils.get_args_raw(message)
        x = int(x) if x.isdigit() else 8
        if x <= 0 or x >= 256:
            x = 8 
        x = 256//x
        im = Image.open(io(await reply.download_media(bytes)))
        w, h = im.size
        mode = im.mode
        out = []
        await message.edit("<b>Processing...</b>")
        for bit in list(im.tobytes()):
            bit = list(range(0, 256+x, x))[bit//x]
            out.append(bit)
        image = Image.frombytes(mode, (w, h), bytes(out))
        output = io()
        image.save(output, "PNG")
        output.seek(0)
        await message.delete()
        await reply.reply(file=output)