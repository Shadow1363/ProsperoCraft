# Client073 — repair audio startup while retaining G1

The user reports only tiny stutters on072but no sound. Fresh reports identify
runclient-01.000.072-1793022349-811312662. The capturedGCwindow has92pauses,
median20.8335ms,p95nearest-rank31.636ms,max49.747ms,andnofullcollection. Actual
young/mixed/concurrentG1activity is recorded at16view/12simulation. This is a
partialwindow plus qualifiedhumanfeedback,not a matchedbenchmark,zero-stutter,
endurance or fullhardwareutilization guarantee. Pin-related evacuationrecords
remainfollow-up evidence. See [072evidence](validation/client072-g1-audio-2026-10-26.json).

Sound fails before speaker-port opening: `sceAudioOutInit` returns
`-2144993278` (`0x80260002`) twice; the game reports failedOpenALdevice. Noactual
open or firstPCMrecord follows. This establishes a nativeinitialization failure,
not simply muted volume. The precisePS5servicecause is unresolved. Public
[AudioOut error definitions](https://github.com/shadps4-emu/shadPS4/blob/main/src/core/libraries/audio/audioout_error.h)
corroborate the commonBusycode0x80260002and distinguishAlreadyInit0x8026000e;
those PS4project definitions do not prove the internalPS5cause.

## Bounded recovery

073keeps the working G1/1536MiBheap/GCworkers/processorhint/C1/graphics/input and
existing quality settings. Only the nativeOpenALstartup recovery changes:

- Successful init is cached. ExplicitAlreadyInit permits an actualportopen.
- On the observedBusyinitresult, probe the realSYSTEM/mainAudioOutport. Busy is
  **not** treated as a successful device: a validport must actually open.
- If Busyinit is followed by Busy/NotInitfromopen, retry atmost10attempts with
  atmost9waitsof50ms(total450msdelay). The last failure is an actualOpenALerror.
- Unknowninit errors, unrelatedopen errors and retry-wait failures abort promptly.
  No unbounded loop, unknown-error suppression, fakePCM or null-backendfallback.
- A successfulrealopen marks service ready and logs recovery. The original real
  mixer/format/pacing/firstPCM/failure-disconnect/join-before-drain/close behavior
  remains. Portownership begins only whenopenreturns a validhandle.

RealOpenALhosttests underASan/UBSan cover transientBusy/NotInitthenrecovery,
permanentBusyboundedfailure,Busywithactualportavailable,AlreadyInit,unknowninit,
unrelatedopenfailure andwaitfailure. ActualPCM,resampling/stereobalance/three
lifecycles/pause-resume/output-disconnect checks remain. Tests assertcalls/waits
and zeroportleaks; hostAudioOutfixtures are not audiblePS5acceptance. Existing
startup/options/audio-policy and fullpackage checks are recorded in
[build validation](validation/client073-audio-build-2026-10-26.json).

## PS5 test

Install073,pressXonce,andtest menu clicks/music plus worldfootsteps/block sounds
while checking that072's improvedresponsiveness remains. Keep theappopen for
native/Java/GC reports. Recovery requires actualopen/firstPCM and human-audible
sound; neither retry logs nor API calls alone establish audibility. If it fails,
reopenwithoutXbeforecollection. Startupbusy may be persistent;073is a scoped
recovery candidate,not proof that the underlyingPS5servicecondition is solved.

Smallstutters,GCpinning/nativeheadroom andextendedplay/save-reload remain open.
No additionalGCtuning or qualityreduction is part of this repair. Exact072package
and symbols remainpreserved; no formalALLPASS or new publicrelease inferred.
Runtime remains1b9206f4290432548b94d19b0a177dba47f6fb47. OfficialgameJARs/assets
are intact. No Storepublication or new release requested. Rawreportsstaylocal.
