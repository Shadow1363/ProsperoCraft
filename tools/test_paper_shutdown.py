#!/usr/bin/env python3
"""Exercise actual native Paper exit-evidence classifier with positive/fault cases."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1];work=root/'build/paper-shutdown-test';work.mkdir(exist_ok=True)
c=work/'check.cpp';c.write_text(r'''
#include "paper_shutdown.hpp"
#include <cassert>
int main(int n,char**v){assert(n==3);return paper_shutdown::clean(v[1],"current-run",std::atoi(v[2]))?0:1;}
'''.replace('#include <cassert>','#include <cassert>\n#include <cstdlib>'))
exe=work/'check';subprocess.run(['/usr/bin/clang++','-std=c++17','-fsanitize=address,undefined','-I'+str(root/'server/native'),str(c),'-o',str(exe)],check=True)
with tempfile.TemporaryDirectory(prefix='paper-exit-') as temp:
 p=Path(temp);(p/'world-paper-v1').mkdir();level=p/'world-paper-v1/level.dat';marker=p/'paper-stop-ready.txt';log=p/'server-console.log'
 def result(expected,code='0'):assert subprocess.run([str(exe),temp,code]).returncode==(0 if expected else 1)
 result(False);level.write_bytes(b'level');marker.write_text('MC_PAPER_EXPECT_EXIT0 current-run\n')
 good="MC_PAPER_EXPECT_EXIT0 checks complete\nPS5_PAPER_PLUGIN_DISABLED version=1.0.0\nHalted I/O scheduler for world 'minecraft:overworld'\nHalted I/O scheduler for world 'minecraft:the_nether'\nHalted I/O scheduler for world 'minecraft:the_end'\nAll RegionFile I/O tasks to complete\n"
 log.write_text(good);result(True);result(False,'70');marker.write_text('MC_PAPER_EXPECT_EXIT0 old-run\n');result(False)
 marker.write_text('MC_PAPER_EXPECT_EXIT0 current-run\n');log.write_text(good+'[Server thread/ERROR]: save failed\n');result(False)
 log.write_text(good+'[Server thread/WARN]: Failed to save player data\n');result(False)
 for missing in ['MC_PAPER_EXPECT_EXIT0 checks complete\n','PS5_PAPER_PLUGIN_DISABLED version=1.0.0\n',"Halted I/O scheduler for world 'minecraft:the_end'\n",'All RegionFile I/O tasks to complete\n']:
  log.write_text(good.replace(missing,''));result(False)
 log.write_text(good);level.write_bytes(b'');result(False)
 actual=root/'build/host-ServerStart25.log'
 if actual.exists() and 'MC_PAPER_EXPECT_EXIT0 checks complete' in actual.read_text():
  level.write_bytes(b'level');log.write_text(actual.read_text());result(True)
print('PASS: actual native Paper exit classifier: current-run marker, saved level, plugin disable, final world save, exit0; stale/missing/error/empty/nonzero cases reject')
