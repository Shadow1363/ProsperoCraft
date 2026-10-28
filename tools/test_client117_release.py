#!/usr/bin/env python3
"""Audit the unchanged117 release and actual native relink results."""
from pathlib import Path
import json,hashlib,zipfile,io
r=Path(__file__).resolve().parents[1];out=r/'dist/releases/client117';candidate=r/'dist/candidates/ProsperoCraft-01.000.117'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=json.loads((r/'docs/validation/client117-build-validation.json').read_text())['package_sha256']
assert sha(candidate/'PPSA99874.zip')==sha(out/'PPSA99874.zip')==expected
with zipfile.ZipFile(out/'PPSA99874.zip')as z:
 assert z.testzip() is None
 names=z.namelist();assert len(names)==len(set(names))
 assert all(n.startswith('PPSA99874/')and '..'not in n.split('/')for n in names)
 assert z.read('PPSA99874/sce_sys/param.json')==(r/'sce_sys/param.json').read_bytes()
 p=json.loads(z.read('PPSA99874/sce_sys/param.json'));assert p['contentVersion']=='01.000.117'and p['titleId']=='PPSA99874'and p['downloadDataSize']==4096 and p['attribute3']&64
 assert not any('/instances/'in n or '/account/'in n or '/game-assets/objects/'in n or n.endswith(('client-26.3.jar','.log','.DS_Store'))for n in names)
 pins=json.loads(z.read('PPSA99874/assets/java25/launcher-dependencies.json'))
 for pin in pins:
  assert pin['id'].startswith(('org.lwjgl:','com.google.code.gson:'))
  assert hashlib.sha256(z.read('PPSA99874/assets/java25/client/jars/'+pin['file'])).hexdigest()==pin['sha256']
 for n in ['pic0.dds','pic1.dds']:assert z.read('PPSA99874/sce_sys/'+n)==(r/'assets/branding/prosperocraft-banner.dds').read_bytes()
 with zipfile.ZipFile(io.BytesIO(z.read('PPSA99874/assets/java25/client-probe.jar')))as j:
  assert j.read('prosperocraft-channel.txt')==b'temp_gametest\n'
  assert not any('private-key'in n or 'session.json'in n for n in j.namelist())
 assert z.read('PPSA99874/licenses/ProsperoCraft-NOTICE.txt')==(r/'NOTICE').read_bytes()
 assert any('GPL'in n for n in names)
with zipfile.ZipFile(out/'client117-openal-source-relink.zip')as z:
 assert z.testzip()is None
 m=json.loads(z.read('manifest.json'));assert m['app_version']=='01.000.117'
 for row in m['files']:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
 assert any('gfx_vk_vk_renderer.cpp.o'in row['path']for row in m['files'])
 for name in ['client117-release-relinked.elf','client117-release-replacement.elf']:
  assert sha(r/'build'/name)==m['original_elf_sha256']==sha(candidate/'bootstrap-symbols.elf')
 for name in ['openal-startup-source/alc/backends/ps5_backend.cpp','openal-startup-source/COPYING','build_openal_replacement.py','relink.py']:assert name in z.namelist()
print('PASS unchanged117 release, identity/CRC/banner/dependency/channel/privacy/notices and exact normal/replacement OpenAL native relinks with toolkit inputs')
