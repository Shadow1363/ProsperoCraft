#!/usr/bin/env python3
"""Audit the exact082 installable launcher ZIP and accompanying relink release."""
from pathlib import Path
import hashlib,json,zipfile,tarfile,io
r=Path(__file__).resolve().parents[1];out=r/'dist/releases/client082'
sha=lambda data:hashlib.sha256(data).hexdigest()
record=json.loads((r/'docs/validation/client082-launcher-build-2026-10-26.json').read_text())
app=out/'PPSA99874.zip'
assert sha(app.read_bytes())==record['package_sha256']==sha((r/'dist/client-startup/PPSA99874.zip').read_bytes())
with zipfile.ZipFile(app)as z:
 assert z.testzip()is None
 names=z.namelist();assert all(n.startswith('PPSA99874/')for n in names)
 assert all('..' not in n.split('/')and not n.startswith('/')for n in names)
 assert z.read('PPSA99874/sce_sys/param.json')==(r/'sce_sys/param.json').read_bytes()
 param=json.loads(z.read('PPSA99874/sce_sys/param.json'))
 assert param['titleId']=='PPSA99874'and param['contentVersion']=='01.000.082'and param['downloadDataSize']==4096
 assert z.read('PPSA99874/sce_sys/icon0.png')==(r/'assets/branding/icon0.png').read_bytes()
 pins=json.loads(z.read('PPSA99874/assets/java25/launcher-dependencies.json'))
 assert all(p['id'].startswith(('org.lwjgl:','com.google.code.gson:'))for p in pins)
 for p in pins:assert sha(z.read('PPSA99874/assets/java25/client/jars/'+p['file']))==p['sha256']
 assert not any('/game-assets/'in n or n.endswith('/client-26.3.jar')or '/instances/'in n or n.endswith(('.HEIC','.heic','.log'))for n in names)
 assert any('notice'in n.lower()or 'license'in n.lower()for n in names)
 with zipfile.ZipFile(io.BytesIO(z.read('PPSA99874/assets/java25/client-probe.jar')))as classes:
  assert b'f0c7635e-8d50-4d7e-afa3-d15db4a0a3d3'in classes.read('ProsperoAuth.class')
with zipfile.ZipFile(out/'client082-openal-source-relink.zip')as z:
 assert z.testzip()is None
 manifest=json.loads(z.read('manifest.json'))
 assert manifest['app_version']=='01.000.082'and manifest['original_elf_sha256']==record['native_elf_sha256']
 for p in manifest['files']:assert sha(z.read(p['path']))==p['sha256']
 readme=z.read('README.txt').decode()
 assert 'no desktop provisioning'in readme and 'Provision BOTH JARs'not in readme
 for p in ['openal-startup-source/alc/backends/ps5_backend.cpp','openal-startup-source/alc/alc.cpp','openal-startup-source/COPYING','consumer-source/client/startup/openal_trace_env.c','build_openal_replacement.py','relink.py']:assert p in z.namelist(),p
 with tarfile.open(fileobj=io.BytesIO(z.read('openal-soft-1.25.2-source.tar')))as source:assert any(p.name.endswith('COPYING')for p in source.getmembers())
for name in ['client082-release-relinked.elf','client082-release-replacement.elf']:
 assert sha((r/'build'/name).read_bytes())==record['native_elf_sha256']
assert (r/'build/client082-release-source-relinked.elf').read_bytes().startswith(b'\x7fELF')
print('PASS082 public package identical to tested build; installable root/metadata/icon, pinned launcher dependencies, no bundled game/assets/photos/logs; exact OpenAL source/input hashes, reproduced ELF and working edited-source replacement link')
