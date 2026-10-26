/* SPDX-License-Identifier: GPL-3.0-or-later */
#pragma once
extern "C" int sceSystemServiceLoadExec(const char*,const char*const*);
namespace prospero_session {
// Success replaces the process and never returns. Any return is failure.
// OS replacement is the ownership barrier for retained WSI/cursor/audio memory,
// native worker threads, the one supported JVM and game classloader statics.
inline int restart_library(){
 const char* arguments[]={"--prospero-library",nullptr};
 return sceSystemServiceLoadExec("/app0/eboot.bin",arguments);
}
}
