import com.google.gson.*;
import java.nio.file.*;
import java.security.*;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

/** Offline lease issued only after the local export helper verifies Java ownership. */
final class ProsperoOfflineAccount {
 static final long WEEK=7L*24*60*60*1000;
 final String name,id;final long expiresAt;
 private ProsperoOfflineAccount(String name,String id,long expiresAt){this.name=name;this.id=id;this.expiresAt=expiresAt;}
 static ProsperoOfflineAccount load(Path root,long now){
  if(!ProsperoChannel.offline())return null;
  try(var key=ProsperoOfflineAccount.class.getResourceAsStream("/offline-import-public-key.der")){if(key==null)return null;return read(root.resolve("offline-account.json"),key.readNBytes(1025),now);}catch(Exception unavailable){return null;}
 }
 static ProsperoOfflineAccount read(Path file,byte[] key,long now)throws Exception {
  if(Files.size(file)>8192||key.length>1024)throw new java.io.IOException("Invalid offline profile");
  var envelope=JsonParser.parseString(Files.readString(file)).getAsJsonObject();
  byte[] payload=Base64.getDecoder().decode(envelope.get("payload").getAsString());
  var verifier=Signature.getInstance("SHA256withRSA");
  verifier.initVerify(KeyFactory.getInstance("RSA").generatePublic(new X509EncodedKeySpec(key)));
  verifier.update(payload);if(!verifier.verify(Base64.getDecoder().decode(envelope.get("signature").getAsString())))throw new java.io.IOException("Offline profile signature mismatch");
  var data=JsonParser.parseString(new String(payload,java.nio.charset.StandardCharsets.UTF_8)).getAsJsonObject();
  String name=data.get("name").getAsString(),id=data.get("id").getAsString();long checked=data.get("verifiedAt").getAsLong(),expires=data.get("expiresAt").getAsLong();
  if(data.get("schema").getAsInt()!=1||!name.matches("[A-Za-z0-9_]{1,16}")||!id.matches("[a-fA-F0-9]{32}")||checked<=0||checked>now+60_000||expires<=checked||expires-checked>WEEK||now>=expires)throw new java.io.IOException("Offline profile needs verification");
  return new ProsperoOfflineAccount(name,id,expires);
 }
 boolean valid(long now){return now<expiresAt;}
 @Override public String toString(){return "Verified offline profile [personal data omitted]";}
}
