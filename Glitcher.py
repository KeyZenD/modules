import asyncio
import logging
import sys, os, random
from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class GlitcherMod(loader.Module):
    """Glitcher of anything"""
    strings = {"name": "Glitcher",
               "reply": "Reply to message!",
               "error": "Impossible to upload file!",
			   "processing": "Work in progress!"}

    @loader.unrestricted
    async def glitchcmd(self, message):
        """.glitch level: float or int <reply to anything>"""
        reply = await message.get_reply_message()
        if not reply:
            await message.edit("".join([ random.choice(html).format(ch) for ch in self.strings("reply", message)]))
            return
        if not reply.file:
            infile = "message.txt"
            f = open(infile,"w")
            f.write(reply.text)
            f.close()
            outfile = "glitched_message.txt"
        else:
            infile = await reply.download_media()
            outfile = "glitched_"+infile
        
        percent = 0.1
        try:
            percent = float(utils.get_args_raw(message))
        except ValueError or TypeError:
            pass
        await message.edit("".join([ random.choice(html).format(ch) for ch in self.strings("processing", message)]))
        with open(infile, 'rb') as inf:
            with open(outfile, 'wb') as outf:
                fileext = infile.split(".")[1]
                try:
                    for byte in range(headersize[fileext]):
                        inbyte = inf.read(1)
                        outbyte = inbyte
                        outf.write(outbyte)
                except KeyError:
                    pass
                while True:
                    inbyte = inf.read(1)
                    if not inbyte:
                        break
                    if (random.random() < percent/100):
                        outbyte = os.urandom(1)
                    else:
                        outbyte = inbyte
                    outf.write(outbyte)
        try:
            await reply.reply(file=outfile)
            await message.delete()
        except:
            await message.edit("".join([ random.choice(html).format(ch) for ch in self.strings("error", message) ]))
        finally:
            [os.remove(file) for file in [infile, outfile]]
        
html = ["<b>{}<b>", "<code>{}</code>", "<i>{}</i>", "<del>{}</del>", "<u>{}</u>", '<a href="https://bruh.moment">{}</a>']
headersize = {'jpg': 9, 'png': 8, 'bmp': 54, 'gif': 14, 'tiff': 8}  
