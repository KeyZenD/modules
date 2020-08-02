from .. import loader, utils
import io
from PIL import Image
from string import hexdigits

def register(cb):
    cb(StickToolsMod())


class StickToolsMod(loader.Module):
    """"""

    strings = {'name': 'StickTools'}

    def __init__(self):
        self.name = self.strings['name']
        
    async def stick2piccmd(self, message):
        """reply to Sticker\nsend stricker as image"""
        await convert(message, False)
        
    async def stick2filecmd(self, message):
        """reply to Sticker\nsend stricker as image"""
        await convert(message, True)
        
async def convert(message, as_file):
    reply = await message.get_reply_message()
    if not reply or not reply.sticker:
        await message.edit("<b>Reply to sticker!</b>")
        return
    fname = reply.sticker.attributes[-1].file_name
    if ".tgs" in fname:
        await message.edit("<b>Reply to not animated sticker!</b>")
        return
    bg =  (0,0,0,0)
    args = utils.get_args(message)
    if args:
        args = args[0]
        if args.startswith("#"):
            for ch in args[1:]:
                if ch not in hexdigits:
                    break
            bg = args
    
    im = io.BytesIO()
    await message.client.download_file(reply, im)
    im = Image.open(im)
    img = Image.new("RGBA", im.size, bg)
    if im.mode == "RGBA":
        img.paste(im, (0,0), im)
    else:
        img.paste(im, (0,0))
    out = io.BytesIO()
    out.name = fname+".png"
    img.save(out, "PNG")
    out.seek(0)
    await message.delete()
    await message.client.send_file(message.to_id, out, force_document=as_file, reply_to=reply)
