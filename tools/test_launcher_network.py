#!/usr/bin/env python3
"""Exercise native-free IPv4 Netty listener/connect and original LAN pinger on host."""
from pathlib import Path
import subprocess,tempfile,json
ROOT=Path(__file__).resolve().parents[1];JDK=Path('/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home')
cp=':'.join(str(ROOT/'.tools/client'/r['file'])for r in json.loads((ROOT/'client/26.3.lock.json').read_text())['artifacts'])
source=r'''
import java.net.*;import java.util.concurrent.*;import io.netty.bootstrap.*;import io.netty.channel.*;import io.netty.channel.nio.*;import io.netty.channel.socket.nio.*;
public class NetworkCheck {
 public static void main(String[]args)throws Exception{
  ProsperoNetwork.check();var group=new NioEventLoopGroup(1);Channel server=null,client=null;
  try{var received=new CountDownLatch(1);server=new ServerBootstrap().group(group).channel(NioServerSocketChannel.class).childHandler(new ChannelInitializer<Channel>(){protected void initChannel(Channel c){c.pipeline().addLast(new ChannelInboundHandlerAdapter(){public void channelActive(ChannelHandlerContext ctx){received.countDown();ctx.close();}});}}).bind(0).sync().channel();
   int port=((InetSocketAddress)server.localAddress()).getPort();client=new Bootstrap().group(group).channel(NioSocketChannel.class).handler(new ChannelInboundHandlerAdapter()).connect("127.0.0.1",port).sync().channel();if(!received.await(3,TimeUnit.SECONDS))throw new AssertionError("Netty accept");
   var pinger=new net.minecraft.client.server.LanServerPinger("Host fixture",Integer.toString(port));if(!net.minecraft.client.server.LanServerPinger.createPingString("Host fixture",Integer.toString(port)).contains(Integer.toString(port)))throw new AssertionError("LAN payload");
   var f=pinger.getClass().getDeclaredField("socket");f.setAccessible(true);((DatagramSocket)f.get(pinger)).close();
   System.out.println("PASS original LAN pinger constructor/datagram bind and advertisement format; real Netty NIO all-interface ephemeral bind/loopback connect/accept/close with native transport disabled; host only");
  }finally{if(client!=null)client.close().syncUninterruptibly();if(server!=null)server.close().syncUninterruptibly();group.shutdownGracefully(0,2,TimeUnit.SECONDS).syncUninterruptibly();}
 }
}
'''
with tempfile.TemporaryDirectory(prefix='prospero-network-')as folder:
 w=Path(folder);(w/'NetworkCheck.java').write_text(source);subprocess.run([str(JDK/'bin/javac'),'-cp',cp,'-d',str(w),str(ROOT/'client/launcher/java/ProsperoNetwork.java'),str(w/'NetworkCheck.java')],check=True)
 subprocess.run([str(JDK/'bin/java'),'-Djava.net.preferIPv4Stack=true','-Dio.netty.transport.noNative=true','-cp',str(w)+':'+cp,'NetworkCheck'],check=True,timeout=30)
