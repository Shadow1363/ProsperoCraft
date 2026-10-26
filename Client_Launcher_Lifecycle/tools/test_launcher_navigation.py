#!/usr/bin/env python3
"""Execute the native launcher's actual input policy, including hold timing."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
source=r'''
#include <cassert>
#include "navigation.hpp"
int main(){
 prospero_menu::Navigation n;
 assert(n.sample(0x4000,255,128,true,1)==0); // held on entry cannot activate or move
 assert(n.sample(0,128,128,true,2)==0);
 assert(n.sample(0,165,128,true,3)==0); // dead zone
 assert(n.sample(0,184,128,true,4)==0x20);
 assert(n.sample(0x20,200,128,true,5)==0); // same D-pad + stick gives no second edge
 assert(n.sample(0,170,128,true,6)==0); // stay engaged below56, above28
 assert(n.sample(0,180,129,true,403)==0);assert(n.repeat(403)==0);
 assert(n.sample(0,180,129,true,404)==0);assert(n.repeat(404)==0x20);
 assert(n.sample(0,180,129,true,503)==0);assert(n.repeat(503)==0);
 assert(n.sample(0,180,129,true,504)==0);assert(n.repeat(504)==0x20);
 assert(n.sample(0,155,128,true,505)==0); // neutral releases
 assert(n.sample(0,180,128,true,506)==0); // doesn't re-engage in hysteresis band
 assert(n.sample(0,184,128,true,507)==0x20);
 assert(n.sample(0,128,128,true,508)==0);
 assert(n.sample(0,128,72,true,509)==0x10);
 assert(n.sample(0,128,128,true,510)==0);
 assert(n.sample(0,72,128,true,511)==0x80);
 assert(n.sample(0,128,128,true,512)==0);
 assert(n.sample(0,128,184,true,513)==0x40);
 assert(n.sample(0x80,128,184,true,514)==0x80); // D-pad precedence
 assert(n.sample(0x80004000,255,128,true,515)==0); // OS intercept clears all
 assert(n.sample(0x4000,255,128,true,516)==0);
 assert(n.sample(0,128,128,true,517)==0);
 assert(n.sample(0x4000,128,128,true,518)==0x4000);
 assert(n.sample(0,128,128,false,519)==0);
 assert(n.sample(0x4000,128,128,true,520)==0);
 assert(n.sample(0,128,128,true,521)==0);
 assert(n.sample(0xa0,128,128,true,522)==0); // opposing D-pad
 assert(n.repeat(900)==0&&!n.nav_armed&&!n.actions_armed); // stale samples
}
'''
with tempfile.TemporaryDirectory(prefix='launcher-navigation-') as folder:
 w=Path(folder);(w/'test.cpp').write_text(source)
 subprocess.run(['clang++','-std=c++20','-fsanitize=address,undefined','-I'+str(root/'client/launcher'),str(w/'test.cpp'),'-o',str(w/'test')],check=True)
 subprocess.run([str(w/'test')],check=True)
print('PASS actual native navigation: dead zone, all directions, hysteresis/neutral rearming, 400/100ms repeat, duplicate/opposed input, launch-held actions, disconnect/intercept/stale clearing')
