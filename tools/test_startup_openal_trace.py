#!/usr/bin/env python3
"""Check private trace lookup forwarding and real pinned OpenAL native logging."""
from pathlib import Path
import json
import os
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
pin = json.loads((ROOT/'client/ports/openal/sources.json').read_text())
source = ROOT/'.tools/openal-soft-src'
assert subprocess.check_output(['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True).strip() == pin['commit']
subprocess.run(['git', '-C', str(source), 'diff', '--exit-code', 'HEAD'], check=True)
library = ROOT/'build/openal-host/libopenal.dylib'
assert library.is_file(), 'Prepare pinned host OpenAL via build_openal_native.py --host'
assert 'Path work=Path.of("/download0/mc-client")'in (ROOT/'client/startup/ClientStartup25.java').read_text()
assert '-Duser.dir=/download0/mc-client'in (ROOT/'client/startup/bootstrap.cpp').read_text()
with tempfile.TemporaryDirectory(prefix='startup-openal-trace-') as temp:
    root = Path(temp)
    (root/'shim.c').write_text(r'''
#include <assert.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
extern char *client_startup_openal_getenv(const char*);
int main(void){
 assert(setenv("ALSOFT_LOGLEVEL","0",1)==0);errno=EBUSY;
 assert(strcmp(client_startup_openal_getenv("ALSOFT_LOGLEVEL"),"3")==0&&errno==EBUSY);
 assert(strcmp(getenv("ALSOFT_LOGLEVEL"),"0")==0);
 unsetenv("ALSOFT_LOCAL_PATH");assert(strcmp(client_startup_openal_getenv("ALSOFT_LOCAL_PATH"),"/download0/mc-client")==0);assert(!getenv("ALSOFT_LOCAL_PATH"));
 assert(setenv("ALSOFT_LOCAL_PATH","",1)==0);assert(strcmp(client_startup_openal_getenv("ALSOFT_LOCAL_PATH"),"/download0/mc-client")==0);
 assert(setenv("ALSOFT_LOCAL_PATH","/explicit/local-data",1)==0);assert(client_startup_openal_getenv("ALSOFT_LOCAL_PATH")==getenv("ALSOFT_LOCAL_PATH"));
 unsetenv("PS5_OPENAL_TRACE_TEST_OTHER");assert(!client_startup_openal_getenv("PS5_OPENAL_TRACE_TEST_OTHER"));
 assert(setenv("PS5_OPENAL_TRACE_TEST_OTHER","unchanged",1)==0);
 assert(strcmp(client_startup_openal_getenv("PS5_OPENAL_TRACE_TEST_OTHER"),"unchanged")==0);
 unsetenv("ALSOFT_DRIVERS");assert(strcmp(client_startup_openal_getenv("ALSOFT_DRIVERS"),"ps5")==0);assert(!getenv("ALSOFT_DRIVERS"));assert(setenv("ALSOFT_DRIVERS","",1)==0);assert(strcmp(client_startup_openal_getenv("ALSOFT_DRIVERS"),"ps5")==0);assert(setenv("ALSOFT_DRIVERS","null",1)==0);assert(client_startup_openal_getenv("ALSOFT_DRIVERS")==getenv("ALSOFT_DRIVERS"));
}
''')
    subprocess.run(['clang', '-std=c11', '-fsanitize=address,undefined', str(root/'shim.c'), str(ROOT/'client/startup/openal_trace_env.c'), '-o', str(root/'shim')], check=True)
    subprocess.run([str(root/'shim')], check=True)
    (root/'native.c').write_text(r'''
#include <stdio.h>
#include <AL/alc.h>
int main(void){
 ALCdevice *device=alcOpenDevice(NULL);
 printf("actual alcOpenDevice nonnull=%d error=%d\n",device!=NULL,alcGetError(device));
 if(device){
  ALCcontext *context=alcCreateContext(device,NULL);
  printf("actual alcCreateContext nonnull=%d error=%d\n",context!=NULL,alcGetError(device));
  if(context){printf("actual alcMakeContextCurrent=%d\n",alcMakeContextCurrent(context));alcMakeContextCurrent(NULL);alcDestroyContext(context);}
  printf("actual alcCloseDevice=%d\n",alcCloseDevice(device));
 }
}
''')
    subprocess.run(['clang', '-I'+str(source/'include'), str(root/'native.c'), '-L'+str(library.parent), '-lopenal', '-Wl,-rpath,'+str(library.parent), '-o', str(root/'native')], check=True)
    for level in ('0', '3'):
        env = dict(os.environ, ALSOFT_LOGLEVEL=level)
        # Keep backend/default-device selection identical across the control.
        env.pop('ALSOFT_LOGFILE', None)
        result = subprocess.run([str(root/'native')], env=env, capture_output=True, text=True, check=True, timeout=20)
        assert 'actual alcOpenDevice nonnull=' in result.stdout
        if level == '3':
            assert 'Initializing library' in result.stderr and 'Supported backends:' in result.stderr, result.stderr
            assert 'null' in result.stderr
            print(result.stdout.strip())
        else:
            assert 'Initializing library' not in result.stderr
    print('PASS private OpenAL configuration:trace3,explicit local path honored,missing/empty local path defaults to game workdir,other lookups forwarded,process environment unchanged,ASan/UBSan;actual pinned host trace/device/context controls. PS5 pending.')
