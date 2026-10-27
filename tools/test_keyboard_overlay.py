#!/usr/bin/env python3
"""Raster the actual tiled keyboard; exercise layout and pixel guards under sanitizers."""
from pathlib import Path
import subprocess,tempfile,struct,zlib
R=Path(__file__).resolve().parents[1]
source=r'''
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include "keyboard_overlay.h"
int main(int argc,char**argv){
 for(int s=0;s<56;s++)for(int d=0;d<4;d++){int dirs[]={-1,1,-10,10};int n=prospero_keyboard_move(s,dirs[d]);assert(n>=0&&n<56);}
 for(int i=0;i<50;i++){assert(prospero_keyboard_character(i,1,0));assert(prospero_keyboard_character(i,1,1));}assert(prospero_keyboard_character(10,1,0)=='q');assert(prospero_keyboard_character(10,0,0)=='Q');assert(prospero_keyboard_character(48,1,0)=='(');
 unsigned sizes[][2]={{320,240},{800,600},{1280,720},{1600,900},{1920,1080},{2560,1440},{3840,2160},{1279,719}};
 for(unsigned n=0;n<sizeof(sizes)/sizeof(*sizes);n++){
  unsigned w=sizes[n][0],h=sizes[n][1];size_t bytes=(size_t)((w+127)/128)*((h+127)/128)*65536;uint8_t*allocation=malloc(bytes+128),*pixels=allocation+64;memset(allocation,0x5a,bytes+128);
  prospero_keyboard_state=(struct prospero_keyboard){0};prospero_keyboard_draw(pixels,w,h);for(size_t i=0;i<bytes;i++)assert(pixels[i]==0x5a);
  prospero_keyboard_state=(struct prospero_keyboard){.visible=true,.selected=11,.lower=1};strcpy(prospero_keyboard_state.preview,"mc.example.org:25565");prospero_keyboard_draw(pixels,w,h);
  for(int i=0;i<64;i++){assert(allocation[i]==0x5a);assert(pixels[bytes+i]==0x5a);}
  if(w==1920){FILE*f=fopen(argv[1],"wb");assert(f);fprintf(f,"P6\n%u %u\n255\n",w,h);for(unsigned y=0;y<h;y++)for(unsigned x=0;x<w;x++){uint32_t c=*(uint32_t*)(pixels+prospero_keyboard_offset(w,x,y));unsigned char rgb[]={c>>16,c>>8,c};fwrite(rgb,1,3,f);}fclose(f);}
  free(allocation);
 }
 puts("PASS actual keyboard layout/navigation and tiled raster at8 sizes under ASan/UBSan; hidden frame unchanged; guards intact; console pending");
}
'''
out=R/'build/keyboard-preview';out.mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='ps5-keyboard-')as folder:
 w=Path(folder);(w/'test.c').write_text(source)
 subprocess.run(['clang','-std=c11','-fsanitize=address,undefined','-I'+str(R/'client/ports/mesa'),str(w/'test.c'),'-o',str(w/'test')],check=True)
 subprocess.run([str(w/'test'),str(out/'keyboard.ppm')],check=True)
 subprocess.run(['sips','-s','format','png',str(out/'keyboard.ppm'),'--out',str(out/'keyboard.png')],check=True,stdout=subprocess.DEVNULL)
patch=(R/'client/ports/mesa/0007-videoout-keyboard-overlay.patch').read_text();assert 'wait_result==VK_SUCCESS' in patch and patch.index('prospero_keyboard_draw')<patch.index('sceVideoOutSubmitFlip')
assert 'sceVideoOutOpen'not in patch and 'malloc'not in patch
