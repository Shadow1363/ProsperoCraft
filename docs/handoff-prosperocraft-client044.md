# Handoff prompt — ProsperoCraft client044 / VideoOut / Prospero Store

Continue this existing project. Read the workspace and consumer AGENTS.md before
editing. Work from current files/history;do not recreate or reset the project.
The user wants the actual original Minecraft Java client to reach a working menu
on PS5. Current blocker is native VideoOut opening,not Minecraft authentication.

## Workspace and publication

Runtime workspace:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew`

Minecraft consumer repository:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/.tools/github-publish/ps5-minecraft-java`

Public repos:
- https://github.com/mateo-cogeanu/ps5-minecraft-java
- https://github.com/mateo-cogeanu/ps5-java25-homebrew

Implementation baseline before this documentation-only handoff:
`647a310b16ed723dfb044be94d519c477811c6f7` on consumer main.
Read current HEAD/status because this handoff is committed afterward.

The human already authorized publication after every completed change. Consumer
changes:check,commit,push main,verify remote HEAD. Runtime fixes:run runtime
`python3 tools/sync_github.py --message "Describe completed changes"`,verify push.
Keep ownership separate. Never force-push or overwrite remote changes. Do not
publish credentials,caches,raw reports,downloaded game JARs or build outputs.
No additional permission question is needed for authorized development/fixes.
Do not spawn agents unless explicitly requested or required by applicable rules.

Preserve frozen passing milestones and exact failed packages. Only actual human
ALL PASS for that exact console build permits a new passing milestone. Host
checks/builds are not PS5 passes. Publish source development even before console
success,with accurate pending status. No new passing milestone/release for044.

Keep official game JARs intact. Client currently executes all54 original pinned
JARs and5147 original asset objects. Compatibility belongs in the Java port or
consumer native dependencies/harness/configuration. Do not add game replacements,
bytecode hooks or server-JAR transformations. Existing server derivative patches
are migration debt;remove only with validated replacements. Never falsely claim
an unmodified server if a derivative still executes.

## Current build and what is still unknown

App:ProsperoCraft. Shared title ID:PPSA99874;retain identity/content ID.
Current client:01.000.044. Its independent counter is separate from older server
builds. Do not reuse044 for a changed binary;next candidate normally045.

Installable full local package:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/dist/PPSA99874.zip`

Matching consumer package:
`dist/client-startup/PPSA99874.zip`

Full ZIP SHA-256:
`3a940fa1e3280b8f665f065ce5af50a00b1b9d2884b608a5a123f41666670443`

Symbols:`build/client-startup-probe/bootstrap-01.000.044-symbols.elf`.
Details:`client/startup/status.json`, `docs/client-startup-044.md`.

044has passed host allocation/launch/retry/helper checks,target compilation and
full-package verification. **No human PS5 outcome for044has been received yet.**
The last “relaunched the app” report belonged to043,confirmed by downloaded
session. Do not mistake saved043reports for an044run. First inspect session/build.
Original menu,presentation/gameplay and later crash resolution remain unvalidated.
The two-hour server endurance run is explicitly deferred;do not start it now.

## Latest evidence and actual failure

Private raw reports live in runtime `logs/client043-result-20261025/`:
`session.txt`, `vm-trace.log`, `exceptions.log`.
Public evidence hashes/interpretation:
`docs/validation/client043-startup-failure-2026-10-25.json`.

043run:`client-01.000.043-1792940581-168525309`.
Saved session remains RUN after process exit;RUN is not proof of current progress.
WSI checkpoints show:

```
WSI create requested1920x1080 mode1920x1080 images3 max5 hostImport1 format44 usage0x2 present2
WSI failure initialization-guard-477 result-3
WSI failure register/ownership result-3
```

Guard477maps to `videoout_register_locked` returning failure because
`videoout_open_locked()` was false. It is **before framebuffer registration or
image allocation**. Extent matches;image count is in range;host-import callback
exists. The native `sceVideoOutOpen(0xff,0,0,NULL)` returned negative.043did not
capture its raw OS error because that message only went to native stderr.
Do not continue blaming4K,image alignment or GPU memory without new evidence.

The driver set `out->opened=true` BEFORE attempting the open,and kept that flag
on failure. Every later attempt therefore returned the same cached negative
handle without another OS call.044repairs that permanent-failure state and adds
raw result logging. It does not establish why the first open failed or prove
that the refusal was transient. Full retrieved VM traces have no captured fatal
signal/abort;043ends during shader compilation. The later crash instruction is
still unknown. Do not invent a crash stack or claim this is a confirmed fix.

## What044changes

Consumer native Mesa adapter only:
`client/ports/mesa/0001-videoout-checkpoints.patch` retains043diagnostics.
`client/ports/mesa/0002-videoout-open-retry.patch`:
- Cache opened=true only after a nonnegative real handle.
- Permit one retry at least2seconds after the first refusal.
- At most two OS open attempts per process.
- Retry only before any buffers/current swapchain exist.
- Retain a successful handle,including0;never reopen/close an owned output.
- Report `WSI VideoOut open attempt%u result0x%08x` through the existing logger.
- Permanent refusal remains failure;never rewrite errors into success.

`tools/build_wsi_diagnostics.py` verifies original pinned Mesa source from its
Git object,applies both patches in ignored `build/wsi-diagnostics`,uses the
recorded target compiler command,and replaces ONE member
`wsi_common_videoout.c.o` in a PRIVATE copy of the RADV static archive. Original
source caches and `build/graphics-radv/src/amd/vulkan/libvulkan_radeon.a` stay
unchanged. Startup alone selects the private archive through
`tools/build_client_gpu.py`/`tools/package_client_vulkan.py`.
GPU integration audit pins source,patches,object and both archives.
Diagnostics use384-byte stack formatting and64bounded events. The existing
logger writes startup and VM trace;retrieve full VM trace because verbose shader
checkpoints can push earlier WSI evidence out of the512KiB startup tail.

Pinned Mesa:1ba9874f478657ccf6da72ce55f0260164cc0bd0.
Native driver source belongs in the consumer repo;this is not a game-JAR edit.

## Retrieve PS5 reports reliably

Current fixed PS5 IP:**192.168.111.72**,not the old .217.
Read-only report server:`http://192.168.111.72:8765/`.
Do NOT embed preset IPs/client filters in new apps. Pass addresses at runtime.

