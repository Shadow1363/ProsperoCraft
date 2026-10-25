#!/usr/bin/env python3
"""Compile actual observer helper with controlled query results and real file IO."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
HARNESS=r'''
#include <sys/resource.h>
#include <cstdint>
#include <cerrno>
#include <cassert>
#include <cstring>
#include <fstream>
#include <sstream>
static bool fail_queries,invalid_total;
static int limit_calls,direct_calls;
static int usage_calls,flexible_calls,status_calls;
static int test_getrusage(int who,struct rusage* usage){
 ++usage_calls;assert(who==RUSAGE_SELF);
 if(fail_queries){errno=EACCES;return -1;}
 usage->ru_maxrss=123;usage->ru_minflt=7;usage->ru_majflt=2;
 usage->ru_utime.tv_sec=4;usage->ru_utime.tv_usec=9;return 0;
}
extern "C" int sceKernelAvailableFlexibleMemorySize(size_t* bytes){++flexible_calls;if(fail_queries)return -7;*bytes=1024;return 0;}
extern "C" unsigned ps5shaderc_fault_status(unsigned* errors){++status_calls;*errors=fail_queries?2:0;return fail_queries?9:15;}
static int test_getrlimit(int resource,struct rlimit* limit){
 ++limit_calls;assert(resource==RLIMIT_DATA||resource==RLIMIT_AS||resource==RLIMIT_RSS);
 if(fail_queries){errno=EACCES;return -1;}
 limit->rlim_cur=resource==RLIMIT_AS?RLIM_INFINITY:100;limit->rlim_max=RLIM_INFINITY;return 0;
}
extern "C" int64_t sceKernelGetDirectMemorySize(){return invalid_total?-5:INT64_C(17179869184);}
extern "C" int sceKernelAvailableDirectMemorySize(int64_t start,int64_t end,size_t alignment,int64_t* position,size_t* bytes){
 ++direct_calls;assert(start==0&&end==INT64_C(17179869184)&&alignment==16384);
 if(fail_queries)return -8;*position=16384;*bytes=UINT64_C(8589934592);return 0;
}
#define getrlimit test_getrlimit
#define getrusage test_getrusage
#include "observer_native.hpp"
#undef getrusage
int main(int argc,char** argv){
 assert(argc==3);errno=EDOM;
 assert(startup_observer::append(argv[1],94000,0)&&errno==EDOM);
 fail_queries=true;assert(startup_observer::append(argv[1],94003,1)&&errno==EDOM);
 invalid_total=true;assert(startup_observer::append(argv[1],94004,0)&&errno==EDOM);
 assert(!startup_observer::append(argv[2],94005,1)&&errno==EDOM);
 assert(usage_calls==4&&flexible_calls==4&&status_calls==4&&limit_calls==12&&direct_calls==2);
 std::ifstream in(argv[1]);std::stringstream data;data<<in.rdbuf();auto s=data.str();
 assert(s.find("elapsed_ms=94000 phase=0 getrusage_rc=0 getrusage_errno=0 maxrss_raw=123")!=std::string::npos);
 assert(s.find("user_us=4000009 system_us=0 flexible_rc=0x00000000 flexible_bytes=1024 fault_owned_mask=0xf fault_query_errors=0x0")!=std::string::npos);
 assert(s.find("elapsed_ms=94003 phase=1 getrusage_rc=-1 getrusage_errno=")!=std::string::npos);
 assert(s.find("flexible_rc=0xfffffff9 flexible_bytes=0 fault_owned_mask=0x9 fault_query_errors=0x2")!=std::string::npos);
 assert(s.find("direct_total=17179869184 direct_rc=0x00000000 direct_largest=8589934592 direct_start=16384")!=std::string::npos);
 assert(s.find("direct_rc=0xfffffff8 direct_largest=0 direct_start=-1")!=std::string::npos);
 assert(s.find("direct_total=-5 direct_rc=0xffffffff direct_largest=0 direct_start=-1")!=std::string::npos);
 assert(s.find("rlimit_data_rc=0 rlimit_data_errno=0 rlimit_data_soft_raw=100")!=std::string::npos);
 assert(s.find("rlimit_as_soft_infinite=1 rlimit_as_hard_infinite=1")!=std::string::npos);
 assert(s.find("rlimit_data_rc=-1 rlimit_data_errno=")!=std::string::npos);
 assert(std::count(s.begin(),s.end(),'\n')==3);
}
'''
with tempfile.TemporaryDirectory(prefix='startup-native-observer-')as folder:
 w=Path(folder);source=w/'check.cpp';source.write_text('#include <algorithm>\n'+HARNESS)
 subprocess.run(['clang++','-std=c++17','-Wall','-Wextra','-Werror','-fsanitize=address,undefined','-I'+str(ROOT/'client/startup'),str(source),'-o',str(w/'check')],check=True)
 subprocess.run([str(w/'check'),str(w/'report.log'),str(w)],check=True)
print('PASS actual native observer helper ASan/UBSan: raw resource/limit/direct-range values/errors/infinity/invalid-total skip,phase/elapsed formatting,append/write failure and errno preservation;controlled query results,not PS5 resource validation')
