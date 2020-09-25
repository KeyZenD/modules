from ..  import loader,utils
from PIL import Image,ImageFilter
import io,random,string
class aMod(loader.Module):
	strings={'name':'MacAshoT'}
	async def maccmd(S,message):
		R=True;Q='image';P='/';M='RGBA';J='<b>Image?</b>';A=message;C=await A.get_reply_message();B=io.BytesIO();K=None
		if A.file:
			if A.file.mime_type.split(P)[0]==Q:await A.download_media(B)
			elif C:
				if C.file:
					if C.file.mime_type.split(P)[0]==Q:K=R;await C.download_media(B)
				else:await A.edit(J);return
			else:await A.edit(J);return
		elif C:
			if C.file:
				if C.file.mime_type.split(P)[0]==Q:K=R;await C.download_media(B)
			else:await A.edit(J);return
		else:await A.edit(J);return
		try:L=Image.open(B).convert(M)
		except:await A.edit(J);return
		await A.edit('<b>Working...</b>');F,G=L.size;B=Image.new(M,(F,G));B.paste(L,(0,0),L);I=min(F//100,G//100);D=Image.new(M,(F+I*40,G+I*40),'#fff');E=Image.new(M,(F,G))
		for N in range(F):
			for O in range(G):
				if B.getpixel((N,O))!=(0,0,0,0):E.putpixel((N,O),(0,0,0))
		E=E.resize((F+I*5,G+I+5));D.paste(E,((D.width-E.width)//2,(D.height-E.height)//2),E);D=D.filter(ImageFilter.GaussianBlur(I*5));D.paste(B,((D.width-B.width)//2,(D.height-B.height)//2),B);H=io.BytesIO();H.name='-'.join([''.join([random.choice(string.hexdigits)for B in range(A)])for A in[5,4,3,2,1]])+'.png';D.save(H,'PNG');H.seek(0)
		if utils.get_args_raw(A):await A.client.send_file(A.to_id,H,force_document=R);await A.delete()
		elif K:await C.reply(file=H);await A.delete()
		else:await A.edit(file=H,text='')
