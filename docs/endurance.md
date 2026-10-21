# Online two-hour PS5 server endurance probe — build01.000.065

This development build extends the passing058 startup/save/stop fixture. The
Server_Start snapshot and exact passing package remain frozen. Runtime pin,
160MiB Java heap,8MiB native worker and interpreter mode are unchanged.

Run the five menu rows in order. Row4 first waits for real Minecraft readiness,
then runs for at least7200 seconds before a final flushed save, clean stop,
server-thread exit and nonempty world/level.dat check. Run Destroy Java VM only
after that row returns. Keep the app open and the console awake throughout.
If a row fails, leave the probe open for log collection before starting new rows.
The native menu timer includes startup; the Java health log measures the timed
endurance phase separately. Startup and shutdown can extend total elapsed time.

The server uses the existing isolated mc-server-start world/configuration.
Automatic pause when empty is disabled using pause-when-empty-seconds=0.
Every30 seconds the fixture sends time query gametime, waits for a fresh reply
and requires game time to advance. Every five minutes it requests save-all
flush and requires the completion acknowledgement. A final flushed save is
required even for a shortened host test. New server-thread ERROR logs, thread
exit, unresponsive commands or stalled game time cause failure. Command replies
have a120-second deadline; save work contributes to the endurance duration.

Log sharing remains on the existing runtime-selected address/port. Read
server.log for MC_ENDURANCE_BEGIN, MC_ENDURANCE_HEALTH and
MC_ENDURANCE_COMPLETE; these record elapsed time, actual game time, check/save
counts and Java heap usage. Success also requires MC_SERVER_ENDURANCE_OK and
the native row returning PASS, followed by VM destruction. Heap usage is Java
memory, not available native memory. A running menu or elapsed clock alone is
not proof of healthy ticks or a passing run.

The baseline workload uses low-distance flat-world settings without simulated
players. Build060 allows the configured account to join and records successful
join counts; it does not require a client to stay connected for the full run.
Loaded-chunk/client gameplay performance and multiplayer endurance need actual
client observations. Forced chunk loading is not added. No preset device IP or client filter is embedded.

For a short host regression after preparation:

```sh
python3 tools/test_server_start.py --endurance-seconds 75
```

The host run uses2-second checks and4-second saves so multiple real command
replies and flushes are exercised, including more than the usual60-second
empty-server pause threshold. It does not establish the requested two-hour
PS5 pass. Saved-world reload, player joins and longer performance/endurance
coverage remain separate validation work.


## Online login observation during059

The current059 console confirms that a LAN client reaches the listening server,
but discovery.minecraftservices.com fails with UnknownHostException. Authlib
then has no SESSION/verify endpoint and rejects login with its generic
Authentication servers are down message. This does not establish a global
service outage. The screenshot's server entry demonstrates status discovery,
not successful authenticated admission. Whitelist is also enabled.

The exact native resolver error is not present in the collected Java report;
that cause must be localized before claiming a DNS repair. No authentication,
whitelist, resolver settings or active console run were changed. The collected
snapshot shows real game-time progression through120seconds and the worker
remains RUN; the full two-hour outcome remains pending. Failed login is separate
from server-thread endurance checks and does not establish multiplayer support.


## Build060 online setup

Package with --join-player YOUR_ACCOUNT. The local app contains only that
account-name setting in a generated join-player.txt asset; the name is not in
source Git. Before server launch the fixture requires genuine DNS and verified
HTTPS responses from discovery/profile/session-profile/public-key services,
then merges the verified account into whitelist.json. Existing entries remain.
Online authentication and certificate validation remain enabled. This preflight
checks service reachability and profile identity, not a successful hasJoined
exchange; real admission is proved only when a client actually joins.