Terminal curl frequently cannot connect even while Safari works. Do not keep
asking whether the IP changed or ask the user to manually download files when
native Safari automation works.

Working CUA workflow:
1. Bind Safari with `await cua.getApp('Safari')` and read returned documentation/
   state. After compaction first call `await cua.rewriteDocumentation()`.
2. Navigate to the index using native address-bar controls.
3. Read a fresh AX tree and locate the actual report link indices.
4. **Option-click a report link**:
   `await safari.click(linkIndex,{key:'alt'})`,then getAXState.
   This directly downloads the file to Downloads without rendering/saving a huge
   page. Re-read indices after UI changes;never guess/reuse stale ones.
5. Inspect newest matching Downloads files via filesystem tools. Safari adds
   suffixes such as vm-trace-3.log/session-33.txt;do not assume the unsuffixed file
   is newest. Copy exact files into a new runtime logs/client044-result-DATE folder.
6. Verify session Build/Run and current app build. Collect session.txt,build.txt,
   vm-trace.log,exceptions.log,startup-tail.log;abort.txt/hs-error.log if available.
   Avoid broad scans of unrelated personal files.

Fallback:context-click link,choose Download Linked File,press Return if menu item
only selects. Safari Save Page often has a disabled Save button;direct Option-click
worked reliably and preserved raw bytes. TextEdit was an earlier slow fallback;
prefer direct downloads now. Native computer use must remain through CUA APIs.
Do not use voice-only capture_screen_context in this text chat.

After a crash the user reopens and leaves the app at ready without X. This
preserves reports and restarts sharing. Do not start another run before collecting
old reports. Collect/inspect,then fix concrete findings and build/check/publish
without waiting for another repair request. If044has not actually run,keep its
validation pending and tell the user to install/pressX once when ready.

## Interpret the next logs

First search full current VM trace for:
`WSI VideoOut open attempt`, `WSI failure`, `WSI create`, `FAULT`, fatal signals.

If first open fails but second succeeds,verify registration,image creation,
presentation and actual visible menu;successfully opening VideoOut is only a
component result. If both fail,decode/investigate the actual raw PS5 code using
pinned SDK/driver evidence or authoritative sources;do not guess error names.
Audit native display ownership,SDK/module binding,initialization and resource
pressure according to that code. Do not add another arbitrary resolution/heap
change. No other output should be opened by a preflight before Minecraft unless
an explicit,validated ownership handoff is implemented. Never fake a handle,
swallow errors or fabricate rendered success. Investigate the later crash
separately if the trace still lacks a fatal record.

Earlier progress:039fixed SDL/LWJGL loader address identity;040truthful zero-layer
discovery allowed real Vulkan instance/device/window initialization;041paired
LWJGL system allocators with the scoped graphics title heap and its actual PS5
3x4MiB/grow8MiB/calloc/alignment preflight passed.042matched enumerated1080p59.94
SDL display and Vulkan surface but did NOT resolve swapchain failure. Keep those
working fixes. Runtime heap remains256MiB,compressed class space64MiB,SerialGC,
-Xint;do not blindly raise it (512MiB reservation previously failed).

Original launch uses offline demo,Vulkan,1280x720 args,disabled multiplayer/chat,
no credentials. SDL fullscreen output uses a real enumerated1080p mode because
this driver enumerates1080p/1440p/4K,not720p. Workdir:/download0/mc-client.
New options mute audio;existing options are preserved. Original Main returning
is intentionally failure,never automatic menu PASS.

