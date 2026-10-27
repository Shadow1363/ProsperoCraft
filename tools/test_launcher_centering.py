#!/usr/bin/env python3
"""Measure rendered glyph pixels inside the actual native top-bar button boxes."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
import argparse
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--toolkit',action='store_true');args=parser.parse_args()
folder='launcher-toolkit-preview' if args.toolkit else 'launcher-preview'
for name,page in [('home',0),('settings',2),('signin',3)]:
 with Image.open(ROOT/'build'/folder/(name+'.png')).convert('RGB') as picture:
  for i,(x,w) in enumerate(zip((865,1245,1555),(350,280,280))):
   bg=(40,79,60) if i=={0:0,2:1,3:2}[page] else (23,46,36)
   points=[(xx,yy) for yy in range(62,110) for xx in range(x+10,x+w-10) if (min(picture.getpixel((xx,yy)))>140 if args.toolkit else picture.getpixel((xx,yy))!=bg)]
   assert points,(name,i,'no rendered label')
   left,right=min(p[0] for p in points),max(p[0] for p in points);top,bottom=min(p[1] for p in points),max(p[1] for p in points)
   # Pixel centers: inclusive ink bounds versus the button's inclusive bounds.
   assert abs((left+right)/2-(x+(w-1)/2))<=1.0,(name,i,'horizontal',left,right)
   assert abs((top+bottom)/2-(52+(68-1)/2))<=1.0,(name,i,'vertical',top,bottom)
print('PASS actual native rendered pixels centered within1px in all3top buttons across home/settings/account states')