Install the complete060 folder with the current probe closed, then run rows in
order. After successful preflight and Done readiness, the7200-second timer
starts automatically. The configured account can try joining with the matching
Minecraft Java26.3 client. Whitelisting occurs before launch. Watch the console
log for MC_ONLINE_PREFLIGHT_OK and later actual player-join output. A preflight
failure reports DNS, HTTP/TLS or profile validation context and leaves the
native resolver stages available in vm-trace.log. No guessed endpoint IP,
offline identity or permissive TLS behavior is used.

Host integration can exercise real online preflight plus a short endurance:

```sh
python3 tools/test_server_start.py --endurance-seconds 75 --online-player YOUR_ACCOUNT
```

Host success cannot establish the PS5 resolver repair or authenticated client
admission. All060 console rows and the actual two-hour result remain pending.


Build060 also fails an online-enabled run if an authentication-thread ERROR is
observed; join/authentication-error counts are logged with health reports.
Monitoring that starts more than one poll interval after readiness is rejected,
so an unobserved readiness interval cannot silently count toward a pass.
The final host integration passes online preflight plus75seconds of live ticks,
36 checks,18 flushes, clean stop and saved metadata, with zero simulated joins.
Actual PS5 online admission and7200seconds remain unvalidated.


## Build061 trust-store repair

060 resolves DNS but TLS preflight fails with no trust anchors, before starting
the server/timer.061 adds genuine java.io descriptor metadata fallback and
relative File resolution for whitelist discovery. Look for MC_TLS_TRUST_FILE
and MC_TLS_TRUST_OK acceptedIssuers before MC_ONLINE_PREFLIGHT_OK. All certificate
and online-identity checks remain standard. The real host HTTPS preflight
passes under injected desktop metadata denial with the target111-root store;
console TLS/admission and the full7200second outcome remain pending.


## Build062 authentication discovery DNS repair

061 gets through standard TLS trust/preflight and real readiness, then its
Minecraft discovery thread cannot allocate a new DNS pool.062 retains one
bounded real pool/resolver pair from preflight and serializes fresh queries.
Expect DNS pool/resolver reuse stages in native trace. The harness now rejects
Minecraft discovery failures before the timed phase and checks discoveryErrors
alongside login errors afterward. This prevents a no-player endurance run
from passing after an observed discovery failure. A zero join count still does
not validate actual player admission. Host40second online readiness/save/stop
passes; PS5 admission and the full two-hour result remain pending. Install062,
run the normal rows and join after readiness; do not treat preflight or package
checks as a console pass. The frozen058 milestone is unchanged.


## Build063 native-memory headroom

062 confirms online identity authentication but native allocation fails during
update_tags configuration, followed by chunk-loading/thread failures and VM
abort.063 uses144MiB max heap and512KiB Java thread stacks and unpooled Netty buffers, retaining real direct
ioBuffer allocation. MC_NETWORK_MEMORY_OK confirms allocator and64KiB growth;
networkErrors records Netty ERROR lines and blocks a pass. Default TLS and
online authentication remain enabled. The host60second workload requests49
flat chunks and validates tick/save/stop at144MiB; it does not reproduce the
console's process memory ceiling or player connection. All063 console rows,
complete authenticated world entry and two-hour completion remain pending.
The console still uses real player chunk loading; validationChunkRadius is an
optional host stress setting and is absent from native launch options.


## Build 064: gameplay checks before sustained-load validation

063 reaches authenticated gameplay but drops to about 11 observed TPS. The
human reports repeating food-use animation below full hunger without food
consumption or an error. No specific food exception is captured, so lag remains
a candidate explanation rather than an established diagnosis.

064 reduces native slab churn, repeated native trace-context lookup and
successful-phase disk logging. It retains 144 MiB heap, 512 KiB Java stacks,
unpooled buffers and interpreter mode. Health logs include observedTps and real
GC totals/deltas. MC_GAMEPLAY_SAMPLE precedes read-only vanilla foodLevel,
foodSaturationLevel and foodExhaustionLevel queries for connected players.
No hunger/game rules are changed. Retest eating and responsiveness for roughly
a minute while leaving the probe open; collect those reports before a full
sustained-load attempt. The configured 7,200-second phase remains available.
PS5 performance/eating, player-data save warning cause and full completion
remain pending. Host telemetry/forced-chunk tests do not validate player eating.


