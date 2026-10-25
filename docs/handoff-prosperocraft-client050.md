# Handoff — ProsperoCraft client050, retrieve logs, fix original client, prepare eventual full release

Continue the existing project from its actual files/history;do not recreate/reset.
Read the runtime workspace AGENTS.md and consumer AGENTS.md before editing.
The user wants the actual original Minecraft Java client to reach a working menu
on PS5 and ultimately a full ProsperoCraft release/Prospero Store download.
**First retrieve the latest console reports,verify build/run,and follow through
with concrete repairs,build/check/publication. Do not stop after collecting logs
or wait for a separate repair request.** Unknown crash causes must remain unknown
until supported by evidence. Do not manufacture a menu/pass/crash diagnosis.

## Paths, repositories, authority

Runtime workspace:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew`

Consumer repo (work here for Minecraft/native dependency integration):
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/.tools/github-publish/ps5-minecraft-java`

Public repos:
- https://github.com/mateo-cogeanu/ps5-minecraft-java
- https://github.com/mateo-cogeanu/ps5-java25-homebrew

Implementation baseline before this documentation-only handoff:
consumer `429c6550e690697f98990903b5b527df590a97b3`;
runtime `6382528c7aee066002d1c2c6a7b5c7116987ae8c`.
This handoff is committed afterward;read current HEAD/status before work.

Human already authorized public source publication after every completed change.
Consumer:relevant checks,commit,push main,verify remote HEAD. Runtime fixes:
`python3 tools/sync_github.py --message "Describe completed changes"` from runtime
root,verify success/push. Runtime tooling changes are published in Development.
No upload-permission question is needed for this authorized development scope.
Keep source ownership separate;no force push/reset/overwrite of remote changes.
No subagents unless explicitly requested or required by applicable rules.
No background watcher/automation is implied. Publish development before console
success,with pending validation truthful. Keep raw logs/caches/credentials/build
outputs/downloaded game material out of Git. Public binaries belong in releases.

Preserve all frozen passing milestones and exact failed candidates. Only human
ALL PASS on that exact console build can establish a new passing milestone.
Original Mojang loading screen is meaningful progress,not menu/gameplay ALL PASS.
Latest frozen passing client is Client_SPIRV_Cross036. Runtime JVM_Startup
01.000.023 is frozen too. Preserve existing server full release and its links;
two-hour server endurance is explicitly deferred:do not start it.

Keep official Minecraft JARs intact. Client executes all54 original pinned JARs
and5147 original asset objects. Put compatibility in the Java runtime or consumer
native dependencies/harness/configuration,not game replacements/bytecode hooks.
Existing server derivative transforms are migration debt;remove only with working
validated replacements and never claim unmodified server while a derivative runs.

## Current candidate and first action

App name:ProsperoCraft. Shared title ID:PPSA99874;retain content ID/identity.
Client versions advance independently of server versions. Installing client
replaces the server app;no side-by-side claim. Current client **01.000.050**.
Do not reuse050 for a changed binary;next candidate normally051.

Installable full local package:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/dist/PPSA99874.zip`

Matching consumer package:`dist/client-startup/PPSA99874.zip`.
Full ZIP SHA-256:
`ffc3b7d47132e7c426b42e1215033fd6649ca36f4a9c5c589bf44e59d935062f`.
Symbols:`build/client-startup-probe/bootstrap-01.000.050-symbols.elf`.
Details:`client/startup/status.json`, `docs/client-startup-050.md`.

050has host exact-worker/retry/helper/owner/resource/recorder/launch/allocation
checks,target compilation and full-package verification. **No050console report
has been retrieved and no human050outcome was supplied before this handoff.**
The latest retrieved reports are049. The previous assistant told the user to
install050,launch and press X once,then reopen without X after failure.
First inspect current build/session. If saved reports are049 or048,do not call
them050. If050has not run,tell the user to install/press X once when ready.
Do not start another run yourself before saving the old reports.

## Retrieve PS5 logs — Safari works when shell networking does not

Current known PS5 address:192.168.111.72.
Read-only report index:`http://192.168.111.72:8765/`.
Never bake this address/client-IP filters into new apps;external helpers take
addresses at runtime. Shell curl often fails while Safari works. Do not repeatedly
ask whether the IP changed or ask for manual downloads when Safari automation works.

