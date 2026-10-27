#!/usr/bin/env python3
"""Verify local ownership export rejects denied/mismatched accounts and excludes secrets."""
import base64,contextlib,io,json,tempfile,subprocess
from pathlib import Path
from unittest.mock import patch
from export_offline_account import export
class Response:
 def __init__(self,data):self.data=data
 def __enter__(self):return io.StringIO(json.dumps(self.data))
 def __exit__(self,*args):pass
class Opener:
 def __init__(self,owns=True,matches=True):self.owns=owns;self.matches=matches;self.urls=[]
 def open(self,request,timeout):
  self.urls.append(request.full_url)
  assert request.get_header('Authorization')=='Bearer PRIVATE_TEST_TOKEN'
  if '/entitlements/' in request.full_url:return Response({'items':[{'name':'game_minecraft'}] if self.owns else []})
  return Response({'id':'1'*32 if self.matches else '2'*32,'name':'OwnedPlayer'})
with tempfile.TemporaryDirectory() as folder:
 w=Path(folder);accounts=w/'accounts.json';key=w/'private.pem';public=w/'public.der';out=w/'profile.json'
 accounts.write_text(json.dumps({'accounts':[{'active':True,'profile':{'id':'1'*32},'ygg':{'token':'PRIVATE_TEST_TOKEN','exp':4102444800},'msa':{'refresh_token':'PRIVATE_REFRESH_TOKEN'}}]}))
 for owns,matches in ((False,True),(True,False)):
  opener=Opener(owns,matches)
  with patch('export_offline_account.urllib.request.build_opener',return_value=opener):
   try:export(accounts,key,public,out);raise AssertionError('invalid account accepted')
   except ValueError:pass
  assert not out.exists() and not key.exists() and not public.exists()
 opener=Opener()
 with patch('export_offline_account.urllib.request.build_opener',return_value=opener),contextlib.redirect_stdout(io.StringIO()) as output:export(accounts,key,public,out)
 raw=out.read_text();payload=base64.b64decode(json.loads(raw)['payload']);assert b'TOKEN' not in payload and 'TOKEN' not in raw and 'TOKEN' not in output.getvalue()
 assert set(json.loads(payload))=={'schema','name','id','verifiedAt','expiresAt'}
 assert key.stat().st_mode&0o777==0o600 and out.stat().st_mode&0o777==0o600
 signature=base64.b64decode(json.loads(raw)['signature']);(w/'signature').write_bytes(signature);(w/'payload').write_bytes(payload)
 subprocess.run(['openssl','dgst','-sha256','-verify',str(public),'-keyform','DER','-signature',str(w/'signature'),str(w/'payload')],check=True,stdout=subprocess.DEVNULL)
 assert len(opener.urls)==2 and all(u.startswith('https://api.minecraftservices.com/') for u in opener.urls)
print('PASS export ownership denial/profile mismatch/secret exclusion/private permissions/RSA signature; no live credentials used')
