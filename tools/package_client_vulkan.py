#!/usr/bin/env python3
"""Prepare the client008 JVM/core/bridge objects; final driver link is consumer-owned."""
import argparse
import hashlib
import json
from pathlib import Path
from build_lwjgl_native import build as build_native
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--runtime-workspace', type=Path, required=True)
parser.add_argument('--java-home', type=Path, required=True)
parser.add_argument('--offline', action='store_true')
parser.add_argument('--shader', action='store_true', help='Build client009 compute shader candidate')
parser.add_argument('--render', action='store_true', help='Build client010 graphics pipeline candidate')
parser.add_argument('--present', action='store_true', help='Build client011 standalone direct presentation candidate')
parser.add_argument('--sdl', action='store_true', help='Build client014 SDL window/input candidate')
parser.add_argument('--runtime-shader', action='store_true', help='Build client023 runtime GLSL compiler candidate')
parser.add_argument('--startup',action='store_true',help='Build064 original Minecraft Main startup with all accepted native components')
parser.add_argument('--native-bootstrap',action='store_true',help='Build026 genuine libffi/OpenAL native acceptance')
parser.add_argument('--opengl-bootstrap',action='store_true',help='Build029 genuine Mesa/OpenGL acceptance')
parser.add_argument('--spvc-bootstrap',action='store_true',help='Build036 genuine SPIRV-Cross translation/reflection acceptance')
parser.add_argument('--vma-bootstrap',action='store_true',help='Build035 genuine VMA allocation/GPU transfer acceptance')
parser.add_argument('--freetype-bootstrap',action='store_true',help='Build033 genuine FreeType glyph rasterization acceptance')
parser.add_argument('--stb-bootstrap',action='store_true',help='Build031 genuine STB codec acceptance')
args = parser.parse_args()
if sum([args.shader,args.render,args.present,args.sdl,args.runtime_shader,args.startup,args.native_bootstrap,args.opengl_bootstrap,args.stb_bootstrap,args.freetype_bootstrap,args.vma_bootstrap,args.spvc_bootstrap])>1:parser.error("Choose one candidate")
if args.startup or args.opengl_bootstrap or args.stb_bootstrap or args.freetype_bootstrap or args.vma_bootstrap or args.spvc_bootstrap:args.native_bootstrap=True
if args.startup or args.native_bootstrap:args.runtime_shader=True
runtime = args.runtime_workspace.resolve()
variant="spvc_bootstrap" if args.spvc_bootstrap else "vma_bootstrap" if args.vma_bootstrap else "freetype_bootstrap" if args.freetype_bootstrap else "stb_bootstrap" if args.stb_bootstrap else "opengl_bootstrap" if args.opengl_bootstrap else "startup" if args.startup else "native_bootstrap" if args.native_bootstrap else "runtime_shader" if args.runtime_shader else "sdl" if args.sdl else "present" if args.present else "render" if args.render else "shader" if args.shader else "vulkan"
version="01.000.036" if args.spvc_bootstrap else "01.000.035" if args.vma_bootstrap else "01.000.033" if args.freetype_bootstrap else "01.000.031" if args.stb_bootstrap else "01.000.029" if args.opengl_bootstrap else "01.000.064" if args.startup else "01.000.026" if args.native_bootstrap else "01.000.023" if args.runtime_shader else "01.000.014" if args.sdl else "01.000.011" if args.present else "01.000.010" if args.render else "01.000.009" if args.shader else "01.000.008"
# Regenerate reusable runtime embedding inputs with the preserved002 build path.
subprocess.run(['python3',str(ROOT/'tools/package_client_probe.py'),'--runtime-workspace',str(runtime),'--java-home',str(args.java_home),*(['--offline']if args.offline else [])],check=True)