## Build 065: existing player-directory startup

064 fails in legacy-player conversion before Done because java.io File.listFiles
returns null. 065 adapts PS5 java.io directory listing to the existing resident
reader and adds MC_LEGACY_DIRECTORY_OK before conversion. It does not remove or
skip legacy files. The actual-JNI host test and an existing-directory server
fixture pass, including readiness, tick checks, saves and clean stop. Retest
065 startup and authenticated gameplay, then reproduce hungry food use while
leaving the probe open. GC/TPS/hunger diagnostics and the configured two-hour
phase remain. Console eating/performance and full endurance are still pending.


## Build 066: gameplay before sustained load

065 authenticates the client but drops to about 10–13 TPS and does not confirm
chicken/mutton consumption below full hunger. 066 is a guarded C1 level-1 test
with one compiler and the existing 8 MiB code cache. Run all rows in order;
preflight must print JIT_WARMUP_OK after actual current-run compilation.
If it fails or crashes, preserve/relaunch to share reports before starting
another run. The current/previous JIT reports are downloadable.

During the server row, join with the vanilla client and test chicken/mutton
below full hunger. MC_ITEM_USE records the server use timer, held/use counts,
food and elapsed ticks/wall time without changing gameplay. Compare with TPS,
GC and native resource samples. MC_ITEM_USE_UNAVAILABLE means this diagnostic
failed, not that consumption succeeded. Host C1 startup/30-second save/stop and
observer initialization pass, with no player. PS5 JIT, food/mob performance,
persistence and full7200seconds remain pending. Readiness starts the timer;
a failed run does not qualify as an endurance pass.


## Build 067: retry verification before gameplay

066 records C1 compilations but fails at the combined management stage with
bare OOM before the explicit warmup or server readiness. 067 adds scoped native
library-name/symbol allocation fallback and separate management checkpoints.
The exact console allocation cause and repair remain pending. Host native fault
regressions, target rebuild, full C1 preflight and package checks pass.

Install067 and run the rows in order. Preserve failed reports if any row fails.
Only after verification passes, run the server row and test chicken/mutton below
full hunger, then inspect MC_ITEM_USE/TPS/GC. The configured two-hour timer still
starts at readiness; neither066 nor067 has a console endurance pass.


## Build 068: compiler/native pressure retest

067 gets past verification and admits the client, then C1 aborts on native arena
allocation at66.53seconds VM uptime. Its8MiB cache has space left but repeatedly
requests full GC at its threshold. 068 bounds unused arena chunk caches/reclaims
on refusal, uses16MiBcache, scaling4 and a2MiB per-compilation arena limit. Heap
remains144MiB. Host60second/49chunk/28check/14save test passes with no player.

Run068 rows in order, then join and compare gameplay interruptions, GC reasons
and native resource growth. Hungry chicken/mutton tests still need an active
MC_ITEM_USE transition, completed stack decrement and hunger restoration.
Preserve crash reports on any failure. The two-hour timer still begins at real
readiness; short startup/join success does not establish the endurance result.


## Build 069: metadata growth during join

068 aborts before admission while the real gameplayprotocol classes need a
new16MiB non-class metadata region. 069 uses4MiB PS5 roots/nodes and explicitly
loads the actual serverbound/clientbound templates after readiness. Look for
MC_GAME_PROTOCOL_OK; this is protocol preparation, not proof of admission.
The timer continues from the original Done timestamp. Host protocol preparation
and60second/49chunk/28check/14save test pass without a player, on desktop geometry.

Retest069 rows in order and join. Preserve the reports on any failure. PS5
metadata/encoding/nativebudget, hungry chicken/mutton consumption, mob latency,
player persistence and7200second completion remain pending. The new4MiB root
also bounds individual metadata allocations to4MiB; total space grows in nodes.


## Build 070: short gameplay/GC check before full endurance

