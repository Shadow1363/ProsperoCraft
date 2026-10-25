#!/usr/bin/env python3
"""Verify actual original-client startup package and all publisher asset objects."""
from pathlib import Path
import argparse,json,zipfile,hashlib,subprocess,struct
ROOT=Path(__file__).resolve().parents[1];LLVM=Path('/opt/homebrew/opt/llvm/bin')
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args();runtime=a.runtime_workspace
work=ROOT/'build/client-startup-probe';package=ROOT/'dist/client-startup/PPSA99874.zip';sha=lambda data:hashlib.sha256(data).hexdigest()
elf=work/'bootstrap-01.000.037-symbols.elf';text=subprocess.check_output([str(LLVM/'llvm-nm'),'--defined-only',str(elf)],text=True);symbols={l.split()[-1]:int(l.split()[0],16)for l in text.splitlines()if len(l.split())==3}
assert symbols['__init_array_start']==symbols['__init_array_end'];assert (symbols['__client_openal_init_end']-symbols['__client_openal_init_start'])//8==15;assert (symbols['__jvm_init_array_end']-symbols['__jvm_init_array_start'])//8==359;assert (symbols['__client_gpu_init_end']-symbols['__client_gpu_init_start'])//8==4;assert (symbols['__client_shaderc_init_end']-symbols['__client_shaderc_init_start'])//8==5
assert (symbols['__client_gl_init_end']-symbols['__client_gl_init_start'])//8==1
for name in ['OSMesaGetProcAddress','OSMesaCreateContextAttribs','ps5_builtin_load_ps5clientgl','ps5_builtin_load_lwjgl_opengl','ffi_prep_closure_loc','ffi_call_plan_alloc','alcLoopbackOpenDeviceSOFT','alcRenderSamplesSOFT','ps5_builtin_load_ps5openal','JNI_CreateJavaVM','ps5_builtin_load_ps5sdl','ps5_builtin_load_ps5shaderc','ps5_builtin_load_ps5clientgpu','radv_CreateInstance','ps5_builtin_load_lwjgl_stb','Java_org_lwjgl_stb_LibSTB_setupMalloc','Java_org_lwjgl_stb_STBImage_nstbi_1load_1from_1memory__JIJJJI','clientstb_org_lwjgl_malloc','ps5_builtin_load_freetype','FT_Init_FreeType','FT_Load_Char','FT_Done_FreeType','ps5_builtin_load_lwjgl_vma','Java_org_lwjgl_util_vma_Vma_nvmaCreateAllocator','ps5_builtin_load_ps5spvc','spvc_context_create','spvc_compiler_compile']:assert symbols.get(name),name
with zipfile.ZipFile(package)as z,zipfile.ZipFile(ROOT/'dist/milestones/Client_Continuous_Direct_Scene-01.000.023/PPSA99874-full-local.zip')as baseline:
 assert z.testzip()is None;prefix='PPSA99874/';param=json.loads(z.read(prefix+'sce_sys/param.json'));old=json.loads(baseline.read(prefix+'sce_sys/param.json'));assert param['contentVersion']=='01.000.037'
 for k in ['titleId','contentId','conceptId']:assert param[k]==old[k]
 assert b'-Xmx128m'in z.read(prefix+'eboot.bin') and b'Minecraft Original Client Startup 01.000.037'in z.read(prefix+'eboot.bin')
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
 groups=json.loads(z.read(prefix+'assets/java25/resident-libraries-audit.json'))['external_resident_libraries'];assert [g['name']for g in groups]==['ps5clientgpu','ps5clientbridge','lwjgl','ps5sdl','ps5shaderc','ps5openal','ps5nativeprobe','ps5clientgl','lwjgl_opengl','lwjgl_stb','freetype','lwjgl_vma','ps5spvc']
 cpp=json.loads(z.read(prefix+'assets/java25/cpp-allocation-audit.json'));assert cpp['scoped_object_sha256']==sha((work/'cpp_runtime.o').read_bytes())
 audit=json.loads(z.read(prefix+'assets/java25/dependency-port-audit.json'));assert audit['activated_for_game']is True
for file in ['eboot.bin','sce_module/libc.prx']:
 report=subprocess.check_output([str(runtime/'build/native/host/ps5-native-tool'),'self','--inspect','--file',str(work/'PPSA99874'/file)],text=True);assert 'integrity: valid'in report
