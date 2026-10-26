> Continuation:060crashed;15paired native scopes then unmatched alcGetIntegerv16. Host reproduces optional HRTF discovery abort with missingcwd;061repairs lookup error handling and captures query arguments. PS5cause/resolution unproven. See [060evidence](validation/client060-startup-failure-2026-10-26.json) and [061repair](client-startup-061.md).

# Current ProsperoCraft handoff — client060

Continue existing files/history. Read runtime+consumerAGENTS.md. No subagents or
server2Hrun. User clarified full goal:polished playable Minecraft Java client on
nativeJava25PS5,with controls/rendering/audio/worldplay/save-reload/stability.
Menu is intermediate,not end goal or full-release acceptance. ConsumerAGENTS.md
andREADME record it. Read [complete054handoff](handoff-prosperocraft-client054.md)
for prior fixes/source ownership/preservation/retrieval/full release gates;
[059handoff](handoff-prosperocraft-client059.md) for combined class logging.
This continuation supersedes current-version/pending059.

## Current package and completed checks

PPSA99874,client01.000.060. Full local package:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/dist/PPSA99874.zip`;
matching consumer `dist/client-startup/PPSA99874.zip`.
SHA256 `899252e805cff1031446cdcceaf6e44c331545601599d7e5b4e04c737502873c`.
Symbols `build/client-startup-probe/bootstrap-01.000.060-symbols.elf`.
Source consumercommit containing [build validation](validation/client060-build-2026-10-26.json);
inspectHEAD/status. Runtime1e9fb4f/image6382528unchanged. Hoststartup/burst/logging,
actual privateOpenALnativeunit/library baselinecompare,ASan/UBSanbounded helper,
targetcompile/link/SELF/fullpackage passed. Original54JARs/5147assets/privatearchive/
header/source/object hashes,unchanged originalarchive,constructor counts and059
preservation verified. Exact002convenienceZIP restored. Build logs client060-host.log,
client060-openal-boundary-host.log,client060-package.log,client060-package-check.log
underbuild/.060PS5nativeobservations/crash resolution/fullclient pending.
Storageabout5GiBfree afterbuild;avoid unnecessary duplicates and preserve failed/raw/
frozen/needed native relink inputs. Do not delete evidence assuming it is public.

## Latest059evidence

User explicitly confirms059crashed before reopening. No different screen/error/
timing supplied. Run client-01.000.059-1793003380-157747534. Safari refreshed at
192.168.111.72:8765;option-click saved12reports,noX/restart. Raw complete files:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/logs/client059-result-20261026/`.
[Hashed interpretation](validation/client059-startup-failure-2026-10-26.json).
Class/GCrotation works:active3817673bytes/rotated4194424. Earliest retained97501ms
JVMuptime,index7962;earlier boot/class/GC records rotated out.18retainedGCstarts/
18ends are partial coverage only. Last sequence verifies OpenAlUtil and ALCcached
classes;lastrecord ALC$ICDStatic$WriteOnce initialization-start164040ms. INFOclass
logging has no generic successful-init completion message;not a hung-class proof.
NativeOpenALNoOutputdevice created,no context completion. Lastburst sample sound
lookup/reload;not atomic with class/native records. No fatal/abort/drivererror/
JavaOOMcaptured. Last sample/class not exact crash instruction/time. Cause unknown.

Read-only original ALC.getICD/ICDStatic.WriteOnce/ALC10.alcGetError->JNIinvokePI shows
cached/router capability lookup. No null/bad pointer or native/class defect proved.
026loopback acceptance differs from original game initialization order. Do not infer
memory exhaustion;keep prior RSS/policy/initialmetadata-null retry caveats. JVMuptime/
observer clocks differ. Saved RUNnot liveness. Menu/fullgame not validated.

##060native diagnostic and next action

Read [060scope](client-startup-060.md). No supported new crash fix. Private pinned
OpenALalc.cpp copy observes5APIbodies:getError,getString,getIntegerv,createContext,
makeContextCurrent. Same APIs/returns/error handling,128scopes/256records perprocess,
saturatingatomic,unique IDs/API/handle,errno preserved,write/flush existingstderr.
Scope-exit can mean exception-unwind before outercatch,not success/APIreturn proof.
Noextra thread/recovery/gamehooks;stdio IOmay allocate/lock/perturb timings/fail.

Builder verifies sourcepin/clean cache,uses actual Ninjacompile flags and original
quote-includes,privatearchive memberalc.cpp.o replacement,existing provider and
constructor renames. Original source/archive retained/hashchecked.058privategetenv
trace applies atop result;only startup variant. Header/unit/archive/object audit.
Host actual private native unit/library results match original device/error/name/
version/context/current/close;all5pairs. ActualheaderASan/UBSan4threads/cap/unwind/
errno checks passed. PS5native behavior still pending. No original54JARs/5147asset,
runtimeimage/SDK,heap/GC/processor/executor/graphics/backendpolicy changes. Prior
WSIowner/stderr/faultrecorder/FILEfix/burst/class+GC/OpenALtrace retained.

Install060,pressX once,note screen/time/error. Afterfailure,reopenwithoutX and
retrieve matching12reports. Inspect native-stderr boundary pairs+OpenAL lifecycle,
activeANDrotated combinedGC/classlogs,exceptionsMAINTRANSITIONs,VM/resources/
build/session/startup/abort/fatal. Check budget consumption and correlation;missing
pairalone not a fatalinstruction. Repair supported concrete defects;otherwise
unknown cause and smallest targetedmissingboundary. Work continues pastmenu through
full playable quality/consoleacceptance. SafarifreshAX/optionclick fallbackworks;
newestcomplete fileidentity/run,never stale names. No rawlogs inGit. Externaltarget
addresses at runtime,inboundapps nopresetIP/filter.

Exact059ZIP SHA25653ce7cc8ff6c83ebec57044951bc44707cbce1322c6188d5e3585745c4857c09,
symbols/status/sourcec18b6e406d23eae9cc0760ccf1d201b550c0d9f3/build+console record
retained ignored dist/failures/Client_Original_Startup-01.000.059. Preserve060before
changed061. All previousfailed/frozen packages retained. Restore002convenienceZIP
afterpackaging. Runtime1e9fb4f/image6382528unchanged. Consumercommit/push here;
runtimechanges via root sync_github.py. Verify pushes.

##Release gates remain

No menu/gameplay/newmilestone/client release/Store download. SharedPPSA99874client
replaces server;retain Fabric/Paper108fullrelease/fallbacks and qualified lifecycle/
deferred2Hlimits. Before eventual release read complete054handoff:acceptedbytes/
accurate scope/human evidence;publicapp-only excludes54officialJARs/5147assets/
personal/game data;complete legitimate pinnedJARANDasset provisioning/reconstruction/
corruption checks;exact OpenALcorrespondingsource/relink/notices/nativeELFmatch
INCLUDING060privatealcunit/header/compilerinputs and058envshim if retained,notold
026/036kit;all dependency notices;version/tag/layout/icon/SELF/upload/downloadSHA
verification;existing reservation under currentcatalogrules/checks. PR737merged,
no duplicate title/PR/full-localZIPupload. Finishwith verifiedGitHubstatus,current
package/version/checksum and exact consolechecks pending.
