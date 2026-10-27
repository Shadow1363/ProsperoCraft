# 099: smaller G1 collection batches for120Hz gameplay

The human reports098has essentially the same short stutters. Safari downloads
identify run client-01.000.098-1793112991-20049337. Quieterlogging is verified in
the report format,but is not an accepted performance fix. During uptime120176–
213373ms,301safepoints have8.257msmedian,15.891msp95 and25.769msmaximum;
144exceed8.34ms. No fullGC occurs. These include ongoing mixed/young pauses and
remark/cleanup,not only startup. Frame-time correlation and other causes remain
unresolved. Exact raw-file hashes and interpretation are recorded separately.

099 changes only the G1 collection-batch policy,plus version:

- MaxGCPauseMillis8→4 gives collection budgeting headroom inside an8.34msframe.
- G1NewSizePercent5→1 permits a smaller minimum young generation (about15MiB
 rather than77MiB once the1.5GiBheap is committed). UnlockExperimentalVMOptions
 is required for this upstream flag. This is a minimum,not a fixed young size.
- G1MixedGCCountTarget8→16 lowers the mandatory old-region work assigned per
 mixed collection. The pinned G1Policy::calc_min_old_cset_length divides the
 original candidate count by this target;expensive mandatory regions can
 otherwise exceed a requested pause goal.

The heap maximum remains1536MiB,G1reserve20percent,parallelworkers4/concurrent1,
ActiveProcessorCount4,C1/audio/input/resolution/quality and120Hzoutput unchanged.
No regionsize,gameJAR,gameoptions or world changes. GCpause goals remain soft;
remark/cleanup and individual expensive regions can still exceed them. More
frequent collections can cost throughput or worsen perceived cadence.

Host control checks effective flag values and retained500MiB524312-byte arrays
plus32MiBsmall-objectring/4GiBchurn contents with both policies.098has60pauses/
4.520msmedian versus099168pauses/2.903msmedian;maxima19.295/18.661ms. No fullGC.
This demonstrates the frequency/size tradeoff only;host timing is not evidence
of PS5frame times. The exact candidate must be compared on console in the same
scene/settings,including worst hitches,not only FPS. Logs retain info GC/safepoint
summaries to compare steady gameplay. Revert this policy if cadence worsens.

Preserve098/097/096packages and frozen milestones.099is a local test candidate,
not a public binary release.098stays draft;ProsperoStore must remain unchanged
until the human explicitly confirms a stutter fix. Verify099footer,120Hz,input/
audio/quit-relaunch and save/reload separately. No ALL PASS or milestone inferred.
