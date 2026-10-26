import com.google.gson.*;
import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.security.cert.Certificate;
import java.time.*;
import javax.net.ssl.*;

public class test_online_rate_limit {
 static void check(boolean b){if(!b)throw new AssertionError();}
 interface Action {void run()throws Exception;}
 static void failure(Action a)throws Exception{try{a.run();throw new AssertionError("failure expected");}catch(IOException expected){}}
 static final class Response extends HttpsURLConnection {
  final int code;final String retry,body;boolean disconnected;
  Response(int code,String retry,String body)throws Exception{super(new URL("https://example.invalid/"));this.code=code;this.retry=retry;this.body=body;}
  public int getResponseCode(){return code;}
  public String getHeaderField(String name){return name.equals("Retry-After")?retry:null;}
  public InputStream getInputStream(){check(code==200);return new ByteArrayInputStream(body.getBytes(java.nio.charset.StandardCharsets.UTF_8));}
  public void disconnect(){disconnected=true;}public boolean usingProxy(){return false;}public void connect(){}
  public String getCipherSuite(){return "test";}public Certificate[] getLocalCertificates(){return null;}public Certificate[] getServerCertificates(){return null;}
 }
 public static void main(String[]args)throws Exception {
  Instant now=Instant.parse("2026-10-21T12:00:00Z");
  check(ServerOnline25.retryDelay(null,now)==5000);
  check(ServerOnline25.retryDelay("2",now)==2000);
  check(ServerOnline25.retryDelay("Wed, 21 Oct 2026 12:00:09 GMT",now)==10000);
  check(ServerOnline25.retryDelay("invalid",now)==5000);
  failure(()->ServerOnline25.retryDelay("31",now));failure(()->ServerOnline25.retryDelay("-1",now));
  int[] calls={0},sleeps={0};long[] delay={0};
  JsonObject result=ServerOnline25.readWithRetry(()->{Response response=new Response(++calls[0]<3?429:200,"2","{\"ok\":true}");try{return ServerOnline25.readResponse(response,"example.invalid");}finally{check(response.disconnected);}},millis->{sleeps[0]++;delay[0]+=millis;});
  check(result.get("ok").getAsBoolean()&&calls[0]==3&&sleeps[0]==2&&delay[0]==4000);
  calls[0]=sleeps[0]=0;
  failure(()->ServerOnline25.readWithRetry(()->{calls[0]++;Response response=new Response(429,"0","");try{return ServerOnline25.readResponse(response,"example.invalid");}finally{check(response.disconnected);}},millis->sleeps[0]++));
  check(calls[0]==3&&sleeps[0]==2);
  for(int status:new int[]{401,404,500}){calls[0]=0;failure(()->ServerOnline25.readWithRetry(()->{calls[0]++;Response response=new Response(status,null,"");try{return ServerOnline25.readResponse(response,"example.invalid");}finally{check(response.disconnected);}},millis->{throw new AssertionError("non-429 retried");}));check(calls[0]==1);}
  failure(()->ServerOnline25.readResponse(new Response(200,null,"[]"),"example.invalid"));
  failure(()->ServerOnline25.readResponse(new Response(200,null,"x".repeat(262145)),"example.invalid"));
  try{ServerOnline25.readWithRetry(()->{throw new ServerOnline25.RateLimited("example.invalid",1);},millis->{throw new InterruptedException();});throw new AssertionError();}catch(InterruptedException expected){}
  Path root=Files.createTempDirectory("online-whitelist-test-");
  try {
   check(ServerOnline25.whitelist(root).isEmpty());
   Files.writeString(root.resolve("whitelist.json"),"[{\"uuid\":\"00112233-4455-6677-8899-aabbccddeeff\",\"name\":\"TestPlayer\"}]");
   var entries=ServerOnline25.whitelist(root);var profile=ServerOnline25.whitelistedProfile(entries,"testplayer");
   check(ServerOnline25.text(profile,"id").equals("00112233445566778899aabbccddeeff"));check(ServerOnline25.whitelistedProfile(entries,"AnotherPlayer")==null);
   ServerOnline25.verifySession(profile,"00112233445566778899aabbccddeeff","TESTPLAYER");
   failure(()->ServerOnline25.verifySession(profile,"ffeeddccbbaa99887766554433221100","testplayer"));
   failure(()->ServerOnline25.verifySession(profile,"00112233445566778899aabbccddeeff","AnotherPlayer"));
   var conflicting=profile.deepCopy();conflicting.remove("id");conflicting.addProperty("uuid","ffeeddcc-bbaa-9988-7766-554433221100");entries.add(conflicting);
   failure(()->ServerOnline25.whitelistedProfile(entries,"TestPlayer"));
   entries.remove(1);entries.get(0).getAsJsonObject().addProperty("uuid","invalid");failure(()->ServerOnline25.whitelistedProfile(entries,"TestPlayer"));
   Files.writeString(root.resolve("whitelist.json"),"{}");failure(()->ServerOnline25.whitelist(root));
  }finally{Files.deleteIfExists(root.resolve("whitelist.json"));Files.delete(root);}
  System.out.println("PASS: actual HTTP response/retry/cleanup paths, bounded429 retries/Retry-After/no retries on other errors/interruption, whitelist reuse/malformed/conflict cases, remote session identity+name validation");
 }
}
