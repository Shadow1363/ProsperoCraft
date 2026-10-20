# Build 081 gameplay review and build 082 candidate

The reports retrieved on 2026-10-20 identify build 01.000.081 and confirm normal
world readiness and an authenticated player joining the original server JAR.
The OP configuration and vanilla NBT file check complete. The unsupported OSHI
hardware/software warnings are caught by the original server, as intended.
No player-save warning appears in this capture. This does not prove inventory
or location persistence after rejoining, a completed save cycle or ALL PASS.

## Captured pauses

The recording covers about 151 seconds of JVM uptime. The last health sample is
121 seconds after readiness: five checks, zero scheduled saves, one join.
Interval tick rates range from 19.84 to 20.17 TPS; the vanilla tick-query averages
are 0.1–13.4 ms. These averages cannot rule out intermittent visible stalls.

| GC cause | Captured events | Full collections | Total pause time | Largest pause |
| --- | ---: | ---: | ---: | ---: |
| Allocation failure | 560 | 5 | 3035.822 ms | 338.456 ms |
| Metadata threshold | 4 | 4 | 487.907 ms | 283.445 ms |
| Code-cache threshold | 1 | 1 | 231.542 ms | 231.542 ms |

The heap full collections occur in bursts around JVM seconds 99–100 and 115.
These remain a concrete source of mob/damage stalls. No client-frame timing or
network RTT was recorded, so the reports do not attribute every delay to GC.
Raw reports and account/address fields stay local.

## Build 082 change

Set the existing MetaspaceSize flag to 128 MiB, deferring metadata-growth-triggered
collections during initial class loading. This is the initial GC trigger threshold,
not an instruction to allocate 128 MiB up front and not MaxMetaspaceSize. Metadata
is still committed on demand. The tradeoff is allowing metadata to grow further
before a threshold-triggered collection, potentially retaining more dead classes
until another collection. Native allocation failure and other GC causes remain
possible; this does not cap memory or guarantee headroom.

Keep the 176 MiB heap, NewRatio 15, 16 MiB code cache, SweeperThreshold 50,
class-space setting, C1 safeguards, original JAR, world/view/player/OP policies,
authentication and readiness-based two-hour timer unchanged. Do not mix a heap
increase or collector switch into this first metadata-threshold comparison.
The five allocation-failure full GCs and code-cache-triggered pause are not fixed
by this setting; further work depends on the next console measurements.

Host controls and package verification are recorded in build-status.json.
Host results are not PS5 pause measurements. Pending: exact 082 console startup,
joined-play GC causes/pause frequency/native usage, persistence/rejoin, respawn,
food and eventual full two-hour run. No new passing milestone is frozen.

## Host stress failure

The first 082 candidate run forced 81 chunks in a fresh normal world at176MiB.
It exhausted the Java heap during loading; the process did not recover after
SIGTERM and was stopped after local reports were copied. This is a failed
stress check, not a console result, and the threshold is not proven to cause
or resolve it. Earlier small-heap world-generation failures remain relevant.
A subsequent light check initially could not bind because that failed JVM had
not yet exited; that invocation is invalid as a candidate comparison. It was
retried only after the failed process exited. Neither failure is hidden by a
lighter check. Repeating sustained generation at this heap remains necessary.

The light normal-world retry (no forced chunk radius, no player) passes real
readiness, the vanilla NBT file check,11tick checks,5saves and cleanstop over
20seconds. Its log has zero metadata-threshold/code-cache full GCs and one
allocation-failure full GC of115.742ms. This only validates basic operation and
the intended trigger deferral in that short host workload. It does not offset
the81chunk failure or prove a PS5 speedup. Keep081as a local fallback.
