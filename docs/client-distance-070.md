# Client070 — reduce active world pressure

The user reports stutters again on069. Fresh reports confirm exact069run
`client-01.000.069-1793019718-823915888`. The captured window includes40completed
full collections, reaching950.997ms. AtGC213,609MiBremains after collection in a
748MiBusable heap. The32MiBcodecache is only around44% used near the end; these
are allocation-triggered full collections. This is not a matched FPS benchmark
or proof of a leak. See [evidence](validation/client069-stutters-2026-10-26.json).

The original game console supplies a concrete workload setting: integrated-server
view distance16and simulation distance12. It also reports falling25,899ms behind.
Increasing heap alone did not resolve the retained-world pressure.070therefore
reduces the active chunk workload using supported options, without another heap,
collector, runtime or renderer change.

## One-time settings migration

At the first070launch, the harness backs up changed options exactly as
`options.before-distances070.txt`, then caps `renderDistance` at6and
`simulationDistance` at5. Missing keys receive those defaults. Existing lower
values and all other option bytes are preserved. CRLF is retained for replaced
lines. Invalid nonnumeric values are left to the game's own validation. A
`distances-enabled-070.txt` marker prevents later launches from overriding user
changes. The original26.3Options bytecode confirms the normal simulation slider
minimum is5; no debug flag or game class replacement is used.

The tradeoff is a shorter visible horizon and a smaller active simulation area.
Settings can be adjusted in the game afterward; increasing them may bring pressure
back. A distance reduction does not predict memory in direct proportion to chunk
area, and does not prove all retained data is terrain. Same-world console play
and memory measurements remain necessary.

## What stays

The768MiBheap/NewRatio3,32MiBcodecache, C1level1/onecompiler and correctness gate,
cleanup policies, working speaker audio, temporary controls, renderer and original
54JARs/5,147asset objects stay. Runtime remains
`bb013f533e14f01f0d93d5f4133dad8232385e3e` with0119. Exact069package/symbols are
preserved under `dist/accepted/Client_Heap-01.000.069`; it is not accepted as a
freeze fix. Earlier067audio/066public release/server fallbacks remain available.

## Checks and PS5 comparison

The actual Java migration is tested for16/12->6/5, exact backup, CRLF/unrelated
bytes, lower values, missing/invalid keys, integer overflow and one-time behavior
preserving later edits. Existing startup/audio migration and full package checks
are recorded in [build validation](validation/client070-distance-build-2026-10-26.json).

Install070,pressXonce,andload the same world. Check the video settings show6/5
or previously lower values. Play first in explored terrain, then move into new
terrain. Compare stutter frequency/duration and audio continuity, keeping the app
open for GC/JIT reports. The goal is a smaller stable retained set, not merely a
later OOM. Actual070distance acceptance, memory plateau, pause behavior and
save/reload remain pending. No new public release or Store publication requested.
If frozen/crashed, reopenwithoutXbefore retrieving saved reports. Raw logs remain
local.068's earlier chunk-save failure remains recorded; no successful save is
inferred from the new candidate.
