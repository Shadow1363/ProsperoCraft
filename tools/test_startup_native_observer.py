#!/usr/bin/env python3
"""Compile actual observer helper with controlled query results and real file IO."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
HARNESS=r'''
#include <sys/resource.h>
#include <cerrno>
#include <cassert>
#include <cstring>
#include <fstream>
#include <sstream>
static bool fail_queries;
static int usage_calls,flexible_calls,status_calls;
static int test_getrusage(int who,struct rusage* usage){
 ++usage_calls;assert(who==RUSAGE_SELF);
 if(fail_queries){errno=EACCES;return -1;}
 usage->ru_maxrss=123;usage->ru_minflt=7;usage->ru_majflt=2;
 usage->ru_utime.tv_sec=4;usage->ru_utime.tv_usec=9;return 0;
}
extern "C" int sceKernelAvailableFlexibleMemorySize(size_t* bytes){++flexible_calls;if(fail_queries)return -7;*bytes=1024;return 0;}
extern "C" unsigned ps5shaderc_fault_status(unsigned* errors){++status_calls;*errors=fail_queries?2:0;return fail_queries?9:15;}
#define getrusage test_getrusage
#include "observer_native.hpp"
#undef getrusage
int main(int argc,char** argv){
 assert(argc==3);errno=EDOM;
 assert(startup_observer::append(argv[1],94000,0)&&errno==EDOM);
 fail_queries=true;assert(startup_observer::append(argv[1],94003,1)&&errno==EDOM);
 assert(!startup_observer::append(argv[2],94004,1)&&errno==EDOM);
 assert(usage_calls==3&&flexible_calls==3&&status_calls==3);
 std::ifstream in(argv[1]);std::stringstream data;data<<in.rdbuf();auto s=data.str();
 assert(s.find("elapsed_ms=94000 phase=0 getrusage_rc=0 getrusage_errno=0 maxrss_raw=123")!=std::string::npos);
 assert(s.find("user_us=4000009 system_us=0 flexible_rc=0x00000000 flexible_bytes=1024 fault_owned_mask=0xf fault_query_errors=0x0")!=std::string::npos);
 assert(s.find("elapsed_ms=94003 phase=1 getrusage_rc=-1 getrusage_errno=")!=std::string::npos);
 assert(s.find("flexible_rc=0xfffffff9 flexible_bytes=0 fault_owned_mask=0x9 fault_query_errors=0x2")!=std::string::npos);
 assert(std::count(s.begin(),s.end(),'\n')==2);
}
'''
with tempfile.TemporaryDirectory(prefix='startup-native-observer-')as folder:
 w=Path(folder);source=w/'check.cpp';source.write_text('#include <algorithm>\n'+HARNESS)
 subprocess.run(['clang++','-std=c++17','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I'+str(ROOT/'client/startup'),str(source),'-o',str(w/'check')],check=True)
 subprocess.run([str(w/'check'),str(w/'report.log'),str(w)],check=True)
print('PASS actual native observer helper ASan/UBSan: raw query values/errors,phase/elapsed formatting,append/write failure and errno preservation;controlled query results,not PS5 resource validation')
