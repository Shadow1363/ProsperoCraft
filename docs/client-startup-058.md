# ProsperoCraft client058 — upstream native OpenAL trace

Human confirms057crashed and reopened. Run
`client-01.000.057-1792957885-18345136`;
[complete report hashes and transition timeline](validation/client057-startup-failure-2026-10-25.json).
Raw13reports:runtime logs/client057-result-20261025. Safari option-click retrieval
worked without X/restart. Class-load/fatal/rotated GC endpoints are unavailable
31byte response bodies,not actual fatal/class records.

057has120complete regular snapshots/native phase pairs and17complete burst
records at97110..97278ms. No burst completion/sample18/normal observer end.
Language parsing progresses through immutable translation-map construction;
sample16is ShaderManager.apply/PipelineCache.clear with lambda generation;
sample17is ClassLoader.defineClass1 via Library.tryOpenDevice283 -> SoundEngine/
SoundManager apply -> Minecraft.runTick/run. Language load is not the failing
operation merely because it was the last regular sample in earlier runs.

Original Library bytecode calls alcOpenDevice atbci1/line281. Line283startsbci5,
compares device with0,then the nonzero branch invokes OpenAlUtil.checkALCError,
which calls alcGetError. The last sample does not identify the defined class,
exact bytecode position or any later failing API;do not infer a native OpenAL
fault or claim exact crash timing.63GCstarts/63ends,last full232M->175M(247M),
342.192ms. No captured fatal signal,abort,driver error or JavaOOM. Cause unknown.

Pinned OpenAL1.25.2(commitb2c48f7718ef3fcf67921a8b6534c4914e328970) supports actual
null and loopback backends in this port;026console acceptance covered loopback
mixing,not the game's native playback/context path. No PS5speaker support claim.
Read-only original Library/SoundEngine/LWJGL/OpenAlUtil disassembly and pinned
OpenAL init/open/context source found no new concrete compatibility defect.

## Narrow native diagnostic

058enables existing upstream OpenAL trace messages using its supported
ALSOFT_LOGLEVEL3input. The original OpenAL object/archive/source are retained.
Only a startup-private copy of the OpenAL object has its getenv reference renamed
to client_startup_openal_getenv. That small consumer shim returns"3"for precisely
ALSOFT_LOGLEVEL and delegates all other names to the existing process getenv.
No global getenv definition/environment mutation,backend/device override,API
replacement or game hook. Existing ALSOFT_LOGFILE selection is forwarded too;
without a prior logfile override,upstream traces go to the already captured
native-stderr.log. Messages/IO can perturb native timing;not atomic crash capture.

The resident OpenAL group adds the private trace object/shim while keeping original
lifecycle constructors. Audit records original/private/shim/source hashes and
unchanged backend selection. Other variants/frozen probes still use original
OpenAL objects. Final accepted startup release/relink materials must include this
exact shim/private-object binding and matching source;an old026/036kit is insufficient.

Host checks exercise the actual shim under ASan/UBSan,forced trace-level only,
other missing/present lookups,process value unchanged,and actual pinned OpenAL
library logging0/3controls/device open/context/current/close. Backend selection is
identical in both host controls. This tests host library output,not target crash
resolution. Target/package checks verify actual private undefined/defined symbol
binding,object/source hashes,constructor counts,original JAR/assets/runtime/native/
SELF audits and preserved057. Existing main-thread burst/GC diagnostics remain.

Exact057fullZIP SHA2568e7b84a3af448df8bc35f4660829ed9771191860fe075646d0b24badb20e4168,
symbols/status/source0d35aa395016beb42e064201085de5468ab67836/build+console record
preserved in ignored dist/failures/Client_Original_Startup-01.000.057. Earlier
failed/frozen packages and successful WSI/stderr/fault-recorder/FILE-routing repairs
remain. Original54JARs/5147assets,runtime image/SDK,heap/GC/processor/executor and
graphics policies unchanged. No game class replacements or transformations.

Install058,press X once,note final display/time/error. After crash,reopen without X;
retrieve matching build/session,native-stderr (OpenAL trace),exceptions/burst,GC/
rotated,VM/process-usage,startup history/tail,abort/fatal reports. Inspect actual
native init/device/context completion/error messages rather than blame the last
sampled class. No menu/milestone/client release/Store download;server2H deferred.
Full release still requires exact accepted bytes,complete legitimate pinned JAR+
asset provisioning,matching OpenAL source/relink/notices and current Store rules.

Host/target/full-package checks passed. [Build validation](validation/client058-build-2026-10-25.json). Full local ZIP SHA256 `cd41f2fd2e98d455a1501e6e5b281894f8e5dba07396093e0cc501abec5a3cef`.058PS5pending.