Working native CUA workflow:
1. First bind `let safari=await cua.getApp('Safari')` and read its documentation/
   AX state. After context compaction,reload documentation using the available
   documented CUA mechanism before continuing. Do not assume a previous JS binding
   exists in a fresh chat. Native UI actions must use CUA,not AppleScript/etc.
2. Existing Safari tab is normally the PS5 probe logs index. Refresh the page to
   discover new routes. Re-read AX state and locate current link indices.
3. Download each link with `await safari.click(index,{key:'alt'})`,then
   `await safari.getAXState()`. Option-click downloads directly without rendering
   huge logs. Re-derive indices from fresh state;never guess/reuse stale ones.
4. Files appear in `/Users/mateocogeanu/Downloads` with suffixes;find newest
   matching build*.txt/session*.txt/vm-trace*.log etc by mtime. The unsuffixed
   file is often old. Check completed file/size if a download is still in progress.
5. Copy the exact current files into a new runtime `logs/client050-result-DATE`
   folder (unique suffix if needed;do not overwrite earlier evidence). Verify
   session Build/Run;native-stderr has its own identity. VM trace can be stale
   when initialization fails before it is reset;do not infer identity from filename.
6. Collect **build.txt,session.txt,native-stderr.log,vm-trace.log,exceptions.log,
   startup-tail.log,abort.txt,hs-error.log**. Full startup.log if needed;class-load,
   process-usage or previous reports only if relevant. Keep raw reports local;
   source-control only hashes/byte counts/interpretation with evidence limits.

The app restarts report sharing when reopened without X and preserves the failed
run's files. Saved RUN does not prove the process is still progressing. If checking
a live black screen,read reports before asking for restart.048was an explicit
setup FAIL,not a hung game. Context-menu Download Linked File is fallback;Save
Page was unreliable. Do not use voice-only capture_screen_context in text chat.

New current native route:`/native-stderr.log` -> `/download0/probe-native-stderr.log`;
previous:`/previous-native-stderr.log`. Runtime `tools/fetch_probe_logs.py` includes
both,for environments where terminal HTTP works. Native FILE capture is confirmed
on049;raw descriptor2 writes are intentionally not captured.

## Evidence chronology — keep the successful changes

- 039fixed SDL/LWJGL function-pointer identity.040truthful zero-layer discovery
  allowed real instance/device/window initialization.041scoped LWJGL system
  allocators to the paired graphics heap;actual PS5 preflight3x4MiB/grow8MiB/
  calloc/aligned allocation and cleanup passed. Keep these fixes.
- 042matched actual enumerated1080p59.94 SDL/Vulkan mode but swapchain still failed.
  Driver enumerates1080p/1440p/4K,not720p. Do not invent720p scanout or re-blame
  image extent/alignment without evidence.
- 043diagnostics showed VideoOut open refusal before buffer registration/image
  allocation.044fixed permanently cached negative open and added one delayed retry
  (>=2s,max2OS opens,before buffers/current swapchain). Both opens still returned
  **0x80020023**,kernel EAGAIN/resource unavailable. Cause not proven transient.
- 045recorded successful kernel resource queries at both refusals:448MiB flexible
  configured/324MiB available,largest direct ranges12622757888 and12373196800 bytes.
  This does not support general pool depletion. Ordinary Java pthread creation
  also fails EAGAIN/errnoENOMEM earlier and succeeds with direct-stack fallback;
  libc/service pressure is a hypothesis,not confirmed VideoOut internals.
- **046works around the late-open refusal by initializing the actual WSI output
  after GPU provider constructors/before original Main.** It uses the SAME output,
  lock/once/static state;successful handle retained for later swapchain. No second
  output/preflight owner/handoff. Negative result remains JNI_OnLoad failure.
  Console early open returns positive0x4e100100,prepare0;3swapchain imports succeed.
  **Human exclaimed original MOJANG LOADING SCREEN,then crash/reopened.** Keep this
  actual visible progress;no menu/gameplay/new passing milestone was established.
