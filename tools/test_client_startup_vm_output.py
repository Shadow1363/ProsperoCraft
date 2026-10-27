#!/usr/bin/env python3
"""Exercise the shipped VM print callback with actual embedded HotSpot logging."""
from pathlib import Path
import argparse
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--java-home', type=Path, required=True)
a = p.parse_args()
current = (ROOT/'client/startup/bootstrap.cpp').read_text()
old = subprocess.check_output(['git', 'show', 'a751f330df4dc5a1ebc989d8c7477ee92e3a0aad:client/startup/bootstrap.cpp'], cwd=ROOT, text=True)
flag = re.search(r'"(-Xlog:gc=info,safepoint=info:[^"]+)"', current).group(1)
with tempfile.TemporaryDirectory(prefix='startup-vm-output-') as temp:
    root = Path(temp)
    (root/'GcFixture.java').write_text('public class GcFixture{public static void main(String[]a){byte[][]k=new byte[32][];for(int i=0;i<512;i++)k[i%32]=new byte[1024*1024];System.gc();}}')
    subprocess.run([str(a.java_home/'bin/javac'), '--release', '25', '-d', str(root), str(root/'GcFixture.java')], check=True)
    for historical, source in ((True, old), (False, current)):
        callback = re.search(r'int vm_print\(FILE \*.*?\n}', source, re.S).group(0)
        cpp = root/('old.cpp' if historical else 'fixed.cpp')
        cpp.write_text('''#include <jni.h>
#include <cstdio>
#include <cstdarg>
#include <cerrno>
#include <cassert>
#include <string>
FILE *startup_log=nullptr;
''' + callback + r'''
int call(FILE *file,const char *format,...){va_list args;va_start(args,format);int n=vm_print(file,format,args);va_end(args);return n;}
int main(int argc,char **argv){
 startup_log=std::fopen(argv[1],"w+");assert(startup_log);
 assert(call(stdout,"console-out %d\n",7)>0);assert(call(stderr,"console-err\n")>0);
 FILE *dedicated=std::fopen(argv[2],"w+");assert(dedicated);
 assert(call(dedicated,"dedicated %d\n",9)==12);
 std::fclose(dedicated);
 std::string cp="-Djava.class.path="+std::string(argv[3]);
 JavaVMOption options[]={{const_cast<char*>("-Xint"),nullptr},{const_cast<char*>("-Xms16m"),nullptr},{const_cast<char*>("-Xmx256m"),nullptr},{const_cast<char*>("-XX:+UseSerialGC"),nullptr},{argv[4],nullptr},{cp.data(),nullptr},{const_cast<char*>("vfprintf"),reinterpret_cast<void*>(&vm_print)}};
 JavaVMInitArgs args{};args.version=JNI_VERSION_1_8;args.nOptions=sizeof(options)/sizeof(options[0]);args.options=options;
 JavaVM *vm=nullptr;JNIEnv *env=nullptr;assert(JNI_CreateJavaVM(&vm,reinterpret_cast<void**>(&env),&args)==JNI_OK);
 jclass cls=env->FindClass("GcFixture");assert(cls);jmethodID method=env->GetStaticMethodID(cls,"main","([Ljava/lang/String;)V");assert(method);
 auto strings=env->NewObjectArray(0,env->FindClass("java/lang/String"),nullptr);env->CallStaticVoidMethod(cls,method,strings);assert(!env->ExceptionCheck());
 assert(vm->DestroyJavaVM()==JNI_OK);std::fclose(startup_log);
}
''')
        executable = cpp.with_suffix('')
        subprocess.run(['clang++', '-std=c++17', '-Wall', '-Wextra', '-Wno-unused-parameter', '-I'+str(a.java_home/'include'), '-I'+str(a.java_home/'include/darwin'), str(cpp), '-L'+str(a.java_home/'lib/server'), '-ljvm', '-Wl,-rpath,'+str(a.java_home/'lib/server'), '-o', str(executable)], check=True)
        for rotate in (False, True):
            case = root/('old-runs' if historical else 'fixed-runs')/('rotated' if rotate else 'exact')
            case.mkdir(parents=True)
            console, dedicated, gc = (case/name for name in ('console.log', 'dedicated.log', 'gc.log'))
            option = flag.replace('/download0/java25-gc.log', str(gc))
            if rotate:
                option = option.replace('filesize=4M', 'filesize=1K')
            subprocess.run([str(executable), str(console), str(dedicated), str(root), option], check=True, capture_output=True, text=True, timeout=45)
            text = console.read_text()
            assert 'console-out 7\n' in text and 'console-err\n' in text
            if historical:
                assert dedicated.read_bytes() == b'' and gc.read_bytes() == b''
                assert 'dedicated 9\n' in text and '[gc' in text and 'Pause Full (System.gc())' in text
            else:
                assert dedicated.read_text() == 'dedicated 9\n'
                assert '[gc' not in text and '[safepoint' not in text and 'dedicated 9\n' not in text
                logs = list(case.glob('gc.log*'))
                combined = ''.join(log.read_text() for log in logs)
                assert '[gc' in combined and '[safepoint' in combined
                assert '[class,load' not in combined and '[class,init' not in combined and '[debug]' not in combined
                if rotate:
                    assert {log.name for log in logs} == {'gc.log', 'gc.log.0'}
                else:
                    assert 'Pause Full (System.gc())' in combined and '[gc,heap' not in combined
    print('PASS actual embedded JVM:055 callback reproduces empty dedicated/GC files;fixed callback preserves console capture,dedicated FILE,GC/safepoints and bounded rollover. Host only;PS5 pending.')
