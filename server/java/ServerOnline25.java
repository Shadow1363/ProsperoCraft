import com.google.gson.*;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import javax.net.ssl.HttpsURLConnection;

/** Verified HTTPS discovery/profile bootstrap; no offline identity or TLS bypass. */
public final class ServerOnline25 {
 static JsonObject object(JsonObject o,String key)throws IOException {if(!o.has(key)||!o.get(key).isJsonObject())throw new IOException("Missing discovery object: "+key);return o.getAsJsonObject(key);}
 static String text(JsonObject o,String key)throws IOException {if(!o.has(key)||!o.get(key).isJsonPrimitive()||!o.get(key).getAsJsonPrimitive().isString())throw new IOException("Missing discovery string: "+key);return o.get(key).getAsString();}
 // Phase names and public endpoint hosts only: never log account URLs or bodies.
 static void checkpoint(String phase,String host) {
  Runtime vm=Runtime.getRuntime();
  System.out.println("MC_ONLINE_PHASE phase="+phase+" host="+host+" heapTotal="+vm.totalMemory()+" heapFree="+vm.freeMemory()+" heapMax="+vm.maxMemory());
  System.out.flush();
 }
 interface OnlineRead { JsonObject get()throws Exception; }
 interface Pause { void sleep(long millis)throws InterruptedException; }
 static final class RateLimited extends IOException {
  final long delayMillis;
  RateLimited(String host,long delayMillis){super("Online endpoint "+host+" returned HTTP 429 (rate limited)");this.delayMillis=delayMillis;}
 }
 static long retryDelay(String value,java.time.Instant now)throws IOException {
  long seconds=5;
  if(value!=null)try{seconds=Long.parseLong(value.trim());}
  catch(NumberFormatException notSeconds){try{seconds=Math.max(0,java.time.Duration.between(now,java.time.ZonedDateTime.parse(value,java.time.format.DateTimeFormatter.RFC_1123_DATE_TIME).toInstant()).getSeconds()+1);}catch(java.time.DateTimeException invalid){seconds=5;}}
  if(seconds<0||seconds>30)throw new IOException("Online rate limit requests a longer wait; retry later");
  return seconds*1000;
 }
 static JsonObject readWithRetry(OnlineRead operation,Pause pause)throws Exception {
  for(int attempt=0;;attempt++)try{return operation.get();}catch(RateLimited limited){
   if(attempt==2)throw limited;
   System.out.println("MC_ONLINE_RATE_LIMIT retry="+(attempt+1)+" delayMillis="+limited.delayMillis);
   pause.sleep(limited.delayMillis);
  }
 }
 static JsonObject read(String address)throws Exception {return readWithRetry(()->readOnce(address),Thread::sleep);}
 static JsonObject readOnce(String address)throws Exception {
  URI uri=URI.create(address);if(!"https".equals(uri.getScheme())||uri.getHost()==null||uri.getUserInfo()!=null)throw new IOException("HTTPS endpoint required");
  System.out.println("MC_ONLINE_CHECK host="+uri.getHost());
  try{if(InetAddress.getAllByName(uri.getHost()).length==0)throw new UnknownHostException(uri.getHost());}
  catch(UnknownHostException e){throw new IOException("Online DNS failed for "+uri.getHost()+"; inspect native DNS stages",e);}
  checkpoint("dns_ok",uri.getHost());
  checkpoint("url_begin",uri.getHost());
  URL url=uri.toURL();
  checkpoint("url_ok",uri.getHost());
  checkpoint("connection_begin",uri.getHost());
  HttpsURLConnection c=(HttpsURLConnection)url.openConnection();
  checkpoint("connection_ok",uri.getHost());
  c.setConnectTimeout(15000);c.setReadTimeout(15000);c.setInstanceFollowRedirects(false);
  checkpoint("configured",uri.getHost());
  return readResponse(c,uri.getHost());
 }
 static JsonObject readResponse(HttpsURLConnection c,String host)throws Exception {
  try{checkpoint("response_begin",host);int status=c.getResponseCode();checkpoint("response_ok",host);
   if(status==429)throw new RateLimited(host,retryDelay(c.getHeaderField("Retry-After"),java.time.Instant.now()));
   if(status!=200)throw new IOException("Online endpoint "+host+" returned HTTP "+status);
   try(InputStream input=c.getInputStream()){checkpoint("body_begin",host);byte[] bytes=input.readNBytes(262145);checkpoint("body_ok",host);if(bytes.length>262144)throw new IOException("Online JSON exceeds256KiB");JsonElement value=JsonParser.parseString(new String(bytes,StandardCharsets.UTF_8));if(!value.isJsonObject())throw new IOException("Expected online JSON object");return value.getAsJsonObject();}
  }finally{checkpoint("disconnect_begin",host);c.disconnect();checkpoint("disconnect_ok",host);}
 }
 static JsonArray whitelist(Path root)throws IOException {
  Path path=root.resolve("whitelist.json");if(!Files.exists(path))return new JsonArray();
  if(Files.size(path)>262144)throw new IOException("Whitelist exceeds256KiB");
  JsonElement value=JsonParser.parseString(Files.readString(path));if(!value.isJsonArray())throw new IOException("Invalid existing whitelist");return value.getAsJsonArray();
 }
 static JsonObject whitelistedProfile(JsonArray entries,String name)throws IOException {
  JsonObject result=null;
  for(JsonElement value:entries){if(!value.isJsonObject())continue;JsonObject entry=value.getAsJsonObject();
   if(!entry.has("name")||!text(entry,"name").equalsIgnoreCase(name))continue;
   String id=text(entry,"uuid");if(!id.matches("[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}"))throw new IOException("Invalid existing whitelist UUID");
   id=id.replace("-","");if(result!=null&&!text(result,"id").equalsIgnoreCase(id))throw new IOException("Conflicting existing whitelist identity");
   result=new JsonObject();result.addProperty("id",id);result.addProperty("name",text(entry,"name"));
  }
  return result;
 }
 static void verifySession(JsonObject session,String id,String name)throws IOException {
  if(!text(session,"id").equalsIgnoreCase(id)||!text(session,"name").equalsIgnoreCase(name))throw new IOException("Online session profile mismatch");
 }

