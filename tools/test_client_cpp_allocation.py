#!/usr/bin/env python3
"""Check paired consumer C++ allocation operators from the unchanged SDK source."""
import argparse,subprocess,tempfile
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--runtime-workspace',type=Path,required=True);a=p.parse_args()
source=a.runtime_workspace/'.tools/native-app/tooling/native/app_cpp_runtime.cpp'
TEST=r'''
#include <new>
#include <cstdlib>
#include <cstdint>
#include <cassert>
#include <cstring>
static unsigned allocations,frees,aligned;
static bool fail;
extern "C" void* clientgpu___wrap_malloc(std::size_t n){if(fail)return nullptr;void*p=std::malloc(n);if(p)++allocations;return p;}
extern "C" void clientgpu___wrap_free(void*p){if(p){++frees;std::free(p);}}
extern "C" int clientgpu___wrap_posix_memalign(void**p,std::size_t a,std::size_t n){if(fail)return 12;int e=posix_memalign(p,a,n);if(!e){++allocations;++aligned;}return e;}
int main(){
 unsigned base=allocations-frees;
 void*p=::operator new[](1024*1024);assert(p);std::memset(p,0x5a,1024*1024);assert(((unsigned char*)p)[1024*1024-1]==0x5a);::operator delete[](p);
 p=::operator new(0);assert(p);::operator delete(p);
 p=::operator new[](64,std::nothrow);assert(p);::operator delete[](p,std::nothrow);
 p=::operator new(4096,std::align_val_t(4096));assert(p&&!(reinterpret_cast<std::uintptr_t>(p)&4095));::operator delete(p,std::align_val_t(4096));
 p=::operator new[](4096,std::align_val_t(256),std::nothrow);assert(p&&!(reinterpret_cast<std::uintptr_t>(p)&255));::operator delete[](p,std::align_val_t(256),std::nothrow);
 fail=true;assert(::operator new(32,std::nothrow)==nullptr);assert(::operator new[](32,std::align_val_t(64),std::nothrow)==nullptr);fail=false;
 assert(aligned==2&&allocations-frees==base);
 return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='cpp-pair-')as folder:
 w=Path(folder);(w/'test.cpp').write_text(TEST)
 subprocess.run(['clang++','-std=c++20','-fno-exceptions','-fno-rtti','-fno-builtin','-Dmalloc=clientgpu___wrap_malloc','-Dfree=clientgpu___wrap_free','-Dposix_memalign=clientgpu___wrap_posix_memalign','-c',str(source),'-o',str(w/'operators.o')],check=True)
 subprocess.run(['clang++','-std=c++20','-fno-exceptions','-fno-builtin',str(w/'test.cpp'),str(w/'operators.o'),'-o',str(w/'test')],check=True)
 subprocess.run([str(w/'test')],check=True)
 print('PASS unchanged SDK C++ operators with paired consumer providers:1MiB array/write/free,zero-size,nothrow allocation+failure,aligned new/delete256/4096,and balanced ownership. Host providers use real host allocation; target direct-memory backend remains console pending.')