- 047holds an outer existing fault-recorder reference around ClientStartup25 JNI
  invocation,so compiler end cannot remove it between compiles.4handlers installed
  on PS5;still no recorded signal/VM abort. It records bounded raw context then
  delegates to prior JVM handlers,never recovers/rewrites context. Historical
  `SHADERC FAULT` prefix now does NOT establish compiler origin. JVM-handled signals
  can be normal;raw96context words have no assumed register layout.
- **048was a diagnostic regression.** Native-stderr dup2 returnedEPERM1 and harness
  stopped check1 before constructors/JVM. Live black-screen session identified this;
  native file contained only build/run header. Old VM trace was not048 evidence.
- **049repairs048.** Runtime helper open/fdopen/configures an unbuffered FILE then
  assigns stderr,never dup2. Setup errors notify/log and startup continues. Previous
  stream/descriptor2 remain owned;no pipe/thread/closing old stream. Native stderr
  report confirms actual output and1080p set0/buffers0-4 registration. Raw write(2)
  and cached old FILE users are outside capture. No GPU refusal/timeout message was
  captured. No fatal signal/VM abort;hs-error unavailable.

Latest retrieved049run:`client-01.000.049-1792947461-290571136`.
Runtime raw evidence:`logs/client049-result-20261025/`.
Public:`docs/validation/client049-startup-failure-2026-10-25.json`.
Earlier046/047/048records are under docs/validation and corresponding local logs.
**046,047,049each show390shader compile entries and390returns. Last shader return
is NOT a confirmed failure location.** Java reports end in resource reload/font
loading. Offline Realms/auth and unsupported narrator errors do not by themselves
identify the crash. No captured crash instruction/stack is known.

## What050adds and how to interpret its reports

Consumer `client/ports/mesa/0005-videoout-present-progress.patch` adds bounded
observations in the existing WSI output:
- Raw flip-thread C11 creation status.
- First8present enqueues:buffer/inFlight.
- First8flip-worker fence begin and actual VkResult after WaitForFences.
- First8native SubmitFlip results:raw code/buffer/argument.
- Later non-success fence/flip results,subject to the shared64-event/384-byte
  logger cap. Initialization events use the same cap;inspect full VM trace.

Search current trace/native stderr for `WSI present`, `WSI flip`, `WSI failure`,
`SHADERC FAULT`, `SIGNAL`, `NATIVE TERMINATION`, `radv/ps5`,GPU timeout/submit errors.
Enqueue proves WSI entry;fence begin without return narrows a wait;fence result
and submit result narrow the next stage. Submit accepted is not proof frame shown.
No markers could mean failure earlier,not proof of a queue-thread crash. First8
bounds cannot locate every later failure. Avoid guessing more heap/resolution/
delay changes from missing evidence.

050is observational:all calls/queue/buffer/argument handling remain unchanged.
**Existing pinned flip worker ignores a failed WaitForFences result and continues
to SubmitFlip.050logs that actual result but does not claim to fix the behavior.**
If console evidence exposes a concrete failure,repair truthfully with host/target
regression and another version;never rewrite failure into success/fake handles.

Private driver build:`tools/build_wsi_diagnostics.py` verifies pinned Mesa Git
object,exports it to ignored build/wsi-diagnostics,applies patches0001-0005 and
replaces only wsi_common_videoout.c.o in a PRIVATE RADV archive. Original source
caches/original build/graphics-radv/src/amd/vulkan/libvulkan_radeon.a stay intact.
Startup selects private archive via build_client_gpu.py/package_client_vulkan.py.
Mesa pin:`1ba9874f478657ccf6da72ce55f0260164cc0bd0`.
Audit pins all patches/source/object/archives.050patch SHA is in status/audit.
No game JAR changes. Tests use controlled OS/kernel responses,not PS5 emulation.

Reusable runtime helper:`java25/probe/native_stderr.hpp`;
routes/archive:`java25/probe/log_share.hpp`;collector:`tools/fetch_probe_logs.py`.
Runtime helper repair commit6382528. SDK reference documenting dup2EPERM/stream
replacement is7a82030dcff6457936d75be97f52aa509b770e1f in mihawk-99/PS5_PayloadSDK,
platform/src/klog.c. Reference only,no dependency upgrade.049confirms FILE capture.

