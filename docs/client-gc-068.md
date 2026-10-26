# Client068 — intermittent freeze investigation

The user confirms that067's game audio works beautifully on PS5, then reports
intermittent freezes. Whether sound continues through a freeze is unknown.
The exact working audio package and native symbols are preserved locally.

## What the current run establishes

Build067, run `client-01.000.067-1793016824-383235260`, contains **15 completed
full GC pauses** in the captured part of its rotated/current logs. These pauses
sum to **7,562.291ms**, with a maximum of **647.647ms**. Seven are allocation
failures, seven are code-cache threshold collections and one is aggressive
code-cache cleanup. Earlier events have rotated out; these are partial-window
counts, not the whole session. See the [evidence record](validation/client067-audio-freezes-2026-10-26.json).

The old generation has349,568KiB of capacity. Just before GC122 it contains
349,567KiB; afterward338,711KiB remain. That leaves little room for promotion
of long-lived objects from the young generation. The16MiB compiled-code cache
also explicitly requests GC, including aggressive cleanup at9.999% free.
The actual HotSpot `CodeCache::gc_on_allocation` implementation explains the
threshold's increasing collection frequency near exhaustion.

These stop-the-world pauses are a confirmed contributor to freezes. The user
has supplied no timestamped freeze markers, so they do not explain every visual
stall or establish that rendering, compilation, chunk generation and I/O never
contribute. No replacement sound/game classes or game-bytecode hooks are used.
Raw reports remain local; published evidence contains hashes and interpretation.

## Candidate changes

| Setting |067 audio build|068 candidate|
| :--- | :--- | :--- |
| Maximum Java heap |512MiB|512MiB|
| Collector |SerialGC|SerialGC|
| Generation ratio |Default2|`-XX:NewRatio=7`|
| Maximum old generation |About341MiB|448MiB|
| Reserved young generation at maximum heap |About171MiB|64MiB|
| Compiled-code cache |16MiB|32MiB|

The generation split gives the observed live set more old-generation headroom
inside the same heap reservation. Smaller young space can mean more frequent
young collections and promotions; it does not eliminate full GC. The larger
code cache postpones pressure at the observed code footprint. It reserves up to
16MiB more native code memory, so PS5 native headroom still needs checking.
SweeperThreshold50, aggressive cleanup at10% free and code-cache flushing remain
in place; no GC or safety cleanup is disabled.

The guarded C1 level1/compiler limits, original game files,512MiB direct-heap
runtime, temporary controls, renderer, view settings and working AudioOut backend
are retained. The one-time067 volume migration marker stays067, preserving later
user volume choices. Runtime implementation remains
`44fdf26ccb74cf8dd9127f1256b85416856981de`.

## Checks and limits

An actual host SerialGC workload retains330MiB, rotates a48MiB live ring and
allocates2GiB of transient arrays. Both layouts preserve every checked value.
The old capacity rises from349,568to458,752KiB; allocation-triggered full pauses
fall from23to20, while young pauses rise from26to84 in this fixture. This is a
modest, workload-specific improvement, not Minecraft frame-time or PS5 proof.

The actual C1 checksum gate and stale/interpreter/missing-log controls pass with
the candidate flags. Startup/observer/native allocation/configuration and audio
migration host controls pass. Target compile/link/SELF and full package checks
verify original JARs/assets, runtime/native audits and preserved067bytes.
See the [build record](validation/client068-gc-build-2026-10-26.json).

## PS5 comparison

Install068 and press X once. Load the same world and spend a few minutes moving,
turning the camera and breaking blocks in an already explored area. Then compare
new terrain generation separately. Note whether freezes are fewer/shorter and
whether sound continues through them. The candidate's PS5 benefit is pending.

Keep the app open for current GC/JIT reports. If it crashes, reopen without X
before collecting saved reports. Confirm build/run identity before interpreting
logs, and compare similar gameplay windows rather than total counts from runs
of different length. Preserve067as the known audible fallback. No new GitHub
release or Store publication is requested; source development is published.
