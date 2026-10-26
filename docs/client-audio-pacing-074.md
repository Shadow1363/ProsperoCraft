# Client074 — early AudioOut initialization and shorter-pause experiment

The user confirms073is stillsilent and its smallstuttersareannoying. Same-run
reports identifyclient-01.000.073-1793023452-211762662. AudioOutInitreturns0x80260002
andportOpenreturns0x8026000f onall20attempts(twoOpenALdeviceattempts). Noport/PCM
success occurred.073's boundedlate-recovery didnotwork. The precisecause of the
serviceinitializationfailure is stillunknown; this doesnot establish thatG1
causedit. See[evidence](validation/client073-audio-stutters-2026-10-26.json).

The partialGCwindow has99pauses,median18.082ms,max41.608ms,andnofullGC. Those pauses
can be noticeable; without frame timestamps they cannot explain everyvisiblehitch.
The enabledstartupstackobserver also causedThreadDumpsafepoints up to8.927444ms.
Existing16view/12simulation/fancyquality remains. Noqualityreduction is proposed.

## Audio initialization order

074calls the realSDK `sceAudioOutInit` on the native startupthread after embedded
coreconstructors but **beforeJNI_CreateJavaVM**, the largeheapreservation andJVM
workerstartup. It logs the signed/hexresult and stores it in a process-local
bootstrapdatum. This rawSDKcall doesnot runOpenALmixing/constructors early, allocate
afakeport, or depend on the laterOpenALscopedmutex/providers.

Only actualearlysuccess or explicitAlreadyInit seeds thebackend's service-ready
state. Failed/unattemptedearlyinitialization still uses073's boundedlate-recovery;
errors are not converted to success. A realAudioOutport must stillopen, mixactual
PCM and be audible. Earlyinit failure is nonfatal to game startup and remains
visible in startup/native logs. The SDK owns serviceinternals; no undocumented
shutdown/reset or otherappportmanipulation is used. Ifearlyinitfails too, this
narrows the timing/affinity/resource hypotheses but doesnot solve them by itself.

The hostrealOpenALASan/UBSantest adds successfulearlyinit/AlreadyInit (no duplicate
backendinit), failed/unattemptedearlyinit (latepath remains) andearlysuccessfollowed
byactualopenfailure (noportleak), with15fault/mix/lifecyclemodes in total.
These do not emulate PS5AudioOut or proveaudibility.

## Remaining stutter experiment

- KeepG1/1536MiBheap/Xms128/20percentreserve/oneconcurrentGCworker/processorhint4.
- LowerG1's softpausegoal30->8ms and use4parallelGCworkers instead of2. This asks
  for smallercollectionbatches withmoreparallelwork;8msisnotaguarantee. Moreworkers
  consumeCPU/native threadresources and can affect gameplaythroughput.
- Startupstackobserver is now opt-in via `ps5.startupObserver`; defaultperformance
  runs do not callitsperiodicall-threadstackwalks. Its boundedimplementation remains
  available for explicitdiagnosis; ordinaryJava/native/GC/JITreports remain.

ExistingC1gate/compilerlimits/codecache/cleanup/audioformat/renderer/input and
qualityoptions stay. The native SDK initializationorder plusGC/observer changes
are a combinedcandidate,not an isolatedcausalbenchmark. HostactualG1workload and
C1/options/observercontrols pass;targetchecks are in
[validation](validation/client074-audio-pacing-build-2026-10-26.json).

## Console test

Install074,pressXonce,andtestmenu/worldsoundandthesamehighsettingsworld. Checkthat
startup/native reports show the pre-JVMinitresult, actualportopen andfirstPCM.
Human-audiblesound is required for audioacceptance. Comparestutters duringexisting
terrain andnewterrain;keeptheappopen forGC/native/Javareports. Ifsilent/crashed,
reopenwithoutXbeforecollection. Audioinitializationorder/GCworkers/nativeheadroom/
pauseimprovement remain pending. Smallstutters,save/reload/endurance remain open.

Exact073package/symbols remain preserved as a failedaudiorecoverycandidate.
No newpublicrelease or Storepublication requested. Runtimeimplementation stays
1b9206f4290432548b94d19b0a177dba47f6fb47; officialgameJARs/assetsstayintact. Rawlogs
remainlocal;publicevidencehashes/interpretation only. Currenthandoff:
[074](handoff-prosperocraft-client074.md).
