#!/usr/bin/env python3
"""Convert supplied banner to PS5 BC7 DDS; preserve source and plain system title."""
from pathlib import Path
import argparse,hashlib,json,subprocess,shutil
from PIL import Image,ImageOps
ROOT=Path(__file__).resolve().parents[1]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--banner',type=Path,required=True);p.add_argument('--bc7enc',type=Path,required=True);p.add_argument('--encoder-source',type=Path,required=True);a=p.parse_args()
 dest=ROOT/'assets/branding';work=ROOT/'build/presentation-assets';work.mkdir(parents=True,exist_ok=True)
 original=dest/'prosperocraft-banner-source.png'
 if a.banner.resolve()!=original.resolve():shutil.copyfile(a.banner,original)
 with Image.open(original)as source:
  source.load();size=source.size;image=ImageOps.fit(source.convert('RGB'),(3840,2160),Image.Resampling.LANCZOS)
 image.save(work/'banner-4k.png');output=dest/'prosperocraft-banner.dds'
 subprocess.run([str(a.bc7enc.resolve()),'-q','-g',str(work/'banner-4k.png'),str(output)],check=True)
 from apply_branding import validate_background
 validate_background(output.read_bytes())
 revision=subprocess.check_output(['git','-C',str(a.encoder_source),'rev-parse','HEAD'],text=True).strip()
 record={'source':original.name,'source_sha256':sha(original),'source_size':size,'provenance':'User-supplied Minecraft-themed banner; underlying artwork retains its original rights. No AI redraw.','processing':'RGB Lanczos center-fit to3840x2160, then BC7_UNORM DX10 DDS; one2Dsurface, no mip chain','encoder':{'project':'https://github.com/richgel999/bc7enc_rdo','revision':revision,'mode':'portable C++ BC7, non-RDO default quality; -q -g','binary_sha256':sha(a.bc7enc)},'background':output.name,'background_sha256':sha(output),'files':{'pic0.dds':output.name,'pic1.dds':output.name},'title':'System-rendered ProsperoCraft text; title PNG not packaged, per user choice','preview_sha256':sha(work/'banner-4k.png'),'console':'Pending actual selected-title and launch display; shell may cache old presentation assets'}
 (dest/'presentation.json').write_text(json.dumps(record,indent=2)+'\n');print('PASS3840x2160BC7 presentation asset and source/encoder hashes',sha(output))
if __name__=='__main__':main()