069 confirms actual chicken consumption/hunger increases and much faster human
reported gameplay, with remaininglag andone~5second recoveredfreeze. Its logs
show many full allocation-failure GCs, but no individual pause above274ms.
070 changes only the generation ratio under the same144MiBcap and adds100tick
wallgap maxima. Runtime4MiBroots and the069food behavior remain. The previous
069run was left alone; no full-duration test was requested or claimed now.

On the next short gameplay check compare GC counts/time and MC_TICK_GAP maxima
alongside food/mobs. A near20TPS average can hide pauses followed by catchup.
Host occupancycontrol and60second/49chunk/29check/14save run pass without a
player. PS5layout tradeoffs/freeze cause and the full7200seconds remain pending.


## Build071: normal terrain and short respawn check first

Install the complete071folder with the probe closed. Start the five-row sequence
as usual. Row4 uses a separate normal world `world-normal-v1`, with structures,
view4chunks, simulation3and max20players. The old flat `world` is preserved.
Use the same authenticated whitelisted account; it receives persisted level4OP
before joining. All admitted whitelisted players receive OP through vanilla
permission APIs. `/gamemode creative` prevents hostile-mob damage; alternatively
`/difficulty peaceful` removes hostile mobs. Neither command is auto-applied.

Check food consumption, mob motion, travel and death/respawn briefly before
committing to a full run. Console071startup/decode/compact-header C1/GC behavior,
normal generation, respawn stability and latency remain unvalidated. A20-player
configured limit is not proof of20-player performance. Four chunks is a
conservative initial view distance for the current memory budget, not a claim
of desktop render distance or optimal speed. Host normal-world attempts without
compact headers hit JavaheapOOM; the final host checks are in build status.

The timer still starts at real server readiness, including any subsequent chunk
generation pauses. Do not treat a successful join or short run as a7200-second
pass. Preserve current-run logs if startup or respawn fails. Frozen058remains
unchanged; no new passing snapshot is created for071.


## Build072: early TLS repair before a timed run

071failed before server readiness.072uses runtime OS entropy seeding and emits
MC_TLS_RANDOM_BEGIN/OK and MC_TLS_FACTORY_BEGIN/OK before network discovery.
First confirm these stages, actual server readiness and a short join/respawn
check. A process crash without fatal/Java/signal evidence is not proven repaired
by the seed-source change. Normal-world/OP settings and the7200second timer from
real Done remain unchanged. The existing game-JAR derivative receives no new
transformations. All072console checks and sustained performance remain pending.


## Build073: kernel RNG confirmation

072crashes at an unresolved direct RNG import.073repairs that runtime call using
checked kernel entropy and preserves all existing world/OP/timer settings.
Confirm PS5_OS_ENTROPY_OK kernel source, MC_TLS_RANDOM_OK, MC_TLS_FACTORY_OK
and actual server readiness before a short gameplay/respawn check and full run.
A kernel-query error must now produce ProviderException, rather than a null
call. Actual console query/TLS acceptance and the earlier071cause are pending.
The existing game derivative and Minecraft harness are unchanged.


## Build074: native image loading confirmation

073completes DRBG but fails loading DTLSInputRecord during TLS factory setup.
074repairs native image ZIP allocation and error handling; Minecraft Java/game
classes remain unchanged. Confirm MC_TLS_RANDOM_OK, MC_TLS_FACTORY_OK, real
online preflight and Done before a short join/respawn check and full run.
Image decode failures should now return an explicit resource error instead of
parsing failed temporary bytes. Actual PS5 acceptance remains pending.

## Build075: isolate HTTPS setup before endurance

074 passes DRBG/TLS factory and DTLS class loading, then crashes after discovery
DNS success. No fatal location was captured.075 emits MC_ONLINE_PHASE markers
with phase, public host and Java heap values around URL/connection construction,
configuration, response/body and cleanup. These diagnostics are not a crash fix.
Keep the probe open after a failure so current-run reports can be retrieved.
Do not begin the two-hour run until readiness and short gameplay/respawn checks
are stable. The timer still starts at real Done; settings and existing game
derivative remain unchanged.

