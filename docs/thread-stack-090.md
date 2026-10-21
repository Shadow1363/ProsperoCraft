# Build090: metadata succeeds, startup Java threads fail

The current session is090 FAIL, not a recorded VM abort. Its native trace confirms
one aligned4MiB direct metadata reservation at64GiB and zero reported direct
failures. Fabric/the smoke mod and1866advancements load. The first server error
is unable to create native thread in DedicatedServer.initServer, at the vanilla
console-handler Thread.start. Shutdown also fails to start an I/O executor.
Ordinary512KiB pthread creation returns EAGAIN/errnoENOMEM repeatedly. No current
JVM fatal report is recorded, and readiness/player join are not reached. The
exact SDK allocation causing refusal remains unidentified. Raw logs stay local.

091retains0104and224MiB heap and adopts runtime0105for the final Java-thread
EAGAIN/errnoENOMEM case. It supplies an owned direct-backed stack via separate
joinable attributes. A native reaper, started early with an ordinary128KiB stack,
joins finished threads before unmapping/releasing their stacks, including TLS/C++
destructors. Ordinary creation/retries stay first; compiler/VM threads and other
errors do not use this fallback. Stack size remains512KiB for these Java threads.
64slots/32MiB stack-held budget share the existing128MiB direct ledger. Stack
purpose tags keep logical guard uncommit from replacing owned direct pages.

Creation/attribute/allocation failures roll back safely. Failed join/release and
non-returning entry paths retain bounded ownership rather than freeing a live
stack. SDK metadata can still fail even with a supplied stack; this is not an
unlimited native-memory or completed startup/stability fix. Native reaper/explicit
stack/guard/TLS/join/NMT behavior still needs actual PS5 validation.

Host tests use the actual owner/helper with real512KiB custom-stack pthreads and
controlled kernel storage under ASan/UBSan. Gated TLS destructors prove no unmap
before successful join.220lifetimes reclaim; allocation/attribute/create/join/
release faults and slot/byte caps are covered. Metadata lifecycle, real attribute/
800thread, pthread release-check, direct fault/concurrency and prefix controls
pass. Exact0105patch and targetHotSpot build pass. Host reaper scheduling is
controlled; it is not a full target-VM/SDK test. Game/probe/loader/smoke JARs stay
unchanged, retaining089host60s/27checks/14saves/25forced-chunk evidence separately.

Music removal remains: no app playback thread/calls or PCM assets. Test silent
startup, native stack create/reap markers, readiness and short joined play with
new chunks/damage/grass/save/rejoin. Full two-hour run remains deferred. Preserve
058frozen and083vanilla fallback plus exact failed090package locally. No ALL PASS
or arbitrary mod/Paper/plugin/20-player capacity claim.
