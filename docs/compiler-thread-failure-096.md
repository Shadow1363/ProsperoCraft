# Build096: class reservation succeeds, compiler thread creation fails

The current PS5 session is096 and aborts inside JNI_CreateJavaVM. Native reports
confirm0108's32MiB direct class reservation,4MiB alignment and zero reported
allocator failures. VM initialization progresses to threadtype3 (compiler_thread),
then four ordinary pthread_create attempts fail with EAGAIN/errnoENOMEM for a
1MiB stack. The abort reports unable to create native thread. Paper never runs.
This is partial class-reservation validation, not full classloading/GC/encoding
or native stability proof. Raw reports remain local.

097 adopts runtime0109: the existing final owned-stack fallback now accepts
compiler_thread as well as java_thread. It preserves the requested1MiB compiler
stack, original thread entry/guards, dedicated joinable attributes and reaper
join through TLS destruction before exact release. Budgets remain32MiB held
stack backing inside the128MiB shared native ledger; no compiler disable, stack
shrink, extra pool or cap increase. Ordinary success, other errors and VM/GC/
watcher threads are not changed. SDK descriptors/TLS can still fail despite
having direct stack backing. See the runtime's
[design and lifecycle limits](https://github.com/mateo-cogeanu/ps5-java25-homebrew/blob/main/Development/docs/java25-compiler-thread-stack.md).

Tests compile the actual create-thread gate and cover45 combinations of thread
type, return code and errno, including preserved stack sizes/entry arguments.
Actual owner tests run real1MiB custom pthread stacks and gated TLS destructors,
join-before-free,220reclaimed lifetimes and allocation/attribute/create/join/
release/slot/budget controls under ASan/UBSan.512KiB Java-stack regressions,
targetHotSpot compilation and exact patch application also pass. These owner
controls do not replace fullPS5 C1 execution, guard, reaper or resource-pressure
testing. No new host game run: Paper/game/probe/plugin/moduleimage and all
settings remain unchanged;095host60s and shortened-play evidence stays separate.

NextPS5: createVM, then VerifyJARs/actualC1 gate. If successful, startPaper/join,
try `/ps5probe`, movement/food/damage/grass/newchunks/respawn/save/rejoin. Circle
requests normal save/stop; reopen for reports after Paper's expected app exit.
Classspace32MiB/Paperheap384MiB/sharedpool128MiB/C1/config/security/whitelist/
level4ops/20slots/silence remain. Full7200s stays deferred; Paper/nativepressure/
playerpersistence remain unvalidated. Preserve failed096/095,Fabric094,vanilla083
and frozen058. Freeze/release only after exact console acceptance, then client.

Final package checks pass:105pins/plugin/audit,allcurrenttargetnativefiles and
linkedruntime,signatures,ZIPintegrity,copies/symbols,singleownershiptables and
retainedfallbackhashes. Exact096Paper/game/probe/plugin/moduleimage andother
nativecode match; onlyruntimeHotSpot changes. Local097 packageSHA256:
`82069ab3d49bb0392915054f509412976be8e83a82828f3411e923d4c4181469`.
This is a development candidate awaiting PS5 validation.
