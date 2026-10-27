import java.nio.charset.StandardCharsets;

/** Build-selected release channel. Missing/invalid metadata always falls back to Demo. */
final class ProsperoChannel {
 static boolean offline(){
  try(var in=ProsperoChannel.class.getResourceAsStream("/prosperocraft-channel.txt")){
   return in!=null&&new String(in.readNBytes(32),StandardCharsets.US_ASCII).strip().equals("offline");
  }catch(Exception ignored){return false;}
 }
 static boolean tempGameTest(){
  try(var in=ProsperoChannel.class.getResourceAsStream("/prosperocraft-channel.txt")){return in!=null&&new String(in.readNBytes(32),StandardCharsets.US_ASCII).strip().equals("temp_gametest");}catch(Exception ignored){return false;}
 }
 static String label(){return tempGameTest()?"TEMP GAMETEST":offline()?"OFFLINE BRANCH":"DEMO BRANCH";}
}