 static String endpoint(JsonObject discovery,String service,String operation)throws IOException {return text(object(object(object(discovery,service),"endpoints"),operation),"uri");}
 static String uuid(String id)throws IOException {if(!id.matches("[0-9a-fA-F]{32}"))throw new IOException("Invalid online profile UUID");return id.substring(0,8)+"-"+id.substring(8,12)+"-"+id.substring(12,16)+"-"+id.substring(16,20)+"-"+id.substring(20);}
 static void checkTrust()throws Exception {
  String store=System.getProperty("javax.net.ssl.trustStore",Path.of(System.getProperty("java.home"),"lib/security/cacerts").toString());File file=new File(store);
  System.out.println("MC_TLS_TRUST_FILE isFile="+file.isFile()+" canRead="+file.canRead()+" bytes="+file.length());
  var factory=javax.net.ssl.TrustManagerFactory.getInstance(javax.net.ssl.TrustManagerFactory.getDefaultAlgorithm());factory.init((java.security.KeyStore)null);
  int count=0;for(var manager:factory.getTrustManagers())if(manager instanceof javax.net.ssl.X509TrustManager x)count+=x.getAcceptedIssuers().length;
  if(count==0)throw new IOException("Default TLS trust store has zero trusted issuers; inspect java.io metadata and packaged cacerts");
  System.out.println("MC_TLS_TRUST_OK acceptedIssuers="+count+" default certificate validation enabled");
 }
 public static void prepare(Path root)throws Exception {
  checkTrust();
  System.out.println("MC_TLS_RANDOM_BEGIN real DRBG initialization");
  var random=java.security.SecureRandom.getInstance("DRBG");byte[] sample=new byte[64];
  random.nextBytes(sample);java.util.Arrays.fill(sample,(byte)0);
  System.out.println("MC_TLS_RANDOM_OK provider="+random.getProvider().getName());
  System.out.println("MC_TLS_FACTORY_BEGIN default verified TLS factory and unconnected socket");
  try(var socket=(javax.net.ssl.SSLSocket)javax.net.ssl.SSLSocketFactory.getDefault().createSocket()) {
   if(socket.getEnabledProtocols().length==0)throw new IOException("No enabled TLS protocols");
  }
  System.out.println("MC_TLS_FACTORY_OK default TLS initialization");
  String name=System.getProperty("ps5.mc.joinPlayer");
  if(name==null){Path file=Path.of(System.getProperty("ps5.mc.joinPlayerFile","/app0/assets/java25/join-player.txt"));if(Files.size(file)>64)throw new IOException("Join-player file too large");name=Files.readString(file).trim();}
  if(!name.matches("[A-Za-z0-9_]{3,16}"))throw new IOException("Join-player file must contain one Minecraft account name");
  JsonObject discovery=object(read("https://discovery.minecraftservices.com/minecraft/client"),"discovery");
  String verify=endpoint(discovery,"session","verify");URI verifyUri=URI.create(verify);if(!"https".equals(verifyUri.getScheme())||verifyUri.getHost()==null)throw new IOException("Invalid online session endpoint");
  // Exercise the same remote session host with the actual profile endpoint;
  // do not submit a fabricated hasJoined request or substitute an identity.
  JsonArray entries=whitelist(root);
  JsonObject profile=whitelistedProfile(entries,name);
  if(profile==null){System.out.println("MC_ONLINE_PROFILE_SOURCE remote-lookup");profile=read(endpoint(discovery,"profiles","getByName").replace("{name}",name));}
  else System.out.println("MC_ONLINE_PROFILE_SOURCE existing-whitelist (session verification still required)");
  String id=text(profile,"id"),canonical=text(profile,"name");if(!canonical.equalsIgnoreCase(name))throw new IOException("Online profile name mismatch");
  String identity=uuid(id);JsonObject session=read(endpoint(discovery,"session","getProfileById").replace("{profileId}",id));
  verifySession(session,id,name);
  JsonObject keys=read(endpoint(discovery,"authentication","getPublicKeys"));
  if(!keys.has("profilePropertyKeys")||!keys.get("profilePropertyKeys").isJsonArray()||keys.getAsJsonArray("profilePropertyKeys").isEmpty())throw new IOException("No authentication public keys");
  Path whitelist=root.resolve("whitelist.json");
  boolean found=false;for(JsonElement entry:entries)if(entry.isJsonObject()&&entry.getAsJsonObject().has("uuid")&&identity.equalsIgnoreCase(entry.getAsJsonObject().get("uuid").getAsString()))found=true;
  if(!found){JsonObject entry=new JsonObject();entry.addProperty("uuid",identity);entry.addProperty("name",canonical);entries.add(entry);}
  Files.writeString(whitelist,new GsonBuilder().setPrettyPrinting().create().toJson(entries));
  System.out.println("MC_ONLINE_PREFLIGHT_OK verified HTTPS discovery/profile/session/public-keys; account whitelisted; online authentication still required");
 }
 public static void main(String[] args)throws Exception{Path root=Path.of(args[0]);Files.createDirectories(root);prepare(root);}
}
