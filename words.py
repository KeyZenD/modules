from .. import loader
import io

class WordsMod(loader.Module):
    strings = {"name": "Words Counter"}
    
    async def wordscmd(self, message):
        reply = await message.get_reply_message()
        object = reply.sender_id if reply else message.sender_id
        chat = message.to_id
        
        await message.edit("<b>Сбор статистики...</b>")
        
        _words = {}
        
        async for msg in message.client.iter_messages(chat, from_user=object):
            if msg and msg.raw_text:
                words = set("".join(map(lambda x: x if (x in [" "] or x.isalpha()) else " ", msg.raw_text)).lower().split())
                for word in words:
                    count = msg.raw_text.lower().count(word)
                    _words[word] = _words.get(word, 0) + count
        all = list(_words.items())
        all.sort(key=lambda i: i[1])
        response = ""
        for word in all[::-1]:
            response += f"{word[0]}: {word[1]}\n"
        file = io.BytesIO(bytes(response, "utf-8"))
        file.name = f"ID:{object}.txt"
        await message.reply(file=file)
        await message.delete()
