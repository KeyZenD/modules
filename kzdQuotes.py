from .. import loader, utils
import telethon
import logging
import io
from telethon.tl.types import (ChannelParticipantsAdmins, ChannelParticipantCreator, ChannelParticipantAdmin, User)
from requests import post
from PIL import Image


logger = logging.getLogger("kzdQuotes")


@loader.tds
class kzdQuotesMod(loader.Module):
    """kzdQuote a message"""
    strings = {
        "name": "kzdQuotes",
        "processing": "<b>️Quoting</b>",
        "processing_api": "<b>Quoting💬</b>",
        "no_reply": "<b>Нет реплая</b>",
        "mediaType_photo": "️Фото",
        "mediaType_video": "Видео",
        "mediaType_videomessage": "Видеосообщение",
        "mediaType_voice": "️Аудиосообщение",
        "mediaType_audio": "Аудио",
        "mediaType_poll": "Голосование",
        "mediaType_quiz": "Викторина",
        "mediaType_location": "Геолокация",
        "mediaType_gif": "GIF",
        "mediaType_sticker": "Стикер",
        "mediaType_file": "Файл: ",
        "diceType_dice": "Кубик", 
        "diceType_dart": "Дартс",
        "ball_thrown": "Бросок мяча",
        "dart_thrown": "Бросок дротика",
        "dart_almostthere": "близко к цели!",
        "dart_missed": "мимо!",
        "dart_bullseye": "в яблочко!",
        "settings": "<b>Доступные настройки:</b>\n<code>color</code> - hex color - Цвет квотеса"
    }

    async def client_ready(self, client, db):
        self.client = client
        self.db = db

    @loader.unrestricted
    @loader.ratelimit
    async def qqcmd(self, message):
        args = utils.get_args_raw(message)
        reply = await message.get_reply_message()
        if not reply:
            await utils.answer(message, self.strings('no_reply', message))
            return
        await utils.answer(message, self.strings('processing', message))
        fwd = via = rtext = file = thumb = rname = admintitle = None
        if ".file" in args:
            file = True
            args = args.replace(".file","").strip()

        text = args or reply.text
        sender = user = reply.sender
        if sender:
            id = sender.id if sender.id != 1087968824 else reply.chat.id
        else:
            id = reply.fwd_from.channel_id
        
        sender = await message.client.get_entity(id)
        name = "Deleted Account" if user and sender.deleted else telethon.utils.get_display_name(sender)
        pfp = await message.client.download_profile_photo(sender, bytes)
        if reply.fwd_from and reply.sender:
            id = reply.fwd_from.from_id or reply.fwd_from.channel_id
            if not id:
                fname = reply.fwd_from.from_name
            else:
                sender = await message.client.get_entity(id)
                fwd  = telethon.utils.get_display_name(sender)

        if reply.via_bot:
            via  = reply.via_bot.username or "magic"

        img = await check_media(message, reply)
        rreply = await reply.get_reply_message()
        if rreply and not args:
            thumb = await check_media(message, rreply, True)
            rtext = rreply.raw_text
            if rreply.media:
                rtext = await get_media_caption(rreply) #спиздено у t.me/rfoxxxy
            rsender = rreply.sender
            rname = telethon.utils.get_display_name(rsender)
            

        if message.chat and reply.sender:
            admins = await message.client.get_participants(message.to_id, filter=ChannelParticipantsAdmins)
            if reply.sender in admins:
                admin = admins[admins.index(reply.sender)].participant
                if not admin:
                    admintitle = None
                else:
                    admintitle = admin.rank
                if not admintitle:
                    if type(admin) == ChannelParticipantCreator:
                        admintitle = "creator" 
                    else:
                        admintitle = "admin"
        else:
            admintitle = "channel" if message.chat else None
            
        
        color = self.db.get("kzdQuotes", "color", None)
        data = {"id":id,"name":name,"admin":admintitle, "via":via, "fwd":fwd,"text":text,"rtext":rtext,"rname":rname, "color":color}
        files = {"pfp": pfp, "img":img, "thumb": thumb}
        await utils.answer(message, self.strings('processing_api', message))
        q = post("https://tyt.keyzend.pw/quote", data=data, files=files).content
        quote = io.BytesIO()
        quote.name = "govnoquotes"+ (".png" if file else ".webp")
        im = Image.open(io.BytesIO(q))
        if not file:
            im.thumbnail((512, 512))
            back = Image.new("RGBA", (im.width, im.height+100), None)
            back.paste(im, (0, 0), im)
            im = back
            im.thumbnail((512, 512))
        im.save(quote, "PNG" if file else "WEBP")
        quote.seek(0)
        await reply.reply(file=quote, force_document=file)
        await message.delete()
        
    @loader.unrestricted
    @loader.ratelimit
    async def qqsetcmd(self, message):
        args = utils.get_args(message)
        if len(args) != 2 or args[0].lower() not in ["color"]:
            await utils.answer(message, self.strings('settings', message))
            return
        key, value = args
        self.db.set("kzdQuotes", key, value)
        await message.edit(f"<b>Значение {args[0]} установлено</b>")
            
            


