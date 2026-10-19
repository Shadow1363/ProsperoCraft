# Build081: original server JAR and remaining mob lag

## Retrieved080evidence

The current080run reaches readiness, admits one authenticated player and remains
RUN in the reports after restart. The capture covers about179seconds JVMuptime;
lasthealth is151seconds afterreadiness,6checks/0scheduledsaves/onejoin, near20TPS.
Heap pressure remains:40allocation-failurefullGCs occur, within1075allocation
collections totaling13503.775ms. The largestGCis352.364ms, and late tick windows
reach572ms. Onecode-cachethresholdGC takes217.478ms; fourmetadataGCs total388.105ms.
The two captures differ in length/workload, so rawcounts are not an A/Bbenchmark.
The data supports heap-GCstalls as a cause of mob/damage lag, not a network
RTTmeasurement or complete attribution of everydelay. Rawreports remain local.

Do not enlarge the heap casually: this run's maxrss_raw reaches497664, and077
previously exhausted native arena allocation. Units/hardlimits are not established
by that field.081retains176MiBheap/NewRatio15/C1/codecache16MiB/SweeperThreshold50
so the vanilla migration does not mix in another memory-budget experiment.
The remaining heap-pressure/collector/memory-headroom work is unresolved.

## Removed transformations

| Development080modification | Development081replacement |
| --- | --- |
| SystemReport.putHardware/putSoftware wrappers | Original signed class; vanilla ignoreErrors catches unsupported PS5 OSHI errors |
| MinecraftServer final-tick injection | Original signed class; JVM counters plus vanilla time/tick/data commands |
| OP grants through injected ServerGameplay25 tick | Standard ops.json written before server start |
| Per-tick food/use and gap observer | Removed; use ordinary gameplay checks and supported administration |
| Unsigned diagnostic derivative | Removed from generation, assets and classpath; original pinned signed JAR executes |

Current active transformations and replacement game classes: **zero**. The
source-controlled execution record pins the official JAR hash. Runtime Java/OS
compatibility patches and a separate harness still exist; unmodified server JAR
does not mean an unmodified JDK or harness. No signature verification is disabled.
Frozen058and older historical source/package snapshots remain unchanged.080is
retained locally for rollback;081has not been validated on PS5 yet.

## Operator and monitoring behavior

At startup, all accounts in the authenticated server's whitelist get vanilla
level4OP entries with bypassesPlayerLimit=false. Existing unrelated operator
entries are preserved. Writes use a probe-owned temporary file and replacement;
invalid policy input leaves the old file intact. The original ServerOpList
loads and verifies these entries in hosttests. Existing online authentication,
whitelist enforcement,20players and permission settings remain.

For whitelist additions during a run, use vanilla op administration or restart
to reapply the startup policy. There is no background game-hook grant. This
change is explicit; it does not silently pretend the old per-tick policy remains.
Vanilla tick query adds targetrate/averagetickcost to logs, alongside gametime,
GCcounters and supported hungerdata queries. Exact injected100tickmaxgap and
food-use transition traces are no longer available. Mean tickrate still does
not prove smoothness. Player-save warning acceptance gates are retained.

## Host checks and console acceptance

- All40official JAR hashes and original execution classpath, no derivative and
  no net/minecraft replacement classes in the helper JAR.
- Original signed SystemReport/MinecraftServer load from server-26.3.jar.
  The original report handles os.name=PS5/unsupportedOSHI through vanilla catch
  behavior while keeping actual JVM memory/flags.
- Level4/no-bypass JSON read by the original vanilla ServerOpList; existing
  entries preserved, repeated preparation idempotent, malformedUUID failure safe.
- Preflight/ZipFS/officialhelp pass; noEULA/worldcreation inhelp.
- Normalworld81-chunk30second C1run passes readiness/NBTsaveprobe,9checks/6saves,
  vanilla tick queries, cleanstop and level.dat. No joinedplayer inhosttest.

PS5pending: VerifyJARs, original-class startup/OSHIwarnings, OPlevel/inventory/
location persistence afterrejoin, shortnormalworldplay andmob/damage/GCstalls,
respawn/food, nativeheadroom/full7200seconds and20playercapacity. Hostchecks do
not prove consoleacceptance or freeze-free play. No new milestone is frozen.

## Next order

First validate the unmodified server and smooth/stable persistence/endurance.
Then test compatible pinned servermodloaders and individualmods. Client work
follows servermods; [PS5_Vulkan](graphics-candidate-ps5-vulkan.md) is a candidate
for that later graphics stage, not an adopted dependency or client proof.
