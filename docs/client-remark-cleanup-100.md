# 100: isolate the remaining remark cleanup spikes

The tester reports much less stutter in 099, with some hitches remaining. The
current Safari session identifies run client-01.000.099-1793113748-238732459.
From 60.002 to 168.382 seconds, 671 safepoints have a 4.368 ms median, 7.522 ms
95th percentile and 21.078 ms maximum. Only 23 exceed the 8.34 ms frame budget.
The largest remaining events are G1PauseRemark, around 13–21 ms. No full GC is
recorded. This supports the partial improvement report, but does not establish
identical workloads or an event-by-event correlation with perceived hitches.

Earlier 097 phase reports put class/compiled-code cleanup at 6.481 ms of a
10.225 ms remark and 17.603 ms of a 28.116 ms remark. Another cleanup took
17.283 ms, including 7.216 ms G1 Complete Cleaning and 6.731 ms Purge Unlinked
NMethods. These are historical phase measurements; 099 summary logs do not
provide a new subphase breakdown. In the pinned runtime, G1ConcurrentMark::remark
runs unload_classes_and_code only when ClassUnloadingWithConcurrentMark is true.

100 adds only -XX:-ClassUnloadingWithConcurrentMark to the 099 policy, plus its
version increment. This tests whether removing that remark work reduces the
remaining spikes. It leaves ClassUnloading enabled, so full collections can still
reclaim unused classes and their loaders. Heap size, quality, workers, C1, input,
audio, 120 Hz and original game JARs remain unchanged. No runtime patch is needed.

This is a reversible isolation candidate, not a completed long-session fix.
Deferring cleanup keeps unused class metadata/loaders/compiled code longer and
can increase heap, metaspace or code-cache pressure, especially after resource
reloads and repeated world/server changes. Full GC itself can cause a longer
pause. Other remark work and ordinary collection pauses remain. Preserve 099 as
the partially improved fallback; do not claim zero stutter or unlimited play.

The host regression uses a real JVM and 120 disposable class loaders. It checks
that the cleanup phase executes in the 099 concurrent control, is absent in the
100 concurrent control, and that an explicit full GC under the 100 policy still
reclaims all 120 fixture classes/loaders while live payload remains intact. It
also checks effective flags. Baseline concurrent unloading counts are permitted
to vary with reachability/timing. These are semantics checks, not PS5 latency or
memory acceptance. Test 100 in the same scene/settings, then check world/server
switches, reloads, audio, controls and Quit/relaunch. Retrieve current GC/JIT logs
if hitches persist or memory/code-cache pressure appears.

No release or ProsperoStore update is authorized until the tester confirms the
stutter fix. Keep 098 in draft and preserve every prior exact package and frozen
milestone. Target build/package validation and checksums are recorded separately.
