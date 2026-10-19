#!/usr/bin/env python3
"""Verify official execution/signatures, vanilla unsupported telemetry and ops JSON."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
r=Path(__file__).resolve().parents[1];j=Path('/opt/homebrew/opt/openjdk@25/bin');jars=r/'build/assets/java25/jars';lock=json.loads((r/'server/26.3.lock.json').read_text());w=r/'build/vanilla-test';w.mkdir(parents=True,exist_ok=True)
for record in lock['jars']:assert hashlib.sha256((jars/record['file']).read_bytes()).hexdigest()==record['sha256']
assert not (jars/'ps5-platform-diagnostics.jar').exists()
with zipfile.ZipFile(jars/'ps5-server-probe.jar') as probe:
 assert not any(n.startswith('net/minecraft/') or n=='ServerGameplay25.class' for n in probe.namelist())
header=(r/'build/server_classpath.hpp').read_text();assert '/jars/server-26.3.jar' in header and 'ps5-platform-diagnostics.jar' not in header
cp=str(jars/'ps5-server-probe.jar')+':'+':'.join(str(jars/v['file']) for v in lock['jars'])
(w/'VanillaTest.java').write_text('''import java.nio.file.*;import java.lang.reflect.*;import java.util.*;import com.google.gson.*;
public class VanillaTest {
 public static void main(String[] args)throws Exception {
  Class.forName("net.minecraft.SharedConstants").getMethod("tryDetectVersion").invoke(null);
  String old=System.getProperty("os.name");System.setProperty("os.name","PS5");
  Class<?> report=Class.forName("net.minecraft.SystemReport");String text=(String)report.getMethod("toLineSeparatedString").invoke(report.getConstructor().newInstance());
  if(!text.contains("Operating system not supported")||!text.contains("Memory (heap)")||!text.contains("JVM Flags"))throw new AssertionError(text);
  for(String name:List.of("net.minecraft.SystemReport","net.minecraft.server.MinecraftServer")) {
   Class<?> type=Class.forName(name);if(!type.getProtectionDomain().getCodeSource().getLocation().toString().endsWith("server-26.3.jar"))throw new AssertionError("Not official class: "+name);
   if(type.getSigners()==null||type.getSigners().length==0)throw new AssertionError("Missing original signature: "+name);
  }
  System.setProperty("os.name",old);System.setProperty("ps5.mc.opAll","true");
  Path root=Files.createTempDirectory("vanilla-ops-");
  try {
   Files.writeString(root.resolve("server.properties"),"online-mode=true\\nwhite-list=true\\n");
   String first="00000000-0000-4000-8000-000000000001",second="00000000-0000-4000-8000-000000000002";
   Files.writeString(root.resolve("whitelist.json"),"[{\\"uuid\\":\\""+first+"\\",\\"name\\":\\"TestPlayerOne\\"},{\\"uuid\\":\\""+second+"\\",\\"name\\":\\"TestPlayerTwo\\"}]");
   Files.writeString(root.resolve("ops.json"),"[{\\"uuid\\":\\"00000000-0000-4000-8000-000000000003\\",\\"name\\":\\"KeepAdmin\\",\\"level\\":2,\\"bypassesPlayerLimit\\":false}]");
   ServerOperators25.prepare(root);ServerOperators25.prepare(root);ServerOperators25.requireReady();
   JsonArray ops=JsonParser.parseString(Files.readString(root.resolve("ops.json"))).getAsJsonArray();if(ops.size()!=3)throw new AssertionError("Existing operator lost or duplicated");
   Class<?> notifications=Class.forName("net.minecraft.server.notifications.NotificationService");Object notify=java.lang.reflect.Proxy.newProxyInstance(notifications.getClassLoader(),new Class<?>[]{notifications},(p,m,a)->null);
   Class<?> listType=Class.forName("net.minecraft.server.players.ServerOpList"),idType=Class.forName("net.minecraft.server.players.NameAndId");Object list=listType.getConstructor(java.io.File.class,notifications).newInstance(root.resolve("ops.json").toFile(),notify);listType.getMethod("load").invoke(list);
   for(String id:List.of(first,second)) {
    Object identity=idType.getConstructor(UUID.class,String.class).newInstance(UUID.fromString(id),id.equals(first)?"TestPlayerOne":"TestPlayerTwo");
    Object entry=listType.getMethod("get",Object.class).invoke(list,identity);if(entry==null)throw new AssertionError("Vanilla OP load failed");
    Object permissions=entry.getClass().getMethod("permissions").invoke(entry);Class<?> permissionType=Class.forName("net.minecraft.server.permissions.LevelBasedPermissionSet");Object level=permissionType.getMethod("level").invoke(permissions);
    if((int)level.getClass().getMethod("id").invoke(level)!=4||(boolean)entry.getClass().getMethod("getBypassesPlayerLimit").invoke(entry))throw new AssertionError("Permission/limit policy");
   }
   String before=Files.readString(root.resolve("ops.json"));Files.writeString(root.resolve("whitelist.json"),"[{\\"uuid\\":\\"bad\\",\\"name\\":\\"BadPlayer\\"}]");
   try{ServerOperators25.prepare(root);throw new AssertionError("Invalid UUID accepted");}catch(IllegalArgumentException expected){}
   if(!before.equals(Files.readString(root.resolve("ops.json"))))throw new AssertionError("Failure damaged existing ops");
  }finally{try(var paths=Files.walk(root)){for(Path path:paths.sorted(Comparator.reverseOrder()).toList())Files.delete(path);}}
  System.out.println("PASS: original signed server classes; vanilla PS5 telemetry error handling; original OP-list loading, level4/no bypass, preservation/idempotence/failure safety");
 }
}''')
subprocess.run([str(j/'javac'),'-cp',cp,'-d',str(w),str(w/'VanillaTest.java')],check=True)
subprocess.run([str(j/'java'),'-Xmx176m','-cp',str(w)+':'+cp,'VanillaTest'],check=True,timeout=60)
print('PASS: all40 original JAR pins, no derivative/replacement classes and original-server execution classpath')
