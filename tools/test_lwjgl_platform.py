#!/usr/bin/env python3
"""Test the real source-built LWJGL dependency port in isolated Java processes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--java-home', type=Path, required=True)
args = parser.parse_args()
work = ROOT / 'build/client-ports/lwjgl-tests';work.mkdir(parents=True, exist_ok=True)
source = work / 'LwjglPlatformTest.java'
source.write_text('''
import java.lang.reflect.*;
public class LwjglPlatformTest {
 public static void main(String[] args) throws Exception {
  System.setProperty("os.name", args[0]);
  System.setProperty("os.arch", args[1]);
  if (args[2].equals("reject")) {
   try { Class.forName("org.lwjgl.system.Platform"); throw new AssertionError("accepted non-x64 PS5"); }
   catch (LinkageError expected) {
    if (!expected.getMessage().startsWith("Unsupported PS5 architecture:")) throw expected;
   }
   System.out.println("PASS rejected PS5 architecture " + args[1]);return;
  }
  Class<?> platform = Class.forName("org.lwjgl.system.Platform");
  Object current = platform.getMethod("get").invoke(null);
  if (!((Enum<?>)current).name().equals(args[2])) throw new AssertionError("wrong platform " + current);
  if (!System.getProperty("os.name").equals(args[0])) throw new AssertionError("OS identity changed");
  String[] original = {"FREEBSD", "LINUX", "MACOSX", "WINDOWS", "PS5"};
  Object[] values = (Object[])platform.getMethod("values").invoke(null);
  for (int i=0;i<original.length;i++) if (!((Enum<?>)values[i]).name().equals(original[i])) throw new AssertionError("ordinal changed");
  if (args[2].equals("PS5")) {
   if (!platform.getMethod("getName").invoke(current).equals("PS5")) throw new AssertionError("display identity");
   Method map = platform.getDeclaredMethod("mapLibraryName",String.class);map.setAccessible(true);
   if (!map.invoke(current,"lwjgl").equals("liblwjgl.so")) throw new AssertionError("PS5 library name");
   if (!map.invoke(current,"/app0/libSDL3.so.0").equals("/app0/libSDL3.so.0")) throw new AssertionError("versioned path");
   Method path = platform.getDeclaredMethod("mapLibraryPathBundled",String.class);path.setAccessible(true);
   if (!path.invoke(null,"liblwjgl.so").equals("ps5/x64/liblwjgl.so")) throw new AssertionError("native resource path");

  }
  System.out.println("PASS real LWJGL platform " + args[0] + "/" + args[1] + " -> " + current + "; original ordinals/identity retained");
 }
}
''')
subprocess.run([str(args.java_home / 'bin/javac'), '--release', '25', '-d', str(work), str(source)], check=True)
jar = ROOT / 'build/client-ports/lwjgl/lwjgl-3.4.3-ps5-platform.jar'
for name, arch, expected in [('PS5','amd64','PS5'),('PS5','x86_64','PS5'),('PS5','aarch64','reject'),('PS5','x86','reject'),('FreeBSD','amd64','FREEBSD'),('Linux','amd64','LINUX'),('Mac OS X','aarch64','MACOSX'),('Windows 11','amd64','WINDOWS')]:
    subprocess.run([str(args.java_home / 'bin/java'), '-Xverify:all', '-cp', str(work)+':'+str(jar), 'LwjglPlatformTest', name, arch, expected], check=True)
audit = json.loads((jar.parent / 'audit.json').read_text())
original = ROOT / '.tools/client/lwjgl-3.4.3.jar'
assert hashlib.sha256(original.read_bytes()).hexdigest() == audit['original_sha256']
assert hashlib.sha256(jar.read_bytes()).hexdigest() == audit['output_sha256']
with zipfile.ZipFile(original) as base, zipfile.ZipFile(jar) as port:
    assert port.testzip() is None
    for name in base.namelist():
        if name not in audit['recompiled_classes']:assert base.read(name) == port.read(name), name
    expected = set(base.namelist()) | set(audit['recompiled_classes']) | {'META-INF/PS5-PORT-LICENSE.txt'}
    assert set(port.namelist()) == expected
    assert not any(name.startswith(('net/minecraft/','com/mojang/')) for name in port.namelist())
print('PASS exact dependency-only JAR delta and original immutable hash; PS5 native provider tested separately with actual core; no console client result')
