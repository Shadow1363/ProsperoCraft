> Continuation:055crash confirmed,reports retrieved. Dedicated GC file stayed empty because vm_print ignored its FILE argument;GC records recovered from full startup.log. See [056repair](client-startup-056.md) and [055evidence](validation/client055-startup-failure-2026-10-25.json).

# ProsperoCraft client055 — GC and safepoint transition capture

The user confirms054 reached close to the end of loading and then crashed;
timing is unknown. Its matching run still has120complete snapshots/native phase
pairs,last observation96993ms. That is not an exact crash time. No menu was
accepted. No fatal signal,abort,Java OOM or driver error was captured. Cause
remains unknown. Safari refresh in this continuation could not connect to the
report server;no newer reports were retrieved and no run was restarted.

Exact054 full ZIP SHA256
`4f42a513d81e89777275368e0d5ad36178d0472827998e5a1a59260f7ac6cbbc`,
symbols,status,implementation commit b94d32466a368881e510dfaad37716d88f58e0a6,
build validation,retrieval observations and updated human evidence are retained
under ignored `dist/failures/Client_Original_Startup-01.000.054/`.

## Read-only investigation

[Class and disassembly hashes/findings](validation/client054-resource-path-inspection-2026-10-25.json)
record the original pinned language/reload/font/texture/backend classes inspected
with JDK25 javap. Language loading does JSON parsing and format-regex substitution;
its reload callback checks player state before updating search trees. It does not
directly upload textures. Font and texture reloads involve separate preparation/
apply futures;their later native dependencies include glyph uploads,texture/view
creation and command-encoder writes into the actual Vulkan backend. These paths
do not prove any specific next call executed. No concrete defect was established.

## Smallest next diagnostic

054last Java heap used244209408 of259522560bytes. Stack sampling does not show
whether collection started,completed,or stopped later. This is a missing boundary,
not evidence of heap exhaustion.055adds HotSpot file output:

```
-Xlog:gc*=debug,safepoint*=debug:file=/download0/java25-gc.log:uptimemillis,level,tags:filecount=1,filesize=4M
```

This captures GC starts/ends,heap/phase details and safepoint transitions independently
of the Java observer. Synchronous native log writes can perturb timing;file creation
and last-record persistence need console verification. It is not a crash recorder
and cannot exclude GPU/system termination. File rotation keeps the active log and
one rotated log at an approximate4MiB threshold each;single records may cross the
threshold. The existing240sample observer/cadence and native resource queries stay.

Reusable runtime log transport exposes `/gc.log`,`/gc-rotated.log` and matching
`/previous-gc.log`,`/previous-gc-rotated.log`. Starting a new run archives them;
menu-only reopen preserves them. External collector accepts target address at
runtime. Reports need matching build/session and remain local.

Only launcher version/logging and reusable report transport change. Original54JARs/
5147assets,JVM image,heap256MiB/SerialGC,class-space64MiB,processor policy,graphics,
early WSI ownership,native stderr and fault-recorder repairs remain. No replacement
game classes/bytecode hooks. This is diagnosis,not a supported crash repair.

Host checks exercise the exact option in a real host SerialGC JVM,collection
phases/full pause/safepoints and one-file rollover. Runtime HTTP/archive/collector
checks use actual helper under ASan/UBSan. Target build/package checks validate
exact bytecode,logging/routes,original JAR/assets,native/runtime/SELF audits and
preserved054. Host checks do not validate PS5 GC correctness or menu acceptance.

Install055 and press X once. Record final screen,approximate time and any console
error. After a crash,reopen without X,and retrieve build/session,all existing nine
reports plus both GC reports before another run. Missing GC logging or unfinished
phases require inspection;neither automatically establishes a cause.

No new passing milestone,client release or Store download. Server endurance stays
deferred. Complete release/provisioning/OpenAL/source/license/Store requirements
remain in [the full054handoff](handoff-prosperocraft-client054.md#brandingstore-and-full-release-requirements).

Host/target/full-package checks passed. [Build validation](validation/client055-build-2026-10-25.json).
Full local ZIP SHA256 `33b22e7241dcaf2bd003badd4f7f5fbdbd2781bb51b229918de0e87a687e939c`. Console055pending.
