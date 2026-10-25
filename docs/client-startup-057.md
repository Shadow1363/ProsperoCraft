# ProsperoCraft client057 — main-thread resource-apply transition burst

User confirms056crashed and reopened. Run
`client-01.000.056-1792956807-188322125`;
[hashed complete reports](validation/client056-startup-failure-2026-10-25.json).
Raw files runtime logs/client056-result-20261025. Safari retrieved all nine usual
reports plus gc.log,gc-rotated.log and full startup history without X/restart.
GC.log now contains406780bytes:056FILE routing repair works on PS5. Rotation did
not occur below4MiB and remains unvalidated on console. Rotated/fatal endpoints
return unavailable31byte bodies;they are not fatal diagnostic records.

121complete Java snapshots/121native phase pairs end at97194/97195ms. Last Main
is regex/Language.loadFromJson85 -> ClientLanguage/LanguageManager -> resource
apply/Minecraft.runTick/run;worker idle. No sample122/normal completion/fatal signal,
abort,driver error or JavaOOM. Exact timing/error not supplied. Last stack/record
is not a failing instruction or exact crash time. Cause remains unknown.

GC has63starts and63summary ends. Last full collection completes158134ms JVM uptime,
232M->176M(247M),343.553ms. Later ThreadDump safepoints through162422ms. Observer
clock starts later;do not equate numeric timestamps. No unfinished GC/OOM captured;
completed collections do not prove native/total memory adequacy. Native242records
report query success,handlers0xf,flexible>=324MiB,largest direct>=12124291072bytes;
raw RSSunits remain unverified. Existing fallback/initial-null caveats still apply.

No new concrete compatibility defect was established. Repeating generic policy
queries or changing heap/resolution would not address the missing next transition.
057uses a narrower diagnostic without game hooks. At the first regular snapshot
containing all three exact frames (Language.loadFromJson,
LanguageManager.onResourceManagerReload,Minecraft.runTick),the same observer daemon
performs one burst of up to500owner.getStackTrace samples,sleeping10ms between.
The trigger excludes initial default-language initialization outside main-loop apply.
Nominal499sleeps=4.99seconds,plus stack capture/IO/scheduling overhead;this is not a
10ms sampling guarantee or a game timeout. If the regular observer misses the trigger,
no burst occurs. At most one burst per run;then the existing240sample schedule resumes.

Every burst record includes counter,observer elapsedMs,heapUsed,state,frame count
and END marker. Changed stacks print up to64frames;identical full arrays reference
the previous full transition record. No platform-thread enumeration/sorting or
native memory/limit queries inside the burst. No added daemon. The ordinary observer
and native phase pairs pause during the burst,then resume if the game survives.
GC/native error logs continue independently. Burst errors use the existing observer
failure path;original Main is not modified or controlled. Close prevents later writes.
Stack,state,heap fields are not atomic,and all observation can perturb timing/memory.
An absent/unmatched record alone cannot establish a cause or process death.

Host checks exercise exact trigger positives and constructor/non-main-loop negatives,
actual live owner stack capture/finite records,heap/time markers and close without
later writes,plus prior startup checks. Package verification compares actual nested/
outer observer classes against host-compiled bytes and checks all original JARs/assets,
runtime/native/SELF audits and preserved056. No host test is PS5 acceptance.

Exact056ZIP SHA256587ca6053d121d6cfd5d49d695adc61ff5edb73c03c111e420a5f3ddf74794e1,
matching symbols/status/source2294d97be3c82e9e75a742f9cdc0ff5cc95a4612/build+console
validation preserved in ignored dist/failures/Client_Original_Startup-01.000.056.
Original54JARs/5147assets,heap256MiB,SerialGC,class-space64MiB,processors/executor,
graphics and prior early-owner/stderr/fault-recorder/FILE-routing repairs remain.

Install057,press X once,record final display/time/error. After crash,reopen without X.
Retrieve build/session,exceptions.log (includes MAIN TRANSITION markers),gc.log and
rotated endpoint,native/VM/process-usage,startup history/tail,abort/fatal reports.
Look for first transition after language apply;do not blame the last sampled class.
No menu accepted,milestone/client release/Store download. Server2H remains deferred;
complete release/provisioning/OpenAL/notices/Store gates from054handoff still apply.

Host/target/full-package checks passed. [Build validation](validation/client057-build-2026-10-25.json). Full local ZIP SHA256 `8e7b84a3af448df8bc35f4660829ed9771191860fe075646d0b24badb20e4168`.057PS5pending.