## Build and validation

Use JDK25:
`/Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home`
LLVM:`/opt/homebrew/opt/llvm/bin`;LLD:`/opt/homebrew/opt/lld/bin/ld.lld`.

From consumer root:

```sh
python3 tools/build_wsi_diagnostics.py
python3 tools/test_videoout_retry_host.py
python3 tools/test_wsi_diagnostics_host.py
python3 tools/test_client_startup_host.py --java-home /Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home
python3 tools/package_client_vulkan.py --runtime-workspace /Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew --java-home /Library/Java/JavaVirtualMachines/openjdk-25.jdk/Contents/Home --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew
```

Run checks appropriate to actual changes. Tests with controlled OS responses are
host state-machine checks,not PS5 OS/GPU success. Host Main exits253 at missing
host-native bootstrap by design;it is not a menu pass. Package checks verify real
JAR/asset pins,runtime image,13resident groups,constructors,paired allocators,
other accepted components,icon and SELF integrity.

When bumping version,replace full version/label tokens,NEVER all bare digits:
this can corrupt historical SHA strings. Preserve all historical checksums.
Before rebuilding,move the exact previous full candidate to its ignored
`dist/failures/Client_Original_Startup-01.000.NNN/`,retain symbols/status and record
failure evidence/source commit/report hashes. Do not overwrite frozen passes.

Packager regenerates baseline002convenience ZIP. Afterward restore exact
`dist/milestones/Client_LWJGL_Core-01.000.002/PPSA99874-full-local.zip`
to `dist/client/PPSA99874.zip` and matching SHA256SUMS. Its SHA is
`d0b9f815ff68c5ad821b2166509879c623c813019d2f70bbacf53769f35e3971`.
Current startup package goes to runtime dist/PPSA99874.zip as above.

Do not restore old multi-GB archives just to check hashes. See
`docs/local-storage.md`:older failed client/server packages are losslessly
compacted in ignored dist/archives with manifests and restore tools;newer failures
are directly retained. Frozen passing packages/symbols remain intact. Avoid
unneeded duplicate600MB packages;the user previously ran out of disk space.

Latest frozen passing client milestone is Client_SPIRV_Cross036,not startup044.
Native component milestones include035VMA,033FreeType,031STB,029OpenGL provider,
026callbacks/OpenAL and023continuous direct GPU/SDL scene. Preserve their releases,
validation/source/packages;broader API/game/menu claims remain unvalidated.

## Branding and Prospero Store

Name:**ProsperoCraft**. The user approved the generated crafting-table PC icon
with complete dark-green letter outlines. Active packaging icon:
`assets/branding/icon0.png` (512RGBA). Master:
`assets/branding/ProsperoCraft-icon-v3-source.png` (1254square).
`assets/branding/branding.json` records hashes;`tools/apply_branding.py` applies
name/icon to future client/server packaging. It has been included since041.
Preserve earlier source art and frozen packages. No more icon redesign is needed.

Prospero Store catalog:
https://github.com/darkxex/ps5-homebrew-catalog
Reservation file:apps/PPSA99874.json.
Original reservation PR353merged2026-10-17.
Rename/description PR737:
https://github.com/darkxex/ps5-homebrew-catalog/pull/737
**MERGED2026-10-25**,verified via gh and upstream file during this handoff.
The upstream file now says ProsperoCraft;do not describe PR737as pending.
Website/store propagation was not independently checked.

Exact catalog description:
“Minecraft Java Edition client and server on PS5, powered by native OpenJDK 25;
vanilla, Fabric and Paper server playtests, with client startup under development.”
It is161characters,within200. Author:mateo-cogeanu;kind:game;category:pc-ports.

It is still a reservation:version,source_repo,artifact_url,sha256,icon_url and
license are all null. Catalog reservation rules require the shared Coming soon
image;do not force the new local icon URL or full development package into an
invalid reservation. Later downloadable listing needs truthful release state,
pinned public icon/artifact and checksum,following current upstream schema.
Never include downloaded Minecraft JARs in public release/catalog artifacts.
Passing client releases use app-only packages plus provisioning helper,validation,
SHA256SUMS and exact matching OpenAL LGPL source/relink kit;verify every upload.
Do not promote044to a passing release before actual console acceptance.

Local catalog checkout:
`/Users/mateocogeanu/Documents/ChatGPT/PS5_Homebrew/.tools/prospero-catalog`
Historical branch:codex/prosperocraft-branding in mateo-cogeanu's fork.
See docs/prospero-store-submission.md for submission context. Do not open a
second rename PR or resend the same change;737is merged.

Server state:vanilla,Fabric and Paper have console playtests and a full release
already exists;preserve its README/release links. Two-hour server endurance is
still pending by user choice. Current priority is original client startup/menu.

Finish each turn with verified GitHub publication status and explicit console
validation still needed. Keep the user updated during sustained work,without
claiming diagnoses/fixes beyond the saved evidence.
