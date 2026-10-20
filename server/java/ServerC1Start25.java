/** Host entry matching the console preflight compilation gate before launch. */
public final class ServerC1Start25 {
 public static void main(String[] args)throws Exception{if(Boolean.getBoolean("ps5.probe.preflightBeforeStart"))ServerPreflight25.main(args);else ps5probe.JitWarmup25.check();ServerStart25.main(args);}
}
