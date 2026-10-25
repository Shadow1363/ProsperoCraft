# Current ProsperoCraft handoff — client056

Continue existing files/history;read both workspace/consumer AGENTS.md.
Read [complete054handoff](handoff-prosperocraft-client054.md) for full history,
source ownership,preservation/retrieval and release/Store requirements. Read
[055handoff](handoff-prosperocraft-client055.md) for GC selection/transport context.
This continuation supersedes their current-version and pending055statements.
No subagents. No deferred two-hour server run.

## Current package and verified checks

PPSA99874,client01.000.056. Full local package:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/dist/PPSA99874.zip`.
Matching consumer `dist/client-startup/PPSA99874.zip`.
SHA256 `587ca6053d121d6cfd5d49d695adc61ff5edb73c03c111e420a5f3ddf74794e1`.
Symbols `build/client-startup-probe/bootstrap-01.000.056-symbols.elf`.
Source:consumer commit containing [build validation](validation/client056-build-2026-10-25.json);
inspect current HEAD/status. Runtime report transport1e9fb4f23a2e84e26c50fe67cc4e746ff371dfa2
and image implementation6382528remain unchanged. Host startup checks,actual embedded
JVM old/fixed callback regression,target compile/link/SELF and full package checks
passed. All54JARs/5147assets verified;prior failed/frozen packages checked.
Exact002convenience ZIP restored. Build logs:build/client056-host.log,
client056-vm-output-host.log,client056-package.log,client056-package-check.log.
056PS5validation pending;no console success follows from these checks.

## Latest console evidence

User confirms055crashed,then reopened. No055timing,error/menu acceptance supplied.
Safari refreshed at runtime target192.168.111.72:8765;option-click saved all nine
standard reports plus empty gc.log/unavailable gc-rotated.log,then full startup
history. No X/restart was triggered. Raw complete reports:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/logs/client055-result-20261025/`.
[Hashes and observations](validation/client055-startup-failure-2026-10-25.json).
Matching run client-01.000.055-1792955969-469497698.120complete snapshots/native
phase pairs;last Java96966/native96967ms. Last Main stack is regex/Language resource
apply,Minecraft.runTick/run;worker idle. No sample121,normal completion/fatal signal/
VM abort/driver error/Java OOM captured. Saved RUN does not prove live process.

Full startup history contains63GC starts0..62 and63completed summary ends.
Last full collection completes at158188ms JVM uptime,232M->176M(247M),342.517ms.
ThreadDump safepoints continue through162475ms. JVM uptime and observer elapsed
have different origins;last record is not exact crash timing. No recorded GC
failure/JavaOOM. These records do not prove native/total memory adequacy. Cause
of game crash remains unknown;do not blame last language/regex stack or guess
anRSSlimit/raise heap without supported evidence.

## Concrete repaired defect

Read [056diagnostic](client-startup-056.md).055vm_print ignored supplied FILE;
HotSpot jio_vfprintf uses the callback for unified file logs too. This redirected
GC logs to startup.log and left gc.log empty.056preserves dedicated FILEs and
retains stdout/stderr capture;null/flush failures return-1. No runtime image/SDK
change. This diagnostic defect is not an established game crash cause.

Regression `tools/test_client_startup_vm_output.py --java-home /Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home`
extracts actual historical055/current callback and embeds real host HotSpot via
JNI_CreateJavaVM. Old reproduces empty files/diverted records;new verifies console/
dedicated GC separation,GC/safepoints/full pause and one-file rollover. Earlier
055test lacked the actual embedding callback and missed this defect. Host checks
cannot establish PS5 file routing/rotation correctness or menu acceptance.

Original54JARs/5147assets,heap256MiB,class-space64MiB,SerialGC,processors/executor,
graphics,early WSI owner,native stderr and fault recorder remain. Official JARs
stay intact;no replacement classes/bytecode hooks. New behavior is consumer harness
only;runtime log transport1e9fb4f remains unchanged and published.

Exact055fullZIP SHA25633b22e7241dcaf2bd003badd4f7f5fbdbd2781bb51b229918de0e87a687e939c,
symbols,status,sourcea751f330df4dc5a1ebc989d8c7477ee92e3a0aad,build/console validation
preserved in ignored dist/failures/Client_Original_Startup-01.000.055. Earlier frozen/
failed snapshots stay intact. Preserve exact056before changed057. Never freeze a
passing milestone from host tests or last stacks. Full local game-containing
packages stay local. Restore002convenience ZIP after packaging as documented.

## Next action and release requirements

Install current056,press X once,record final screen/time/error. After crash,reopen
without X and retrieve matching build/session,gc.log/gc-rotated.log plus earlier
nine reports and full startup history. Existing GC routes/collector accept runtime
client target addresses;no app preset IP/filter. Safari native option-click remains
the working retrieval fallback when shell networking fails. Fresh AX indices,
newest completed downloads verified by run/file identity;never overwrite older raw
runs. Menu-only reopen preserves logs,X initializes/archives a new run.

056PS5log file contents/rotation,crash resolution,working menu and broader client
acceptance remain pending. No client release/Store download. Shared PPSA99874means
client replaces server app;preserve Fabric/Paper108full release and exact server
fallbacks,with deferred2H/lifecycle limits explicit.

Before release reread complete054handoff:exact accepted bytes/scope/human evidence;
public app-only artifacts exclude official game JARs/assets/personal data;complete
legitimate hash-pinned54JAR+5147asset provisioning/reconstruction/corruption checks;
exact matching OpenAL corresponding-source/relink kit/notices and verified matching
native ELF;all dependency notices;version/tag/layout/icon/SELF/asset upload+download
SHA checks. Update README truthfully,then existing catalog reservation under current
upstream rules/checks. PR737already merged;no duplicate title. Source ownership:
consumer changes commit/push here,runtime changes via workspace sync_github.py.
Verify pushes and report current ZIP/version/checksum and exact pending console tests.
