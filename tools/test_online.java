import com.google.gson.*;
import java.io.*;
public class test_online {
 public static void main(String[] args)throws Exception {
  if(!ServerOnline25.uuid("00112233445566778899aabbccddeeff").equals("00112233-4455-6677-8899-aabbccddeeff"))throw new AssertionError();
  for(String id:new String[]{"short","00112233445566778899aabbccddeefg"})try{ServerOnline25.uuid(id);throw new AssertionError("bad UUID accepted");}catch(IOException expected){}
  JsonObject d=JsonParser.parseString("{\"session\":{\"endpoints\":{\"verify\":{\"uri\":\"https://example.invalid/check\"}}}}").getAsJsonObject();
  if(!ServerOnline25.endpoint(d,"session","verify").equals("https://example.invalid/check"))throw new AssertionError();
  try{ServerOnline25.endpoint(d,"profiles","getByName");throw new AssertionError("missing endpoint accepted");}catch(IOException expected){}
  for(String url:new String[]{"http://example.invalid/","file:///etc/passwd","https://user:pass@example.invalid/"})try{ServerOnline25.read(url);throw new AssertionError("unsafe endpoint accepted");}catch(IOException expected){}
  System.out.println("PASS: actual discovery schema/UUID validation, missing endpoints rejected, HTTPS-only/no-userinfo URL policy before DNS");
 }
}
