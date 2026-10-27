#!/usr/bin/env python3
"""Decode real BC7 image and check application/ZIP branding insertions and preservation."""
from pathlib import Path
import hashlib,json,math,shutil,tempfile,zipfile
from PIL import Image,ImageChops,ImageStat,ImageOps
from apply_branding import apply_app,apply_package,validate_background,presentation_assets,BRANDING
R=Path(__file__).resolve().parents[1];meta=json.loads((BRANDING/'presentation.json').read_text())
sha=lambda b:hashlib.sha256(b).hexdigest()
assert sha((BRANDING/meta['source']).read_bytes())==meta['source_sha256']
data=(BRANDING/meta['background']).read_bytes();validate_background(data)
with Image.open(BRANDING/meta['source'])as original:
 expected=ImageOps.fit(original.convert('RGB'),(3840,2160),Image.Resampling.LANCZOS)
with Image.open(BRANDING/meta['background'])as image:
 assert image.size==(3840,2160);decoded=image.convert('RGB');decoded.save(R/'build/presentation-assets/banner-decoded.png')
rms=ImageStat.Stat(ImageChops.difference(expected,decoded)).rms;mse=sum(v*v for v in rms)/3;psnr=10*math.log10(255*255/mse)if mse else float('inf');assert psnr>35,psnr
with tempfile.TemporaryDirectory(prefix='prospero-presentation-')as folder:
 w=Path(folder);app=w/'PPSA99874';(app/'sce_sys').mkdir(parents=True);shutil.copy2(R/'client/startup/param.json',app/'sce_sys/param.json');(app/'sce_sys/icon0.png').write_bytes(b'old icon');(app/'keep.bin').write_bytes(b'unrelated executable fixture')
 package=w/'test.zip'
 with zipfile.ZipFile(package,'w')as z:
  for p in app.rglob('*'):
   if p.is_file():z.write(p,str(p.relative_to(w)))
 apply_app(app);apply_package(package);apply_package(package)
 with zipfile.ZipFile(package)as z:
  assert z.testzip()is None
  assert len(z.namelist())==len(set(z.namelist()))
  for name,pixels in presentation_assets().items():assert z.read('PPSA99874/sce_sys/'+name)==pixels==(app/'sce_sys'/name).read_bytes()
  assert json.loads(z.read('PPSA99874/sce_sys/param.json'))['localizedParameters']['en-US']['titleName']=='ProsperoCraft'
  assert z.read('PPSA99874/keep.bin')==b'unrelated executable fixture'
  assert z.read('PPSA99874/sce_sys/icon0.png')==(BRANDING/'icon0.png').read_bytes()
  assert not any('title.png'in n for n in z.namelist())
print(f'PASS real4KBC7header/decode, PSNR{psnr:.2f}dB, source pins, app and ZIP paired backgrounds, idempotence, plain title, retained icon and unrelated bytes')
