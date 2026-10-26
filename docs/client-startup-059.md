# ProsperoCraft client059 — class load/initialization boundary

User confirms058crashed and reopened. Run
`client-01.000.058-1793002231-31904375`;
[complete report hashes/measurements](validation/client058-startup-failure-2026-10-26.json).
Raw12reports remain runtime logs/client058-result-20261026. Safari option-click
retrieval succeeded without X/restart. No exact screen/error/timing supplied.

058upstream OpenAL trace confirms1.25.2-b2c48f7initialization,null playback backend,
and creation of No Output playback device. No Created context completion appears;
this neither proves entry to alcCreateContext nor identifies a fault there.
Warnings about missing kern.proc.pathname/empty binary path/no capture backend
are recorded,not established crash causes. This is silent/null output,no physical
PS5speaker validation.

122complete regular snapshots/native phase pairs,12complete main-only burst
records,last97727ms/heap246144128bytes. Last stack is Class.initClassName/getName/
getPackageName/ClassLoader.postDefineClass viaLibrary.tryOpenDevice283,Sounds apply,
Minecraft.runTick/run. Exact class unknown;last stack/time not crash instruction/
exact timing. No burst13/completion or fatal signal/abort/driver error/JavaOOM.
63GCstarts/63summary ends,lastfull232M->175M(247M),349.955ms. No unfinishedGC
captured;this does not establish total/native memory adequacy. Cause unknown.

Read-only original Library bytecode shows alcOpenDevice then handle comparison/
OpenAlUtil.checkALCError,device-name query,ALC capabilities and context creation.
Device open success is observed. No specific later failing API or class is proven.
No new concrete supported compatibility defect was established.

## Narrow next diagnostic

059adds class+load=info and class+init=info to the existing native JVM file output:

```
-Xlog:gc*=debug,safepoint*=debug,class+load=info,class+init=info:file=/download0/java25-gc.log:uptimemillis,level,tags:filecount=1,filesize=4M
```

The existing gc.log/gc-rotated.log routes now contain GC,safepoint AND class-load/
initialization records,tagged by JVM uptime/level/tags. Native FILE routing repair
remains. Active+one rotation have approximate4MiB thresholds each;individual records
can cross a threshold. Retrieve BOTH files after failure;earlier records may rotate.
Previous-run archival/collector still apply. No new listener/thread or report route.

This can reveal which classes load/initialize after native device creation and
whether initialization starts/completes before records stop. It does not itself
prove a class caused termination. Class logging/IO may perturb timings,allocation
and scheduling. JVMuptime differs from observer elapsed;do not equate timestamps.
OpenAL traces remain native-stderr;owner-only burst remains exceptions.log.

Host checks run the exact selector in actual SerialGC JVMs,verify class-load/init
records plus GC/heap/fullpause/safepoints and one-file rollover. Embedded-JVM check
uses the actual callback,confirms dedicated combined-file records and rollover,
and reproduces historical055redirect behavior as control. Target/package checks
verify option bytes,matching Java classes,privateOpenAL binding/source/object hashes,
original54JARs/5147assets,runtime/native/SELF and preserved058. Host success is not
PS5class logging/crash resolution/menu acceptance.

Exact058fullZIP SHA256cd41f2fd2e98d455a1501e6e5b281894f8e5dba07396093e0cc501abec5a3cef,
matching symbols/status/source0eb453224730ec638eeb6adf4c5c8c7ab9378403/build+console
record retained in ignored dist/failures/Client_Original_Startup-01.000.058.
All frozen/failed snapshots retained. Original JAR/assets,runtime image/SDK,heap/
GC/processor/executor/graphics,earlyWSIowner,native stderr/faultrecorder/FILErepair
and058startup-only OpenAL trace binding remain. No replacement game classes/hooks.

Install059,press X once,note display/time/error. After crash,reopen without X.
Retrieve build/session,both GC files,class-tagged records included,native-stderr,
exceptions/burst,VM/process-usage,startup history/tail,abort/fatal. Identify actual
class load/init completion and native device/context sequence before choosing a
repair. Missing/unmatched final records alone cannot identify a fatal instruction.
No menu/milestone/client release/Store download;server2H remains deferred. Complete
release gates including pinned JAR+asset provisioning and exact OpenAL source/relink/
notices/private-shim materials/current catalog rules still apply.

Host/embedded-JVM/target/full-package checks passed. [Build validation](validation/client059-build-2026-10-26.json). Full local ZIP SHA256 `53ce7cc8ff6c83ebec57044951bc44707cbce1322c6188d5e3585745c4857c09`.059PS5pending.
