# Build076 console performance review

The user reports much better native gameplay but remaining sluggishness. The
recorded076run reaches normal-world Done, grants the configured operator policy
and admits one authenticated player. The latest health record covers332seconds
after readiness and includes one flushed world save. This is not ALLPASS, a
completed two-hour run or proof that player data persisted.

## Captured measurements

-70tick windows cover7000tick intervals;72intervals exceed100ms.
- Largest recorded tick gap:567ms. Many settled windows peak around52–60ms.
- Health samples report approximately20TPS; mean TPS does not rule out stutter.
- Across the captured JVM lifetime:74full GC pauses total18657.002ms; all GC
  pauses total20919.409ms. Worst individual GC pause:353.761ms.
- Repeated allocation-failure full GCs retain about146–157MiB in a173MiB
  effective heap. Heap cap remains176MiB; the difference includes collector
  layout/alignment. The old generation's share at NewRatio7 is tight.
- Code cache remains around53–59percent occupied near later full GCs; no
  captured full-code-cache/compiler-disabled condition establishes it as the
  bottleneck. The last resource maxrss_raw is522624; units/meaning must not be
  treated as proof of a hard memory cap.
- Three player-data save warnings occur around an automatic save, the explicit
  world save and disconnect. Vanilla PlayerDataStorage catches Exception and
  logs only a warning without the caught cause. World-save acknowledgement
  therefore does not establish successful player persistence.

Raw reports and identity/address fields remain local. No network RTT, packet
throughput or client-frame timing was measured; these logs cannot exclude a
separate network/chunk-delivery or client bottleneck.

## Build077 candidate

Try NewRatio15 within the same176MiB heap and native/code-cache budget. This
gives the old generation a larger share at the cost of a smaller young
generation and potentially more minor collections. It is a console tuning
candidate, not established optimal performance.

Two sequential host normal-world81-chunk30second tests complete saves and clean
stop at the same176MiB cap/C1/compactheaders. NewRatio15:20full collections,
3080.1ms total GC,185.975ms worst GC,11231ms maximum initial generation gap;
9checks/5saves. NewRatio7:14full collections,2158.6ms total GC,159.432ms worst GC,
6554ms maximum initial gap;12checks/7saves. They have no joined player and use
fresh procedurally generated worlds. These are not controlled identical-world
benchmarks and do not demonstrate an improvement from NewRatio15. Actual PS5
comparison is required;076configuration remains the recorded baseline.

077also exercises vanilla NbtIo.writeCompressed(Path), which requests SYNC,
then vanilla Util.safeReplaceFile twice, validates backup creation and reads
back each revision. All files live in a fresh probe-owned directory inside
the world, removed after checking. A failing phase prints the real exception
and fails the test. This tests the file pipeline, not full player serialization.
Player-save warnings now fail endurance acceptance, including final stop.
The game derivative and existing official JARs receive no changes.

Pending: PS5 save pipeline and actual player save/rejoin persistence, post-join
GC/tick-gap comparison, respawn/food/mob/chunk-delivery checks, full7200seconds
and20-player capacity. Preserve frozen058;076is not a new passing milestone.
