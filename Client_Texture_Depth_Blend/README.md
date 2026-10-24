# Client Texture,Depth and Blending — PS5 ALL14 PASS

Frozen **PPSA99874 01.000.021**,accepted2026-10-24. The user reports
**“nice pass!”** Saved run `client-01.000.021-1792844052-984973201` records
ALL14 PASS. [Validation](validation.json) pins exact tested source/package,
dependencies,native adaptations and console evidence.

The new offscreen workload uploads a2x2RGBA texture through a staging buffer,
binds an actual combined sampled-image descriptor and renders through original
LWJGL Vulkan APIs. A D32_SFLOAT depth attachment rejects a farther blue layer;
a depth-disabled control must replace it. Standard source-alpha blending mixes
a half-alpha white layer; a blend-disabled control must replace the color.
Three sessions perform27draws and verify every pixel of9full256x256images plus
256guard bytes per readback,allowing1UNORM rounding step per channel.

The new graphics shaders are compiled offline and spirv-val checked. The
existing separate real runtime shaderc row also passes its3compiler/invalid
controls and18GPU output workloads. Physical SDL input/display then passes
318frames with eventMask15/stateMask15,and DestroyJavaVM completes. The visible
tiles remain the existing SDL baseline; this is not a new visible textured scene.

Original54Java/game JARs,JVM/SDK source and native dependency ports are unchanged.
The020 paired C++ allocation providers and disclosed compiler checkpoint/fault
recorder adaptations remain. Native SDL/display resources stay retained until
app close; full teardown is not established.

Download the four assets from the
[release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Texture_Depth_Blend-v01.000.021):

1. Verify the app-only ZIP,validation.json and helper against SHA256SUMS.
2. Extract `PPSA99874-client-texture-depth-blend-app-only.zip`.
3. Prepare matching originals with `python3 tools/prepare_client.py`,then run `python3 provision_client_release.py --manifest validation.json --app-dir PPSA99874 --jars-dir /absolute/path/to/build/client/jars`.
4. Install PPSA99874. At Client021 ready,release X and press X once.
5. After offscreen compiler/texture checks,the SDL Input ready prompt asks for X/Circle/D-pad Left/strong left-stick movement. Confirm final PASS and visible tiles.

Provisioning restores every exact tested file and rejects checksum mismatches.
Installing replaces the shared-ID client/server app. Tested binaries were not
rebuilt; embedded audit fields retain their pre-test pending values while this
external record contains the later acceptance.

Full tested package SHA256:
`5adbcd8dda4e355c69ab027c4630c0603bb095250e9afb2251e678ce9e58bc81`.

Texture filtering/mips,perspective,vertex/index buffers,a new visible textured
scene,actual Minecraft startup,larger shaders/includes/callbacks/HLSL,complete
SDL/Vulkan coverage,global teardown and prolonged/low-memory robustness remain
unvalidated. Server two-hour endurance remains explicitly deferred.
