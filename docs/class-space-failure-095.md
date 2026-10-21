# Build095 VM creation: compressed class-space reservation fails

The user reports a crash while creating the VM. Current095 session/abort/startup
and native-trace reports confirm an initialization abort before Paper starts:
`Could not allocate compressed class space: 33554432 bytes`. Native output shows
repeated ordinary32MiB reserves with ENOMEM and a final37,748,736-byte aligned
attempt with ENOMEM. The candidate requests384MiB Java heap and32MiB compressed
class space. This is not a Paper gameplay/plugin failure or a measurement of
available system RAM. Startup history contains older runs; their gameplay is
not attributed to095. Raw reports remain local.

096 adopts reusable runtime0108: only PS5AMD64 with compact headers, after all
ordinary class-space placement/reservation fails with ENOMEM, tries the existing
bounded direct-memory metadata backend. It keeps the normal range/encoding
initialization and protection zone. The allocation is zeroed, PROT_NONE and NMT
tagged mtClass; existing metadata commit/subrange-uncommit/exact-release paths
retain ownership. It does not add a pool, raise the shared128MiB cap, lower the
class-space size, or change the384MiB heap. The32MiB class backing is physically
charged immediately, leaving less shared budget for other native data and stacks.
Further pressure failures remain possible. See the runtime repository's
[0108 design and limits](https://github.com/mateo-cogeanu/ps5-java25-homebrew/blob/main/Development/docs/java25-compact-class-space-direct.md).

Host checks execute the actual reservation, shared ledger and release dispatcher
under ASan/UBSan over controlled kernel APIs with real aligned storage. They
cover32MiB/4MiB alignment, mtClass NMT, inaccessible/zeroed storage, subrange
uncommit/recommit/adjacent data, ordinary-success/error/header/range gates,
shared-budget refusal and allocation/map/protect/release faults. Compact-pointer
arithmetic roundtrips are checked; full HotSpot classloading/GC/encoding/NMT
behavior on PS5 is not proven. Existing non-class metadata controls, target
HotSpot build and exact patch application pass.

No new host game run is needed for the unchanged consumer JARs/config. The095
hostPaper60s/28healthchecks/14flushedsaves/normalexit and separate shortened play
fixture remain host evidence only. Paper artifacts, probe/plugin bytes, module
image,384MiBheap, view4/simulation3, online authentication/whitelist/ops/20slots,
normal shutdown classification and silence are retained. No game-JAR rewrite,
replacement game class or extra Paper patch is introduced.

NextPS5: VM creation first; inspect the class-space direct-reservation marker.
Then verify/start/join, `/ps5probe`, movement/food/damage/grass/chunks/respawn,
save/rejoin and Circle for normal stop. Reopen for reports after Paper exits.
ActualPS5 classloading/C1/GC/protection/nativeheadroom and Paper/plugin persistence
remain pending. Full two-hour test stays deferred. Preserve exactfailed095,
Fabric094,vanilla083 and frozen058. No passing Paper release yet; freeze/release
after exact console acceptance, then client work.

Final package checks pass: current targetnative libraries/modules,105upstream
pins/plugin/audit,linked0108 marker/singleledger/previousruntimeexports,signatures,
ZIPintegrity andmatchingpackage/symbolcopies. Game/probe/plugin/moduleimage and
othernativecode match095; exactfailed095/Fabric094/vanilla083/frozen058 preserved.
Local096 packageSHA256:
`ce96d3ad3aee39dcc11476f97e9f3b9d41e9c4971e9afee8d93561a55d190497`.
This is a development candidate, not a passing release asset.
