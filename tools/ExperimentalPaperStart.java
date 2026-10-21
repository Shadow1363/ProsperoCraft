/** Host-only fixture reproducing PS5's internal version label without changing VM code. */
public final class ExperimentalPaperStart {
 public static void main(String[]args)throws Exception {
  if(Runtime.version().feature()!=25)throw new AssertionError("Java25 host required");
  System.setProperty("java.version","25.0.4-internal");
  ServerC1Start25.main(args);
 }
}
