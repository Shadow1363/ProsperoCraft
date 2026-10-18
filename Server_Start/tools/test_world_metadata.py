#!/usr/bin/env python3
"""Exercise the actual early metadata preflight, before any server initialization."""
from pathlib import Path
import subprocess
r=Path(__file__).resolve().parents[1];w=r/'build/world-metadata-test';w.mkdir(parents=True,exist_ok=True)
p=w/'WorldMetadataTest.java';p.write_text('''import java.nio.file.*;
public class WorldMetadataTest {
 public static void main(String[] args)throws Exception {
  Path root=Files.createTempDirectory("ps5-world-meta-");
  try {
   ServerStart25.checkWorldMetadata(root); // Missing world is allowed, not fabricated as an existing directory.
   if(Files.exists(root.resolve("world")))throw new AssertionError("Preflight created world");
   Files.createDirectory(root.resolve("world"));ServerStart25.checkWorldMetadata(root);Files.delete(root.resolve("world"));
   Files.writeString(root.resolve("world"),"file");ServerStart25.checkWorldMetadata(root);Files.delete(root.resolve("world")); // Official server retains validation policy.
   Files.createSymbolicLink(root.resolve("world"),Path.of("absent"));ServerStart25.checkWorldMetadata(root);Files.delete(root.resolve("world")); // Host lstat returns real link attributes.
   try{ServerStart25.checkWorldMetadata(root.resolve("missing-root"));throw new AssertionError("Missing root accepted");}
   catch(java.io.IOException expected){if(!expected.getMessage().contains("World metadata preflight (NOFOLLOW_LINKS)"))throw expected;}
   System.out.println("PASS: actual early world metadata preflight, genuine NOFOLLOW, missing world stays absent, official type/link policy retained, contextual IO failure");
  }finally{Files.deleteIfExists(root.resolve("world"));Files.delete(root);}
 }
}''')
jdk='/opt/homebrew/opt/openjdk@25/bin/';subprocess.run([jdk+'javac','-d',str(w),str(r/'server/java/ServerStart25.java'),str(p)],check=True);subprocess.run([jdk+'java','-cp',str(w),'WorldMetadataTest'],check=True)
