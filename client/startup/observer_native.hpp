/* SPDX-License-Identifier: GPL-3.0-or-later */
#pragma once
#include <cerrno>
#include <cstddef>
#include <cstdint>
#include <cstdio>
#include <fcntl.h>
#include <sys/resource.h>
#include <unistd.h>
extern "C" int sceKernelAvailableFlexibleMemorySize(size_t *);
extern "C" unsigned ps5shaderc_fault_status(unsigned *);
extern "C" int64_t sceKernelGetDirectMemorySize();
extern "C" int sceKernelAvailableDirectMemorySize(int64_t,int64_t,size_t,int64_t*,size_t*);
namespace startup_observer {
// Observation only;raw RSS units are intentionally unspecified. Query errors
// invalidate corresponding values. No limits,handlers or game state are changed.
inline bool append(const char* path,long long elapsed,int phase) {
 int saved_errno=errno;
 struct rusage usage{};errno=0;
 int usage_rc=getrusage(RUSAGE_SELF,&usage),usage_errno=usage_rc?errno:0;
 size_t flexible=0;int flexible_rc=sceKernelAvailableFlexibleMemorySize(&flexible);
 unsigned query_errors=0,owned=ps5shaderc_fault_status(&query_errors);
 int64_t direct_total=sceKernelGetDirectMemorySize(),direct_start=-1;size_t direct_largest=0;
 int direct_rc=direct_total>0?sceKernelAvailableDirectMemorySize(0,direct_total,16384,&direct_start,&direct_largest):-1;
 char line[2048];int length=std::snprintf(line,sizeof(line),
  "elapsed_ms=%lld phase=%d getrusage_rc=%d getrusage_errno=%d maxrss_raw=%lld minflt=%lld majflt=%lld user_us=%lld system_us=%lld flexible_rc=0x%08x flexible_bytes=%llu fault_owned_mask=0x%x fault_query_errors=0x%x direct_total=%lld direct_rc=0x%08x direct_largest=%llu direct_start=%lld",
  elapsed,phase,usage_rc,usage_errno,(long long)usage.ru_maxrss,
  (long long)usage.ru_minflt,(long long)usage.ru_majflt,
  (long long)usage.ru_utime.tv_sec*1000000+usage.ru_utime.tv_usec,
  (long long)usage.ru_stime.tv_sec*1000000+usage.ru_stime.tv_usec,
  (unsigned)flexible_rc,(unsigned long long)flexible,owned,query_errors,(long long)direct_total,(unsigned)direct_rc,(unsigned long long)direct_largest,(long long)direct_start);
 bool ok=length>0&&(size_t)length<sizeof(line);
 const int resources[]={RLIMIT_DATA,RLIMIT_AS,RLIMIT_RSS};
 const char* names[]={"data","as","rss"};
 for(unsigned i=0;ok&&i<3;++i){
  struct rlimit limit{};errno=0;int rc=getrlimit(resources[i],&limit),error=rc?errno:0;
  int added=std::snprintf(line+length,sizeof(line)-(size_t)length,
   " rlimit_%s_rc=%d rlimit_%s_errno=%d rlimit_%s_soft_raw=%llu rlimit_%s_hard_raw=%llu rlimit_%s_soft_infinite=%d rlimit_%s_hard_infinite=%d",
   names[i],rc,names[i],error,names[i],(unsigned long long)limit.rlim_cur,names[i],(unsigned long long)limit.rlim_max,
   names[i],rc==0&&limit.rlim_cur==RLIM_INFINITY,names[i],rc==0&&limit.rlim_max==RLIM_INFINITY);
  if(added<0||(size_t)added>=sizeof(line)-(size_t)length)ok=false;else length+=added;
 }
 if(ok&&length+1<(int)sizeof(line))line[length++]='\n';else ok=false;
 int fd=-1;
 if(ok)fd=::open(path,O_WRONLY|O_CREAT|O_APPEND,0600);
 if(fd<0)ok=false;
 size_t written=0;
 while(ok&&written<(size_t)length){ssize_t n=::write(fd,line+written,(size_t)length-written);if(n<0&&errno==EINTR)continue;if(n<=0){ok=false;break;}written+=(size_t)n;}
 if(fd>=0&&::close(fd)!=0)ok=false;
 errno=saved_errno;return ok;
}
}
