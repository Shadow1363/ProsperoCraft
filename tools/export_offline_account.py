#!/usr/bin/env python3
"""Verify the active local Prism account and export a signed seven-day offline profile.
Only name/UUID/timestamps leave this process. Never export login/refresh tokens.
The signing key stays local; the matching public key must be packaged in the app.
"""
import argparse, base64, json, os, subprocess, tempfile, time, urllib.request, urllib.error, uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def verify(accounts):
    data=json.loads(accounts.read_text())
    active=[a for a in data.get('accounts',[]) if a.get('active')]
    if len(active)!=1: raise ValueError('Exactly one active Prism account is required')
    account=active[0]; session=account.get('ygg',{})
    if not isinstance(session.get('token'),str) or session.get('exp',0)<=time.time()+60:
        raise ValueError('Open Prism and sign in again; its Minecraft session has expired')
    def get(path):
        request=urllib.request.Request('https://api.minecraftservices.com/'+path,headers={'Authorization':'Bearer '+session['token'],'User-Agent':'ProsperoCraft-offline-import'})
        # No redirects: never forward the bearer credential to a different endpoint.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*args): return None
        with urllib.request.build_opener(NoRedirect).open(request,timeout=25) as response:
            return json.load(response)
    license=get('entitlements/license?requestId='+str(uuid.uuid4()))
    if not any(i.get('name') in ('game_minecraft','product_minecraft') for i in license.get('items',[])):
        raise ValueError('Minecraft Services did not confirm Java ownership')
    profile=get('minecraft/profile')
    import re
    if profile.get('id')!=account.get('profile',{}).get('id') or not re.fullmatch('[a-fA-F0-9]{32}',profile.get('id','')) or not re.fullmatch('[A-Za-z0-9_]{1,16}',profile.get('name','')):
        raise ValueError('Minecraft profile does not match the local account')
    now=int(time.time()*1000)
    return dict(schema=1,name=profile['name'],id=profile['id'],verifiedAt=now,expiresAt=now+7*24*60*60*1000)

def export(accounts,key,public,output):
    profile=verify(accounts) # No key/output changes until genuine ownership/profile checks pass.
    key.parent.mkdir(parents=True,exist_ok=True)
    if not key.exists():
        subprocess.run(['openssl','genpkey','-algorithm','RSA','-pkeyopt','rsa_keygen_bits:2048','-out',str(key)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    os.chmod(key,0o600)
    pub=subprocess.run(['openssl','pkey','-in',str(key),'-pubout','-outform','DER'],check=True,capture_output=True).stdout
    if public.exists() and public.read_bytes()!=pub: raise ValueError('Signing key does not match the packaged public key; refusing to replace it')
    public.parent.mkdir(parents=True,exist_ok=True);public.write_bytes(pub)
    payload=json.dumps(profile,separators=(',',':'),sort_keys=True).encode()
    signature=subprocess.run(['openssl','dgst','-sha256','-sign',str(key)],input=payload,check=True,capture_output=True).stdout
    output.parent.mkdir(parents=True,exist_ok=True)
    envelope=dict(payload=base64.b64encode(payload).decode(),signature=base64.b64encode(signature).decode())
    # Restrict access even though the exported record has no credentials.
    fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_TRUNC,0o600)
    with os.fdopen(fd,'w') as stream:json.dump(envelope,stream,separators=(',',':'))
    print('PASS Java ownership and matching profile verified; signed offline record exported. No tokens exported.')

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--accounts',type=Path,default=Path.home()/'Library/Application Support/PrismLauncher/accounts.json')
    p.add_argument('--signing-key',type=Path,default=ROOT/'.tools/offline-account/signing-key.pem')
    p.add_argument('--public-key',type=Path,default=ROOT/'client/launcher/offline-import-public-key.der')
    p.add_argument('--output',type=Path,default=ROOT/'build/offline-account/offline-account.json')
    a=p.parse_args()
    try:export(a.accounts,a.signing_key,a.public_key,a.output)
    except Exception as e:
        # Never print response bodies, tokens, account contents or exception request details.
        print('Offline export failed:',('Minecraft Services HTTP '+str(e.code)) if isinstance(e,urllib.error.HTTPError) else str(e) if isinstance(e,ValueError) else type(e).__name__)
        raise SystemExit(1)