## Build,checks and exact candidate preservation

JDK25:`/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home`.
LLVM:`/opt/homebrew/opt/llvm/bin`;LLD:`/opt/homebrew/opt/lld/bin/ld.lld`.
From consumer root:

```sh
python3 tools/build_wsi_diagnostics.py
python3 tools/test_videoout_present_host.py
python3 tools/test_videoout_retry_host.py
python3 tools/test_videoout_resources_host.py
python3 tools/test_wsi_diagnostics_host.py
python3 tools/test_videoout_early_owner_host.py
python3 tools/test_shaderc_fault.py
python3 tools/test_client_startup_host.py --java-home /Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home
python3 tools/package_client_vulkan.py --runtime-workspace /Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew --java-home /Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew
```

Run checks relevant to actual changes;no needless repeated broad builds. Runtime
capture changes:tools/test_native_stderr.py,test_probe_log_share.py,
test_probe_report_writer.py. Host Main exit253 at absent host-native bootstrap is
expected,not a menu pass. Package checks cover54JAR/5147asset hashes,exact runtime,
13resident groups/constructors/paired allocators/native audits/icon/SELF integrity.

Before changing/rebuilding050,retain exact full ZIP under ignored
`dist/failures/Client_Original_Startup-01.000.050/`,plus matching symbols,status,
source commit and failure evidence/report hashes. Do not call it passed/freeze a
passing milestone without human acceptance. Replace full version/label tokens,
NEVER all bare digits (historical SHA strings must remain exact).

Packager regenerates baseline002convenience ZIP. After building,restore exact
`dist/milestones/Client_LWJGL_Core-01.000.002/PPSA99874-full-local.zip`
to `dist/client/PPSA99874.zip` and SHA256SUMS. Its SHA:
`d0b9f815ff68c5ad821b2166509879c623c813019d2f70bbacf53769f35e3971`.
Active startup goes to runtime dist/PPSA99874.zip as above.

Storage is limited (~17GiB available at last check). Avoid needless duplicate
600MBfull packages. See docs/local-storage.md. Older failed packages are losslessly
compacted in ignored dist/archives with manifests/restore tools;newer retained
directly. Do not expand multi-GBarchives merely to inspect hashes. Current package
test verifies archived failures without restoring them. Never delete frozen passes.

Heap remains256MiB,compressed class space64MiB,SerialGC,-Xint. Prior512MiB reserve
failed;do not blindly raise memory. Original supported offline demo args use
1280x720 logical size but enumerated1080p59.94 scanout. No credentials,multiplayer/
chat disabled;workdir /download0/mc-client. Audio options muted only on new config;
existing options preserved. Main return is deliberately failure,never automaticPASS.

## Branding and Prospero Store “Coming soon” — verified during this handoff

Approved app name/icon are settled;no redesign needed:
`assets/branding/icon0.png` (512RGBA),master
`assets/branding/ProsperoCraft-icon-v3-source.png` (1254square),branding.json hashes.
Generated crafting-table PC icon has complete dark-green outlines. apply_branding.py
applies it to future client/server packaging. Preserve earlier art/frozen assets.

Catalog:https://github.com/darkxex/ps5-homebrew-catalog
Record:`apps/PPSA99874.json`.
Local checkout:`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/.tools/prospero-catalog`.
Original reservation PR353merged2026-10-17. Rename/description PR737:
https://github.com/darkxex/ps5-homebrew-catalog/pull/737
**MERGED2026-10-25T12:49:50Z**,reverified via gh during this handoff. Upstream record
says ProsperoCraft;do not duplicate the rename PR or call it pending. Website/store
propagation has not been independently checked.

Exact current description (161characters):
“Minecraft Java Edition client and server on PS5, powered by native OpenJDK 25;
vanilla, Fabric and Paper server playtests, with client startup under development.”
Author mateo-cogeanu,kind game,category pc-ports,titleidPPSA99874.
**license,version,source_repo,artifact_url,sha256,icon_url are all null.** This is
still a reservation,with shared Coming soon artwork and no download. The approved
local icon must not be forced into an invalid reservation. Do not link the full
local600MBgame-containing development ZIP as a public catalog download.

