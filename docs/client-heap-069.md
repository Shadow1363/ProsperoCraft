# Client069 — heap exhaustion after escalating stutters

The human first reports two stutters in068, then many more and finally a complete
freeze. Three read-only snapshots identify the same exact068run. The first has
full pauses640.757ms and713.728ms as plausible stutter contributors. The later
capture has87completed full collections. The frozen capture explicitly records
Java heap OOM, an observer stopped by OOM, and a chunk-save failure caused by OOM.
Near its end, full collections repeatedly reclaim nothing:499M->499M in a505MiB
usable heap, around610ms each. The log ends duringGC711; it does not prove a native
renderer deadlock. These are overlapping partial snapshots, not counts to sum.
See [068 evidence](validation/client068-stutters-2026-10-26.json).

The32MiBcodecache reduced the earlier captured code-cache pressure, but068's
512MiBheap and generation split did not contain the growing live set. That build
is preserved for diagnosis and is **not accepted as a freeze fix**. Save success
cannot be assumed: the retrieved run includes a failed chunk save.

## Candidate069

- Maximum Java heap increases from512to768MiB, with uncompressed oops retained.
- `NewRatio=3` allows576MiB old space and192MiB reserved young space at maximum
  heap, instead of068's448/64MiB split. Total usable heap excludes one survivor
  space, so reported capacity is lower than the raw maximum reservation.
- C1level1, onecompiler,32MiBcodecache, threshold/cleanup rules, compact headers,
  renderer, controller mapping, sound and game files remain unchanged.
- Runtime patch0119 raises only the separately bounded direct Java-heap ceiling
  to768MiB. The native data/metadata budget remains256MiB. It does not bypass
  physical-memory errors or change executable-mapping policy. Existing gates,
  ledger ownership, zero/protection/NMT, subrange commit and whole-release safety
  remain. Runtime source is published separately in the Java repository.

The runtime reservation test exercises an actual768MiBaligned host fixture under
ASan/UBSan, including zero/protection/uncommit/recommit, neighboring data, all
purpose/error gates, rollback failures, over-budget refusal and release ownership.
Target HotSpot builds. A separate Java occupancy fixture retains472MiB plus a
48MiBrotating ring:512MiBfails with Java heap OOM;768MiBpreserves checked contents
through512MiBtransient churn. This models pressure, not Minecraft or PS5 memory.
The actual C1checksum gate and existing startup host checks pass.

## Console test and limits

After a freeze, reopen without X before retrieving saved reports. Install069,
press X once, and compare the same world while keeping sound enabled. Check
startup, movement, sound, existing-area play and new terrain separately. Keep the
app open for GC/JIT/native reports. A successful768MiBphysical reservation and
longer play without saturation remain pending. More heap can reduce collection
frequency while making eventual full collections larger; this is not a guarantee
of zero pauses, absence of a leak, save integrity or long-term memory sufficiency.

Do not change saved-world settings or overwrite known-good backups as part of
this comparison. The app retains the same title and replaces the prior install.
Accepted067audio and066public playable release are preserved. No new release or
Store publication is requested. Raw reports remain local; original game JARs and
assets stay intact. See [build evidence](validation/client069-heap-build-2026-10-26.json)
and [continuation](handoff-prosperocraft-client069.md).
