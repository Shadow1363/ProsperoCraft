#!/usr/bin/env python3
"""Inspect actual Vulkan007 ELF/package, constructor ownership and dependency scoping."""
import argparse,hashlib,json,struct,subprocess,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];LLVM=Path('/opt/homebrew/opt/llvm/bin')
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args();runtime=a.runtime_workspace.resolve()
work=ROOT/'build/client-vulkan-probe';package=ROOT/'dist/client-vulkan/PPSA99874.zip';sha=lambda b:hashlib.sha256(b).hexdigest()
elf=work/'bootstrap-01.000.007-symbols.elf';raw=elf.read_bytes()
text=subprocess.check_output([str(LLVM/'llvm-nm'),'--defined-only',str(elf)],text=True)
symbols={line.split()[-1]:int(line.split()[0],16)for line in text.splitlines()if len(line.split())==3}
for name in ['JNI_CreateJavaVM','JNI_GetCreatedJavaVMs','Java_java_lang_System_registerNatives','ps5_builtin_load_lwjgl','ps5_builtin_load_ps5clientgpu','ps5_ps5clientgpu_JNI_OnLoad','Java_ClientGpu25_open','Java_ClientGpu25_transfer','Java_ClientGpu25_close','vkGetInstanceProcAddr','vk_icdGetInstanceProcAddr','radv_CreateDevice','radv_DestroyDevice','radv_CmdFillBuffer','__dlopen']:
 assert symbols.get(name),name
assert symbols['__init_array_start']==symbols['__init_array_end']
assert (symbols['__client_gpu_init_end']-symbols['__client_gpu_init_start'])//8==4
assert (symbols['__jvm_init_array_end']-symbols['__jvm_init_array_start'])//8==359
# Read the actual GPU initializer array from the linked ELF; priority90 must be
# compiler-rt CPU detection, before the three normal-priority Mesa initializers.
shoff=struct.unpack_from('<Q',raw,40)[0];entsize,count=struct.unpack_from('<HH',raw,58)
for i in range(count):
 section=struct.unpack_from('<IIQQQQIIQQ',raw,shoff+i*entsize)
 address,offset,size=section[3:6]
 if address<=symbols['__client_gpu_init_start']<address+size:
  start=offset+symbols['__client_gpu_init_start']-address;values=struct.unpack_from('<4Q',raw,start);break
else:raise AssertionError('GPU constructor array missing')
# PIE pointer slots carry RELA addends until the native loader relocates them.
relocations={}
for i in range(count):
 section=struct.unpack_from('<IIQQQQIIQQ',raw,shoff+i*entsize)
 if section[1]==4:
  for pos in range(section[4],section[4]+section[5],24):
   target,info,addend=struct.unpack_from('<QQq',raw,pos)
   if info&0xffffffff==8:relocations[target]=addend
values=tuple(relocations.get(symbols['__client_gpu_init_start']+i*8,v)for i,v in enumerate(values))
assert values[0]==symbols['__cpu_indicator_init'],values
assert all(values)
assert symbols['__cxa_thread_atexit_impl']==symbols['clientgpu_ps5___cxa_thread_atexit_impl']
for name in ['malloc','calloc','realloc','free','pthread_create','pthread_join']:
 assert symbols['__wrap_'+name]!=symbols['clientgpu___wrap_'+name]
for name in ['deflate','inflate','crc32','zcalloc','zcfree']:
 assert symbols[name]!=symbols['clientgpu_zlib_'+name]
