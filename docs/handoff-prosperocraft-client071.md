# ProsperoCraft071 continuation

Goal: smooth highsettings on nativePS5Java25. Human accepted070only as a diagnostic
comparison, then reports briefsuperresponsiveness followed by super stutters.
They explicitly didnot change settings. Current070reports identify run
client-01.000.070-1793020510-120920601; still16view/12simulation,34capturedfullGCs,
max917.602ms,592MiBretained afterGC181.070's intended6/5comparison was not achieved.
Actual070Main calls prepareDistances; options/marker/preset/datafix effect remains
unresolved. Do not blame user or claim a lower-distancecomparison passed.
See[evidence](validation/client070-stutters-2026-10-26.json).

071disables the active070distance migration, preservesexistingoptions andlogs
onlyselectedversion/graphicsPreset/renderDistance/simulationDistance plus070marker
beforeMain, bounded64chars/value. It doesnotforcehighorlowsettings orrestoreunknown
backups. Human shouldcheck intendedqualitysettings. No furtherqualitycutasfinalfix.

Runtime0120addsopt-inbounded retainedhistograms usingexistinggc+classhisto=trace:
afterexistingfullGConly,retained>=512MiB,atmost3samples,16eligibleGCsapart,top40rows
plusall-class totals/omittedcount. NoextraGC/gamehooks/allocationpolicychanges.
OtherPS5histogramsalsohave40rowoutputcap. Sampledheapwalk/table/sort addsdiagnostic
pause/native-memoryoverhead. Categoriesareshallowbytes/counts,notretainingpaths
orleakproof. ActualPS5heapinspection remains pending. Runtimepublishedat
1ef9b719c749684f4f30f09f928ec599d44c7de8. Sourcegate/outputASanUBSanfixturesand
targetHotSpotbuildpass. Originalupstreamheapwalkmechanismnotreimplemented.

Retain768MiBheap/NewRatio3/32MiBcache/C1level1/cleanup/audio/input/renderer. Game
JARs/assets untouched. Package dist/client-startup/PPSA99874.zip,titlePPSA99874,
version01.000.071,SHA256ea3fb4a81dc2401d0a4a3007e8c14790c42031aa8b717ce287c6ddf29ede9d2c.
[Guide](client-retention-071.md) ·[Build checks](validation/client071-retention-build-2026-10-26.json).
No newpublicrelease/Storepublication. Exact070bytes/symbolspreserved under
dist/accepted/Client_Distance-01.000.070; earlier069/068/067/066/serverfall backs
remain. Preserveacceptedbinaryversions,notformalALLPASSfromplaytestfeedback.

Next: install071,pressXonce,reproducehighqualityworldload,collectGCcurrent/rotated
plusJava/native/JIT/build/session reports assoon as stutters recur. SearchGCfor
PS5 retained histogram sample and topclassrows; compare samplecounts/bytes before
choosingmemory/collectorfix. Treatdiagnosticpausesseparatelyfrombaseline. Current
optionssummaryhelpsinvestigate070migrationfailure. Ifcrashed,reopenwithoutXbefore
retrieval. SafariAXread-onlylinksworkwhenshellLANfails; freshdownloadtimestamps
mustmatchrun. Rawlogsremainlocal. Save/reload/enduranceandnativeheadroompending;
068chunksavefailurestillrecorded,noassumedsavesuccess.

READMEconcise,historyinCHANGELOG;publishconsumerchangeshere, reusableJavafixesvia
runtime syncscript. NoofficialgameJARtransforms/replacementclasses. Nativeport,
noWine. Do notkeepaddingheapordowngradingsettingswithoutretentionevidence.

## Superseded by072

071retrieved3boundedhistograms:worldchunkcontainer/longarraygrowth,stablequadcount,
unsampledSerialfullGCmax933.366ms. Samplesadd257–285msinspection. Actual16/12both
fileandgameconsole.072testsG1/1536MiB/2parallel+1concurrentGCworkers/nohistograms
whilepreservingquality. See[072handoff](handoff-prosperocraft-client072.md) and
[evidence](validation/client071-retained-heap-2026-10-26.json). NoleakprooforG1passyet.
