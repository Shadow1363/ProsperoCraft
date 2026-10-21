#pragma once
#include <cstdio>
#include <cstring>
#include <sys/stat.h>
// Only native file inspection is safe in the JNI exit hook: the VM has exited.
namespace paper_shutdown {
inline bool clean(const char* root,const char* run,int exit_code) {
 if(exit_code!=0)return false;
 char path[1024],expected[256],line[8192];
 std::snprintf(path,sizeof(path),"%s/paper-stop-ready.txt",root);
 FILE* file=std::fopen(path,"r");if(!file)return false;
 bool read=std::fgets(line,sizeof(line),file)!=nullptr;std::fclose(file);
 std::snprintf(expected,sizeof(expected),"MC_PAPER_EXPECT_EXIT0 %s\n",run);
 if(!read||std::strcmp(line,expected)!=0)return false;
 std::snprintf(path,sizeof(path),"%s/world-paper-v1/level.dat",root);
 struct stat info{};if(stat(path,&info)!=0||!S_ISREG(info.st_mode)||info.st_size<=0)return false;
 std::snprintf(path,sizeof(path),"%s/server-console.log",root);
 file=std::fopen(path,"r");if(!file)return false;
 bool stopping=false,disabled=false,saved=false,error=false;unsigned dimensions=0;
 while(std::fgets(line,sizeof(line),file)) {
  if(std::strstr(line,"MC_PAPER_EXPECT_EXIT0 checks complete"))stopping=true;
  if(!stopping)continue;
  if(std::strstr(line,"PS5_PAPER_PLUGIN_DISABLED version=1.0.0"))disabled=true;
  if(std::strstr(line,"Halted I/O scheduler for world 'minecraft:overworld'"))dimensions|=1;
  if(std::strstr(line,"Halted I/O scheduler for world 'minecraft:the_nether'"))dimensions|=2;
  if(std::strstr(line,"Halted I/O scheduler for world 'minecraft:the_end'"))dimensions|=4;
  if(std::strstr(line,"All RegionFile I/O tasks to complete"))saved=true;
  if(std::strstr(line,"/ERROR]")||std::strstr(line,"Exception stopping")||std::strstr(line,"Failed to save"))error=true;
 }
 bool ok=!std::ferror(file);std::fclose(file);return ok&&stopping&&disabled&&saved&&dimensions==7&&!error;
}
}