When the client actually works and the exact build is accepted,the user wants a
full release and conversion of this existing reservation to a real downloadable
listing. Read current upstream docs/submitting.md,docs/artifact-formats.md,
docs/versioning.md and schema/checker before doing that;rules can change.
Current local docs require one app JSON per PR,submitted from source owner account,
release tag/version agreement,GitHub-release app-folder ZIP,pinned SHA256/icon.
Use python3 -m catalog check,python3 -m catalog verify PPSA99874 and relevant tests;
verify release asset digest,not an invented checksum. Preserve PPSA99874 identity.
Update the existing reservation,not another title ID/new app. Historical catalog
fork branch:codex/prosperocraft-branding;inspect current branch/remotes before edits.
See docs/prospero-store-submission.md for context. Keep eventual description truthful
about what client/server functionality is tested and about deferred endurance.

## Full release readiness — do after actual success,not from host checks

1. Obtain actual human acceptance for that exact version and intended scope.
   Working menu is the current goal;do not silently label gameplay/save/rejoin/
   stability passed without testing. Record limitations and any remaining original
   startup crash. Preserve original exact package/symbols/tested source commit.
2. Freeze the accepted snapshot only under the existing ALL PASS rules;publish
   validation with title/version/run/human results and matching local ZIP SHA.
   Keep earlier passes intact. Update consumer README/banner/release links.
3. Prepare public app-only artifact from the accepted bytes without rebuilding
   accepted binaries. **Do not redistribute downloaded official Minecraft JARs
   or asset objects/game data.** Full startup currently has54JARs and5147assets;
   existing older milestone release helpers are not a complete startup release.
   Extend/validate legitimate hash-pinned provisioning for excluded original JARs
   AND assets as needed,so users can actually reconstruct a runnable install.
   No credentials/personal files/raw logs in release. Clearly describe provisioning
   and ensure catalog download/install expectations are satisfied before listing.
4. Inspect existing Client_SPIRV_Cross/earlier release validation and provisioning
   patterns. tools/provision_client_release.py currently allows only older named
   milestones and restores JARs,NOT full startup assets. Do not claim it already
   handles a future client-startup release. tools/provision_release.py is server
   flavor provisioning,not a client substitute.
5. This app statically links OpenAL Soft. Public release needs exact matching LGPL
   corresponding-source/relink inputs/instructions and notices. Reuse/adapt
   tools/build_client_openal_relink.py with explicit --variant startup,--version
   accepted version,--tested-source exact implementation commit;defaults026are
   historical. Verify unmodified relink with tools/relink_client_openal.py matches
   the accepted native ELF. Include source/relink ZIP and validation/SHA256SUMS.
   Do not attach an old036/026kit to a different binary. Preserve other dependency
   license/source obligations and assets' rights;prepare all needed materials.
6. Verify every public ZIP retained/excluded file and hash;exercise provisioning
   reconstruction/corruption rejection. Validate package layout/icon/SELF,release
   tag/version/notes,asset upload success and downloaded/GitHub-reported hashes.
   Public app-only SHA differs from full local ZIP SHA;record both clearly.
7. Publish a truthful full release only for the accepted scope,then fill valid
   catalog release fields with pinned public artifact/icon/source/license/version
   and SHA. The eventual downloadable catalog update is separate from PR737.
   Keep server Fabric-Paper-v01.000.108 full-release history and fallback packages;
   all share title identity,so document client replaces server installation.

Do not release050or claim readiness just because native setup/host checks pass.
If new app code is needed for provisioning/UI,that changed binary needs its own
version/console validation;do not silently replace an accepted artifact.

## Turn follow-through

Retrieve first,inspect complete current-run reports,fix concrete issues within
scope,build/check,publish sources in the proper repo and verify pushes. If no
cause is established,say so;design the smallest useful diagnostic based on the
missing evidence rather than speculative “fixes.” Keep original game code intact.
Give updates during sustained work. Finish with verified GitHub status,current
package/version/checksum/location and exact console validation still needed.
