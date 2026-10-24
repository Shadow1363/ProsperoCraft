# Client Continuous Direct Scene — PS5 human PASS

Frozen **PPSA99874 01.000.023**,accepted2026-10-24. The user reports **“PASS”**
after explicit ALL15 and visible pastel/blue/white phase instructions.
Current-run reports could not be retrieved:the PS5 log endpoint refused
connections. No independently verified session ID or exact frame count is
claimed. [Validation](validation.json) records the evidence boundary and pins
exact tested source/package/dependencies.

The shared actual vertex-buffer/perspective renderer records three draws into
each acquired SDL BGRA swapchain color attachment. D32 depth,real sampled
texture and alpha-blend pipelines exercise pastel/blue/white phases every60
frames. Acceptance requires at least180FIFO frames,36independent1/W reference
samples+256guards per frame,physical eventMask15/stateMask15 and JVM shutdown.
These are workload requirements;the precise observed frame count remains unknown.
There is no captured-scene upload/blit in the presenter. The older offscreen
scene still runs as a separate baseline. Native display/renderer resources
remain retained until app close.

The same renderer passes81draws/27fullBGRA images+guards across3sessions/all
phases and completed-work cleanup on a real host MoltenVK GPU. Host targets
are offscreen and do not establish PS5 WSI behavior. Original54Java/game JARs,
JVM/SDK source and native ports remain unchanged. Existing paired C++ allocation
and compiler diagnostics stay active. Camera controls are not implemented.

Download the four assets from the
[release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Continuous_Direct_Scene-v01.000.023):

1. Verify the app-only ZIP,validation.json and helper against SHA256SUMS.
2. Extract `PPSA99874-client-continuous-direct-scene-app-only.zip`.
3. Prepare matching originals with `python3 tools/prepare_client.py`,then run `python3 provision_client_release.py --manifest validation.json --app-dir PPSA99874 --jars-dir /absolute/path/to/build/client/jars`.
4. Install PPSA99874. At Client023 ready,release X and press X once.
5. Look for pastel/blue/white scene phases on magenta;complete X/Circle/D-pad Left/strong left-stick prompts and confirm ALL15 PASS.

Provisioning reconstructs every exact tested file and rejects checksum mismatches.
Installing replaces the shared-ID client/server app. Tested binaries were not
rebuilt. Embedded pending audits reflect the pre-test package;the external
validation records the subsequent human acceptance and absent log corroboration.

Full tested package SHA256:
`846cd9adea6f9e6b04f80df461424c26b1fec6aa080ed641c35e7cfb16488ea4`.

Current-run log retrieval,camera controls,index buffers,filtering/mips,larger
models/shaders,Minecraft startup,full SDL/Vulkan coverage,native teardown and
prolonged/low-memory robustness remain unvalidated. Server two-hour endurance
remains explicitly deferred.