## Build076: resource-buffer fallback before readiness

075stops constructing the HTTPS connection, before a request; no fatal native
address was captured.076repairs ordinary native image output-buffer allocation
with scoped PS5 fallback/checked refusal and terminal-header handling. This
addresses a source gap; the crash cause is not proven. Confirm phase progress
and actual Done, then short join/respawn/food/latency checks before7200seconds.
Game derivative, world/view/simulation/OP/JIT/heap/security options stay unchanged.

## Build077: GC comparison and player-save gate

076admits a player and averages near20TPS in health samples, but full-GC pauses
and repeated player-save warnings remain.077tries NewRatio15 at the same176MiB
cap and runs a vanilla NBT SYNC-write/replacement/backup/readback check. Require
MC_SAVE_CHECK_OK and no player-save warning; validate actual inventory/location
persistence after rejoin. A successful file probe cannot prove player
serialization works. Save warnings now fail the monitor and final-stop checks.
Compare PS5 post-join GC/tick gaps with076before claiming a speedup; host results
do not demonstrate improvement. See[measurements](performance-076.md). The
7200-second timer remains anchored to actual Done. Do not freeze a milestone
until the human reports ALLPASS for the exact build.

## Build078: native memory headroom before a full run

077crashes at97.573s with confirmedC1nativearenaOOM, despite muchbetterreported
gameplay.078uses a1MiBresidentJavaimageindex with on-demandresourcereads, saving
25.8MiBofpersistentcopy and retaining176MiBheap/NewRatio15/C1/settings. Confirm
the index-onlytrace, normalstartup and a shortjoinedchunk-loading session first.
VanillaNBTfilecheckpassedon077; actualplayersave/rejoinpersistence is stillneeded.
No full-durationpass or compilerOOMbailout is claimed. See[repairlimits](native-memory-077.md).

## Build079: require Java/native image-reader agreement

078failsverification after all40JARhashchecks because Java still expects a full
map while the native reader supplies only its index.079aligns Java's PS5mode,
retains the memorysaving and records nested causes. Require verify-row success
and realstartup before joinedchunk-loading/save/rejoin checks. Actualnative
headroom and7200second stability remain pending. See[details](image-reader-078.md).

## Build080: measure pause frequency, not only peak duration

079has repeated code-cache-triggered SerialfullGCs before the cache is full.080
defers that heuristic with SweeperThreshold50, preserving10percentfreeaggressive
cleanup and existing budgets. Host code-triggerGCcount falls2to0, but other
pauses remain. Compare actualPS5postjoin pausefrequency, worsttickgaps, GCcauses
and memoryheadroom before7200seconds. See[measurements](pauses-079.md). Do not
claim freeze-free operation from average20TPS or a shorthostrun.

## Build081: original-server acceptance before server mods

081executes the original pinned signed server JAR and removes both gameclass
transformations. Confirm verification/startup, vanilla ops.json level4/no bypass,
player-save/rejoin, mob/damage/GC behavior and shortplay before7200seconds.
Use vanilla tick/time/data outputs and JVM counters; injected per-tick/fooduse
metrics are gone. Current startup-whitelist accounts get OP through ops.json;
use vanilla op or restart after runtime whitelist additions. See[migration](vanilla-081.md).
After the stable unmodified-server baseline, work proceeds to servermods, then
clientgraphics/input. PS5_Vulkan is recorded as a later candidate.

## Build 082: isolate metadata-triggered pauses

081 starts the original server and admits a player, but metadata, heap and
code-cache full-GC pauses remain.082 uses MetaspaceSize=128m to defer only the
metadata trigger; allocation is still on demand. Compare joined-play GC causes,
frequency, longest pauses and native usage. The heap remains176MiB. Require
save/rejoin checks before the full two-hour test; this tuning is not ALL PASS.
See[the current review](pauses-081.md).

