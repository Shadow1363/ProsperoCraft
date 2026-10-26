# Client071 — identify retained heap at existing quality settings

The user wants smooth high settings.070was accepted only as a diagnostic
comparison, then briefly felt responsive before severe stutters returned. The
human explicitly did not raise settings. Retrieved070run
`client-01.000.070-1793020510-120920601` still logs16view/12simulation,34completed
fullGCs in the captured partial window, and a maximum917.602ms pause.592MiBremain
afterGC181; the log ends duringGC184. The intended6/5comparison therefore did not
occur. See [evidence](validation/client070-stutters-2026-10-26.json).

The actual070Main bytecode invokes its migration. Its effective output still
needs diagnosis: no saved options file, marker or graphics-preset/version values
were captured. The original game's Options uses data fixing and graphics presets,
but their involvement here has not been established. Do not blame user changes,
claim6/5passed, or infer the failed comparison proves lower settings ineffective.

## What071does

071does not invoke070's distance migration. It preserves existing options and logs
only version, graphicsPreset, renderDistance, simulationDistance and presence of
the070marker before originalMain. Each value is bounded to64characters; unrelated
settings are not logged. It neither forces lower settings nor silently restores
unknown backups. Check the game settings still match the intended high profile.

The Java runtime gains opt-in bounded retained-class histograms using its existing
upstream `gc+classhisto=trace` heap inspection path. On PS5:

- Only after a naturally occurring fullGC with at least512MiBretained.
- At most3samples,16eligiblefullcollections apart; no pre-GChistogram.
- Largest40class rows by shallow bytes, explicit omitted-row count and totals
  covering all classes. Other PS5 histogram output also has this40row cap.
- No extraGC request, game-class replacement, bytecode hook or allocation policy
  change. Native table allocation failure uses upstream reporting.

A sampled heap walk/table/sort adds diagnostic overhead inside its fullGC pause.
Do not use071's sampled pauses as a clean performance benchmark. Class histograms
show shallow categories/counts, not reference paths, exact owners or proof of a
leak. Three samples may show growth and guide the next repair. They cannot by
themselves establish that every stutter is GC or whether all memory is justified.

Heap768MiB/NewRatio3,codecache32MiB,C1level1/compilerlimits,cleanup,sound,input and
renderer remain. Runtime patch0120source is published separately. Official game
JARs/assets remain intact. No new release/Storepublication requested.

## Checks and console run

ASan/UBSan fixtures compile the actual runtime sampling gate and histogram output
loop:before/thresholdrejection,stride16,cap3,40rows/all-class totals/smallhistograms.
TargetHotSpot builds. The actual Java selected-options observer is tested for
read-only behavior,high settings/CRLF preservation,private-fieldexclusion,bounds,
missingvalues and070marker. Mainbytecode verifies no active distance migration.
Existingstartup tests exercise the exact newloggingoption on real hostSerialGC,
including fullhistogram availability and file rollover; audio migration remains.
Fulltargetpackagechecks are in [validation](validation/client071-retention-build-2026-10-26.json).

Install071,pressXonce,check the intended quality settings,and reproduce the same
world workload. Keep it open for GC/native/Java reports. Once stutters return,
retrieve reports before restarting; the classhistograms are inGCand safepoints
(current/rotated). If crashed,reopenwithoutX. No guaranteed speed improvement is
claimed. Actual PS5 heap inspection,tablememory overhead and retainedcategories
remain pending. Stop using070as an automatic quality-reduction policy; the goal
is smooth highsettings, with runtime/resources/collector decisions based on evidence.
