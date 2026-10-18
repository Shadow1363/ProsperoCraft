#!/usr/bin/env python3
"""Validate exactly scoped diagnostic changes and run the PS5 report path on host."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
ROOT=Path(__file__).resolve().parents[1];JDK=Path('/opt/homebrew/opt/openjdk@25/bin');jars=ROOT/'build/assets/java25/jars'
lock=json.loads((ROOT/'server/26.3.lock.json').read_text())
original=jars/'server-26.3.jar';derived=jars/'ps5-platform-diagnostics.jar'
assert hashlib.sha256(original.read_bytes()).hexdigest()==next(r['sha256'] for r in lock['jars'] if r['file']=='server-26.3.jar')
with zipfile.ZipFile(original) as source,zipfile.ZipFile(derived) as output:
    changed=[]
    for name in output.namelist():
        if output.read(name)!=source.read(name):changed.append(name)
    assert set(changed)=={'META-INF/MANIFEST.MF','net/minecraft/SystemReport.class'},changed
    for name in set(source.namelist())-set(output.namelist()):
        upper=name.upper();assert upper.startswith('META-INF/') and (upper.endswith(('.SF','.RSA','.DSA','.EC')) or upper.startswith('META-INF/SIG-')),name
    assert not any(name.upper().endswith(('.SF','.RSA','.DSA','.EC')) for name in output.namelist())
cp=str(derived)+':'+':'.join(str(jars/r['file']) for r in lock['jars'] if r['file']!='server-26.3.jar')
subprocess.run([str(JDK/'javac'),'-cp',cp,'-d',str(ROOT/'build'),str(ROOT/'tools/test_platform_diagnostics.java')],check=True)
subprocess.run([str(JDK/'java'),'-Xint','-Xverify:all','-cp',str(ROOT/'build')+':'+cp,'test_platform_diagnostics'],check=True)
print('PASS: original artifact checksum intact; only SystemReport and unsigned-derivative manifest changed; other server resources/classes identical')
