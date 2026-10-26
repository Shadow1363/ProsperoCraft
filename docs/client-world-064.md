# Client064 — heap headroom for demo world generation

The user reports that063controls work and menu behavior improved. Loading a demo
world then stalled, with an animated background around5FPS. This confirms temporary
menu interaction only; neither world readiness nor full-client performance passed.

Matching run `client-01.000.063-1793010969-702521342` records a real
`OutOfMemoryError: Java heap space` on Worker-Main-1 during class/manifest loading
from entity creation in mineshaft decoration/chunk generation. Afterward the
integrated server repeatedly logs spawn preparation at16percent. The user's visible
roughly30percent is a different observation, not an interchangeable progress metric.
The render thread and integrated server stay active; animation alone is not world
progress. No VM abort was captured. Raw reports remain local; see the
[hashed evidence](validation/client063-world-failure-2026-10-26.json).

Late full SerialGC collections retain roughly224MiB of a247MiB usable heap,
with the old generation full. This is concrete Java heap pressure. It does not
establish total process/native memory availability or a leak. Realms,discovery,
narrator and OSHI warnings are separate from the captured world-generation OOM.

064 increases `-Xmx256m` to `-Xmx384m`, retaining `-Xms16m`, SerialGC, compact
object headers, interpreter mode and the existing runtime/SDK. A historical512MiB
reservation failed in024, so384MiB reservation/commit on the actualPS5 is still
unverified. No direct-memory heap fallback is added; the runtime's metadata-specific
fallback does not apply to the Java heap. No heap increase can promise this world
will fit, and interpreter-mode world generation can remain slow.

The existing bounded observer now takes390regular samples instead of240,
retaining its5second late interval and finite500sample language-transition burst.
This extends late world-loading coverage to roughly20minutes depending on sampling
cost. It does not run indefinitely, restart failed workers or change game state.
Existing native diagnostics remain; logging can perturb timing.

The temporary063controls and supported minimized-only inactivity policy are
retained. Game JARs and original assets remain intact. No world files are deleted,
rewritten or reset; retry through the ordinary demo-menu flow. The exact063package,
symbols and console/build records are independently preserved under ignored
`dist/accepted/Client_Controls-01.000.063/`. This is scoped acceptance of controls
and menu improvement, not a new formal ALL PASS milestone or release.

Host verification includes actual SerialGC allocation at both heap limits:
224MiB retained arrays plus512MiB transient churn fails with a real heap OOM at256MiB
and completes with data intact at384MiB. This is an occupancy control, not Minecraft,
a PS5 memory-map emulation, world-load benchmark or sufficiency proof. Existing
startup host checks and exact package checks are required as well.

Install064,pressXonce,and try the demo world again. Check whether VM startup succeeds,
whether loading advances past the previous stall,and whether the world actually
appears. Allow for slow interpreter generation; record progress and approximate time.
If it stops or crashes,reopen withoutX and retrieve current reports before rerunning.
World interaction,save/reload,speaker output and stability remain pending. No new
GitHub release or Prospero Store submission is made for this candidate.

## Checked candidate

PPSA99874,version01.000.064. Local package:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/dist/PPSA99874.zip`.
SHA256 `87b09e6d64b86f2f0741b12405abf10e165256e2551b34d19fe2ac8ffac3f4c9`.
ActualPS5heap reservation,world progress and performance remain pending.
