import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.zip.GZIPInputStream;

/** Read-only, bounded vanilla world/server discovery. No game classes or rewrites. */
final class ProsperoDestinations {
 record Entry(String kind,String target,String name){}
 static String label(String text){return text==null?"":text.replaceAll("[\\p{Cntrl}]"," ").strip().substring(0,Math.min(80,text.replaceAll("[\\p{Cntrl}]"," ").strip().length()));}
 static boolean valid(String kind,String target){return target!=null&&!target.isBlank()&&target.length()<=255&&!target.chars().anyMatch(c->Character.isISOControl(c))&&(kind.equals("WORLD")?!target.equals(".")&&!target.equals("..")&&!target.contains("/")&&!target.contains("\\"):kind.equals("SERVER")&&!target.chars().anyMatch(Character::isWhitespace));}
 static List<Entry> read(Path game)throws IOException {
  for(Path p=game;p!=null&&p.startsWith(game.getParent().getParent());p=p.getParent())if(Files.isSymbolicLink(p))throw new IOException("Instance storage contains an unexpected link");
  List<Entry> result=new ArrayList<>();Path saves=game.resolve("saves");
  if(!Files.isSymbolicLink(saves)&&Files.isDirectory(saves))try(var dirs=Files.list(saves)){
   for(Path world:dirs.limit(512).sorted().toList())if(!Files.isSymbolicLink(world)&&Files.isDirectory(world)&&Files.isRegularFile(world.resolve("level.dat"),LinkOption.NOFOLLOW_LINKS)){
    String target=world.getFileName().toString(),name=target;if(!valid("WORLD",target))continue;
    try{Object data=nbt(world.resolve("level.dat"));if(data instanceof Map<?,?> m&&m.get("Data")instanceof Map<?,?> d&&d.get("LevelName")instanceof String title&&!title.isBlank())name=title;}catch(IOException malformed){}
    result.add(new Entry("WORLD",target,label(name)));
   }
  }
  Path servers=game.resolve("servers.dat");if(Files.isRegularFile(servers,LinkOption.NOFOLLOW_LINKS))try{
   Object data=nbt(servers);if(data instanceof Map<?,?> map&&map.get("servers")instanceof List<?> list)for(Object item:list){if(result.size()>=1024)break;if(item instanceof Map<?,?> server&&server.get("ip")instanceof String ip&&valid("SERVER",ip)){String name=server.get("name")instanceof String s&&!s.isBlank()?s:ip;var entry=new Entry("SERVER",ip,label(name));if(result.stream().noneMatch(e->e.kind.equals(entry.kind)&&e.target.equals(entry.target)))result.add(entry);}}
  }catch(IOException malformed){throw new IOException("Saved server list could not be read. Minecraft files were kept.",malformed);}
  return List.copyOf(result);
 }
 private static Object nbt(Path path)throws IOException {
  if(Files.size(path)>8*1024*1024)throw new IOException("NBT file too large");
  try(var input=new BufferedInputStream(Files.newInputStream(path))){input.mark(2);int a=input.read(),b=input.read();input.reset();InputStream decoded=a==31&&b==139?new GZIPInputStream(input):input;
   var limited=new FilterInputStream(decoded){int left=16*1024*1024;public int read()throws IOException{if(--left<0)throw new IOException("NBT expanded limit");return super.read();}public int read(byte[]b,int o,int n)throws IOException{if(left<=0)throw new IOException("NBT expanded limit");int count=in.read(b,o,Math.min(n,left));if(count>0)left-=count;return count;}public long skip(long n)throws IOException{if(left<=0)throw new IOException("NBT expanded limit");long count=in.skip(Math.min(n,left));left-=count;return count;}};
   var in=new DataInputStream(limited);int type=in.readUnsignedByte();if(type!=10)throw new IOException("NBT compound expected");in.readUTF();return payload(in,type,0,new int[]{65536});
  }
 }
 private static Object payload(DataInputStream in,int type,int depth,int[] budget)throws IOException {
  if(depth>32||--budget[0]<0)throw new IOException("NBT structure limit");
  return switch(type){case 1->in.readByte();case 2->in.readShort();case 3->in.readInt();case 4->in.readLong();case 5->in.readFloat();case 6->in.readDouble();case 8->in.readUTF();
   case 7,11,12->{int length=in.readInt(),unit=type==7?1:type==11?4:8;if(length<0||length>16*1024*1024/unit)throw new IOException("NBT array limit");in.skipNBytes((long)length*unit);yield null;}
   case 9->{int child=in.readUnsignedByte(),length=in.readInt();if(length<0||length>budget[0]||child==0&&length>0)throw new IOException("NBT list limit");List<Object> values=new ArrayList<>();for(int i=0;i<length;i++)values.add(payload(in,child,depth+1,budget));yield values;}
   case 10->{Map<String,Object> values=new HashMap<>();for(int tag;(tag=in.readUnsignedByte())!=0;){String name=in.readUTF();values.put(name,payload(in,tag,depth+1,budget));}yield values;}
   default->throw new IOException("Unknown NBT tag");};
 }
}
