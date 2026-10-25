#!/usr/bin/env python3
"""Exercise real fault recorder delegation/restoration in isolated host children."""
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
HARNESS=r'''
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
int ps5shaderc_fault_begin(void);
void ps5shaderc_fault_end(void);
static void old_one(int sig){_exit(sig==SIGILL?73:75);}
static void old_three(int sig,siginfo_t*info,void*context){_exit(sig==SIGSEGV&&info&&context?74:76);}
int main(int argc,char**argv){
 if(argc!=2)return 1;
 struct sigaction action={0},current;
 action.sa_handler=old_one;sigemptyset(&action.sa_mask);sigaddset(&action.sa_mask,SIGUSR1);
 if(sigaction(SIGILL,&action,0))return 2;
 int mode=atoi(argv[1]);
 if(mode==2||mode==4){action.sa_sigaction=old_three;action.sa_flags=SA_SIGINFO;if(sigaction(SIGSEGV,&action,0))return 3;}
 if(ps5shaderc_fault_begin()!=4)return 4;
 if(mode==3||mode==4){
  if(ps5shaderc_fault_begin()!=4)return 8;
  ps5shaderc_fault_end(); // Compiler scope ends,outer startup scope remains.
  raise(mode==3?SIGILL:SIGSEGV);
 }
 if(mode==1)raise(SIGILL);
 if(mode==2)raise(SIGSEGV);
 if(ps5shaderc_fault_begin()!=4)return 5;
 ps5shaderc_fault_end();
 if(sigaction(SIGILL,0,&current)||current.sa_handler==old_one)return 6;
 ps5shaderc_fault_end();
 if(sigaction(SIGILL,0,&current)||current.sa_handler!=old_one||!sigismember(&current.sa_mask,SIGUSR1))return 7;
 ps5shaderc_fault_end();
 return 0;
}
'''
with tempfile.TemporaryDirectory(prefix='shaderc-fault-')as folder:
 w=Path(folder);(w/'test.c').write_text(HARNESS);report=w/'report.log'
 # Desktop ucontext layouts differ; test only four guaranteed initial words.
 # Target intentionally records96 raw words using its pinned SDK probe range.
 subprocess.run(['clang','-std=c11','-D_GNU_SOURCE','-Wall','-Wextra','-Werror','-DPS5_SHADERC_CONTEXT_WORDS=4','-DPS5_SHADERC_FAULT_LOG="'+str(report)+'"',str(ROOT/'client/ports/shaderc/fault.c'),str(w/'test.c'),'-pthread','-o',str(w/'test')],check=True)
 subprocess.run([str(w/'test'),'0'],check=True)
 for mode,code in [('1',73),('2',74),('3',73),('4',74)]:
  report.unlink(missing_ok=True)
  result=subprocess.run([str(w/'test'),mode]);assert result.returncode==code,result.returncode
  data=report.read_text();assert 'SHADERC FAULT signal='in data and 'SHADERC FAULT address='in data
  assert data.count('SHADERC FAULT context-word=')==4,data
 print('PASS real fault recorder: nested install/restoration/mask preservation,outer startup scope survives compiler end, SIGILL one-argument handler and SIGSEGV SA_SIGINFO delegation, bounded raw context written before original handler; no recovery. PS5 context capture pending.')