assert package.read_bytes()==(runtime/'dist/PPSA99874.zip').read_bytes()
for folder,digest in [('Client_Continuous_Direct_Scene-01.000.023','846cd9adea6f9e6b04f80df461424c26b1fec6aa080ed641c35e7cfb16488ea4'),('Client_Visible_Perspective_Scene-01.000.022','9d49135a4dcbd66e93ef496e442c7845964e08aa6664c9dc26546a94196e450e')]:assert sha((ROOT/'dist/milestones'/folder/'PPSA99874-full-local.zip').read_bytes())==digest
with zipfile.ZipFile(package)as z:
 assert z.read('PPSA99874/assets/java25/ports/lwjgl-3.4.3-ps5-modules.jar')==(ROOT/'build/client-ports/lwjgl-modules/lwjgl-3.4.3-ps5-modules.jar').read_bytes()
 validation=json.loads((ROOT/'Client_OpenGL_Provider/validation.json').read_text())
 assert json.loads(z.read('PPSA99874/assets/java25/opengl-provider-audit.json'))['objects_sha256']==validation['opengl_provider_audit']['objects_sha256']
 assert json.loads(z.read('PPSA99874/assets/java25/opengl-jni-audit.json'))['object_sha256']==validation['opengl_jni_audit']['object_sha256']
 assert sha(z.read('PPSA99874/assets/java25/ports/lwjgl-3.4.3-ps5-modules.jar'))==validation['module_platform_audit']['output_sha256']
 assert (work/'classes/ClientStartup25.class').read_bytes()==(ROOT/'build/startup-host-037/ClientStartup25.class').read_bytes()
 assert b'OSMesa'in z.read('PPSA99874/assets/java25/classes/ClientStartup25.class')
 assert b'ps5clientgl'in z.read('PPSA99874/assets/java25/classes/ClientStartup25.class')
 assert sha((ROOT/'dist/milestones/Client_OpenGL_Provider-01.000.029/PPSA99874-full-local.zip').read_bytes())=='ed0cc6f49528b44b6d131c800e3c6359d01e009ae52524b7e96262a71491b685'
 stb_validation=json.loads((ROOT/'Client_STB_Codecs/validation.json').read_text())
 with zipfile.ZipFile(ROOT/'dist/milestones/Client_STB_Codecs-01.000.031/PPSA99874-full-local.zip')as stb_baseline:
  assert z.read(prefix+'assets/java25/stb-audit.json')==stb_baseline.read(prefix+'assets/java25/stb-audit.json')
  assert next(g for g in groups if g['name']=='lwjgl_stb')==json.loads(stb_baseline.read(prefix+'assets/java25/resident-libraries-audit.json'))['external_resident_libraries'][-1]
 with zipfile.ZipFile(ROOT/'dist/milestones/Client_OpenGL_Provider-01.000.029/PPSA99874-full-local.zip')as gl_baseline:
  assert [g for g in groups if g['name']in ['ps5clientgl','lwjgl_opengl']]==json.loads(gl_baseline.read(prefix+'assets/java25/resident-libraries-audit.json'))['external_resident_libraries'][-2:]
 assert sha((ROOT/'build/lwjgl-stb-ps5/lwjgl-stb.o').read_bytes())==json.loads(z.read(prefix+'assets/java25/stb-audit.json'))['object_sha256']
 assert sha((ROOT/'dist/milestones/Client_STB_Codecs-01.000.031/PPSA99874-full-local.zip').read_bytes())==stb_validation['tested_full_package_sha256']
 assert sha((ROOT/'dist/failures/Client_Original_Startup-01.000.030/PPSA99874-full-local.zip').read_bytes())=='1eb5bc45080aa65b9d38817db58e4984ff58668f491598322783c83c41cc8ce1'
 with zipfile.ZipFile(ROOT/'dist/milestones/Client_FreeType_Fonts-01.000.033/PPSA99874-full-local.zip')as font_baseline:
  assert z.read(prefix+'assets/java25/freetype-audit.json')==font_baseline.read(prefix+'assets/java25/freetype-audit.json')
  assert next(g for g in groups if g['name']=='freetype')==json.loads(font_baseline.read(prefix+'assets/java25/resident-libraries-audit.json'))['external_resident_libraries'][-1]
 assert sha((ROOT/'dist/milestones/Client_FreeType_Fonts-01.000.033/PPSA99874-full-local.zip').read_bytes())=='e7666f17dedda986507f9ba19fa11183bf89baf07971044659dcee2416022afc'
 assert sha((ROOT/'dist/failures/Client_Original_Startup-01.000.032/PPSA99874-full-local.zip').read_bytes())=='5d6fb33084876e0d0b08e5b020c6de196b98508d31b983a6f33cd9028635e434'
 for milestone,version,group,audit in [('Client_VMA_Allocator','01.000.035','lwjgl_vma','vma'),('Client_SPIRV_Cross','01.000.036','ps5spvc','spvc')]:
  record=json.loads((ROOT/milestone/'validation.json').read_text());frozen=ROOT/'dist/milestones'/(milestone+'-'+version)/'PPSA99874-full-local.zip'
  assert sha(frozen.read_bytes())==record['tested_full_package_sha256']
  with zipfile.ZipFile(frozen)as accepted:
   assert z.read(prefix+'assets/java25/'+audit+'-audit.json')==accepted.read(prefix+'assets/java25/'+audit+'-audit.json')
   assert next(g for g in groups if g['name']==group)==json.loads(accepted.read(prefix+'assets/java25/resident-libraries-audit.json'))['external_resident_libraries'][-1]
 assert b'ps5spvc'in fixture and b'SPVC_LIBRARY_NAME'in fixture
 assert sha((ROOT/'dist/failures/Client_Original_Startup-01.000.034/PPSA99874-full-local.zip').read_bytes())=='ee306f748fc37c171eec6edb1afaf5dfe59d12ef0cb57b56feb56bf8b3ba4a79'
 assert b'ps5openal'in z.read('PPSA99874/assets/java25/classes/ClientStartup25.class')
 assert sha((ROOT/'dist/milestones/Client_Callbacks_OpenAL-01.000.026/PPSA99874-full-local.zip').read_bytes())=='e158f9fd76ce91f16091b6e9ee2c54a4cbaf11863f08bf77853204b6ef984d82'
print('PASS037 actual package/CRC/signatures,all54 original JARs/all5147 original asset SHA1s,exact023 runtime image/native libs,359+4+5+15+1staged constructors/13real resident groups/actual036 SPIRV-Cross+035 VMA+033 FreeType+031 STB+029 OSMesa/OpenGL+026 libffi+OpenAL+module overlay/paired C++ allocator/actual Main invocation bytecode/workdir/log config and preserved022/023 packages. PS5 original startup/menu remains pending. SHA256',sha(package.read_bytes()))
