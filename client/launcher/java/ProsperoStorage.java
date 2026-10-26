import java.io.IOException;
import java.nio.file.FileSystemException;

/** Safe storage failure categories. Capacity queries remain unsupported on PS5. */
public final class ProsperoStorage {
 static String code(IOException error){
  String text=error instanceof FileSystemException file?file.getReason():error.getMessage();if(text==null)return "IO";text=text.toLowerCase(java.util.Locale.ROOT);
  if(text.contains("no space")||text.contains("enospc"))return "ENOSPC";if(text.contains("quota"))return "QUOTA";if(text.contains("permission")||text.contains("access denied"))return "ACCESS";if(text.contains("read-only"))return "READ_ONLY";return "IO";
 }
}
