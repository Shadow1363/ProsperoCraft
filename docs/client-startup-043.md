# ProsperoCraft client043 — bounded native WSI diagnostics

042run client-01.000.042-1792939125-381634840 confirms actual SDL1920x1080 at
59.94Hz and Vulkan surface capabilities with the same extent,images2-5 and
usage0x9f. Original Minecraft still repeatedly fails swapchain creation with
VK_ERROR_INITIALIZATION_FAILED at1080p/FIFO;the user reports a crash. Saved full
VM trace and512KiB startup tail contain no fatal signal. VM trace ends
DONE:Metadata zeroing. The exact swapchain rejection and subsequent crash
instruction remain unresolved;reducing4K did not fix the driver failure.

043is diagnostic development,not a confirmed crash fix. A small native Mesa WSI
patch reports requested/mode extents,image count and limit,host-import callback
availability,format/usage/present mode,registration error,image byte/alignment
requirements,and memory-type intersection. Initialization guards and failing
operations retain their original Vulkan result and are labelled in the report.
The existing client_gpu_stage logger sends checkpoints to startup and VM trace.
The formatter uses a384-byte stack buffer and limits output to64events;no new
allocation path is added in the helper. Native graphics calls/parameters and
all return values stay unchanged. No errors are swallowed or converted to PASS.

Build tool tools/build_wsi_diagnostics.py verifies pinned Mesa source against its
Git object,applies client/ports/mesa/0001-videoout-checkpoints.patch in an ignored
private work folder,and compiles using its exact recorded target command/options.
It copies the original static RADV archive,replaces only wsi_common_videoout.c.o,
verifies embedded member bytes,and checks the original archive's hash remains
unchanged. Startup packaging alone selects this private archive. Other build
profiles and frozen artifacts retain their original driver. The GPU integration
audit records source/patch/object/private/original archive hashes.

The previous real1080p selection,scoped LWJGL allocator,256MiB heap,approved v3
icon,original game JARs and JVM global behavior remain unchanged. Exact failed
042package/symbols/status and all frozen passing milestones are preserved.

Checks/build:

```sh
python3 tools/build_wsi_diagnostics.py
python3 tools/test_wsi_diagnostics_host.py
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

The host test extracts the actual helper and checks unchanged success/failure
codes,oversized message truncation and64event limit under4threads with ASan/UBSan.
It does not simulate the Vulkan driver or validate OS failure paths. Target
checks prove private object/archive selection,diagnostic strings in the app,
original archive preservation,all54JARs/5147assets,exact runtime,accepted native
components/scoped allocations/constructors,icon and signatures. Host launch and
native allocation preflight remain component checks,not a PS5 menu pass.

Install local dist/client-startup/PPSA99874.zip or runtime dist/PPSA99874.zip,
launch and press X once. Report failure promptly. After a crash,reopen without
X so logs remain available. The next diagnostic run should name the WSI rejection
branch;PS5 swapchain/presentation/menu,crash cause/resolution,memory/performance,
network and teardown remain pending. Server2H endurance stays deferred.

Host helper/launch/allocation checks,target WSI compile and full-package checks
pass. Full local ZIP SHA-256:`80094940d09e25479fae0dbb6106a6d65b11ffe3c6582ac234b6dae38fd2afe3`.
PS5 diagnostic run and swapchain/crash resolution remain pending.

Console outcome:checkpoint initialization-guard-477 identifies negative VideoOut
open before image allocation. Driver caches its first failure permanently. See
[043evidence](validation/client043-startup-failure-2026-10-25.json) and
[044bounded retry](client-startup-044.md). Original refusal/crash remain pending.
