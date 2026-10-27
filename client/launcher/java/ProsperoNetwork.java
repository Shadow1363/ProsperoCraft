import java.net.*;
import java.nio.channels.*;

/** Short-lived vanilla socket preflight. No fixed client/server IP or port. */
final class ProsperoNetwork {
 static void check(){
  try(ServerSocketChannel tcp=ServerSocketChannel.open()){tcp.configureBlocking(false);tcp.bind(new InetSocketAddress(0));System.err.println("PS5_NETWORK TCP_LISTEN=PASS");}catch(Exception failure){report("TCP_LISTEN",failure);}
  try(DatagramSocket udp=new DatagramSocket()){udp.setBroadcast(true);System.err.println("PS5_NETWORK UDP_BIND=PASS");}catch(Exception failure){report("UDP_BIND",failure);}
 }
 static void report(String stage,Exception failure){String message=failure.getMessage();System.err.println("PS5_NETWORK "+stage+"=FAIL type="+failure.getClass().getSimpleName()+" detail="+(message==null?"unavailable":message.replaceAll("[\\r\\n]"," ")));}
}
