# ProsperoCraft client062 — explicit OpenAL application data directory

Goal remains full polished playable Minecraft Java on nativeJava25PS5:controls,
rendering,audio,worldplay/save-reload/stability. Menu intermediate.

User confirms061crashed,reopened. Run
`client-01.000.061-1793006813-300348241`;
[report hashes/interpretation](validation/client061-startup-failure-2026-10-26.json).
Raw12reports runtime logs/client061-result-20261026;Safari retrieval,noX/restart.
NativeIDs1..15paired;ID16alcGetIntegerv param0x1994,size1/outputpointer confirms
ALC_NUM_HRTF_SPECIFIERS_SOFT. Devicecreated,then App-localcurrent_pathbegin,no result/
warning/scopeexit/contextentry. Last recordnot exactfailinginstruction/time. No
captured fatal/abort/JavaOOM/drivererror. Class/burst/native recordsnot atomic;
JVMuptime/observer clocksdiffer. Earlyclass/GCdata rotatedout,retainedcounts partial.

061host-reproduced filesystem_error escape repair remains valid,but targetstops
before current_path(error_code) returns. Actual rootmechanism is unproven.
ReadonlySDKroutine has AVX,rawpathconf syscall191 andgetcwdimport;none establishes
ISA/syscall/import failure without targetcontext. NoSDK/ISA/limit change.

## Supported app-local configuration

JavaStartup already creates /download0/mc-client and uses it as gameDir/user.dir.
OpenAL's default app-local HRTFsearch still attempted ambientnativecwd,which is
unreliable in this sandboxed integration.062supplies supportedALSOFT_LOCAL_PATH
through the existing startup-private getenvbinding. If real process setting is
nonempty,return it unchanged;missing/empty fallsback to /download0/mc-client.
Global environment is not mutated. LOGLEVEL3override stays;otherlookups forwarded.
No change to backend/device selection,SDK,gameclasses,graphics or memory policy.

Upstream explicit-localpath branch avoids current_path and still runs real .mhr
file discovery. Configured/global/default HRTFpaths remain. No forcedemptylist,
fakecount or audiobackenddisable. ExactSDKfailure mechanism remains unproven;
this nativeconfiguration aligns applicationdata with existing gameworkdirectory.

Privatehelpers.cpp adds fixed checkpoints around explicit-path selection,path
normalization,existence and directoryiteration. Iteration-scope completion may follow
caught errors;not proof allfiles loaded. Existing TRACE/errors and native128scope/
256record metadata/burst/class+GC records stay. NativeTRACEIO can perturb timing;
upstream traces are separate from the bounded scopebudget. Dataabsence/errors are
not automatically a crashcause or successfulinitialization.

Host actual originalANDprivate OpenAL with currentdirectory removed and explicit
validlocalpath returns HRTFcount1/error0. Private traces prove explicitbranch used,
no current_pathbegin,and realfilesystem stages. Filenamefixture only,no HRTFdecode/
mixing acceptance. Existing missing-cwd hostabort control and061errorcode repair,
normalAPIbaseline comparisons and helperASan/UBSan remain. Shimtests verify explicit
path honored,missing/emptyfallback,otherlookup forwarding/globalenvironmentunchanged,
and consistency with targetJavaworkdir. No hosttest is a PS5pass.

Only startupprivate envshim and helpers.cpp tracepoints change. ActualNinjaflags/
quoteincludes/privatealc+helpers archive substitutions,originalsource/archive hashes,
header/source/object audits remain. Targetpackagechecks verify fallback/override
metadata,original54JARs/5147assets/runtime/native/SELF,preserved061. OriginalgameJARs
are intact,no hooks/transforms. Frozen/failed snapshots and allprior fixes retained.

Exact061ZIP SHA256d1a338b5e7c3d542bf5d4be974e3780c8ea3260ccd812939ea290dd755629429,
symbols/status/sourcec43e0ec9edde15a4b880c1558f03ca6da108bb76/build+console record
retained ignored dist/failures/Client_Original_Startup-01.000.061. Futureaccepted
source/relink materials must include exact062shim/privatehelpers+alc/header/compiler
inputs,notold026/036kits. No currentclientrelease/Storedownload.

Install062,pressX once,notefinalscreen/time/error. ReopenwithoutX afterfailure;
retrieve matching12reports. Inspect explicitpathselection/normalization/existence/
iteration stages,HRTFqueryscopeexit/context progress,combinedGC/class bothfiles,
burst/VM/resources/startup/build/session/abort/fatal. Identify actual next failing
boundary,repair supported defects. Fullplayability/audio/input/performance/save-
reload/stability still need consolevalidation. Server2H remains deferred;complete
accepted-byte/provisioning/license/relink/catalog gates from054handoff stillapply.

Host/native/configuration/target/full-package checks passed. [Buildvalidation](validation/client062-build-2026-10-26.json). Full local ZIP SHA256 `26f31cc26bc960d3c7e35205c0280e8b83bc6e475a17b8383c778583cf952b88`.062PS5pending.
