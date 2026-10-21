# Build099: online preflight passes, Paper rejects internal Java label

Current099 session/server/exception/startup/native reports were retrieved. The
worker enters Java and all verified online discovery/session/public-key preflight
steps complete. The DNS preparation candidate therefore gets past its earlier
failure in this run. Paper then prints `Unsupported Java detected (25.0.4-internal)`
and returns before server startup. The harness records failure to reach readiness.
No Paper gameplay/plugin execution is established. Raw reports remain local.

100 enables Paper's explicit `Paper.IgnoreJavaVersion=true` policy when the
actualJava25 runtime's java.version contains a prerelease/internal suffix. The
harness still requires Runtime.version().feature()==25. The real runtime version,
vendor and VM remain unchanged and an explicit experimental-runtime message is
logged. No claim of official GA support or upstream validation is made. This is
an intentional Paper configuration opt-in for our experimental port, not a
server-JAR rewrite or runtime identity disguise. It does not change TLS, login
authentication, whitelist, game/ops policy, native memory limits or C1 settings.

A host-only fixture sets the internal version label before the real Paper launch
to reproduce the exact rejection, then exercises the actual configured launch.
The fixture is outside packaged sources/JARs. A focused policy test covers GA
(no new opt-in), internal-label opt-in and preservation of runtime identity and
actual feature25. Runtime native code, moduleimage, upstreamPaper/game/plugin
artifacts remain unchanged. Only separate probe online/version policy code and
consumer version change. Existing Paper plugin/start/save/stop checks remain.

NextPS5: createVM/verify/play; confirm the experimental label message followed
by actualPaper startup. Then join, try `/ps5probe`, movement/food/damage/grass/
chunks/respawn/save/rejoin and Circle for normal save/stop. Reopen after expected
Paper app exit for reports. Native pressure, plugin compatibility and persistence
are unvalidated. Full7200s stays deferred; preserve failed099/098..095,Fabric094,
vanilla083/frozen058. Freeze/release after exact console acceptance, then client.

The host internal-label run passes realPaper105-JARpreflight/startup/plugin
enable/scheduler/command,NBT/protocol,25forcedchunks,15s/7healthchecks/4flushed
saves,normalexit0 andpersistedlevel/regions at384MiB/C1. No player joined. This
is functional host validation, not a PS5/performance/fullendurance claim.
Finalpackage checks pass: onlyServerPaper25probeclass differsfrom099; runtime/
moduleimage/game/plugin unchanged; optin/featuregate/message present,hostfixtures
excluded,105pins/signatures/ZIP/copies/symbols/fallbackhashes match.
Local100 packageSHA256:
`79879fbddcadb64b2aba01358ca2bfb20179cc4093f20aed33e8d13851fde883`.
Development candidate pending actualPS5 validation.
