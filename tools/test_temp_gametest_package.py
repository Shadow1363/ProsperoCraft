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
for version,digest in {'093':'ed433c1c3e2567987e876357ae0cc2982e259655e92afc55d9f4a1640c1f1ee8','094':'4847dc4eaa43987c9473362076ef27aedf579854924d6de7d72c107f9567587b'}.items():assert sha((ROOT/('dist/candidates/ProsperoCraft-Temp_gametest-01.000.'+version+'/PPSA99874.zip')).read_bytes())==digest
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
  assert b'PLAY'in jar.read('ProsperoLauncher.class')
  assert b'--quickPlaySingleplayer'not in jar.read('ProsperoLauncher.class') and b'--quickPlayMultiplayer'not in jar.read('ProsperoLauncher.class')
  assert b'Home'not in jar.read('ProsperoLauncher.class')
  assert b'servers.dat'in jar.read('ProsperoDestinations.class') and b'level.dat'in jar.read('ProsperoDestinations.class')
  assert b'pending-delete'in jar.read('ProsperoLibrary.class')
  assert b'restore'not in jar.read('ProsperoLibrary.class')
  assert b'AES/GCM/NoPadding'in jar.read('ProsperoAccountStore.class')
  assert b'refresh_token'in jar.read('ProsperoAuth.class')
  assert b'textures.minecraft.net'in jar.read('ProsperoAvatar.class')
  assert b'PS5_NETWORK'in jar.read('ProsperoNetwork.class')
  assert not any(b'SECRET_TEST_TOKEN'in jar.read(n)for n in jar.namelist())
 assert b'-Djava.net.preferIPv4Stack=true'in new.read('PPSA99874/eboot.bin')
 assert b'-Dio.netty.transport.noNative=true'in new.read('PPSA99874/eboot.bin')
 assert b'-Dps5.net.traceBindFailures=true'in new.read('PPSA99874/eboot.bin')
 for name in ('instance_icons.hpp','login_qr.hpp'):
  assert new.read(prefix+'launcher-toolkit/'+name)==(ROOT/'client/launcher'/name).read_bytes()
 pin=json.loads((ROOT/'assets/launcher-icons/attribution.json').read_text())
 for name,digest in pin['sha256'].items():assert sha(new.read(prefix+'launcher-icons/'+name))==digest
 assert 'prismlauncher'in new.read(prefix+'launcher-icons/UPSTREAM-COPYING.md').decode().lower().replace('prism launcher','prismlauncher')
 assert not any('/account/session' in n or '/account/key' in n for n in new.namelist())
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
  assert set(changed)-bookkeeping=={'java.base/sun/nio/fs/UnixFileSystem.class','java.base/java/io/IOException.class'},changed
  assert b'PS5_HOST_IO'in(w/'new/java.base/java/io/IOException.class').read_bytes()
  changed=['java.base/sun/nio/fs/UnixFileSystem.class']
  assert b'sun.nio.fs.ps5Sandbox'in(w/'new'/changed[0]).read_bytes()
print('PASS Temp_gametest095 auth/channel/ownership/profile endpoints, no Offline key or fixture token; module bytecode delta is UnixFileSystem plus bounded IOException socket diagnosis (generated javac bookkeeping excluded); Offline089 package unchanged')