subprocess.run(['python3',str(ROOT/'tools/prepare_client.py'),*(['--offline']if args.offline else [])],check=True)
subprocess.run(['python3',str(ROOT/'tools/build_lwjgl_platform.py'),'--java-home',str(args.java_home),*(['--offline']if args.offline else [])],check=True)
work=ROOT/('build/client-'+variant+'-probe');work.mkdir(parents=True,exist_ok=True)
assets=work/'assets';shutil.rmtree(assets,ignore_errors=True)
java=assets/'java25';java.mkdir(parents=True)
shutil.copytree(ROOT/'build/client',java/'client')
if args.startup:
 from prepare_client_assets import prepare as prepare_assets
 asset_source=prepare_assets(offline=args.offline)
 shutil.copytree(asset_source,java/'game-assets')
 shutil.copyfile(ROOT/'client/startup/log4j2-startup.xml',java/'log4j2-startup.xml')
ports=java/'ports';ports.mkdir()
port=ROOT/'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar';shutil.copyfile(port,ports/port.name)
audit=json.loads((ROOT/'build/client-ports/lwjgl/audit.json').read_text());audit['activated_for_probe']=True;audit['activated_for_game']=bool(args.startup)
(java/'dependency-port-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
lock=json.loads((ROOT/'client/26.3.lock.json').read_text())
module_port=None
if args.native_bootstrap:
 from build_lwjgl_module_platform import build as build_module_platform
 module_port=build_module_platform(args.java_home,args.offline);shutil.copyfile(module_port,ports/module_port.name)
 shutil.copyfile(ROOT/'build/client-ports/lwjgl-modules/audit.json',java/'module-platform-audit.json')
classpath='/app0/assets/java25/client-probe.jar:/app0/assets/java25/ports/'+port.name+':'+':'.join('/app0/assets/java25/client/jars/'+row['file']for row in lock['artifacts']if not row['id'].startswith('org.lwjgl:lwjgl:'))
if module_port:classpath='/app0/assets/java25/ports/'+module_port.name+':'+classpath
(work/'client_classpath.hpp').write_text('#pragma once\n#define CLIENT_CLASSPATH_OPTION '+json.dumps('-Djava.class.path='+classpath)+'\n')
sources=[*sorted((ROOT/'client/java').glob('*.java')),ROOT/'client/gpu/ClientGpu25.java',ROOT/'client/vulkan/ClientVulkan25.java']
if args.spvc_bootstrap:sources += [ROOT/'client/spvc_bootstrap/ClientSPVC25.java']
if args.vma_bootstrap:sources += [ROOT/'client/vma_bootstrap/ClientVMA25.java']
if args.freetype_bootstrap:sources += [ROOT/'client/freetype_bootstrap/ClientFreeType25.java']
if args.stb_bootstrap:sources += [ROOT/'client/stb_bootstrap/ClientSTB25.java']
if args.opengl_bootstrap:sources += [ROOT/'client/opengl_bootstrap/ClientOpenGL25.java']
if args.startup:sources += [ROOT/'client/startup/ClientStartup25.java']
if args.native_bootstrap:sources += [ROOT/'client/native_bootstrap/ClientNativeBootstrap25.java']
if args.shader or args.render or args.present or args.sdl or args.runtime_shader:
 from compile_client_shader import compile_shader
 sources += [ROOT/'client/shader/ClientShader25.java',compile_shader()]
 shutil.copyfile(ROOT/'build/client-shader/audit.json',java/'shader-audit.json')
 (java/'shaders').mkdir()
 shutil.copyfile(ROOT/'build/client-shader/workload.spv',java/'shaders/workload.spv')
 shutil.copyfile(ROOT/'client/shader/workload.comp',java/'shaders/workload.comp')
if args.render:
 from compile_client_render import compile_render
 sources += [ROOT/'client/render/ClientRender25.java',compile_render()]
 shutil.copyfile(ROOT/'build/client-render/audit.json',java/'render-audit.json')
 for name in ['fullscreen.vert','pattern.frag']:
  shutil.copyfile(ROOT/'client/render'/name,java/'shaders'/name)
  shutil.copyfile(ROOT/'build/client-render'/(name+'.spv'),java/'shaders'/(name+'.spv'))
if args.present or args.sdl or args.runtime_shader:
 from compile_client_present import compile_present
 sources += [ROOT/('client/continuous/ClientContinuousSDL25.java' if args.runtime_shader else 'client/sdl/ClientSDL25.java' if args.sdl else 'client/present/ClientPresent25.java'),compile_present()]
 shutil.copyfile(ROOT/'build/client-present/audit.json',java/'present-audit.json')
 (java/'shaders/present').mkdir()
 for name in ['fullscreen.vert','pattern.frag']:
  shutil.copyfile(ROOT/'client/present'/name,java/'shaders/present'/name)
  shutil.copyfile(ROOT/'build/client-present'/(name+'.spv'),java/'shaders/present'/(name+'.spv'))
if args.runtime_shader:
 sources += [ROOT/'client/runtime_shader/ClientRuntimeShader25.java']
 from compile_client_texture import compile_texture
 sources += [ROOT/'client/texture/ClientTexture25.java',compile_texture()]
 from compile_client_scene import compile_scene
 sources += [ROOT/'client/scene/ClientScene25.java',compile_scene()]
 sources += [ROOT/'client/continuous/ClientDirectScene25.java']
 shutil.copyfile(ROOT/'build/client-scene/audit.json',java/'scene-audit.json')
 (java/'shaders/scene').mkdir()
 for name in ['panel.vert','panel.frag']:
  shutil.copyfile(ROOT/'client/scene'/name,java/'shaders/scene'/name)
  shutil.copyfile(ROOT/'build/client-scene'/(name+'.spv'),java/'shaders/scene'/(name+'.spv'))
 shutil.copyfile(ROOT/'build/client-texture/audit.json',java/'texture-audit.json')
 (java/'shaders/texture').mkdir()
 for name in ['fullscreen.vert','texture.frag']:
  shutil.copyfile(ROOT/'client/texture'/name,java/'shaders/texture'/name)
  shutil.copyfile(ROOT/'build/client-texture'/(name+'.spv'),java/'shaders/texture'/(name+'.spv'))
cp=':'.join([str(port),*[str(ROOT/'.tools/client'/row['file'])for row in lock['artifacts']if not row['id'].startswith('org.lwjgl:lwjgl:')]])
classes=work/'classes';shutil.rmtree(classes,ignore_errors=True);classes.mkdir()
subprocess.run([str(args.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(classes),*[str(p)for p in sources]],check=True)
with zipfile.ZipFile(java/'client-probe.jar','w',zipfile.ZIP_DEFLATED)as output:
 for path in sorted(classes.rglob('*.class')):
  info=zipfile.ZipInfo(str(path.relative_to(classes)));info.compress_type=zipfile.ZIP_DEFLATED;output.writestr(info,path.read_bytes())
modules=json.loads((ROOT/'server/26.3.lock.json').read_text())['modules']
spec={'menu_audio':False,'source':str(ROOT/'client'/variant/'bootstrap.cpp'),'param':str(ROOT/'client'/variant/'param.json'),'asset_dir':str(assets),'java_sources':[str(p)for p in sources],'modules':modules,'java_compile_classpath':[str(port),*[str(ROOT/'.tools/client'/row['file'])for row in lock['artifacts']if not row['id'].startswith('org.lwjgl:lwjgl:')]],'include_dirs':[str(work),str(ROOT/'client/native'),str(runtime/'java25/probe')]}
# A genuine named JNI library is built into the resident registry. Its native
# methods use normal JVM symbol resolution, not RegisterNatives injection.
obj=work/'resident-library.o'
headers=runtime/'.tools/java25/openjdk/build/ps5-bootstrap/support/modules_include/java.base'
sdk=runtime/'.tools/native-sdk/ps5-payload-sdk'
subprocess.run(['/opt/homebrew/opt/llvm/bin/clang','-target','x86_64-sie-ps5','-std=c11','-O2','-fPIC','-fvisibility-nodllstorageclass=default','-isysroot',str(sdk),'-I'+str(headers),'-I'+str(headers/'freebsd'),'-c',str(ROOT/'client/native/resident_library.c'),'-o',str(obj)],check=True)
native_objects=build_native(runtime,args.java_home,offline=args.offline)
from build_client_gpu import build as build_gpu
gpu_support,gpu_bridge,gpu_audit=build_gpu(runtime,args.java_home,wsi_diagnostics=args.startup)
# Only the original LWJGL memory JNI entry points use the graphics title heap.
# Keep the entire allocation family paired;never replace JVM/global libc symbols.
if args.startup:
 allocation_names=['malloc','calloc','realloc','free','posix_memalign','aligned_alloc']
 allocation_bindings={name:gpu_audit['graphics_bindings'][name] for name in allocation_names}
 allocation_map=work/'lwjgl-memory-bindings.txt';allocation_map.write_text(''.join(a+' '+b+'\n' for a,b in sorted(allocation_bindings.items())))
 scoped_memory=[]
 for unit in native_objects:
  if unit.name in ['org_lwjgl_system_MemoryAccessJNI.c.o','org_lwjgl_system_libc_LibCStdlib.c.o']:
   target=work/('scoped-'+unit.name)
   subprocess.run(['/opt/homebrew/opt/llvm/bin/llvm-objcopy','--redefine-syms='+str(allocation_map),str(unit),str(target)],check=True)
   scoped_memory.append(target)
  else:scoped_memory.append(unit)
 native_objects=scoped_memory
 allocation_audit={'scope':'Only startup LWJGL MemoryAccessJNI/LibCStdlib objects;existing scoped graphics title-heap family;JVM globals unchanged','bindings':allocation_bindings,'objects_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in native_objects if p.name.startswith('scoped-')},'runtime_global_allocator_modified':False,'console':'PENDING PS5 large render-buffer allocation'}
 assert len(allocation_audit['objects_sha256'])==2
 (java/'lwjgl-allocation-audit.json').write_text(json.dumps(allocation_audit,indent=2)+'\n')
# Standard loader entry into the actual resident ICD; no VK Java class rewrite.
loader=work/'vulkan-loader.o'
subprocess.run(['/opt/homebrew/opt/llvm/bin/clang','-std=c11','-O2','-Wall','-Wextra','-Werror','-fPIC','-target','x86_64-sie-ps5','-march=x86-64','-mno-avx','-mno-avx2','-mno-fma','-fvisibility-nodllstorageclass=default','-isysroot',str(runtime/'.tools/native-sdk/ps5-payload-sdk'),'-I'+str(ROOT/'.tools/PS5_Mesa/include'),'-c',str(ROOT/'client/vulkan/loader.c'),'-o',str(loader)],check=True)
gpu_audit['vulkan_binding']={'jar':'Original upstream lwjgl-vulkan3.4.3 unchanged','bootstrap':'Supported VK.create(FunctionProvider) with PS5Library resident provider; vkGetInstanceProcAddr forwards to actual ICD','loader_object_sha256':hashlib.sha256(loader.read_bytes()).hexdigest(),'fixture_source_sha256':hashlib.sha256((ROOT/'client/vulkan/ClientVulkan25.java').read_bytes()).hexdigest(),'scope':'Real upstream VkInstance/VkDevice capability tables, structs and generic JNI commands; selected transfer/lifecycle commands tested, not complete Vulkan coverage'}
spec['resident_libraries']=[{'name':'ps5clientgpu','objects':[str(gpu_bridge),str(loader)]},{'name':'ps5clientbridge','objects':[str(obj)]},{'name':'lwjgl','objects':[str(p)for p in native_objects]}]
if args.sdl or args.runtime_shader:
 from build_sdl_native import build as build_sdl
 sdl_object=build_sdl(runtime)
 # Bind SDL's libc/thread references to the same genuine scoped graphics
 # providers as RADV, without changing global JVM symbol resolution.
 scoped=work/'resident-sdl.o'
 mapping=ROOT/'build/client-gpu/sdl-bindings.txt'
 bindings=gpu_audit['graphics_bindings']
 mapping.write_text(''.join(k+' '+v+'\n' for k,v in sorted(bindings.items())))
 subprocess.run(['/opt/homebrew/opt/llvm/bin/llvm-objcopy','--redefine-syms='+str(mapping),str(sdl_object),str(scoped)],check=True)
 spec['resident_libraries'].append({'name':'ps5sdl','objects':[str(scoped)]})
 sdl_audit=json.loads((ROOT/'build/sdl3-native/audit.json').read_text());sdl_audit['scoped_object_sha256']=hashlib.sha256(scoped.read_bytes()).hexdigest();sdl_audit['binding_scope']='Existing graphics provider binding map; JVM global providers unchanged'
 (java/'sdl-audit.json').write_text(json.dumps(sdl_audit,indent=2)+'\n')
 licenses=java/'sdl-licenses';licenses.mkdir()
 for name in ['Zlib.txt','MIT.txt']:shutil.copyfile(ROOT/'client/ports/sdl'/name,licenses/name)
 shutil.copyfile(ROOT/'build/sdl-src/LICENSE.txt',licenses/'SDL-LICENSE.txt')
if args.runtime_shader:
 from build_shaderc_native import build as build_shaderc
 compiler,lifecycle,compiler_audit=build_shaderc(runtime,offline=args.offline)
 spec['resident_libraries'].append({'name':'ps5shaderc','objects':[str(compiler),str(lifecycle)]})
 (java/'shaderc-audit.json').write_text(json.dumps(compiler_audit,indent=2)+'\n')
 licenses=java/'shaderc-licenses';licenses.mkdir()
 for name,path in [('shaderc-LICENSE.txt',ROOT/'.tools/shaderc-src/LICENSE'),('glslang-LICENSE.txt',ROOT/'.tools/shaderc-src/third_party/glslang/LICENSE.txt'),('SPIRV-Tools-LICENSE.txt',ROOT/'.tools/shaderc-src/third_party/spirv-tools/LICENSE'),('SPIRV-Headers-LICENSE.txt',ROOT/'.tools/shaderc-src/third_party/spirv-headers/LICENSE')]:shutil.copyfile(path,licenses/name)
if args.native_bootstrap:
 from build_libffi_native import build as build_ffi
 ffi_object,ffi_audit=build_ffi(runtime,args.java_home,offline=args.offline)
 scoped_ffi=work/'ffi.o';subprocess.run(['/opt/homebrew/opt/llvm/bin/llvm-objcopy','--redefine-syms='+str(ROOT/'build/client-gpu/sdl-bindings.txt'),str(ffi_object),str(scoped_ffi)],check=True)
 spec['resident_libraries'][2]['objects'].append(str(scoped_ffi));ffi_audit['scoped_object_sha256']=hashlib.sha256(scoped_ffi.read_bytes()).hexdigest();(java/'ffi-audit.json').write_text(json.dumps(ffi_audit,indent=2)+'\n')
 from build_openal_native import build as build_openal
 al_object,al_lifecycle,al_audit=build_openal(runtime,offline=args.offline)
 al_objects=[str(al_object),str(al_lifecycle)]
 if args.startup:
  # Retain the original object/archive. Only this private OpenAL dependency
  # observes a fixed upstream trace level;global environment/backend unchanged.
  traced=work/'startup-openal.o';trace_env=work/'startup-openal-trace-env.o'
  from build_openal_startup_boundaries import build as build_alc_boundaries
  boundary_object,boundary_audit=build_alc_boundaries()
  al_audit['startup_boundaries']=boundary_audit
  subprocess.run(['/opt/homebrew/opt/llvm/bin/llvm-objcopy','--redefine-sym','getenv=client_startup_openal_getenv',str(boundary_object),str(traced)],check=True)
  subprocess.run(['/opt/homebrew/opt/llvm/bin/clang','-target','x86_64-sie-ps5','-O2','-fPIC','-fvisibility-nodllstorageclass=default','-isysroot',str(ROOT/'.tools/graphics-sdk'),'-c',str(ROOT/'client/startup/openal_trace_env.c'),'-o',str(trace_env)],check=True)
  al_objects=[str(traced),str(al_lifecycle),str(trace_env)]
  al_audit['startup_trace']={'scope':'Startup-private OpenAL trace3 and explicit app-local data fallback;configured nonempty localpath honored,other lookups/global getenv/backend unchanged','source_sha256':hashlib.sha256((ROOT/'client/startup/openal_trace_env.c').read_bytes()).hexdigest(),'private_object_sha256':hashlib.sha256(traced.read_bytes()).hexdigest(),'shim_object_sha256':hashlib.sha256(trace_env.read_bytes()).hexdigest(),'original_object_sha256':hashlib.sha256(al_object.read_bytes()).hexdigest(),'output':'existing native-stderr.log;native trace timing/coverage pending PS5','backend_selection_changed':False,'local_data_directory_default':'/download0/mc-client','explicit_local_path_honored':True}
 spec['resident_libraries'].append({'name':'ps5openal','objects':al_objects});(java/'openal-audit.json').write_text(json.dumps(al_audit,indent=2)+'\n')
 helper=work/'callback-helper-raw.o';headers=runtime/'.tools/java25/openjdk/build/ps5-bootstrap/support/modules_include/java.base'
 subprocess.run(['/opt/homebrew/opt/llvm/bin/clang','-target','x86_64-sie-ps5','-O2','-fPIC','-fvisibility-nodllstorageclass=default','-isysroot',str(ROOT/'.tools/graphics-sdk'),'-I'+str(headers),'-I'+str(headers/'freebsd'),'-c',str(ROOT/'client/native_bootstrap/callback_probe.c'),'-o',str(helper)],check=True)
 scoped_helper=work/'callback-helper.o';subprocess.run(['/opt/homebrew/opt/llvm/bin/llvm-objcopy','--redefine-syms='+str(ROOT/'build/client-gpu/sdl-bindings.txt'),str(helper),str(scoped_helper)],check=True);spec['resident_libraries'].append({'name':'ps5nativeprobe','objects':[str(scoped_helper)]})
 licenses=java/'native-bootstrap-licenses';licenses.mkdir()
 for name,path in [('libffi-LICENSE.txt',ROOT/'build/libffi-ps5/source/LICENSE'),('OpenAL-COPYING.txt',ROOT/'.tools/openal-soft-src/COPYING'),('OpenAL-BSD.txt',ROOT/'.tools/openal-soft-src/BSD-3Clause'),('PFFFT-LICENSE.txt',ROOT/'.tools/openal-soft-src/LICENSE-pffft'),('fmt-LICENSE.txt',ROOT/'.tools/openal-soft-src/fmt-11.2.0/LICENSE'),('GSL-LICENSE.txt',ROOT/'.tools/openal-soft-src/gsl/LICENSE')]:shutil.copyfile(path,licenses/name)
if args.opengl_bootstrap or args.startup:
 from build_osmesa_resident import prepare as prepare_gl
 from build_lwjgl_opengl_native import build as build_gl_jni
 gl_objects,gl_audit=prepare_gl(runtime,args.offline)
 gl_jni=build_gl_jni(runtime,args.java_home,offline=args.offline)
 spec['resident_libraries'] += [{'name':'ps5clientgl','objects':[str(p)for p in gl_objects]}, {'name':'lwjgl_opengl','objects':[str(gl_jni)]}]
 (java/'opengl-provider-audit.json').write_text(json.dumps(gl_audit,indent=2)+'\n')
 shutil.copyfile(ROOT/'build/lwjgl-opengl-ps5/audit.json',java/'opengl-jni-audit.json')
 licenses=java/'opengl-licenses';licenses.mkdir()
 for name,path in [('Mesa-COPYING.txt',ROOT/'build/mesa-osmesa-source/docs/license.rst'),('zlib-README.txt',ROOT/'build/mesa-osmesa-source/subprojects/zlib-1.3.1/README')]:shutil.copyfile(path,licenses/name)
 # Preserve every upstream Mesa per-file copyright/license notice locally.
 shutil.copyfile(ROOT/'.tools/mesa-osmesa-24.3.4.tar.xz',licenses/'mesa-24.3.4-source.tar.xz')
 for patch in sorted((ROOT/'client/ports/opengl').glob('*.patch')):shutil.copyfile(patch,licenses/patch.name)

if args.stb_bootstrap or args.startup:
 from build_lwjgl_stb_native import build as build_stb
 stb=build_stb(runtime,args.java_home,offline=args.offline)
 spec['resident_libraries'].append({'name':'lwjgl_stb','objects':[str(stb)]})
 shutil.copyfile(ROOT/'build/lwjgl-stb-ps5/audit.json',java/'stb-audit.json')
 licenses=java/'stb-licenses';licenses.mkdir()
 shutil.copyfile(ROOT/'client/ports/lwjgl/LICENSE.md',licenses/'LWJGL-LICENSE.txt')
 # Original STB implementations carry their own MIT/public-domain notices.
 for row in json.loads((ROOT/'client/ports/stb/native-sources.json').read_text())['files']:
  shutil.copyfile(ROOT/'.tools/lwjgl-stb-src'/row['file'],licenses/row['file'])
if args.freetype_bootstrap or args.startup:
 from build_freetype_native import build as build_freetype
 font_object=build_freetype(runtime,offline=args.offline)
 spec['resident_libraries'].append({'name':'freetype','objects':[str(font_object)]})
 shutil.copyfile(ROOT/'build/freetype-ps5/audit.json',java/'freetype-audit.json')
 fontdir=java/'font-probe';fontdir.mkdir()
 shutil.copyfile(ROOT/'.tools/Abel-Regular.ttf',fontdir/'Abel-Regular.ttf')
 shutil.copyfile(ROOT/'.tools/Abel-OFL.txt',fontdir/'OFL.txt')
 licenses=java/'freetype-licenses';licenses.mkdir()
 shutil.copytree(ROOT/'build/freetype-source/docs',licenses/'docs')
 shutil.copyfile(ROOT/'build/freetype-source/LICENSE.TXT',licenses/'LICENSE.TXT')
if args.vma_bootstrap or args.startup:
 from build_lwjgl_vma_native import build as build_vma
 vma_object=build_vma(runtime,args.java_home,offline=args.offline)
 spec['resident_libraries'].append({'name':'lwjgl_vma','objects':[str(vma_object)]})
 shutil.copyfile(ROOT/'build/lwjgl-vma-ps5/audit.json',java/'vma-audit.json')
 licenses=java/'vma-licenses';licenses.mkdir()
 shutil.copyfile(ROOT/'client/ports/lwjgl/LICENSE.md',licenses/'LWJGL-LICENSE.txt')
 for row in json.loads((ROOT/'client/ports/vma/native-sources.json').read_text())['files']:
  target=licenses/row['file'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'.tools/lwjgl-vma-src'/row['file'],target)
if args.spvc_bootstrap or args.startup:
 from build_spvc_native import build as build_spvc
 spvc_object=build_spvc(runtime,offline=args.offline)
 spec['resident_libraries'].append({'name':'ps5spvc','objects':[str(spvc_object)]})
 shutil.copyfile(ROOT/'build/spvc-ps5/audit.json',java/'spvc-audit.json')
 licenses=java/'spvc-licenses';licenses.mkdir()
 shutil.copyfile(ROOT/'build/spvc-source/LICENSE',licenses/'SPIRV-Cross-LICENSE.txt')
 shutil.copyfile(ROOT/'client/ports/lwjgl/LICENSE.md',licenses/'LWJGL-LICENSE.txt')
 shutil.copyfile(ROOT/'.tools/spirv-cross-source.tar.gz',licenses/'SPIRV-Cross-source.tar.gz')
 shutil.copyfile(ROOT/'client/ports/spvc/0001-ps5-native-localeconv.patch',licenses/'0001-ps5-native-localeconv.patch')
shutil.copyfile(ROOT/'build/client-ports/lwjgl-native/ps5/audit.json',java/'lwjgl-native-audit.json')
specfile=work/'probe-spec.json';specfile.write_text(json.dumps(spec,indent=2)+'\n')
# Prepare the normal JVM/core embedding first using the existing002 tool/spec.
# Its generated native-libc, registry, moduleimage and wrapper objects stay real.
# A temporary stub is never linked or generated: the bridge's external driver
# symbols are supplied by the final link below.
from package_client_gpu_link import finish
finish(runtime,args.java_home,work,assets,spec,gpu_support,gpu_audit,variant=variant,version=version)
