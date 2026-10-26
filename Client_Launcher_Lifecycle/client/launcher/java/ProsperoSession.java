import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

/** Evidence for a single original Main call. Never mutates game classes/threads. */
public final class ProsperoSession {
 private final Path logs;private final String marker;
 public ProsperoSession(Path logs)throws IOException {
  this.logs=logs;marker="PS5_MAIN_SESSION "+UUID.randomUUID();
  Files.createDirectories(logs);
  Files.writeString(logs.resolve("latest.log"),"\n"+marker+"\n",StandardCharsets.UTF_8,StandardOpenOption.CREATE,StandardOpenOption.APPEND);
 }
 static final class Evidence {
  boolean current=false,stopping=false,failed=false;
  void line(String line,String marker){
   if(line.equals(marker)){current=true;stopping=false;failed=false;return;}
   if(!current)return;
   if(line.endsWith("/INFO]: Stopping!"))stopping=true;
   if(line.contains("/FATAL]")||line.contains("Reported exception thrown!")||line.contains("Unreported exception thrown!")||line.contains("Shutdown failure!")||line.contains("Failed to create window:")||line.contains("#@?@#"))failed=true;
  }
  boolean clean(boolean instanceStopped,boolean sdlStopped){return current&&stopping&&!failed&&instanceStopped&&sdlStopped;}
 }
 public void verifyCleanReturn(ClassLoader loader)throws ReflectiveOperationException,IOException {
  Evidence evidence=new Evidence();
  for(String name:List.of("previous-1.log","previous-2.log","latest.log")){
   Path file=logs.resolve(name);if(!Files.exists(file))continue;
   if(Files.size(file)>8*1024*1024)throw new IOException("Session log exceeds bounded shutdown audit");
   try(var lines=Files.newBufferedReader(file,StandardCharsets.UTF_8)){
    for(String line;(line=lines.readLine())!=null;)evidence.line(line,marker);
   }
  }
  Class<?> minecraft=Class.forName("net.minecraft.client.Minecraft",false,loader);
  Object instance=minecraft.getMethod("getInstance").invoke(null);
  boolean stopped=instance!=null&&Boolean.FALSE.equals(minecraft.getMethod("isRunning").invoke(instance));
  Class<?> sdl=Class.forName("org.lwjgl.sdl.SDLInit",false,loader);
  boolean sdlStopped=((Number)sdl.getMethod("SDL_WasInit",int.class).invoke(null,0)).longValue()==0;
  if(!evidence.clean(stopped,sdlStopped))throw new IllegalStateException("Original Main returned without verified clean shutdown;current="+evidence.current+" stopping="+evidence.stopping+" failure="+evidence.failed+" instanceStopped="+stopped+" sdlStopped="+sdlStopped);
 }
}
