# Current ProsperoCraft handoff — client064

Continue existing sources/history. Read both AGENTS.md,client-world-064.md,and
handoff063/complete054for historical requirements. No subagents or server2Hrun.
Goal:polished playable nativeJava25PS5Minecraft;menu is intermediate.

## Latest console evidence

User confirms063controls work and menu lag improved,but still feels slow. Demo
world attempted;human~30percent then apparentstall,animatedbackground~5FPS.
Retrieved13current reports read-only through Safari,noX/restart. Run
client-01.000.063-1793010969-702521342. Raw runtime logs/client063-world-20261026;
public hashed record docs/validation/client063-world-failure-2026-10-26.json.
Actual Worker-Main-1 Java heap OOM while loading class/manifest fromEntityType
creation,mineshaft decoration/chunkgeneration. Spawn log repeats16percent after
OOM;humanUI30percent is a different metric. Render/server remainactive;animation
notprogress. NoVMabort/fatal captured;otherRealms/discovery/narrator/OSHIwarnings
notdiagnosedcausal. FullGC late238–239MiB->224MiB/247MiBusable,old174784KiBfull.
Observerended436137ms;GCcontinues777608ms/full175. Noatomiccrash/deadlockproof.

## 064 change

Only Java heap cap256->384MiB plus observer240->390samples/5slatecadence and
version labels. Xms16m,SerialGC,compactheaders,interpreter,SDK/runtime unchanged.
Historical024512MiBreservationfailed;384PS5reservation/commit/sufficiencyunproven.
Noheapdirectfallback:runtimeMemoryReserverdirectfallbackmetadataspecific only.
Actualhost224MiBretainedarrays+512MiBtransientchurnfails256heapOOM,completes384
contentsintact. Occupancymodel,notMinecraft/PS5mapping/performanceproof.
Existing063SDLtemporarycontrols/idleminimizedpolicy,062OpenALexplicitpathretained.
All54originalJARs/5147assetsintact;noworldfileschanged/deleted/nogamehooks.

Exact063fullZIPa1c62a8a6ccc8554c77ea3166633545fd08da6ca2b8e1ebffaf0c843677545f0,
symbols/buildstatus/buildvalidation/consoleresult preservedindependentCOWunder
ignored dist/accepted/Client_Controls-01.000.063. Thisisscopedcontrols/menuacceptance,
notformalALLPASS/newfrozenmilestone/release.062menuGitHubrelease/tagunchanged.

## Next console test

Install064,pressXonce,trydemoagain.CheckVMstartup,progresspastpriorstall,actual
worldappearance.Thencheckinteraction/save/reloadaspossible;noautomaticpass.
Ifappstops/crashes,reopenwithoutX,retrievecurrentreportsbeforeanyrestart.
Shellnetworkcanfail;SafariAXfreshindices/Optionclickdownloadsworkatknownexternal
runtimeIP.NoIP/filterbakedinapps.Strictdownloadmtime/basenames/runidentity.
Rawlogslocalonly;publishhashes/interpretation.NoJartransform/replacementclasses.
384maystillbeinsufficientorunreservable;followactuallogs,notblindheapchanges.
Interpreterworldgenerationcanremainveryslow;JITisfutureseparateruntimevalidation.

## Storage/source/publication

Privatefailed037–061archiveplusJSONremain;packagetestsverifywithoutfullrestore.
Disk~27GiBfree;avoidneedlessduplicatepackages/relinkextractions.PreserveSDK/JDK/
nativeobjects,frozenpasses,logs,serverfallbacks,062accepted,063accepted.
Consumerchangescommit/pushmainandverify.Runtimeunchanged1e9fb4f,image6382528;
onlyruntimechangesusesync_github.py.NoStore/catalog/newreleaseauthorizedhere.
If064fails,preserveexactZIP/symbols/source/status/evidencebeforechanged065.
EveryfuturebinaryreleasehasmatchingOpenALsources/relink/shim/unitsandcomplete
JAR+assetprovisioning/checks/notices;neverusehistoric026kitforcurrentbinary.

## Current checked package

PPSA99874client01.000.064;runtime dist/PPSA99874.zip andconsumer
dist/client-startup/PPSA99874.zip matchSHA256
87b09e6d64b86f2f0741b12405abf10e165256e2551b34d19fe2ac8ffac3f4c9.
Symbols build/client-startup-probe/bootstrap-01.000.064-symbols.elf.
See docs/validation/client064-build-2026-10-26.json for source hashes/checks.
Targetnativecompile/link/SELFpassed;hoststartup/heapmodelpassed.
002convenienceZIPrestored;062/063acceptedchecksumsverified bypackagecheck.
Console064pending;do notclaimworldsuccessor384reservationuntilactualconsole.
