# Short stutters at120FPS:097logs and098follow-up

Safari downloads identify build097run client-01.000.097-1793111842-641999695.
The retrieved GC window spans uptime368788–427677ms (58.889seconds).
125recorded stop-the-world safepoints have10.886ms median,15.797ms95th percentile
and23.792ms maximum total duration.115exceed the8.34ms120Hz frame budget;
five exceed16.68ms. These pauses are a strong explanation for brief hitches,
but no captured frame-time/stutter timestamps establish event-by-event causality.

Most pauses collect young/mixedG1regions. No fullGC occurs in the window.
The worst23.469ms GC spends16.26ms evacuating the collection set;one worker
spends12.74ms copying objects. The configured8ms pause goal is not a hard limit.
One humongous-allocation collection reports pinned-region evacuation failure,
without observed fullGC escalation. Many524312-byte arrays exceed half the1MiB
region size and take the humongous allocation path;region-size changes require
separate validation and are not included in098.

The app also runs verbose gc*/safepoint*debug and class-load/class-init logging,
producing4MiB in roughly55seconds.098retains bounded GC/safepoint info summaries
and rollover,removing that debug/class trace from the hot path. This reduces
avoidable diagnostic work;it does not remove object-copy pauses or prove the
hitches fixed. Heap1536MiB,G1,8ms goal,four parallel workers,one concurrent worker,
C1,quality settings and original gameJARs stay unchanged.

Actual embedded-host JVM checks verify summary delivery through the real native
FILE callback,original console separation and one-file rollover. Exact098PS5
pause distribution/game-frame comparison and lifecycle remain pending. Native
stderr matches the097run;Minecraft-console endpoint reports unavailable. Safari
lost the PS5 connection before startup/JIT/resource reports could be collected.
Raw reports stay local;public validation contains only hashes and findings.

A fresh Safari tab restored the connection. The later run
client-01.000.097-1793112568-226082328 has 148safepoints,
10.173msmedian/30.408msmaximum,with no fullGC.
Session/native identities agree. JIT compilation continues during startup;no
code-cache-full/disabled diagnostic was observed. Minecraft logging includes
resource/chunk-buffer growth;no frame correlation establishes those as the
reported hitches. Observer output contains only its header,not memory samples.
The two run distributions remain separate in the validation record.
