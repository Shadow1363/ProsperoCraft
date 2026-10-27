import java.util.*;

/** SDL USB-HID scancodes and explicit mouse bindings, persisted by the launcher. */
final class ProsperoInput {
 static final int[] DEFAULT={82,81,80,79,40,41,43,42,26,22,4,7,44,8,225,224,9,20,62,58,59,60,23,56,15,68,30,38,513,514};
 static final String[] ACTIONS={"Menu Up","Menu Down","Menu Left","Menu Right","Confirm","Back","Tab","Backspace","Left stick Up","Left stick Down","Left stick Left","Left stick Right","Cross","Triangle","Circle","L3","Square","D-pad Down","R3","Touchpad + Left","Touchpad + Right","Touchpad + Up","Touchpad + Triangle","Touchpad + Square","Touchpad + Down","Touchpad + Options","D-pad Left","D-pad Right","R2","L2"};
 static final ArrayList<String> LABELS=new ArrayList<>();static final ArrayList<Integer> CODES=new ArrayList<>();
 static{add("Unbound",0);for(int i=0;i<26;i++)add(""+(char)('A'+i),4+i);for(int i=0;i<10;i++)add(""+(i==9?0:i+1),30+i);for(int i=0;i<12;i++)add("F"+(i+1),58+i);String[] labels={"Space","Enter","Escape","Backspace","Tab","Left Shift","Left Ctrl","Left Alt","Up","Down","Left","Right","Slash","Mouse left","Mouse right","Mouse middle"};int[] codes={44,40,41,42,43,225,224,226,82,81,80,79,56,513,514,515};for(int i=0;i<codes.length;i++)add(labels[i],codes[i]);}
 static void add(String name,int code){LABELS.add(name);CODES.add(code);}
 static String label(int code){int at=CODES.indexOf(code);return at<0?"Key "+code:LABELS.get(at);}
 static String hint(int[] values){return java.util.Arrays.stream(values).mapToObj(String::valueOf).collect(java.util.stream.Collectors.joining(","));}
 static void validate(int[] values){if(values==null||values.length!=30)throw new IllegalArgumentException("Invalid controller bindings");for(int v:values)if(v<0||v>515||(v>511&&v<513))throw new IllegalArgumentException("Invalid controller key");for(int n=0;n<8;n++)if(values[n]!=DEFAULT[n])throw new IllegalArgumentException("Menu controls must remain available");}
}
