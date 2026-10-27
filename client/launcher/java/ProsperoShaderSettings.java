import java.io.IOException;
import java.nio.file.*;

/** Vitrail's supported per-instance pack settings; no shader or game rewriting. */
final class ProsperoShaderSettings {
 static Path path(Path game)throws IOException {Path p=game.resolve("vitrail/pack.txt");ProsperoDownloads.noLinks(p);return p;}
 static String read(Path p)throws IOException {if(!Files.exists(p))return "";if(!Files.isRegularFile(p)||Files.size(p)>65536)throw new IOException("Vitrail settings cannot be read safely");return Files.readString(p);}
 static int scale(Path game)throws IOException {for(String line:read(path(game)).lines().toList())if(line.startsWith("shadowmapscale="))try{return Math.clamp(Integer.parseInt(line.substring(15).strip()),25,100);}catch(NumberFormatException bad){throw new IOException("Invalid Vitrail shadow scale");}return 100;}
 static int toggle(Path game)throws Exception {
  Path file=path(game);String before=read(file);int next=scale(game)>50?50:100;
  String after=before.replaceAll("(?m)^shadowmapscale=[^\\r\\n]*","shadowmapscale="+next);
  if(after.equals(before))after+=(after.isEmpty()||after.endsWith("\n")?"":"\n")+"shadowmapscale="+next+"\n";
  Path backup=file.resolveSibling("pack.before-prospero106.txt");ProsperoDownloads.noLinks(backup);if(Files.isRegularFile(file)&&!Files.exists(backup))Files.copy(file,backup);
  ProsperoInstall.save(file,after);return next;
 }
}