async def get_media_caption(reply):
    if reply and reply.media:
        if reply.photo:
            return kzdQuotesMod.strings["mediaType_photo"]
        if reply.text:
            return reply.raw_text
        dice = False
        try:
            dice = True if reply.dice else False
        except AttributeError:
            try:
                dice = True if type(reply.media) == telethon.tl.types.MessageMediaDice else False
            except AttributeError:
                pass
        if dice:
            dice_type = ""
            dice_text = reply.media.value
            if reply.media.emoticon == "🎲":
                dice_type = kzdQuotesMod.strings["diceType_dice"]
                return "{} {}: {}".format(reply.media.emoticon,
                                                      dice_type,
                                                      dice_text)
            elif reply.media.emoticon == "🎯":
               if dice_text == 1:
                   dice_text = kzdQuotesMod.strings["dart_missed"]
               elif dice_text == 5:
                   dice_text = kzdQuotesMod.strings["dart_almostthere"]
               elif dice_text == 6:
                   dice_text = kzdQuotesMod.strings["dart_bullseye"]
               else:
                    return "{} {}".format(reply.media.emoticon, kzdQuotesMod.strings["dart_thrown"])
               dice_type = kzdQuotesMod.strings["diceType_dart"]
               return "{} {}: {}".format(reply.media.emoticon, dice_type, dice_text)
            elif reply.media.emoticon == "🏀":
                return "{} {}".format(reply.media.emoticon, kzdQuotesMod.strings["ball_thrown"])
            else:
                 return "Unsupported dice type ({}): {}".format(reply.media.emoticon, reply.media.value)
        elif reply.poll:
            try:
                if reply.media.poll.quiz is True:
                    return kzdQuotesMod.strings["mediaType_quiz"]
            except Exception:
                pass
            return kzdQuotesMod.strings["mediaType_poll"]
        elif reply.geo:
             return kzdQuotesMod.strings["mediaType_location"]
        elif reply.document:
            if reply.gif :
                return kzdQuotesMod.strings["mediaType_gif"]
            elif reply.video:
                if reply.video.attributes[0].round_message:
                    return kzdQuotesMod.strings["mediaType_videomessage"]
                else:
                    return kzdQuotesMod.strings["mediaType_video"]
            elif reply.audio:
                return kzdQuotesMod.strings["mediaType_audio"]
            elif reply.voice:
                return kzdQuotesMod.strings["mediaType_voice"]
            elif reply.file:
                if reply.file.mime_type == "application/x-tgsticker":
                        emoji = ""
                        try:
                            emoji = reply.media.document.attributes[0].alt
                        except AttributeError:
                            try:
                                emoji = reply.media.document.attributes[1].alt
                            except AttributeError:
                                emoji = ""
                        caption = "{} {}".format(emoji, kzdQuotesMod.strings["mediaType_sticker"]) if emoji != "" else kzdQuotesMod.strings["mediaType_sticker"]
                        return caption
                else:
                    if reply.sticker:
                        emoji = ""
                        try:
                            emoji = reply.file.emoji
                            logger.debug(len(emoji))
                        except TypeError:
                            emoji = ""
                        caption = "{} {}".format(emoji, kzdQuotesMod.strings["mediaType_sticker"]) if emoji != "" else kzdQuotesMod.strings["mediaType_sticker"]
                        return caption
                    else:
                        return kzdQuotesMod.strings["mediaType_file"] + reply.file.name
        else:
            return ""
    else:
        return ""
   
    return ""

async def check_media(message, reply, x=None):
    if reply and reply.media:
        if reply.photo:
            data = reply.photo
        elif reply.document:
            if reply.gif or reply.video or reply.file.mime_type == "application/x-tgsticker":
                return await reply.download_media(bytes, thumb=-1) if x else None
            if reply.audio or reply.voice:
                return None
            data = reply.media.document
        else:
            return None
    else:
        return None
    if not data or data is None:
        return None
    else:
        return await message.client.download_file(data, bytes)


