# Fabric084 native allocation abort and085candidate

Update:085 confirms raw direct mapping/release, then native ZIP allocation stops
the server during a chunk save. See [086follow-up](save-memory-085.md); pending
sections below describe the original085candidate.

The current084run retrieved on2026-10-20 confirms actualPS5 Fabric Loader0.19.5,
the ps5-fabric-smoke entrypoint and Knot target loader. The original underlying
server artifact starts world-fabric-v1, reports real Done readiness, passes the
NBT file-pipeline check and admits an authenticated player. Last health is91s
after readiness/4checks/0scheduledsaves/1join. This is partial compatibility,
not ALL PASS, persistence/rejoin or a two-hour result.

At124.632s JVM uptime, C1CompilerThread0 aborts in Chunk::new requesting32664
native bytes while compiling Netty MessageToMessageEncoder.write(295bytes).
Both32KiB raw anonymous-page attempts fail with ENOMEM. This is a native malloc
abort, not a Java heap OutOfMemoryError or failure to execute the Fabric mod.
The heap is also busy (tenured95%used), so future Java-heap pressure is possible.
Metaspace uses112212KiB/commits113216KiB; code cache uses11512KiB of16MiB.
maxrss_raw reaches524304, with its units/hard-limit significance unproven.

Read-only policy samples show32GiB RLIMIT_DATA and unlimited RLIMIT_AS/RSS.
Those are not available-memory measurements or proof of a flexible/direct pool's
real enforced budget. They do not justify increasing a process limit. Raw
reports, accounts and addresses remain local.

## Runtime0101 and candidate085

The reusable Java-port fix belongs in the runtime repository:
[bounded native direct fallback](https://github.com/mateo-cogeanu/ps5-java25-homebrew/blob/main/Development/docs/java25-native-direct-fallback.md).
Keep the192MiB heap and every084Fabric/game/probe/mod JAR unchanged. Only when
the raw native allocator's ordinary anonymous mapping returns ENOMEM can its
new ledger request real PS5 direct memory for native data, with CPU RW access
and no fixed mapping. The ledger is bounded to2048slots/128MiB held bytes;
this does not preallocate128MiB. Java heap/metaspace/code-cache mapping and
C1 settings are unchanged. No project game transformation is added.

Exact address/size/physical ownership is retained for both small fallback slabs
and large blocks. Map failure rolls back allocation; free unmaps before releasing
backing. Cleanup failure keeps the ledger budget and physical ownership rather
than freeing still-mapped memory or falsely counting a successful release. This
can leak storage until process exit; failure counters make that explicit. All
backend/budget failures can still reach the original fatal allocation contract.
This is not a C1 compiler OOM bailout, a universal native allocator replacement,
or a guarantee that remaining platform operations can allocate under pressure.

Host ASan/UBSan exercises the actual raw allocator/ledger with real aligned
storage and simulated kernel calls: exact32KiB allocation, successful/failed
resize preserving bytes, slab cleanup, allocation/map/rollback/unmap/release
faults, budget/slot exhaustion and4000concurrent lifetimes. Existing raw os.cpp
NMT/preinit and allocation-prefix controls pass with direct memory unavailable.
The patch applies exactly, HotSpot rebuilds, and package checks retain all47
pins, matching modules/libraries, signed containers and one linked ledger with
all five kernel imports. There is no new host game run: unchanged Java artifacts
retain084host Fabric preflight/save-stop evidence; a host JDK cannot exercise
this target kernel fallback.

Pending actual085PS5: direct mapping/release/failure counters, kernel type/cache
behavior, native headroom, joined-play latency/stability, food/respawn, player
save/rejoin and later endurance. Keep083vanilla fallback and084failed package/
matching symbols locally for diagnosis. Start with a short Fabric play check.
Paper/plugins follow a stable Fabric test; the two-hour run remains deferred.
