# Client072 — G1 and measured world headroom at existing quality

071's retained-heap diagnosis succeeded on PS5. Three actual postfullGC samples
contain551,162,968then608,649,976then616,281,760totalshallowbytes. PalettedContainer
counts grow179,438->230,705->251,939; longarrays grow77,685,728->112,050,120->117,765,672bytes.
Chunksections/storage also grow, while BakedQuad count remains149,288and string
count is almoststable. This supports a substantial growingworlddata workload;
it doesnot prove a leak or identify reference owners. FillerElementbytes are
heap filler,not usefulworldobjects. See[evidence](validation/client071-retained-heap-2026-10-26.json).

The optionsfilebeforeMain and originalgameconsole both confirm16view/12simulation,
fancypreset,version5023and070markertrue. The070migrationdiscrepancy remains
unresolved; no furtherautomaticqualityreduction is active. Highsettingsremain
the productgoal. Donotclaim a6/5comparisonpassed or that thehumanchangedsettings.

SerialGC repeatedly compacts the heap with a576MiBoldgeneration nearfull and
roughly600MiBretained. Unsampled fullGCsreach933.366ms.071's three sampledGCs
also include257.222/281.430/284.651msdiagnosticinspection. Those extras do not
explain repeated unsampled stalls, but sampled pauses are not clean benchmarks.

## Candidate policy

| Policy |071diagnostic|072candidate|
| :--- | :--- | :--- |
| Collector |SerialGC|G1(alreadybuiltintoruntime)|
| Heap maximum |768MiB|1536MiB|
| Initial committedheap target |16MiB|128MiB|
| Generation layout |NewRatio3,fixed576/192MiBmaximumsplit|G1adaptive;noNewRatioflag|
| Processor count hint |2|4|
| GCworkers |Serial|2parallel/1concurrent|
| Pause goal |Serial|MaxGCPauseMillis30,softtargetonly|
| G1reserve |N/A|20percent|
| Histograms |3boundedpostfullGCsamples|Disabled|
| Qualityoptions |Preserved|Preserved|

The larger heap is based on measuredretention and allows room for young allocation,
evacuation and the continuing client/integratedserver workload. It doesnot prove
sufficiencyfor everyworld,absenceofleak or guaranteedmemoryavailability. Raising
heapalone already failed in069; G1changes collectionpolicy ratherthan retaining
the same repeatedwholeheapcompaction approach. G1can stillfall back to longfullGCs.
TwoGCworkers/oneconcurrentworker and processorhint4 are a bounded experiment,not
proof of fullPS5utilization. Moreworkers/GCtables use additionalnativememory.

Runtime0121raises only the separate explicitlyuncompressed directheapceiling to
1536MiB. The256MiBnativedata budget, unhinted/nonexec/ENOMEMgates,physicalerrors,
zero/protection/NMT,subrangecommit andwhole-releaseownership remain. G1uses the
existing OScommit/uncommit interfaces; actualPS5G1auxiliarymappings/workers remain
unvalidated. Directfallback physically backs its reservation up front, so Xms128
is not a promise that physicalheapusage starts at128MiB. ExistingC1level1,compiler
limits,32MiBcodecache,cleanup,audio,input,renderer and originalgamefiles remain.

## Checks

The actual1536MiBalignedreservation helperfixture passes underASan/UBSan with a
synthetic2GiBkernelpool,zero/protection/subrangecommit/adjacentdata,ownership/error/
rollback/release andoverbudgetcontrols. TargetHotSpotbuilds withG1enabled.

RealhostG1withcandidateflags retains600MiBplus48MiBlivering through4GiBtransient
churn, preservescheckedcontents, performsconcurrentmarking andhas nofullGCinthis
fixture. NoexplicitSystem.gc is called. This is notMinecraft,PS5timing or a leak
test; arrays alsoexercisehumongousallocation. ActualC1checksum40960/negativecontrols,
startup/logging/optionsobserver and audio-policy tests pass. Fulltargetpackagechecks
are in[validation](validation/client072-g1-build-2026-10-26.json).

## PS5 test

Install072,pressXonce,andconfirmtheexisting16/12qualitysettings. Loadthesameworld,
play in exploredterrain thennewterrain,andcomparepausefrequency/audioresponsiveness.
Keep theappopen forGC/JIT/native/Java reports. Check actualUsingG1,startupreservation,
young/mixed/concurrentcycles,fullGC/evacuationfailures,nativeheadroom andretainedset
ratherthanonlyinitialsmoothness. Ifitcrashes,reopenwithoutXbeforecollectingreports.
G1startup,mapping/workerbehavior,longerplay,memoryplateau andsave/reload remainpending.

Exact071diagnosticbytes/symbols remainpreserved. No newpublicrelease/Storepublication.
Thepublic066playable release and067audio/serverfallbacks remain. Rawreportsstaylocal;
noMinecraftJARtransforms/replacementclasses. Currenthandoff:
[072](handoff-prosperocraft-client072.md).
