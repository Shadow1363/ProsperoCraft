> Continuation:061crashed;query0x1994confirmed,current_pathbegin/noresult.062uses explicit app-local game directory to avoid ambientlookup and logs laterfilesystem stages. Hostexceptionrepair remains valid,PS5mechanism unproven. See [061evidence](validation/client061-startup-failure-2026-10-26.json) and [062configuration](client-startup-062.md).

# ProsperoCraft client061 — optional data discovery error handling

Product goal remains a polished full Minecraft Java client on nativeJava25PS5:
controls/rendering/audio/worldplay/save-reload/stability. Menu is intermediate.

User reports060crashed,reopened. Run
`client-01.000.060-1793005053-213311378`;
[report hashes/interpretation](validation/client060-startup-failure-2026-10-26.json).
Raw12reports runtime logs/client060-result-20261026;Safari retrieval,noX/restart.
Nativebodybudget only16of128used. IDs1..15have paired enter/scopeexit;device-created,
error/string/version/capability queries progress;ID16alcGetIntegerv enters with the
created handle,no scopeexit. No context entry. Scopeexit not success/returnproof.
No queryparam/size/output was recorded in060;absence of exit not exact crashsite.
Last classrecordWriteOnce alone is not a cached-class defect,as later ALCcalls ran.
No captured fatal signal/abort/JavaOOM/driver error. PS5termination cause unproven.

## Concrete host-reproduced native defect

Original Library.createAttributes firstqueries6548/0x1994
(ALC_NUM_HRTF_SPECIFIERS_SOFT). Native HRTFcount enumerates optional files via
SearchDataFiles. Its app-local search calls throwing fs.current_path outside the
DirectorySearch exception handler. Exported alcGetIntegerv is noexcept and catches
al::base_exception,not std::filesystem::filesystem_error. Thus a failed current-
directory lookup can escape and terminate the process.060sequence is consistent
with this path,but exact query and target cwd failure were not captured.

Regression uses actual pinned unmodified OpenAL1.25.2:open null device,remove its
current directory,query HRTFcount. Original abortsSIGABRT/-6 with filesystem_error,
current_path/getcwdENOENT. Core dumps disabled in fixture. No game or OSstub.

061private POSIXhelpers.cpp uses fs.current_path(error_code). Lookupfailure logs a
warning and skips only unavailable app-local search. ExplicitALSOFT_LOCAL_PATH,
valid cwd/configured/global/default HRTFpaths and normal directory enumeration stay.
No forced empty HRTFlist,backend/audio disable,gameclass change or fake API success.
Trace markers before/after directory lookup plus existing native/class logs remain.
Other errors such as allocation failures are not claimed fixed.

Actual repaired library returns count0/error0 and creates context in missing-cwd
case. Valid local .mhr filename enumeration is1on both original/repaired libraries;
fixture does not decode/mix HRTFdata. Ordinary device/error/name/version/context/
current/close results still match. These hostresults establish the native defect
and repair behavior,not that it caused or resolves PS5termination.

## Capture and private build

Existing scope records now add param(hex),size,output pointer for alcGetIntegerv,
without dereferencing output or querying/consuming error state. Other API records
use0/null metadata. Same128scope/256record cap,errno preservation,exception-unwind
semantics. This will identify the actual next scalarquery if records reach it.

Private pinned alc.cpp retains5APIbodyScopes;private core/helpers.cpp has the POSIX
lookup repair. Compile actual Ninja flags/original quote-includes;replace exactly
alc.cpp.o and helpers.cpp.o in private archive,existing provider/constructor renames.
Original cache/source/archive untouched/hashchecked.058private traceenv binding
retained. Audit pins both source/unit hashes,header and archive/final object hashes.
Only startup uses variant. Future accepted source/relink kit must include both
private units/header/compilerinputs and traceenvshim,not old026/036kit.

Host checks actual original/repaired missing-cwd HRTFquery,valid-file enumeration,
normal APIresults and metadata formatting,bounded4thread helper/errno/unwinding
underASan/UBSan. Target/package checks verify both members/source/object hashes,
originalarchive unchanged,constructorcounts,all54JARs/5147assets,runtime/native/
SELFaudits and preserved060. No hosttest establishes PS5API/cwd/crash/playability.

Exact060ZIP SHA256899252e805cff1031446cdcceaf6e44c331545601599d7e5b4e04c737502873c,
symbols/status/sourcef2b414ebac16d7398c7d54dadbf98f3d7f7ffa3b/build+console record
retained ignored dist/failures/Client_Original_Startup-01.000.060. OriginalgameJARs/
assets/runtimeimage/SDK,heap/GC/processor/executor/backend/graphics,priorfrozenpasses/
WSIowner/stderr/faultrecorder/FILE/burst/class/OpenALtrace retained.

Read-only060SDKfilesystem.current_path disassembly also contains AVXinstructions;
no targetOSfeature/fault evidence establishes an ISA cause. No SDK/AVX-policy change.
If lookup-begin lacks a result after061,inspect exact recorded operation rather than
assume either filesystemexception or ISA fault. Raw RSSunits/totalmemory adequacy
remain unverified;no heap increase.

Install061,pressX once,note screen/time/error. After failure,reopen withoutX,retrieve
matching12reports. Inspect native-stderr queryparam/size/output,lookupbegin/result/
warning,scopepair/nativecontext progress,combinedGC/class activeANDrotated,burst/
VM/resources/startup/abort/fatal. Repair only supported causes. Fullclient console
playability/audio/input/performance/save/reload/stability acceptance remains pending;
no newmilestone/clientrelease/Storedownload. Server2H remains deferred. Fullaccepted-
byte/provisioning/license/relink/catalog gates from054handoff still apply.

Host/native/target/full-package checks passed. [Build validation](validation/client061-build-2026-10-26.json). Full local ZIP SHA256 `d1a338b5e7c3d542bf5d4be974e3780c8ea3260ccd812939ea290dd755629429`.061PS5pending.
