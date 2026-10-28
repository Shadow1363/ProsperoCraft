#!/usr/bin/env python3
"""Consumer namespace bindings for the Java runtime's optional genuine storage JNI builds."""
from pathlib import Path
import importlib.util,json,shutil
ROOT=Path(__file__).resolve().parents[1]
def build(runtime,offline=False):
 spec=importlib.util.spec_from_file_location('java25_storage',runtime/'tools/java25_native_storage.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 output=[];audits={};licenses={}
 for component,namespace,group,cache in [('zstd','dhcomgithubluben.zstd','ps5zstddh','zstd-jni-1.5.7-12'),('sqlite','dh_sqlite','ps5sqlitedh','sqlite-jdbc-3.53.2.1')]:
  source=ROOT/'.tools'/cache
  if offline and not source.exists():raise FileNotFoundError('Offline source cache missing: '+str(source))
  obj=module.build(component,namespace,False,source);output.append({'name':group,'objects':[str(obj)]});audits[component]=json.loads((obj.parent/'audit.json').read_text());licenses[component]=obj.parent/'source'
 return output,audits,licenses
