#!/usr/bin/env python3
"""Exercise the real bounded scope helper and private pinned native ALC unit."""
from pathlib import Path
import os
import re
import subprocess
import tempfile
from build_openal_startup_boundaries import build

ROOT=Path(__file__).resolve().parents[1]
library,audit=build(host=True)
with tempfile.TemporaryDirectory(prefix='openal-boundaries-')as temp:
 root=Path(temp)
 (root/'bounds.cpp').write_text(r'''
#include "startup_boundary.hpp"
#include <cassert>
#include <stdexcept>
#include <thread>
void run(){for(int i=0;i<100;i++){errno=EBUSY;{client_openal_boundary::Scope scope{"controlled",nullptr};assert(errno==EBUSY);}assert(errno==EBUSY);}}
int main(){try{client_openal_boundary::Scope s{"unwind",nullptr};throw std::runtime_error("control");}catch(const std::runtime_error&){}std::thread a{run},b{run},c{run};run();a.join();b.join();c.join();assert(client_openal_boundary::issued.load()==128);}
''')
 subprocess.run(['clang++','-std=c++17','-pthread','-fsanitize=address,undefined','-I'+str(ROOT/'client/ports/openal'),str(root/'bounds.cpp'),'-o',str(root/'bounds')],check=True)
 result=subprocess.run([str(root/'bounds')],capture_output=True,text=True,check=True,timeout=20)
 records=re.findall(r'PS5 OpenAL boundary id=(\d+) phase=(enter|scope-exit) api=(\S+)',result.stderr)
 assert len(records)==256
 for i in range(1,129):assert sorted(phase for n,phase,_ in records if int(n)==i)==['enter','scope-exit']
 assert 'api=unwind'in result.stderr and 'runtime error:'not in result.stderr
 (root/'calls.c').write_text(r'''
#include <dlfcn.h>
#include <stdio.h>
#include <assert.h>
#include <AL/alc.h>
int main(int argc,char **argv){
 void *lib=dlopen(argv[1],RTLD_NOW|RTLD_LOCAL);assert(lib);
 ALCdevice *(*openDevice)(const ALCchar*)=dlsym(lib,"alcOpenDevice");
 ALCenum (*getError)(ALCdevice*)=dlsym(lib,"alcGetError");
 const ALCchar *(*getString)(ALCdevice*,ALCenum)=dlsym(lib,"alcGetString");
 void (*getInteger)(ALCdevice*,ALCenum,ALCsizei,ALCint*)=dlsym(lib,"alcGetIntegerv");
 ALCcontext *(*createContext)(ALCdevice*,const ALCint*)=dlsym(lib,"alcCreateContext");
 ALCboolean (*makeCurrent)(ALCcontext*)=dlsym(lib,"alcMakeContextCurrent");
 void (*destroyContext)(ALCcontext*)=dlsym(lib,"alcDestroyContext");
 ALCboolean (*closeDevice)(ALCdevice*)=dlsym(lib,"alcCloseDevice");
 assert(openDevice&&getError&&getString&&getInteger&&createContext&&makeCurrent&&destroyContext&&closeDevice);
 ALCdevice *device=openDevice(NULL);assert(device);
 printf("open=1 error=%d name=%s\n",getError(device),getString(device,ALC_DEVICE_SPECIFIER));
 ALCint major=0;getInteger(device,ALC_MAJOR_VERSION,1,&major);printf("major=%d\n",major);
 ALCcontext *ctx=createContext(device,NULL);assert(ctx);printf("context=1 current=%d error=%d\n",makeCurrent(ctx),getError(device));
 makeCurrent(NULL);destroyContext(ctx);printf("close=%d\n",closeDevice(device));
}
''')
 subprocess.run(['clang','-I'+str(ROOT/'.tools/openal-soft-src/include'),str(root/'calls.c'),'-o',str(root/'calls')],check=True)
 results=[]
 for lib in [ROOT/'build/openal-host/libopenal.dylib',library]:
  env=dict(os.environ,ALSOFT_LOGLEVEL='0');env.pop('ALSOFT_LOGFILE',None)
  result=subprocess.run([str(root/'calls'),str(lib)],capture_output=True,text=True,check=True,timeout=30);results.append(result)
 assert results[0].stdout==results[1].stdout
 assert 'PS5 OpenAL boundary'not in results[0].stderr
 for name in audit['functions']:
  assert 'phase=enter api='+name in results[1].stderr and 'phase=scope-exit api='+name in results[1].stderr,name
 print(results[1].stdout.strip())
 print('PASS actual private pinned OpenAL ALC unit:all5body scope pairs,baseline device/error/name/version/context/current/close results unchanged;actual helper128scope cap,4threads,exception unwinding,errno under ASan/UBSan. PS5 behavior pending.')
