#!/usr/bin/env python3
"""Exercise actual thread lookup without collecting native stack traces."""
from pathlib import Path
import subprocess
r=Path(__file__).resolve().parents[1];w=r/'build/thread-lookup-test';w.mkdir(parents=True,exist_ok=True)
p=w/'ThreadLookupTest.java';p.write_text('''import java.util.concurrent.CountDownLatch;
public class ThreadLookupTest {
 public static void main(String[] args)throws Exception {
  if(ServerStart25.serverThread()!=null)throw new AssertionError("phantom server");
  CountDownLatch finish=new CountDownLatch(1),started=new CountDownLatch(81);
  ThreadGroup group=new ThreadGroup("lookup-sibling");Thread[] workers=new Thread[81];
  try {
   for(int i=0;i<workers.length;i++){
    workers[i]=new Thread(group,()->{started.countDown();try{finish.await();}catch(InterruptedException e){throw new RuntimeException(e);}},i==80?"Server thread":"fixture-"+i);workers[i].start();
   }
   started.await();if(ServerStart25.serverThread()!=workers[80])throw new AssertionError("missing server after 64-thread truncation");
  }finally{finish.countDown();for(Thread t:workers)if(t!=null)t.join();}
  if(ServerStart25.serverThread()!=null)throw new AssertionError("dead server");
  System.out.println("PASS: absent/live/exited platform server thread and enumeration growth beyond64");
 }
}''')
jdk='/opt/homebrew/opt/openjdk@25/bin/';subprocess.run([jdk+'javac','-d',str(w),str(r/'server/java/ServerStart25.java'),str(p)],check=True);subprocess.run([jdk+'java','-cp',str(w),'ThreadLookupTest'],check=True)