response=[json.loads(line)for line in (work/'combined-link.rsp').read_text().splitlines()]
assert not any(p.startswith('--defsym=getaddrinfo=')or p.startswith('--defsym=malloc=')or p.startswith('--defsym=pthread_create=')for p in response)
assert '--defsym=__cxa_thread_atexit_impl=0'not in response
undefined=subprocess.check_output([str(LLVM/'llvm-nm'),'--dynamic','--undefined-only',str(elf)],text=True)
for name in ['mmap','mprotect','sceAgcInit','sceAgcDriverSubmitDcb']:assert any(line.endswith(' '+name)for line in undefined.splitlines()),name
with zipfile.ZipFile(package)as z,zipfile.ZipFile(ROOT/'dist/milestones/Client_LWJGL_Core-01.000.002/PPSA99874-full-local.zip')as old:
 assert z.testzip()is None;prefix='PPSA99874/'
 param=json.loads(z.read(prefix+'sce_sys/param.json'));base=json.loads((ROOT/'server/param.json').read_text())
 assert param['contentVersion']=='01.000.007'
 assert all(param[k]==base[k]for k in ['titleId','conceptId','contentId'])
 assert not any(name.endswith(('.pcm','.at9'))for name in z.namelist())
 assert not any('/sounds/'in name or '/libSceAgc.so'in name or '/libSceAgcDriver.so'in name for name in z.namelist())
 assert b'Client Vulkan Bindings 01.000.007'in z.read(prefix+'eboot.bin')
 assert b'ClientGpu25'in z.read(prefix+'eboot.bin')and b'-Xint'in z.read(prefix+'eboot.bin')
 fixture=z.read(prefix+'assets/java25/classes/ClientVulkan25.class')
 assert b'mapLibraryName'in fixture and b'ps5clientgpu'in fixture
 registry=(runtime/'build/java25/builtin-libraries.cpp').read_text()
 assert '{\"libps5clientgpu.so\", symbols_ps5clientgpu,'in registry
 assert 'new PS5Library(System.mapLibraryName(\"ps5clientgpu\"))'in (ROOT/'client/vulkan/ClientVulkan25.java').read_text()
 lock=json.loads((ROOT/'client/26.3.lock.json').read_text())
 for row in lock['artifacts']:assert sha(z.read(prefix+'assets/java25/client/jars/'+row['file']))==row['sha256']
 for name in old.namelist():
  if '/assets/java25/client/'in name or name.endswith('/lib/modules')or name.endswith('.so'):assert old.read(name)==z.read(name),name
 audit=json.loads(z.read(prefix+'assets/java25/gpu-integration-audit.json'))
 for name,digest in audit['objects_sha256'].items():assert digest==sha((ROOT/'build/client-gpu'/name).read_bytes())
 assert audit['constructors']['normalized_priorities']=={'.ctors':65535,'.ctors.65445':90}
 assert audit['console']=='pending'
 groups=json.loads(z.read(prefix+'assets/java25/resident-libraries-audit.json'))['external_resident_libraries']
 assert [r['name']for r in groups]==['ps5clientgpu','ps5clientbridge','lwjgl']
 assert groups[0]['objects_sha256']==[sha((ROOT/'build/client-gpu/gpu-bridge.o').read_bytes()),sha((work/'vulkan-loader.o').read_bytes())]
 assert audit['vulkan_binding']['loader_object_sha256']==sha((work/'vulkan-loader.o').read_bytes())
 assert audit['vulkan_binding']['fixture_source_sha256']==sha((ROOT/'client/vulkan/ClientVulkan25.java').read_bytes())
 core=json.loads(z.read(prefix+'assets/java25/lwjgl-native-audit.json'))
 assert groups[2]['objects_sha256']==list(core['objects_sha256'].values())
 for klass in ['ClientGpu25','ClientLwjglCore25','ClientVulkan25']:
  assert z.read(prefix+'assets/java25/classes/'+klass+'.class')==(work/'classes'/(klass+'.class')).read_bytes()
 for path in ['eboot.bin','sce_module/libc.prx']:
  out=subprocess.check_output([str(runtime/'build/native/host/ps5-native-tool'),'self','--inspect','--file',str(work/'PPSA99874'/path)],text=True);assert 'integrity: valid'in out
assert package.read_bytes()==(runtime/'dist/PPSA99874.zip').read_bytes()
assert (ROOT/'dist/client-vulkan/SHA256SUMS').read_text().split()[0]==sha(package.read_bytes())
for folder,digest in [('Client_Foundation-01.000.000','e2eb90a727fc670418437937b292b152c5177e3e02077aa114049bc6c9c11fbf'),('Client_Native_Loading-01.000.001','abc6aef0f162d9d134dec298742f27dfdb91a80345bb81ac54498239d34fd890'),('Client_LWJGL_Core-01.000.002','d0b9f815ff68c5ad821b2166509879c623c813019d2f70bbacf53769f35e3971'),('Client_Native_Graphics-01.000.003','82895fc3d9381a08c61f979e9ba33a56943ea5f890830786c7dd4c1c684bf812'),('Client_GPU_Integration-01.000.004','0077d9f72e7a468e16bacfc075527c096d68decab1849e1252ba18405cf444b5')]:assert sha((ROOT/'dist/milestones'/folder/'PPSA99874-full-local.zip').read_bytes())==digest
for version,digest in [('094','97ec74c40b9c495884130f9dae0ab10bf393e521265cbe82177f06190176df2d'),('108','18dc7f06d59ff11b33c7e96b85f813a28a2cb19638fe0d6eacfd4224513781e7')]:assert sha((runtime/'build/java25'/f'PPSA99874-{version}-full-local.zip').read_bytes())==digest
print('PASS Vulkan007 actual ELF:359 deferred JVM constructors,4 explicit priority-correct GPU constructors/no automatic startup; real JNI/GPU exports/imports, scoped allocator/thread/zlib and real TLS callback; CRC/signatures/54upstream pins/exact002 moduleimage and native libraries/three resident groups/object hashes and preserved000-003/Fabric094/Paper108. PS5 ten-row console pending. SHA256',sha(package.read_bytes()))
