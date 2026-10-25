# ProsperoCraft client056 — honor dedicated JVM log FILEs

User confirms055crashed and reopened. Matching run:
`client-01.000.055-1792955969-469497698`.
[Hashed reports/observations](validation/client055-startup-failure-2026-10-25.json).
Raw complete reports remain in runtime `logs/client055-result-20261025/`.
Safari index/option-click retrieval worked;no new run was started. Full startup
history was additionally retrieved because the GC file was empty.

055has120complete snapshots/120native phase pairs,last Java96966ms/native96967ms.
Main applies language resources via Matcher.reset/Language.loadFromJson85;
Worker-Main is idle. Saved RUN is not proof of liveness. No sample121,completion,
fatal signal,VM abort,driver error or Java OOM captured. Human timing/error not
supplied. Neither last stack nor last recorded timestamp locates the crash.

GC output exists in the matching run's startup history:63starts0..62 and63summary
ends,no unmatched start. Last full GC completes at158188ms JVM uptime:
232M->176M(247M),342.517ms. Later thread-dump safepoints reach162475ms.
JVM uptime differs from the observer's later start clock. These records show
completed collections,not evidence of GCfailure/JavaOOM or total memory adequacy.
Cause of the game crash remains unknown.

## Concrete diagnostic defect and repair

HotSpot `jvm.cpp:jio_vfprintf(FILE*,...)` invokes the registered Invocation API
vfprintf callback for file logging too. The consumer's vm_print ignored that FILE,
called std::vfprintf(startup_log,...) and flushed startup_log. Therefore native
GC.log was created but empty while all GC text went to startup.log. Rotation
accounting referred to the wrong destination. Source plus actual target reports
support this defect;it is not established as the game crash cause.

056routes stdout/stderr to startup_log as before,and preserves all other requested
FILE destinations. If no capture exists,stdout/stderr retain their original stream.
Null destination returns-1/EINVAL;flush failure returns-1. The callback neither
closes nor replaces supplied FILEs. JVM GC log flush/rotation now act on the same
stream receiving bytes. No JVM runtime image/SDK change is needed.

The regression extracts the actual shipped callback and historical055callback,
then embeds a real host JVM via JNI_CreateJavaVM with the same logging selection
and a finite SerialGC fixture.055reproduces empty dedicated/GC files and diverted
console records.056checks dedicatedFILE/console separation,real GC/safepoints,
full pause and one-file rollover. This addresses the prior test gap:the earlier
host check ran Java without this Invocation API callback. Host success does not
establish target PS5 correctness.

Exact055full ZIP/symbols/status/sourcea751f330df4dc5a1ebc989d8c7477ee92e3a0aad/
build validation/console observations retained under ignored
`dist/failures/Client_Original_Startup-01.000.055/`. Full ZIP SHA256
`33b22e7241dcaf2bd003badd4f7f5fbdbd2781bb51b229918de0e87a687e939c`.
Prior failed/frozen snapshots remain. Original54JARs/5147assets,heap256MiB,
class-space64MiB,SerialGC,processor/executor policy,graphics,early WSI owner,
stderr and signal-recorder repairs remain. This changes harness logging only.

Install056,press X once,and note final display/time/error. After crash,reopen
without X,then retrieve build/session,gc.log/gc-rotated.log,exceptions,VM/native
stderr,process-usage,startup history/tail,abort/fatal reports before restarting.
Check actual nonempty GC file and sequence against other clocks. Missing/unmatched
records alone do not identify a fatal instruction or prove memory exhaustion.

No menu accepted,client milestone/full release or Store download. Server2H deferred.
Full release still requires accepted bytes,legitimate complete JAR+asset provisioning,
matching OpenAL source/relink/notices and verified public app-only artifact checksums;
follow complete054handoff release requirements before updating existing reservation.

Host/embedded-JVM/target/full-package checks passed. [Build validation](validation/client056-build-2026-10-25.json). Full local ZIP SHA256 `587ca6053d121d6cfd5d49d695adc61ff5edb73c03c111e420a5f3ddf74794e1`.056PS5pending.
