# Build098: worker enters Java, early online DNS pool creation fails

Current098 session/server/exception/startup/native reports confirm that the
worker enters ServerStart25. Network allocation check and TLS trust (111issuers),
DRBG and default TLS factory complete. The first discovery lookup then fails:
native `DNS pool create` returns0x804101ce,net_errno206,errnoENOMEM, followed by
getaddrinfo EAI_FAIL and UnknownHostException. No remote DNS query or Paper
startup is established. This is a native resolver-pool initialization failure,
not proof of an external service outage. Raw reports remain local.

099 calls the reusable ps5_dns_prepare before JNI_CreateJavaVM. It creates the
same pinned SDK16KiB pool/resolver pair and releases its lookup lease, retaining
the pair for later fresh lookups. It performs no DNS query, stores no answer,
adds no extra resolver/pool and includes no preset device address. Preparation
is idempotent, preserves errors and releases the lease after partial failure.
Early preparation failure is reported explicitly on the createVM row with
native detail. Actual online preflight, verified TLS and login authentication
remain required. See [runtime design and checks](https://github.com/mateo-cogeanu/ps5-java25-homebrew/blob/main/Development/docs/java25-early-dns-pair.md).

Host ASan/UBSan tests compile the actual adapter and hash-pinned SDK lookup/free
plus JDK conversion allocation blocks: pool/resolver preparation failures,
partial retry, lease release, repeated zero-query preparation and errno; existing
400serializedcross-threadfreshlookups while late pool/resolver/heap allocation
is refused, changed answers, query errors/recovery and result allocation cleanup
remain passing. Controlled network APIs do not provePS5earlynetworkavailability,
late query/TLS behavior or native headroom. No new host game run is needed for
the unchanged game/probe/plugin files;095hostPaper evidence is kept separately.

099 changes native bootstrap/adapter preparation only. HotSpot/runtime native
libraries,Paper/game/probe/plugin/moduleimage,C1,384MiBheap/class32MiB/shared128MiB
budget,online/whitelist/ops/20slots/world/view and silence remain. ActualPS5
worker full guard/Detach/join/TLS lifetime remains unvalidated despite callback
entry success. Preserve failed098/097/096/095,Fabric094,vanilla083,frozen058.

NextPS5: createVM/verify/play. If preparation fails, retrieve that native error;
if preflight proceeds, check Paper startup/plugin/joinedplay/food/damage/grass/
chunks/respawn/save/rejoin. Circle requests normal save/stop, then reopen for
reports after expected Paper app exit. Full7200s stays deferred. Freeze/release
only after exact console acceptance; client work follows the server release.

Finalpackagechecks pass: earlyDNSprepare symbol/ready/failuremarkers,105pins/
plugin/audit,currentnativefiles/modules,signatures/ZIP/copies/symbols/silence,
ownershiptables/fallbackhashes. Exact098HotSpot/othernativecode/game/probe/plugin/
moduleimage match. Local099 packageSHA256:
`95c64819077dc00237a856f0a7e942946362efa3493520f17e33b2cf61eab850`.
Development candidate awaiting actualPS5 validation.
