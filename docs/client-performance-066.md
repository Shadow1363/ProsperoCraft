# Client066 — guarded C1 and software mouse capture

The user confirms that065loads the demo world and punching works,but loading
is very slow,movement fails and severe lag makes it unplayable. Exact065bytes
are preserved and published as the first-world GitHub release;066is a separate
performance/input candidate. No original Minecraft JAR or asset is modified.

## Java execution speed

065runs every Java method in the interpreter. Live reports show CPU-heavy world
generation and world rendering plus integrated-server overload warnings. That
supports testing compilation;it does not identify every bottleneck or prove
GPU utilization. RADV/Vulkan already executes GPU work; enabling JIT is not a
claim of full PS5 CPU/GPU utilization or a promised frame rate.

066uses the guarded C1 configuration already exercised in server development:

```text
-Xmixed
-XX:TieredStopAtLevel=1
-XX:CICompilerCount=1
-XX:CompileThresholdScaling=4.0
-XX:CompileCommand=MemLimit,*.*,2M
-XX:ReservedCodeCacheSize=16m
-XX:SweeperThreshold=50.0
```

A single compiler and per-compilation2MiB arena limit bound compilation pressure.
The512MiB uncompressed direct-backed heap,16MiBinitialheap,SerialGC,SDK/runtime,
AVX-disabled/SSE2policy and two reported processors remain unchanged. This first
candidate isolates compilation before increasing worker count or other resource
budgets. C1level1does not provide C2optimization;larger caches/moreworkers/more
advanced compilation are later measured steps,not unvalidated promises.

Before original Main,the existing Java-port `ps5probe.JitWarmup25` gate checks
mixed/level1/singlecompiler flags,requires a fresh current-run level1 compilation
record for an integer kernel,and verifies expected results before and after
compilation. Interpreter/stale/missing-log controls are refused. A failed gate
stops startup rather than silently claiming JIT success. No Minecraft classes
are transformed;the helper is part of the separate launch harness.

The bounded JIT log is `/download0/java25-jit.log`,exposed by the existing
`/jit.log` route. The4MiBlog rotates once;both current and rotated files can be
collected when available. Existing report index may expose only currentJIT;
record missing coverage rather than treating a rotated-away compile as absent.
Currentstartupmarkers report the actual gate result. Diagnosticlogging and the
bounded observer remain and can perturb performance.

## Movement and camera

The PS5video backend had no `SetRelativeMouseMode` callback. Actual upstream SDL
rejects capture without it and rolls back the window's relative-mode flag. The
temporary mapper checks that flag to switch from menu arrows to WASD and look.
This is a concrete input-path defect consistent with the user's movement report;
actualPS5recovery still needs validation.

066registers a software-relative callback. There is no OS cursor to capture for
the stick-driven mouse;SDL keeps its normal focus/window/capture state and the
existing adapter supplies real relative deltas. The host test executes actual SDL
window/global mode functions: reproduces065failure,then checks callbacksuccess,
retainedcapture,focusloss/reacquire,menurelease and idempotence underASan/UBSan.
The existing adapter tests cover buffered taps,releases,mode mappings and bounded
look. No fake game-state access or forced player movement is introduced.

When captured:leftstick=WASD,rightstick=look,X=jump,Triangle=inventory,R2=punch,
L2=use,Circle=Escape. Inmenus:D-pad/leftstick=arrows,X=Enter,Triangle=Tab,
Circle=back,Square=Backspace. Fullinventory/textentry/rebinding/hotbar/rumble/gyro
andcontrollerpolish remain futurework. Thebridgehands off whenSDLgamepadsinitialize
andhasexplicitopt-out forfutureControlifyintegration.

## Console comparison

Install066andpressXonce. Check whether the C1gate passes and menu appears. Load
the same demo world;compare approximate load time and responsiveness with065.
Try movement,right-stickcamera,jump,punch,pause/inventory and return to menus.
Distinguish slow generation from a crash,stuck input or worker failure. A reused
world can load faster due to saved/generated data,so that alone is not a controlled
JITspeedbenchmark. Actualframetimes/ticks/heap/compile/cache logs will guide next
changes. If it fails,reopenwithoutXandretain currentreports before restarting.

NoPS5C1/gameplay/performance/stability pass is implied by hosttests or packaging.
Save/reload,speaker audio,longdurationtests and polishedfullclientqualityremain
pending. 065release retains its exactinterpretedbytes and knownissues. NoStorework.

## Checked066 package

PPSA99874client01.000.066. Local:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/dist/PPSA99874.zip`.
Matching consumer `dist/client-startup/PPSA99874.zip`.
SHA256 `0b549873222b155fd21b4a441535390660598096f3f32c27081a963d00ea7802`.
Symbols `build/client-startup-probe/bootstrap-01.000.066-symbols.elf`.
Allhost/native/packagecheckspass;actualPS5speed/movement/stabilitypending.
Source/checkhashes:docs/validation/client066-build-2026-10-26.json.
