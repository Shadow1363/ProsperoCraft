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
parser.add_argument('--runtime-shader', action='store_true', help='Build client022 runtime GLSL compiler candidate')
args = parser.parse_args()
if sum([args.shader,args.render,args.present,args.sdl,args.runtime_shader])>1:parser.error("Choose one candidate")
runtime = args.runtime_workspace.resolve()
variant="runtime_shader" if args.runtime_shader else "sdl" if args.sdl else "present" if args.present else "render" if args.render else "shader" if args.shader else "vulkan"
version="01.000.022" if args.runtime_shader else "01.000.014" if args.sdl else "01.000.011" if args.present else "01.000.010" if args.render else "01.000.009" if args.shader else "01.000.008"
# Regenerate reusable runtime embedding inputs with the preserved002 build path.
subprocess.run(['python3',str(ROOT/'tools/package_client_probe.py'),'--runtime-workspace',str(runtime),'--java-home',str(args.java_home),*(['--offline']if args.offline else [])],check=True)

subprocess.run(['python3',str(ROOT/'tools/prepare_client.py'),*(['--offline']if args.offline else [])],check=True)
subprocess.run(['python3',str(ROOT/'tools/build_lwjgl_platform.py'),'--java-home',str(args.java_home),*(['--offline']if args.offline else [])],check=True)
work=ROOT/('build/client-'+variant+'-probe');work.mkdir(parents=True,exist_ok=True)
assets=work/'assets';shutil.rmtree(assets,ignore_errors=True)
java=assets/'java25';java.mkdir(parents=True)
shutil.copytree(ROOT/'build/client',java/'client')
ports=java/'ports';ports.mkdir()
port=ROOT/'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar';shutil.copyfile(port,ports/port.name)
audit=json.loads((ROOT/'build/client-ports/lwjgl/audit.json').read_text());audit['activated_for_probe']=True;audit['activated_for_game']=False
(java/'dependency-port-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
lock=json.loads((ROOT/'client/26.3.lock.json').read_text())
classpath='/app0/assets/java25/client-probe.jar:/app0/assets/java25/ports/'+port.name+':'+':'.join('/app0/assets/java25/client/jars/'+row['file']for row in lock['artifacts']if not row['id'].startswith('org.lwjgl:lwjgl:'))
(work/'client_classpath.hpp').write_text('#pragma once\n#define CLIENT_CLASSPATH_OPTION '+json.dumps('-Djava.class.path='+classpath)+'\n')
sources=[*sorted((ROOT/'client/java').glob('*.java')),ROOT/'client/gpu/ClientGpu25.java',ROOT/'client/vulkan/ClientVulkan25.java']
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
 sources += [ROOT/('client/scene/ClientSceneSDL25.java' if args.runtime_shader else 'client/sdl/ClientSDL25.java' if args.sdl else 'client/present/ClientPresent25.java'),compile_present()]
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
gpu_support,gpu_bridge,gpu_audit=build_gpu(runtime,args.java_home)
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
shutil.copyfile(ROOT/'build/client-ports/lwjgl-native/ps5/audit.json',java/'lwjgl-native-audit.json')
specfile=work/'probe-spec.json';specfile.write_text(json.dumps(spec,indent=2)+'\n')
# Prepare the normal JVM/core embedding first using the existing002 tool/spec.
# Its generated native-libc, registry, moduleimage and wrapper objects stay real.
# A temporary stub is never linked or generated: the bridge's external driver
# symbols are supplied by the final link below.
from package_client_gpu_link import finish
finish(runtime,args.java_home,work,assets,spec,gpu_support,gpu_audit,variant=variant,version=version)
