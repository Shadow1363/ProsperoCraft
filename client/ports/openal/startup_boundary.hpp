/* SPDX-License-Identifier: MIT */
#pragma once
#include <atomic>
#include <cerrno>
#include <cstdio>
namespace client_openal_boundary {
inline std::atomic<unsigned> issued{0};
inline unsigned reserve() {
 unsigned count=issued.load(std::memory_order_relaxed);
 while(count<128)if(issued.compare_exchange_weak(count,count+1,std::memory_order_relaxed))return count+1;
 return 0;
}
inline void record(unsigned id,const char *phase,const char *api,const void *handle) {
 int saved=errno;
 std::fprintf(stderr,"PS5 OpenAL boundary id=%u phase=%s api=%s handle=%p\n",id,phase,api,handle);
 std::fflush(stderr);errno=saved;
}
struct Scope {
 unsigned id;const char *api;const void *handle;
 Scope(const char *name,const void *value):id(reserve()),api(name),handle(value){if(id)record(id,"enter",api,handle);}
 ~Scope(){if(id)record(id,"scope-exit",api,handle);}
};
}