## Build083: heap-pressure follow-up

082joined play reaches repeated near-full live heaps and spends15seconds of one
30-second interval in GC.083tries192MiB maximum heap with other GC/C1 policies
unchanged, plus read-only process-policy limit sampling. The original server JAR
remains intact. First validate startup and short joined play/native headroom;
do not treat the60-second host81-chunk save-stop pass as a console or two-hour
pass. Full GCs and world-generation stalls still require investigation.
See [evidence and tradeoffs](pauses-082.md).

## User deferral and Fabric084

On2026-10-20 the user reports no lag in083joined play and defers the full two-hour
run until later. Continue with Fabric/mods, then Paper/plugins, before client
work. This is not a completed endurance result or ALL PASS. Preserve083vanilla.
084is a short loader/mod compatibility play test in world-fabric-v1. Its monitor
can remain open up to7200seconds with300-second saves, but a short session does
not establish that result. See [Fabric instructions](fabric-084.md).

## Build085: native C1 allocation follow-up

084Fabric/mod/world/join work on PS5, then a32KiB native C1 arena allocation
aborts the VM at124.632s.085uses runtime0101bounded direct-memory fallback for
raw anonymous-map ENOMEM, retaining192MiB heap and all084JARs. First validate
kernel mapping/release counters and short joined play. Heap/metaspace/codecache
mapping is unchanged; other allocators can still fail. No full two-hour result.
See [evidence and limitations](native-memory-084.md).

## Build086: shared native ZIP/image save allocation

085direct mapping/release is observed on PS5, then a chunk-save Deflater native
allocation fails and the server closes the client connection.086shares the VM
ledger with native ZIP/image buffers, retaining all game artifacts and192MiB
heap/settings. Validate short joined play plus actual player/world saves/rejoin.
The row is called Server play test; full7200seconds remains deferred, not passed.
See [evidence and limits](save-memory-085.md).

## Build087: player-save cause and spawn building

086 fails after disconnect with a player-save warning; no current VM abort is
established.087 disables spawn protection, tests the exact players/data directory
and captures bounded standard VM exception logs. Save repair is not yet proven;
short building/leave/rejoin checks come first. Full7200seconds remains deferred.
See [evidence and diagnostic limits](player-save-086.md).

## Build088: native thread headroom control

087 admits the player then fails native worker creation during chunk generation.
088 tests176MiB heap instead of192MiB and adds standard VM thread diagnostics.
It does not guarantee a native reserve; GC/heap tradeoffs and actual PS5 join,
movement/save/rejoin need validation. Full7200seconds remains deferred.
See [evidence and limitations](native-thread-087.md).

## Build089: heap headroom with bounded VM libc use

088joined gameplay suffers repeated full GC (29.072seconds in one30-second
interval), matching delayed updates.089uses224MiB heap plus runtime0103VM-owned
libc budget, retaining view4/simulation3 and normal world. Expected packet
exception logging is disabled; native thread diagnostics remain bounded. Actual
PS5 performance/thread headroom/save/rejoin pending. Full7200seconds deferred.
See [evidence and limits](gc-pressure-088.md).

## Build090: metadata reservation and silent app

089aborts on an ordinary4MiB metadata reservation.090retains224MiB heap and uses
runtime0104's bounded non-class metadata fallback with exact lifecycle handling.
App music/playback thread/PCM assets are removed at user request. ActualPS5
startup/memory lifecycle/silent menu/joined speed/save/rejoin pending;7200seconds
remains deferred. See [evidence and limitations](metaspace-crash-089.md).

## Build091: owned Java thread stacks

090directmetadata reservation succeeds, then ordinaryJava thread creation fails
EAGAIN/ENOMEM.091adds runtime0105explicit stack/join-before-free reaping while
retaining224MiB and silence. ActualSDK stack/guard/TLS/join/NMT/startup/joined
play/save/rejoin remain pending; full7200seconds deferred.
See [evidence and ownership limits](thread-stack-090.md).
