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
 unsetenv("PS5_OPENAL_TRACE_TEST_OTHER");assert(!client_startup_openal_getenv("PS5_OPENAL_TRACE_TEST_OTHER"));
 assert(setenv("PS5_OPENAL_TRACE_TEST_OTHER","unchanged",1)==0);
 assert(strcmp(client_startup_openal_getenv("PS5_OPENAL_TRACE_TEST_OTHER"),"unchanged")==0);
 assert(client_startup_openal_getenv("ALSOFT_DRIVERS")==getenv("ALSOFT_DRIVERS"));
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
    print('PASS private OpenAL trace lookup:level3 only,other environment forwarded,process state unchanged,ASan/UBSan;real pinned host OpenAL trace/control and actual device/context calls. PS5 pending.')
