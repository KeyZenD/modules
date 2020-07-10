from .. import loader, utils
from hashlib import md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s

def register(cb):
	cb(HasherMod())
	
class HasherMod(loader.Module):
	"""Hashing text and files"""
	strings = {'name': 'Hasher'}
	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []
	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()
	
	async def md5cmd(self, message):
		""".md5 <(text or media) or (reply to text or media)>\nHashing to md5"""
		await hashing(message, 0)
	async def sha1cmd(self, message):
		""".sha1 <(text or media) or (reply to text or media)\nHashing to sha1"""
		await hashing(message, 1)
	async def sha224cmd(self, message):
		""".sha224 <(text or media) or (reply to text or media)\nHashing to sha224"""
		await hashing(message, 2)
	async def sha256cmd(self, message):
		""".sha255 <(text or media) or (reply to text or media)\nHashing to sha256"""
		await hashing(message, 3)
	async def sha384cmd(self, message):
		""".sha384 <(text or media) or (reply to text or media)\nHashing to sha384"""
		await hashing(message, 4)
	async def sha512cmd(self, message):
		""".sha512 <(text or media) or (reply to text or media)\nHashing to sha512"""
		await hashing(message, 5)
	async def blake2bcmd(self, message):
		""".blake2 <(text or media) or (reply to text or media)\nHashing to blake2"""
		await hashing(message, 6)
	async def blake2scmd(self, message):
		""".blake2s <(text or media) or (reply to text or media)\nHashing to blake2s"""
		await hashing(message, 7)
	
async def hashing(m, type):
	types = [md5, sha1, sha224, sha256, sha384, sha512, blake2b, blake2s]
	typez = ["md5", "sha1", "sha224", "sha256", "sha384", "sha512", "blake2b", "blake2s"]
	
	reply = await m.get_reply_message()
	mtext = utils.get_args_raw(m)
	if m.media:
		await m.edit("<b>D o w n l o a d i n g . . .</b>")
		data = await m.client.download_file(m, bytes)
	elif mtext:
		data = mtext.encode()
	elif reply:
		if reply.media:
			await m.edit("<b>D o w n l o a d i n g . . .</b>")
			data = await m.client.download_file(reply, bytes)
		else:
			data = reply.raw_text.encode()
	else:
		await m.edit(f"<b>What hashing to {typez[type]}?</b>")
		return
			
	await m.edit("<b>H a s h i n g . . .</b>")
	try:
		result = types[type](data) 
		await m.edit(typez[type].upper()+": <code>" + str(result.hexdigest()).upper()+"</code>")
	except:
		await m.edit("<b>ERЯOR!</b>")
