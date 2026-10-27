#!/usr/bin/env python3
"""Audit Temp_gametest channel, personal auth, module delta and preserved089."""
from pathlib import Path
import hashlib,io,json,subprocess,tempfile,zipfile
ROOT=Path(__file__).resolve().parents[1]
JDK=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
sha=lambda b:hashlib.sha256(b).hexdigest()
base=ROOT/'dist/candidates/ProsperoCraft-Offline-01.000.089/PPSA99874.zip'
package=ROOT/'dist/client-startup-temp_gametest/PPSA99874.zip'
assert sha(base.read_bytes())=='59aa7b29d228a4485ea8ccf21f9c066fd509e1072c186806e92cc34df159d623'
with zipfile.ZipFile(base)as old,zipfile.ZipFile(package)as new:
 assert new.testzip()is None
 prefix='PPSA99874/assets/java25/'
 with zipfile.ZipFile(io.BytesIO(new.read(prefix+'client-probe.jar')))as jar:
  assert jar.read('prosperocraft-channel.txt')==b'temp_gametest\n'
  assert 'offline-import-public-key.der'not in jar.namelist()
  assert b'00000000402b5328'in jar.read('ProsperoAuth.class')
  assert b'service::user.auth.xboxlive.com::MBI_SSL'in jar.read('ProsperoAuth.class')
  endpoint=jar.read('ProsperoAuth$Endpoint.class')
  for u in (b'https://login.live.com/oauth20_connect.srf',b'https://login.live.com/oauth20_token.srf',b'https://api.minecraftservices.com/entitlements/license',b'https://api.minecraftservices.com/minecraft/profile'):assert u in endpoint
  assert b'microsoftonline.com'not in endpoint
  assert b'TEMP GAMETEST'in jar.read('ProsperoChannel.class')
  assert b'PLAY FULL GAME'in jar.read('ProsperoLauncher.class')
  assert not any(b'SECRET_TEST_TOKEN'in jar.read(n)for n in jar.namelist())
 with tempfile.TemporaryDirectory(prefix='prospero-modules-delta-')as folder:
  w=Path(folder)
  for name,z in [('old',old),('new',new)]:
   image=w/(name+'.modules');image.write_bytes(z.read(prefix+'lib/modules'))
   subprocess.run([str(JDK/'bin/jimage'),'extract','--dir',str(w/name),str(image)],stdout=subprocess.DEVNULL,check=True)
  inventories=[]
  for name in ('old','new'):inventories.append({str(p.relative_to(w/name)):sha(p.read_bytes())for p in(w/name).rglob('*')if p.is_file()})
  assert set(inventories[0])==set(inventories[1])
  changed=[n for n,d in inventories[0].items()if inventories[1][n]!=d]
  bookkeeping={'java.base/_the.java.base_batch.modfiles','java.base/_the.java.base_batch.modfiles.fixed'}
  assert set(changed)-bookkeeping=={'java.base/sun/nio/fs/UnixFileSystem.class'},changed
  changed=['java.base/sun/nio/fs/UnixFileSystem.class']
  assert b'sun.nio.fs.ps5Sandbox'in(w/'new'/changed[0]).read_bytes()
print('PASS Temp_gametest090 auth/channel/ownership/profile endpoints, no Offline key or fixture token; module bytecode delta is UnixFileSystem only (generated javac bookkeeping excluded); Offline089 package unchanged')
