# Build 082 gameplay review and build 083 heap candidate

The current-run reports retrieved on 2026-10-20 identify 01.000.082. The user
reports much better startup followed by increasingly bad lag. Original-server
readiness, OP configuration, vanilla NBT file validation and authenticated joined
play complete. No player-save warning or current-run Java exception appears in
this capture. These observations do not establish persistence or ALL PASS.

## What deteriorated

| GC cause | Captured events | Full collections | Total pause time | Largest pause |
| --- | ---: | ---: | ---: | ---: |
| Allocation failure | 647 | 79 | 23498.720 ms | 360.657 ms |
| Metadata threshold | 0 | 0 | 0 ms | none |
| Code-cache threshold | 2 | 2 | 520.914 ms | 285.064 ms |

The metadata threshold experiment deferred that collection cause in this run;
this is not a controlled A/B test of total gameplay performance. Heap-pressure
collections dominate later. A health interval ending 121 seconds after readiness
records 7087 ms collecting, followed by 15096 ms in the next 30-second interval.
The server reports a 2040 ms / 40-tick overload and tick-query P95 of267.3 ms,
P99 of350.6 ms in one 100-tick sample. Near-20 interval TPS averages obscure
bursts of stalled ticks followed by catch-up.

Full collections repeatedly retain about164–170 MiB inside the approximately
174 MiB effective heap. This is inadequate allocation headroom for the observed
working set, rather than solely an unnecessarily early metadata trigger. The
player later disconnects after death; the capture does not establish a PS5 crash.
The final health sample is181seconds after readiness,7checks/0scheduledsaves/1join;
after departure another interval records no collections. maxrss_raw reaches
503760; its units and the real container/pool limit are not established here.
No network RTT or client frame timing was measured. Raw reports stay private.

## Build 083 change and limits

Increase only the maximum Java heap from176 to192 MiB, retaining the16MiB code
cache, NewRatio15, MetaspaceSize128m, C1 safeguards, index-only image, original
signed Minecraft JAR, world/view/simulation/player/OP/security policies and the
readiness-based two-hour timer. This adds16MiB potential heap use and reduces
native headroom when committed. It is a cautious console experiment, not proof
that native allocation failures are solved. Keep082as a local fallback.

The reusable native sampler also records read-only RLIMIT_DATA/AS/RSS results,
raw soft/hard values and infinity indicators at startup/every60seconds. These
are process policy limits, not available memory or proof of a physical/flexible
pool budget. Failed queries are explicitly marked unavailable by result/errno;
no limits are changed and caller errno is preserved. The runtime repository
owns this shared diagnostic change.

A fresh normal-world C1 host run at192MiB with81forced chunks passes60seconds,
25progress checks,13flushed saves, vanilla NBT validation, clean stop and saved
level.dat. It records769allocation collections, including7full,1915.151ms total
and166.546ms maximum pause; zero metadata/code-cache full collections. Initial
chunk generation also causes a multi-second tick outlier; this is not a smooth
world-generation claim. No host player joined. The seed differs from082's
failed176MiB stress run, so this is a functionality check, not an isolated heap
performance comparison. Prior082stress failure remains recorded.

The native ASan/UBSan report/HTTP/collector test covers real limit queries,
injected query failures, errno preservation and failed output paths. Exact083
package verification is recorded in build-status.json. Host success does not
establish console native headroom, smoothness, player save/rejoin persistence,
food/respawn,20-player capacity or a completed7200seconds. First compare a short
joined-play session and memory/GC reports. No new passing milestone is frozen.
