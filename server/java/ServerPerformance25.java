import java.lang.management.*;
import java.util.*;

/** Interval timing and real GC counters; does not alter game ticks or food. */
public final class ServerPerformance25 {
 private final List<GarbageCollectorMXBean> collectors=ManagementFactory.getGarbageCollectorMXBeans();
 private long previousCount=-1,previousMillis=-1;
 static String rate(long before,long current,long from,long now) {
  if(before<0||from<=0||now<=from||current<before)return "observedTps=unavailable";
  return String.format(Locale.ROOT,"observedTps=%.2f",(current-before)*1_000_000_000.0/(now-from));
 }
 String sample() {
  long count=0,millis=0;boolean known=!collectors.isEmpty();
  for(var bean:collectors){long c=bean.getCollectionCount(),t=bean.getCollectionTime();if(c<0||t<0){known=false;break;}count+=c;millis+=t;}
  if(!known)return "gc=unavailable";
  String result="gcCollections="+count+" gcMillis="+millis+" intervalGcCollections="+(previousCount<0?0:count-previousCount)+" intervalGcMillis="+(previousMillis<0?0:millis-previousMillis);
  previousCount=count;previousMillis=millis;return result;
 }
}
