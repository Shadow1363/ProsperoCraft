#!/usr/bin/env python3
"""Apply ProsperoCraft branding and project legal notices to future consumer packages."""
from pathlib import Path
import argparse,hashlib,json,shutil,zipfile,struct
ROOT=Path(__file__).resolve().parents[1];BRANDING=ROOT/'assets/branding'
def validate_background(data):
 assert len(data)==148+3840*2160 and data[:4]==b'DDS ', 'Expected single4KBC7DDS'
 assert struct.unpack_from('<I',data,4)[0]==124
 assert struct.unpack_from('<II',data,12)==(2160,3840)
 assert struct.unpack_from('<I',data,28)[0]in(0,1)
 assert struct.unpack_from('<I',data,76)[0]==32 and data[84:88]==b'DX10'
 assert struct.unpack_from('<I',data,112)[0]==0
 assert struct.unpack_from('<4I',data,128)==(98,3,0,1), 'Expected BC7_UNORM2Dsingle surface'
def presentation_assets():
 manifest=BRANDING/'presentation.json'
 if not manifest.exists():return {}
 record=json.loads(manifest.read_text());assert set(record['files'])=={'pic0.dds','pic1.dds'}
 assert record['background']=='prosperocraft-banner.dds'
 data=(BRANDING/record['background']).read_bytes();assert hashlib.sha256(data).hexdigest()==record['background_sha256'];validate_background(data)
 assert all(name==record['background']for name in record['files'].values())
 return {name:data for name in record['files']}
def project_notices():
 return {'licenses/ProsperoCraft-LICENSE-GPL-3.0.txt':(ROOT/'LICENSE').read_bytes(),
         'licenses/ProsperoCraft-NOTICE.txt':(ROOT/'NOTICE').read_bytes()}
def apply_app(app):
 app=Path(app);record=json.loads((BRANDING/'branding.json').read_text());icon=BRANDING/record['icon']
 assert hashlib.sha256(icon.read_bytes()).hexdigest()==record['icon_sha256']
 param=app/'sce_sys/param.json';data=json.loads(param.read_text());assert data['titleId']==record['title_id']
 for language,value in data['localizedParameters'].items():
  if isinstance(value,dict)and 'titleName'in value:value['titleName']=record['name']
 param.write_text(json.dumps(data,indent=2)+'\n');shutil.copyfile(icon,app/'sce_sys/icon0.png')
 for name,content in presentation_assets().items():(app/'sce_sys'/name).write_bytes(content)
 for relative,content in project_notices().items():
  path=app/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
def apply_package(package,app=None):
 package=Path(package);record=json.loads((BRANDING/'branding.json').read_text());icon=BRANDING/record['icon'];assert hashlib.sha256(icon.read_bytes()).hexdigest()==record['icon_sha256'];temporary=package.with_suffix('.branding.tmp')
 if app is not None:apply_app(app)
 notices={record['title_id']+'/'+p:data for p,data in project_notices().items()};notices.update({record['title_id']+'/sce_sys/'+name:data for name,data in presentation_assets().items()});seen=set()
 with zipfile.ZipFile(package)as source,zipfile.ZipFile(temporary,'w',zipfile.ZIP_DEFLATED)as target:
  for info in source.infolist():
   data=source.read(info.filename)
   if info.filename==record['title_id']+'/sce_sys/param.json':
    value=json.loads(data);assert value['titleId']==record['title_id']
    for language,localized in value['localizedParameters'].items():
     if isinstance(localized,dict)and 'titleName'in localized:localized['titleName']=record['name']
    data=(json.dumps(value,indent=2)+'\n').encode()
   elif info.filename==record['title_id']+'/sce_sys/icon0.png':data=icon.read_bytes()
   if info.filename in notices:data=notices[info.filename];seen.add(info.filename)
   target.writestr(info,data)
  for name,data in notices.items():
   if name not in seen:target.writestr(name,data)
 with zipfile.ZipFile(temporary)as check:assert check.testzip()is None
 temporary.replace(package)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--package',type=Path,required=True);p.add_argument('--app-dir',type=Path);a=p.parse_args();apply_package(a.package,a.app_dir)
