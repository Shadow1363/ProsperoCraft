> Continuation:060crashed;15paired native scopes then unmatched alcGetIntegerv16. Host reproduces optional HRTF discovery abort with missingcwd;061repairs lookup error handling and captures query arguments. PS5cause/resolution unproven. See [060evidence](validation/client060-startup-failure-2026-10-26.json) and [061repair](client-startup-061.md).

# ProsperoCraft client060 — native ALC API body scopes

Final product goal is a polished,playable Minecraft Java client on nativeJava25PS5:
responsive controls,smooth rendering,working audio,world play/save/reload and
stability. Menu is a debugging checkpoint,not sufficient full-client acceptance.

User explicitly confirms059crashed before reopening. Run
`client-01.000.059-1793003380-157747534`;
[hashed reports/interpreted measurements](validation/client059-startup-failure-2026-10-26.json).
Raw12reports runtime logs/client059-result-20261026. Safari retrieved current output
without X/restart. No different final screen/error/timing supplied.

Active combined JVM log3817673bytes,rotated4194424bytes:target rotation works.
Earliest retained record97501ms JVMuptime,initialization index7962;earlier boot/
class/GC records rotated out. Retained18GCstarts/18summary ends are partial-run
coverage,not total run collections. Last class sequence verifies OpenAlUtil,
ALC$ICD/ICDStatic/ICDStatic$WriteOnce;last initialization-start at164040ms.
HotSpot class+init INFO emits initialization-start,not a generic completion record;
absence of completion does not prove stuck/failed initialization.

OpenAL still creates No Output device;no context completion. Last mainburst sample
is sound-event lookup/reload,not atomic with later class records. No captured fatal
signal,abort,driver error or JavaOOM. Exact crash instruction/time unknown. Original
ALC.getICD cached router/capability lookup and ALC10.alcGetError JNIinvokePI inspected
read-only.026loopback and original-game initialization order differ. No bad/null
pointer or class/native defect established. Cause remains unknown.

## Narrow native capture

060recompiles only a private copy of pinned OpenAL alc.cpp,with entry/scope-exit
observations in alcGetError,alcGetString,alcGetIntegerv,alcCreateContext and
alcMakeContextCurrent. HeaderScope uses a saturating atomic128call budget per
process,at most256records,unique IDs,API/handle and phase. No extra thread,heap
allocation in the helper itself,signal recovery or API/error-query substitution.
It writes/flushes existing native stderr and restores errno. Underlying stdio can
allocate/lock/fail;IO perturbs timings. No persistence/signal/crash-capture guarantee.

Scope-exit runs for normal return ANDexception unwinding before an outer handler;
it is not a success result or proof the complete exported call returned. A missing
scope-exit narrows an observed gap,not automatically a faulty instruction. Existing
OpenAL trace/error handling retains actual outcomes. The limit may be consumed by
earlier calls;do not infer missing later records without checking the counter.

Builder verifies exact pinned source commit/clean source,uses original Ninja
compiler flags with original alc quote-include path,substitutes only alc.cpp.o in a
private archive,retains original source/object/archive,then applies existing scoped
provider/constructor renames.058private getenv trace binding applies to this result.
Only startup uses it;other variants/frozen probes remain original. Audits include
source/header/unit/archive/final object hashes and original-archive unchanged proof.
No game JAR changes,replacement classes or bytecode hooks. C++ABI/backend selection,
runtime image/SDK,heap/executor/graphics policies and prior fixes remain.

Host test uses actual private patched alc.cpp/sharedlibrary and compares real native
device/error/name/version/context/current/close results with original pinned library;
all5scope pairs observed. Actual header under ASan/UBSan checks4threads,128scope
saturation/256records,exception unwinding and errno. Target/package checks verify
same header/source/archive/object hashes,constructor counts,actual strings,original
54JARs/5147assets,runtime/native/SELF audits and preserved059. Host does not validate
PS5 call ordering,failure behavior or crash resolution.

Exact059fullZIP SHA25653ce7cc8ff6c83ebec57044951bc44707cbce1322c6188d5e3585745c4857c09,
symbols/status/sourcec18b6e406d23eae9cc0760ccf1d201b550c0d9f3/build+console record
retained in ignored dist/failures/Client_Original_Startup-01.000.059. All previous
failed/frozen snapshots retained. Native stderr/faultrecorder,earlyWSIowner,FILE
routing,mainburst/class+GC/OpenALtrace continue. Future accepted release/relink kit
must include exact private native ALC unit/header/compiler inputs plus058shim;old
026/036kit cannot satisfy matching binary/source requirements.

Install060,pressX once,note finalscreen/time/error. After failure,reopen withoutX,
retrieve matching reports,native-stderr boundary pairs plus OpenAL traces,combined
GC/class activeANDrotated,exceptions/mainburst,VM/resources/build/session/startup/
abort/fatal. Inspect whether native getError/query/context scopes are entered/exited;
choose evidence-based repairs. No menu/gameplay/newmilestone/client release/Store
download accepted. Deferredserver2H untouched. Complete provisioning/license/
relink/accepted-byte/catalog gates from054handoff remain.

Host/native/target/full-package checks passed. [Build validation](validation/client060-build-2026-10-26.json). Full local ZIP SHA256 `899252e805cff1031446cdcceaf6e44c331545601599d7e5b4e04c737502873c`.060PS5pending.
