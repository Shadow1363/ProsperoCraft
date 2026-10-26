#!/usr/bin/env python3
"""Verify actual mmap/mprotect/execute/unmap and adapter fault paths;not FFI ABI."""
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[1];w=ROOT/'build/ffi-wx-host-026';w.mkdir(exist_ok=True);port=ROOT/'client/ports/libffi';include=ROOT/'build/libffi-host/target/include'
subprocess.run(['clang','-std=c11','-O1','-g','-fsanitize=undefined','-I'+str(include),'-Dmmap=test_mmap','-Dmprotect=test_mprotect','-Dmunmap=test_munmap','-c',str(port/'closures_wx.c'),'-o',str(w/'adapter.o')],check=True)
subprocess.run(['clang','-std=c11','-O1','-g','-fsanitize=undefined','-I'+str(include),str(port/'test_closures_wx.c'),str(w/'adapter.o'),'-o',str(w/'test')],check=True)
subprocess.run([str(w/'test')],check=True)
