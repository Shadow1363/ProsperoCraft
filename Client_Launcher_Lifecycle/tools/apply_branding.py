#!/usr/bin/env python3
"""Apply user-selected ProsperoCraft title/icon to future consumer app packages."""
from pathlib import Path
import argparse,hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1];BRANDING=ROOT/'assets/branding'
def apply_app(app):
 app=Path(app);record=json.loads((BRANDING/'branding.json').read_text());icon=BRANDING/record['icon']
 assert hashlib.sha256(icon.read_bytes()).hexdigest()==record['icon_sha256']
 param=app/'sce_sys/param.json';data=json.loads(param.read_text());assert data['titleId']==record['title_id']
 for language,value in data['localizedParameters'].items():
  if isinstance(value,dict)and 'titleName'in value:value['titleName']=record['name']
 param.write_text(json.dumps(data,indent=2)+'\n');shutil.copyfile(icon,app/'sce_sys/icon0.png')
def apply_package(package,app=None):
 package=Path(package);record=json.loads((BRANDING/'branding.json').read_text());icon=BRANDING/record['icon'];assert hashlib.sha256(icon.read_bytes()).hexdigest()==record['icon_sha256'];temporary=package.with_suffix('.branding.tmp')
 if app is not None:apply_app(app)
 with zipfile.ZipFile(package)as source,zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED)as target:
  for info in source.infolist():
   data=source.read(info.filename)
   if info.filename==record['title_id']+'/sce_sys/param.json':
    value=json.loads(data);assert value['titleId']==record['title_id']
    for language,localized in value['localizedParameters'].items():
     if isinstance(localized,dict)and 'titleName'in localized:localized['titleName']=record['name']
    data=(json.dumps(value,indent=2)+'\n').encode()
   elif info.filename==record['title_id']+'/sce_sys/icon0.png':data=icon.read_bytes()
   target.writestr(info,data)
 with zipfile.ZipFile(temporary)as check:assert check.testzip()is None
 temporary.replace(package)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--package',type=Path,required=True);p.add_argument('--app-dir',type=Path);a=p.parse_args();apply_package(a.package,a.app_dir)
