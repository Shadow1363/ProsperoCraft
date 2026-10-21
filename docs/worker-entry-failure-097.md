# Build097: VM/C1 pass, play test fails before worker callback

Current097 session/status, server/exception placeholders, native trace and fresh
startup-tail reports were retrieved. VM creation completes, including a successful
1MiB owned compiler stack, and the105-JAR/C1 preflight returns normally. The play
row is FAIL, but no worker-attached stage, ServerStart25 stage or Java/server
output exists. Old native worker callers did not persist start/join phase and
numeric error. The precise cause (attribute/create/attach) therefore remains
unknown; do not attribute an observed EAGAIN or ENOMEM to this play failure.
A first downloaded startup-tail copy was stale; only fresh097 content supports
this diagnosis. Raw reports stay local.

098 adds reusable JNI-worker preparation before VM creation, caching separate
ordinary and fallback pthread attributes before native pressure. It still tries
the ordinary8MiB stack first. Only pthread_create EAGAIN with errnoENOMEM onPS5
can use a direct stack, limited to8MiB through the existing shared VM ledger.
Runtime0110 supplies stack-purpose ownership, preserving guard-removal subrange
handling rather than replacing direct pages with anonymous MAP_FIXED. Existing
8MiB size, normal AttachCurrentThread/callback/Detach and real join through TLS
completion are retained. Failed join/unmap retains ownership and blocks reuse;
other errors do not falsely succeed. No heap/budget increase or game changes.

The consumer saves phase/code/errno on launch failures to startup and both
current/server exception routes. Completion failures save their phase/code in
startup. This is a concrete pressure-path candidate plus missing-diagnostics
repair; the old report cannot establish which fallback will be exercised.
See [runtime ownership design and limits](https://github.com/mateo-cogeanu/ps5-java25-homebrew/blob/main/Development/docs/java25-jni-worker-stack.md).

Host tests run the actual worker header with a real JVM and pthreads: ordinary
attachment/distinctJNIEnv/callback/detach, late attribute ENOMEM after early
preparation, ordinary create ENOMEM followed by real8MiB explicit-stack success,
non-ENOMEM exclusion, map/create/join/release faults and gated TLS destructors
proving join-before-free. A second test executes the actual0110VMABI/shared
ledger under ASan/UBSan: stack-purpose tag,8MiBcap/page gates, guard-subrange
zero/uncommit/recommit/adjacent data and exact release. TargetHotSpot/exactpatch
pass. Controlled APIs are not fullPS5 kernel/TLS/stack pressure proof.

No new host game run: all Paper/game/probe/plugin/moduleimage bytes remain097;
095hostgame evidence is kept separately. Native JNIworker/bootstrap and libjvm
change. Paper384MiB/class32MiB/sharedpool128MiB/C1/world/view/security/ops/20slots/
silence remain. Preserve failed097/096/095,Fabric094,vanilla083 andfrozen058.

NextPS5: createVM/verify/start. If play entry still fails, retrieve phase/code
before further changes. If it starts, join and test `/ps5probe`, movement, food,
damage, grass, chunks, respawn and save/rejoin; Circle requests normal save/stop,
then reopen for reports. Actual worker launch/guards/attach/lifecycle/native
pressure and Paper gameplay/persistence remain pending. Full7200s stays deferred;
freeze/release only after exact console acceptance, then client work.

Final package checks pass:105pins/plugin/audit,currentnativefiles/modules,linked
0110stackABI,earlyprepare/error-phase/reportstrings,singleownershiptables,
signatures/ZIP/copies/symbols/silence andfallbackhashes. Exact097game/probe/plugin/
moduleimage/othernativecode remain; HotSpotandnativebootstrap change. Local098
packageSHA256:
`1d00d6ce503feb82b9c8fa7209d68b23b81d0baac7c53aa8ae4ea1c6fc1cbe59`.
It is a development candidate awaiting actualPS5 validation.
