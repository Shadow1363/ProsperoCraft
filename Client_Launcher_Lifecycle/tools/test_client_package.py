#!/usr/bin/env python3
"""Check the separate client foundation package, artifact pins and shared title identity."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);p.add_argument('--package',type=Path,help='Explicit client002 package, e.g. preserved milestone ZIP');args=p.parse_args();runtime=args.runtime_workspace.resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
package=args.package.resolve()if args.package else runtime/'dist/PPSA99874.zip';lock=json.loads((ROOT/'client/26.3.lock.json').read_text())
with zipfile.ZipFile(package)as z:
 assert z.testzip()is None
 prefix='PPSA99874/'
 param=json.loads(z.read(prefix+'sce_sys/param.json'));assert param['titleId']=='PPSA99874'and param['contentVersion']=='01.000.002'
 server_identity=json.loads((ROOT/'server/param.json').read_text())
 assert all(param[key]==server_identity[key]for key in ['titleId','conceptId','contentId'])
 assert not any(n.endswith('.pcm')or'/sounds/'in n for n in z.namelist())
 for row in lock['artifacts']:
  data=z.read(prefix+'assets/java25/client/jars/'+row['file']);assert len(data)==row['size']and sha(data)==row['sha256'],row['file']
 jars={n.rsplit('/',1)[-1]for n in z.namelist()if '/client/jars/'in n and n.endswith('.jar')};assert jars=={row['file']for row in lock['artifacts']}
 assert not any('/paper-plugins/'in n or '/fabric-mods/'in n or n.endswith('join-player.txt')for n in z.namelist())
 audit=json.loads(z.read(prefix+'assets/java25/dependency-port-audit.json'));assert audit['activated_for_probe']and not audit['activated_for_game']and not audit['game_jar_modified']
 port=z.read(prefix+'assets/java25/ports/lwjgl-3.4.3-ps5-platform.jar');assert sha(port)==audit['output_sha256']
 with zipfile.ZipFile(io.BytesIO(z.read(prefix+'assets/java25/client/jars/lwjgl-3.4.3.jar')))as original,zipfile.ZipFile(io.BytesIO(port))as patched:
  for name in original.namelist():
   if name not in audit['recompiled_classes']:assert original.read(name)==patched.read(name),name
  assert set(patched.namelist())==set(original.namelist())|set(audit['recompiled_classes'])|{'META-INF/PS5-PORT-LICENSE.txt'}
 assert z.read(prefix+'assets/java25/lib/modules')==(runtime/'build/java25/boot-image/lib/modules').read_bytes()
 for name,module in [('java','java.base'),('zip','java.base'),('jimage','java.base'),('net','java.base'),('nio','java.base'),('verify','java.base'),('management','java.management')]:
  assert z.read(prefix+'assets/java25/lib/lib'+name+'.so')==(runtime/'.tools/java25/openjdk/build/ps5-bootstrap/support/modules_libs'/module/('lib'+name+'.so')).read_bytes()
 assert z.read(prefix+'assets/java25/lib/server/libjvm.so')==(runtime/'.tools/java25/openjdk/build/ps5-bootstrap/support/modules_libs/java.base/server/libjvm.so').read_bytes()
 eboot=z.read(prefix+'eboot.bin')
 for marker in [b'Client LWJGL Core 01.000.002',b'-Xint',b'-Xmx128m',b'-XX:+UseCompactObjectHeaders',b'ClientInventory25',b'ClientPlatform25',b'ClientBridge25',b'()J',b'(Ljava/nio/ByteBuffer;J)J',b'PPSA99874',b'probe-session.txt',b'probe-exception.txt']:
  assert marker in eboot,marker
 assert b'-Djava.class.path=/app0/assets/java25/client-probe.jar:/app0/assets/java25/ports/lwjgl-3.4.3-ps5-platform.jar:'in eboot
 with zipfile.ZipFile(io.BytesIO(z.read(prefix+'assets/java25/client-probe.jar')))as probe:
  assert set(probe.namelist())=={'ClientArtifactProbe25.class','ClientInventory25.class','ClientPlatform25.class','ClientBridge25.class','ClientLibrary25.class','ClientLwjglCore25.class'}
 resident=json.loads(z.read(prefix+'assets/java25/resident-libraries-audit.json'))['external_resident_libraries']
 assert len(resident)==2 and [row['name']for row in resident]==['ps5clientbridge','lwjgl']
 assert resident[0]['objects_sha256']==[sha((ROOT/'build/client-probe/resident-library.o').read_bytes())]
 native=json.loads(z.read(prefix+'assets/java25/lwjgl-native-audit.json'))
 assert resident[1]['objects_sha256']==list(native['objects_sha256'].values())
 assert native['upstream_commit']=='30fac9b95f99cda97312232be25ba55297bf9951'
 assert native['compile_profile']=='x86-64/SSE2; AVX/AVX2/FMA disabled'
 disassembly=subprocess.check_output(['/opt/homebrew/opt/llvm/bin/llvm-objdump','-d',str(runtime/'build/java25/embedded-lwjgl.o')],text=True)
 assert '%ymm' not in disassembly and '%zmm' not in disassembly and 'vzeroupper' not in disassembly
 assert 'cpuid' in disassembly

 symbols=subprocess.check_output(['/opt/homebrew/opt/llvm/bin/llvm-nm','--defined-only',str(runtime/'build/native/llvm-pie.elf')],text=True)
 for symbol in ['ps5_builtin_load_ps5clientbridge','ps5_ps5clientbridge_JNI_OnLoad','Java_ClientLibrary25_loadCount','Java_ClientLibrary25_resolvedChecksum','ps5_client_checksum']:
  assert any(line.endswith(' '+symbol)for line in symbols.splitlines()),symbol
 assert b'--enable-native-access=ALL-UNNAMED'in eboot
 assert b'--add-exports=java.base/jdk.internal.misc=ALL-UNNAMED'in eboot
 for symbol in ['ps5_builtin_load_lwjgl','ps5_lwjgl_JNI_OnLoad','Java_org_lwjgl_system_MemoryUtil_ngetPageSize','Java_org_lwjgl_system_ps5_PS5Library_nOpen','ps5_lwjgl_pointer_size']:
  assert any(line.endswith(' '+symbol)for line in symbols.splitlines()),symbol
 with zipfile.ZipFile(io.BytesIO(z.read(prefix+'assets/java25/client-probe.jar')))as probe:
  assert b'ps5clientbridge'in probe.read('ClientLibrary25.class') and b'loadLibrary'in probe.read('ClientLibrary25.class')
 assert not any(n.endswith('server-26.3.jar')or n.endswith('paper-26.3.jar')for n in z.namelist())
assert package.read_bytes()==(ROOT/'dist/client/PPSA99874.zip').read_bytes()
assert (runtime/'build/native/llvm-pie.elf').read_bytes()==(ROOT/'build/client-probe/bootstrap-01.000.002-symbols.elf').read_bytes()
assert sha((runtime/'build/java25/PPSA99874-108-full-local.zip').read_bytes())=='18dc7f06d59ff11b33c7e96b85f813a28a2cb19638fe0d6eacfd4224513781e7'
assert sha((runtime/'build/java25/PPSA99874-094-full-local.zip').read_bytes())=='97ec74c40b9c495884130f9dae0ab10bf393e521265cbe82177f06190176df2d'
assert (runtime/'build/java25/package-client-002.log').read_text().count('integrity: valid')==2
print('PASS Client LWJGLCore002 package CRC/signatures/title74,54immutable upstream artifacts/exact dependency port/current runtime/symbols/copies/options/silence; Fabric094/Paper108 unchanged. No game launch, GPU or console pass. SHA256',sha(package.read_bytes()))

frozen=ROOT/'dist/milestones/Client_Foundation-01.000.000/PPSA99874-full-local.zip'
assert sha(frozen.read_bytes())=='e2eb90a727fc670418437937b292b152c5177e3e02077aa114049bc6c9c11fbf'
with zipfile.ZipFile(frozen)as old,zipfile.ZipFile(package)as now:
 for name in old.namelist():
  if '/assets/java25/client/'in name or name.endswith('.so')or name.endswith('/lib/modules'):assert old.read(name)==now.read(name),name
print('PASS current resident JNI discovery/exports/audit and exact frozen000 original client/moduleimage/native-library bytes; updated source-built dependency port; frozen full-package SHA retained')

assert sha((ROOT/'dist/milestones/Client_Native_Loading-01.000.001/PPSA99874-full-local.zip').read_bytes())=='abc6aef0f162d9d134dec298742f27dfdb91a80345bb81ac54498239d34fd890'
print('PASS frozen001 retained; current native LWJGL core/discovery/provider exports and object-hash inventory linked')
