public class test_paper_java_policy {
 public static void main(String[]args) {
  if(Runtime.version().feature()!=25)throw new AssertionError();
  String before=System.getProperty("java.version");
  System.clearProperty("Paper.IgnoreJavaVersion");System.setProperty("java.version","25.0.4");
  ServerPaper25.configureJavaPolicy();if(System.getProperty("Paper.IgnoreJavaVersion")!=null)throw new AssertionError("GA path changed");
  System.setProperty("java.version","25.0.4-internal");ServerPaper25.configureJavaPolicy();
  if(!Boolean.getBoolean("Paper.IgnoreJavaVersion"))throw new AssertionError("opt-in missing");
  if(!System.getProperty("java.version").equals("25.0.4-internal")||Runtime.version().feature()!=25)throw new AssertionError("identity changed");
  System.setProperty("java.version",before);
  System.out.println("PASS actual experimental-Java policy preserves runtime identity and Java25 gate; GA branch unchanged");
 }
}
