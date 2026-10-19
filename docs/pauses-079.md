# Build079 frequent pauses and080candidate

The user reports shorter but more frequent freezes, which feel worse. The goal
is smooth tick delivery; reducing only individual pause duration is inadequate.
Current079reports reach normal-world readiness and an authenticated join. The
available trace ends near49seconds JVMuptime and primarily covers startup and
firstjoin. It is not a sustained gameplay sample or ALLPASS.

## Measured cause

Five Serialfullcollections explicitly caused by CodeCacheGCThreshold occur at
16.385,22.931,24.802,26.239,33.534seconds. They total1029.431ms and individually
take177.555–269.367ms. Cacheoccupancy attrigger is37.117–57.227percent, well
below exhausted. DefaultSweeperThreshold15scales the growth threshold as free
space shrinks; the collector can stop the game every fewseconds during C1warmup.
The native port's actualcode/codeCache.cpp and runtimeflag definitions confirm
this trigger. It does not establish that every reported freeze has this cause.

The521youngallocation-failure pauses total1269.837ms,maximum8.245ms. Three
metadatafullpauses total134.402ms,maximum98.226ms. Healthinterval averages20TPS
despitevisiblepauses; meanTPS cannot establish smoothness. No networkRTT/client
frametime was measured. No rawaccount/address/reportdata is published.

## Change and tradeoff

080sets the existing productflag SweeperThreshold=50.0 with the same16MiB
codecache,176MiBheap,NewRatio15,C1limits and index-onlymoduleimage. It keeps
StartAggressiveSweepingAt=10 and UseCodeCacheFlushing=true: near-full cleanup
remains. It does not disable GC/unloading or enlarge budgets. The tradeoff is
less eager unloading and potentially greater cacheoccupancy before collection.
Laternear-fullcleanup, heap/metadataGC, resourceIO/saves and other causes remain.

Two sequential hostC1flatworld81-chunk20second controls use the same settings
except SweeperThreshold15or50. Both pass readiness, vanillaNBTsavepipeline,
10tickchecks/5saves and cleanstop. Threshold15:2code-triggerGCs/212.348ms,
6fullGCs,1113.055ms totalGC,max130.067ms. Threshold50:0code-triggerGCs,5fullGCs,
1049.508ms totalGC,max133.172ms. Maxinitialtickgap760ms versus699ms; subsequent
windowmaxima are60–74ms versus57–80ms. These short no-playerhost runs support
the intendedtriggerchange, not freeze-free PS5play or a strictlatencybenchmark.
Supportedflag parsing confirms aggressive10percentfreecleanup/flushing remain.

No server-JAR transformation, gameclass replacement, world/view/simulation/
player/OP/authentication/security/timerpolicy changes are introduced. Consumer
launchconfig owns the setting; the runtime remains pinned with its index-only
reader repairs. Preserve frozen058and record actualPS5pausefrequency/longest
gaps/nativeheadroom/postjoinGCcauses before the full7200second run. Player
persistence/respawn/food/mobdamage and20playercapacity remain pending.
