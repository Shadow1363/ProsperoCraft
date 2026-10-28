#!/usr/bin/env python3
"""Check the complete source-built PS5 mod and its actual namespace-bound JNI APIs."""
from pathlib import Path
import json,hashlib,zipfile,subprocess
ROOT=Path(__file__).resolve().parents[1];RUNTIME=ROOT.parents[2];JDK=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
w=ROOT/'build/dh112-research';record=json.loads((ROOT/'dist/candidates/DistantHorizons-PS5-112/build.json').read_text());jar=ROOT/'dist/candidates/DistantHorizons-PS5-112'/record['artifact'];assert hashlib.sha256(jar.read_bytes()).hexdigest()==record['sha256']
metadata=json.loads((w/'metadata.json').read_text());original=w/next(f['filename']for f in metadata['files']if f['primary']);pin=next(f for f in metadata['files']if f['primary']);assert hashlib.sha512(original.read_bytes()).hexdigest()==pin['hashes']['sha512']
with zipfile.ZipFile(jar)as z:
 assert z.testzip()is None;mod=json.loads(z.read('fabric.mod.json'));assert mod['id']=='distanthorizons'and 'ps5.112'in mod['version'];assert 'com/seibel/distanthorizons/core/jar/EPlatform.class'in z.namelist()
(w/'PlatformCheck.java').write_text('''public class PlatformCheck{public static void main(String[]a)throws Exception{Class<?>p=Class.forName("com.seibel.distanthorizons.core.jar.EPlatform");Object value=p.getMethod("get").invoke(null);if(!value.toString().equals("PS5")||!(Boolean)p.getMethod("isUnix").invoke(value)||!p.getMethod("getArchitecture").invoke(null).toString().equals("X64"))throw new AssertionError(value);if(!System.getProperty("os.name").equals("PS5"))throw new AssertionError("OS identity changed");System.out.println("PASS source-built PS5 platform enum/Unix semantics/x86_64 while retaining true PS5 OS identity");}}''')
subprocess.run([str(JDK/'bin/javac'),'-d',str(w),str(w/'PlatformCheck.java')],check=True)
base=[str(JDK/'bin/java'),'-Dos.name=PS5','-Dos.arch=amd64','-cp']
old=subprocess.run([*base,str(w)+':'+str(original),'PlatformCheck'],capture_output=True,text=True);assert old.returncode!=0 and 'Unknown platform: ps5'in old.stderr
subprocess.run([*base,str(w)+':'+str(jar),'PlatformCheck'],check=True)
subprocess.run(['python3',str(RUNTIME/'tools/test_java25_native_storage.py'),'--jar',str(jar),'--zstd-namespace','dhcomgithubluben.zstd','--sqlite-namespace','dh_sqlite','--jdbc-protocol','dh_sqlite'],check=True)
print('PASS official mod hash preserved;full PS5 mod build contains explicit platform support;its actual JNI compression/database APIs pass against genuine native source builds. PS5 rendering/startup/save testing pending.')
