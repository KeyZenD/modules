from requests import head,get
from urllib.parse import urlsplit as E,parse_qs as H
import json,io,re
from ..  import loader as A,utils
class TikTokDlMod(A.Module):
	strings={'name':'TikTokDl'}
	async def ttcmd(J,message):
		A=message;B=await A.get_reply_message();F=utils.get_args_raw(A);C=lambda x:f"<b>{x}</b>"
		if F:D=F
		elif B and B.raw_text:D=B.raw_text
		else:return await A.edit(C('No url.'))
		if'.tiktok.com'not in D:return await A.edit(C('Bad url.'))
		await A.edit(C('Loading...'));G,K=await I(D)
		try:await A.client.send_file(A.to_id,file=G,reply_to=B);await A.delete()
		except:
			try:await A.edit(C('DownLoading...'));H=get(G).content;E=io.BytesIO(H);E.name='video.mp4';E.seek(0);await A.client.send_file(A.to_id,file=E,reply_to=B);await A.delete()
			except:await A.edit(C('я чёт нихуя не могу загрузить...'))
async def I(url):
	A=url
	async def F(video_id,_):
		A=f"https://api-va.tiktokv.com/aweme/v1/multi/aweme/detail/?aweme_ids=%5B{video_id}%5D";A=get(A);B=A.json().get('aweme_details')
		if not B:return 0,0,A
		return B,True,A
	A=head(A).headers;A=A.get('Location')
	try:
		I=H(E(A).query);B=I.get('share_item_id')[0];G,C,D=await F(B,1)
		if not C:raise
	except:
		B=''.join(re.findall('[0-9]',E(A).path.split('/')[-1]));G,C,D=await F(B,2)
		if not C:return False,D
	return G[0]['video']['bit_rate'][0]['play_addr']['url_list'][-1],D
