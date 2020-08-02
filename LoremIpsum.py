from .. import loader, utils
import io
from requests import get

def register(cb):
	cb(LoremIpsumMod())


class LoremIpsumMod(loader.Module):
	"""Lorem Ipsum generation"""

	strings = {'name': 'LoermIpsum'}

	def __init__(self):
		self.name = self.strings['name']
		
	async def loremipsumcmd(self, message):
		""".loremipsum <count: int> <length: str> <file?>
count - number of paragraphs| std: 1
length - s-short, m-medium, l-long, v-verylong|std: m(edium)
file - if nothing- send as message, if anything- send as file"""
		s = 'small'
		m = length = 'medium'
		l = 'long'
		v = 'verylong'
		args = utils.get_args(message)
		count = 1
		as_file = False
		if args:
			count = int(args[0]) if args[0].isdigit() else 1
			if len(args) == 2:
				lenght = args[1].lower()
				length = s if lenght in [s[:i+1] for i in range(len(s))] else l if lenght in [l[:i+1] for i in range(len(l))] else v if lenght in [v[:i+1] for i in range(len(v))] else m # сижу ахуел
			if len(args) >= 3:
				as_file = True
		url = f"https://loripsum.net/api/{count}/{length}/plaintext"
		out = get(url)
		if as_file:
			out = io.BytesIO(out.content)
			out.name = f"LoremIpsum.{count}.txt"
			out.seek(0)
		else: out = out.text
		await utils.answer(message, out)
		