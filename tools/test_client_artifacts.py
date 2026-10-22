#!/usr/bin/env python3
"""Real-JVM client preflight and exact upstream PS5 platform rejection control."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--java-home', type=Path, required=True)
args = parser.parse_args()
java, javac = (args.java_home / 'bin' / name for name in ['java', 'javac'])
work = ROOT / 'build/client-tests'; work.mkdir(parents=True, exist_ok=True)
boundary = work / 'ClientPlatformBoundary.java'
boundary.write_text('''
import java.net.*;
import java.nio.file.*;
public class ClientPlatformBoundary {
 public static void main(String[] args) throws Exception {
  try (var loader = new URLClassLoader(new URL[]{Path.of(args[0]).toUri().toURL()}, ClassLoader.getPlatformClassLoader())) {
   System.setProperty("os.name", "PS5");
   try {
    Class.forName("org.lwjgl.system.Platform", true, loader);
    throw new AssertionError("Expected current upstream PS5 platform rejection");
   } catch (LinkageError failure) {
    if (!"Unknown platform: PS5".equals(failure.getMessage())) throw failure;
    System.out.println("KNOWN_CLIENT_PORT_BOUNDARY " + failure + "; upstream unchanged; no native API initialized");
   }
  }
 }
}
''')
subprocess.run([str(javac), '--release', '25', '-d', str(work), str(ROOT / 'client/java/ClientArtifactProbe25.java'), str(boundary)], check=True)
command = [str(java), '-Xverify:all', '-cp', str(work), 'ClientArtifactProbe25', str(ROOT / 'build/client')]
subprocess.run(command, check=True)
subprocess.run([str(java), '-Xverify:all', '-cp', str(work), 'ClientPlatformBoundary', str(ROOT / 'build/client/jars/lwjgl-3.4.3.jar')], check=True)
# A same-size artifact mutation must fail its hash check, not reach class loading.
client = ROOT / 'build/client/jars/client-26.3.jar'; original = client.read_bytes()
try:
    changed = bytearray(original); changed[-1] ^= 1; client.write_bytes(changed)
    failure = subprocess.run(command, capture_output=True, text=True)
    assert failure.returncode != 0 and 'Hash mismatch: client-26.3.jar' in failure.stderr
    assert 'MC_CLIENT_CLASS_OK' not in failure.stdout
finally:
    client.write_bytes(original)
audit = json.loads((ROOT / 'build/client/execution-audit.json').read_text())
assert audit['desktop_conditional_artifacts_staged'] == 0 and audit['project_game_transformations'] == []
print('PASS client preflight, real upstream PS5 rejection, corrupt artifact refusal, original client restored; console graphics/input/native bindings pending')
