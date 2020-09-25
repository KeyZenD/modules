from ..  import loader,utils
from PIL import Image,ImageFilter
import io
class aMod(loader.Module):
 strings={'name':'MacAshoT'}
 async def maccmd(S,message):
  R=True;Q='image';P='/';M='RGBA';L='<b>Image?</b>';B=message;C=await B.get_reply_message();A=io.BytesIO();J=None
  if B.file:
   if B.file.mime_type.split(P)[0]==Q:await B.download_media(A)
   elif C:
    if C.file:
     if C.file.mime_type.split(P)[0]==Q:J=R;await C.download_media(A)
    else:await B.edit(L);return
   else:await B.edit(L);return
  elif C:
   if C.file:
    if C.file.mime_type.split(P)[0]==Q:J=R;await C.download_media(A)
   else:await B.edit(L);return
  else:await B.edit(L);return
  K=Image.open(A).convert(M);F,G=K.size;A=Image.new(M,(F,G));A.paste(K,(0,0),K);H=min(F//100,G//100);D=Image.new(M,(F+H*40,G+H*40),'#fff');E=Image.new(M,(F,G))
  for N in range(F):
   for O in range(G):
    if A.getpixel((N,O))!=(0,0,0,0):E.putpixel((N,O),(0,0,0))
  E=E.resize((F+H*5,G+H+5));D.paste(E,((D.width-E.width)//2,(D.height-E.height)//2),E);D=D.filter(ImageFilter.GaussianBlur(H*5));D.paste(A,((D.width-A.width)//2,(D.height-A.height)//2),A);I=io.BytesIO();I.name='macos.png';D.save(I,'PNG');I.seek(0)
  if J:await C.reply(file=I);await B.delete()
  else:await B.edit(file=I,text='')