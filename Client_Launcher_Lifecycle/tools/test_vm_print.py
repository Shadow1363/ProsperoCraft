#!/usr/bin/env python3
"""Exercise the actual JNI print hook with real independent FILE streams."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1];W=ROOT/'build/vm-print-test';W.mkdir(parents=True,exist_ok=True)
s=(ROOT/'server/native/bootstrap.cpp').read_text();s=s[s.index('int vm_print('):s.index('void save_vm_failure(')]
cpp='''#include <cstdio>
#include <cstdarg>
#include <cassert>
#include <cstring>
FILE* startup_log=nullptr;
namespace ps5_vm_diagnostics { int calls=0; void capture(const char*,va_list){++calls;} }
'''+s+r'''
int print(FILE*f,const char*fmt,...){va_list a;va_start(a,fmt);int n=vm_print(f,fmt,a);va_end(a);return n;}
void check(FILE*f,const char*expected){rewind(f);char b[128]={};size_t n=fread(b,1,sizeof(b)-1,f);assert(n==strlen(expected)&&strcmp(b,expected)==0);}
int main(){
 startup_log=tmpfile();FILE*classes=tmpfile();assert(startup_log&&classes);
 assert(print(classes,"class %s %d\n","Loaded",23)==16);
 assert(ps5_vm_diagnostics::calls==0);check(classes,"class Loaded 23\n");
 assert(print(stderr,"failure %d\n",7)==10);assert(ps5_vm_diagnostics::calls==1);check(startup_log,"failure 7\n");
 fclose(classes);fclose(startup_log);startup_log=nullptr;
 assert(print(stdout,"ignored\n")==0);assert(ps5_vm_diagnostics::calls==2);
 puts("PASS: actual print hook keeps file/class log output separate; console capture/format counts retained");
}
'''
# Exact formatted length is 16 including newline.
p=W/'test.cpp';p.write_text(cpp)
subprocess.run(['/usr/bin/clang++','-std=c++20','-O1','-g','-fsanitize=address,undefined',str(p),'-o',str(W/'test')],check=True)
subprocess.run([str(W/'test')],check=True)
