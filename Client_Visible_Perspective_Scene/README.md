# Client Visible Perspective Scene — PS5 ALL15 PASS

Frozen **PPSA99874 01.000.022**,accepted2026-10-24. Human **“all pass”** follows
the explicit ALL15/controller/visible-panel checklist. Retrieved run
`client-01.000.022-1792845723-859007196` records ALL15 PASS.
[Validation](validation.json) pins exact source/package/dependencies and evidence.

Six actual position/UV vertices form a panel with camera-space Z2on the left
and4on the right. The vertex shader performs perspective projection and the
fragment shader samples a real texture with perspective-correct UVs. An
independent barycentric1/W reference checks all pixel centers of9full256x256
images plus256guards across3sessions/27draws with depth/blend controls.

The final normal-phase actual GPU readback is copied to Java bytes,uploaded once
and nearest-blitted into the SDL BGRA swapchain. The static pastel panel on a
magenta background passes295FIFO frames with36actual swapchain pixel samples
and256guards each,physical eventMask15/stateMask15,and DestroyJavaVM. This is
an explicit render/readback/re-upload/blit handoff; it does not establish
continuous scene rendering directly into the swapchain or camera/gameplay input.

Existing runtime shaderc/invalid-source/GPU checks and the separate021 texture
controls also pass. New graphics shaders are compiled offline/spirv-val checked.
Original54Java/game JARs,JVM/SDK source and native ports remain unchanged. Prior
C++ allocation/diagnostic adaptations remain disclosed in audits. Native SDL/
display resources stay retained until app close.

Download the four assets from the
[release](https://github.com/mateo-cogeanu/ps5-minecraft-java/releases/tag/Client_Visible_Perspective_Scene-v01.000.022):

1. Verify the app-only ZIP,validation.json and helper against SHA256SUMS.
2. Extract `PPSA99874-client-visible-perspective-scene-app-only.zip`.
3. Prepare matching originals with `python3 tools/prepare_client.py`,then run `python3 provision_client_release.py --manifest validation.json --app-dir PPSA99874 --jars-dir /absolute/path/to/build/client/jars`.
4. Install PPSA99874. At Client022 ready,release X and press X once.
5. After offscreen checks,press X/Circle/D-pad Left and move the left stick strongly when prompted. Confirm ALL15 PASS and the static textured panel on magenta.

Provisioning reconstructs every exact tested file and rejects checksum mismatches.
Installing replaces the shared-ID client/server app. Tested binaries are preserved
without rebuilding. Embedded audits retain their pre-test pending fields; the
external validation record captures the subsequent console acceptance.

Full tested package SHA256:
`9d49135a4dcbd66e93ef496e442c7845964e08aa6664c9dc26546a94196e450e`.

Continuous/direct scene rendering,camera control,index buffers,filtering/mips,
larger workloads,Minecraft startup,full SDL/Vulkan coverage,native teardown and
prolonged/low-memory robustness remain unvalidated. Server two-hour endurance
remains explicitly deferred.
