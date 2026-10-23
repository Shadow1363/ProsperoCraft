#!/usr/bin/env python3
"""Prepare the client005 JVM/core/bridge objects; final driver link is consumer-owned."""
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
args = parser.parse_args()
runtime = args.runtime_workspace.resolve()
# Regenerate reusable runtime embedding inputs with the preserved002 build path.
subprocess.run(['python3',str(ROOT/'tools/package_client_probe.py'),'--runtime-workspace',str(runtime),'--java-home',str(args.java_home),*(['--offline']if args.offline else [])],check=True)

subprocess.run(['python3',str(ROOT/'tools/prepare_client.py'),*(['--offline']if args.offline else [])],check=True)
subprocess.run(['python3',str(ROOT/'tools/build_lwjgl_platform.py'),'--java-home',str(args.java_home),*(['--offline']if args.offline else [])],check=True)
work=ROOT/'build/client-vulkan-probe';work.mkdir(parents=True,exist_ok=True)
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
cp=':'.join([str(port),*[str(ROOT/'.tools/client'/row['file'])for row in lock['artifacts']if not row['id'].startswith('org.lwjgl:lwjgl:')]])
classes=work/'classes';shutil.rmtree(classes,ignore_errors=True);classes.mkdir()
subprocess.run([str(args.java_home/'bin/javac'),'--release','25','-cp',cp,'-d',str(classes),*[str(p)for p in sources]],check=True)
with zipfile.ZipFile(java/'client-probe.jar','w',zipfile.ZIP_DEFLATED)as output:
 for path in sorted(classes.rglob('*.class')):
  info=zipfile.ZipInfo(str(path.relative_to(classes)));info.compress_type=zipfile.ZIP_DEFLATED;output.writestr(info,path.read_bytes())
modules=json.loads((ROOT/'server/26.3.lock.json').read_text())['modules']
spec={'menu_audio':False,'source':str(ROOT/'client/vulkan/bootstrap.cpp'),'param':str(ROOT/'client/vulkan/param.json'),'asset_dir':str(assets),'java_sources':[str(p)for p in sources],'modules':modules,'java_compile_classpath':[str(port),*[str(ROOT/'.tools/client'/row['file'])for row in lock['artifacts']if not row['id'].startswith('org.lwjgl:lwjgl:')]],'include_dirs':[str(work),str(ROOT/'client/native'),str(runtime/'java25/probe')]}
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
shutil.copyfile(ROOT/'build/client-ports/lwjgl-native/ps5/audit.json',java/'lwjgl-native-audit.json')
specfile=work/'probe-spec.json';specfile.write_text(json.dumps(spec,indent=2)+'\n')
# Prepare the normal JVM/core embedding first using the existing002 tool/spec.
# Its generated native-libc, registry, moduleimage and wrapper objects stay real.
# A temporary stub is never linked or generated: the bridge's external driver
# symbols are supplied by the final link below.
from package_client_gpu_link import finish
finish(runtime,args.java_home,work,assets,spec,gpu_support,gpu_audit,variant="vulkan",version="01.000.005")
