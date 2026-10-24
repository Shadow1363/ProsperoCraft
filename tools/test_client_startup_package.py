#!/usr/bin/env python3
"""Verify actual original-client startup package and all publisher asset objects."""
from pathlib import Path
import argparse,json,zipfile,hashlib,subprocess,struct
ROOT=Path(__file__).resolve().parents[1];LLVM=Path('/opt/homebrew/opt/llvm/bin')
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args();runtime=a.runtime_workspace
work=ROOT/'build/client-startup-probe';package=ROOT/'dist/client-startup/PPSA99874.zip';sha=lambda data:hashlib.sha256(data).hexdigest()
elf=work/'bootstrap-01.000.027-symbols.elf';text=subprocess.check_output([str(LLVM/'llvm-nm'),'--defined-only',str(elf)],text=True);symbols={l.split()[-1]:int(l.split()[0],16)for l in text.splitlines()if len(l.split())==3}
assert symbols['__init_array_start']==symbols['__init_array_end'];assert (symbols['__client_openal_init_end']-symbols['__client_openal_init_start'])//8==15;assert (symbols['__jvm_init_array_end']-symbols['__jvm_init_array_start'])//8==359;assert (symbols['__client_gpu_init_end']-symbols['__client_gpu_init_start'])//8==4;assert (symbols['__client_shaderc_init_end']-symbols['__client_shaderc_init_start'])//8==5
for name in ['ffi_prep_closure_loc','ffi_call_plan_alloc','alcLoopbackOpenDeviceSOFT','alcRenderSamplesSOFT','ps5_builtin_load_ps5openal','JNI_CreateJavaVM','ps5_builtin_load_ps5sdl','ps5_builtin_load_ps5shaderc','ps5_builtin_load_ps5clientgpu','radv_CreateInstance']:assert symbols.get(name),name
with zipfile.ZipFile(package)as z,zipfile.ZipFile(ROOT/'dist/milestones/Client_Continuous_Direct_Scene-01.000.023/PPSA99874-full-local.zip')as baseline:
 assert z.testzip()is None;prefix='PPSA99874/';param=json.loads(z.read(prefix+'sce_sys/param.json'));old=json.loads(baseline.read(prefix+'sce_sys/param.json'));assert param['contentVersion']=='01.000.027'
 for k in ['titleId','contentId','conceptId']:assert param[k]==old[k]
 assert b'-Xmx128m'in z.read(prefix+'eboot.bin') and b'Minecraft Original Client Startup 01.000.027'in z.read(prefix+'eboot.bin')
 assert b'net.minecraft.client.main.Main'in z.read(prefix+'assets/java25/classes/ClientStartup25.class')
 fixture=z.read(prefix+'assets/java25/classes/ClientStartup25.class');assert b'java/lang/reflect/Method'in fixture and b'launchArguments'in fixture and b'--demo'in fixture and b'--disableMultiplayer'in fixture
 assert b'no automatic menu PASS'in z.read(prefix+'eboot.bin')
 bootstrap=(ROOT/'client/startup/bootstrap.cpp').read_text();assert 'test_count=4'in bootstrap and 'int i=step;'in bootstrap and 'ClientContinuousSDL25'not in bootstrap
 assert not any(n.endswith(('.pcm','.at9'))for n in z.namelist())
 lock=json.loads((ROOT/'client/26.3.lock.json').read_text())
 for row in lock['artifacts']:assert sha(z.read(prefix+'assets/java25/client/jars/'+row['file']))==row['sha256'],row['file']
 for name in baseline.namelist():
  if name.endswith('/lib/modules')or name.endswith('.so'):assert z.read(name)==baseline.read(name),name
 asset_root=prefix+'assets/java25/game-assets/';data=z.read(asset_root+'indexes/34.json');pin=lock['asset_index']
 assert hashlib.sha1(data).hexdigest()==pin['sha1'] and len(data)==pin['size'];index=json.loads(data);objects={v['hash']:v['size']for v in index['objects'].values()}
 for digest,size in objects.items():
  data=z.read(asset_root+'objects/'+digest[:2]+'/'+digest);assert len(data)==size and hashlib.sha1(data).hexdigest()==digest,digest
 assert len(objects)==5147
 assert z.read(prefix+'assets/java25/log4j2-startup.xml')==(ROOT/'client/startup/log4j2-startup.xml').read_bytes()
 groups=json.loads(z.read(prefix+'assets/java25/resident-libraries-audit.json'))['external_resident_libraries'];assert [g['name']for g in groups]==['ps5clientgpu','ps5clientbridge','lwjgl','ps5sdl','ps5shaderc','ps5openal','ps5nativeprobe']
 cpp=json.loads(z.read(prefix+'assets/java25/cpp-allocation-audit.json'));assert cpp['scoped_object_sha256']==sha((work/'cpp_runtime.o').read_bytes())
 audit=json.loads(z.read(prefix+'assets/java25/dependency-port-audit.json'));assert audit['activated_for_game']is True
for file in ['eboot.bin','sce_module/libc.prx']:
 report=subprocess.check_output([str(runtime/'build/native/host/ps5-native-tool'),'self','--inspect','--file',str(work/'PPSA99874'/file)],text=True);assert 'integrity: valid'in report
assert package.read_bytes()==(runtime/'dist/PPSA99874.zip').read_bytes()
for folder,digest in [('Client_Continuous_Direct_Scene-01.000.023','846cd9adea6f9e6b04f80df461424c26b1fec6aa080ed641c35e7cfb16488ea4'),('Client_Visible_Perspective_Scene-01.000.022','9d49135a4dcbd66e93ef496e442c7845964e08aa6664c9dc26546a94196e450e')]:assert sha((ROOT/'dist/milestones'/folder/'PPSA99874-full-local.zip').read_bytes())==digest
with zipfile.ZipFile(package)as z:
 assert z.read('PPSA99874/assets/java25/ports/lwjgl-3.4.3-ps5-modules.jar')==(ROOT/'build/client-ports/lwjgl-modules/lwjgl-3.4.3-ps5-modules.jar').read_bytes()
 assert b'ps5openal'in z.read('PPSA99874/assets/java25/classes/ClientStartup25.class')
 assert sha((ROOT/'dist/milestones/Client_Callbacks_OpenAL-01.000.026/PPSA99874-full-local.zip').read_bytes())=='e158f9fd76ce91f16091b6e9ee2c54a4cbaf11863f08bf77853204b6ef984d82'
print('PASS027 actual package/CRC/signatures,all54 original JARs/all5147 original asset SHA1s,exact023 runtime image/native libs,359+4+5+15staged constructors/7real resident groups/actual026 libffi+OpenAL+module overlay/paired C++ allocator/actual Main invocation bytecode/workdir/log config and preserved022/023 packages. PS5 original startup/menu remains pending. SHA256',sha(package.read_bytes()))
