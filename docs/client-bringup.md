# Client bring-up

The user authorized client work on 2026-10-22 after positive Fabric094/Paper108 console feedback, explicitly leaving the two-hour server test pending. The Fabric/Paper release is now a full release at the user's request. This changes the work order; it does not add a formal ALL PASS or endurance result. Server packages remain preserved and client preparation uses a separate build directory.

## First completed stage: pinned artifacts and class preflight

`client/26.3.lock.json` pins the official 26.3 client plus 53 unconditional Java libraries, metadata and the asset index by published size/SHA-1 and locally checked SHA-256. The official client JAR is unchanged. All 61 conditional desktop artifacts are recorded but excluded from PS5 staging, including LWJGL platform binaries and desktop Netty transports. Some unconditional JARs themselves contain desktop native resources (JNA:26, LZ4:8, counted by native-file suffix); those signed JARs remain intact and their native resources are not initialized/extracted by the preflight. No desktop binary is claimed to be PS5-compatible.

The current official metadata differs from the server's earlier metadata snapshot only in the asset index. Client JAR bytes are identical: SHA-1 `e877b6a07acd633fb3bb475002175cec036e7b87`. Client preparation pins the newer asset index without changing server pins. Asset index34 is verified; its roughly485MB of asset objects are not yet fetched. No account tokens or credentials are requested or stored by these tools.

Prepare locally:

```sh
python3 tools/prepare_client.py
```

Artifacts stay in ignored `.tools/client/` and `build/client/`. `--offline` requires the complete verified cache and makes no download requests. A cached size/hash mismatch is an error. All inputs are checked before the separate client staging directory is replaced. The working server asset directory and current package are untouched.

Run the host preflight with an actual Java25 toolchain:

```sh
python3 tools/test_client_artifacts.py --java-home /path/to/jdk25
```

The real JVM runs with `-Xverify:all`, verifies all54 JAR hashes, and loads the original main client, window, SDL event, RenderPearl Vulkan backend/instance and LWJGL SDL/Vulkan classes with initialization disabled. The probe does not invoke Minecraft, native initialization, login, a GPU call or rendering. A deliberate same-size client-JAR corruption is rejected before class loading and restored afterward. No class or bytecode transformation is applied.

A separate real-JVM control initializes the original LWJGL Platform class under `os.name=PS5` and reproduces `LinkageError: Unknown platform: PS5`. This is the first known dependency port boundary, not a solved client-launch test. No OS identity override is used to make the game run.

## Graphics and native integration

The inspected official client already contains a Vulkan renderer and SDL integration. Its original VulkanInstance bytecode requests Vulkan1.2 and calls `SDL_Vulkan_GetInstanceExtensions`; the Java/backend classes alone do not establish driver, surface or feature compatibility. A renderer replacement is not assumed necessary at this stage.

[PS5_Vulkan](https://github.com/mihawk-99/PS5_Vulkan/tree/f410e67a0241b3e8edcdbcd2a9b285dfc4a412ed) remains an evaluation candidate. `client/graphics-candidates.json` records its inspected source revision and the Mesa/SDK revisions named by its upstream build scripts. Those are source-evaluation pins, not built or validated dependencies. The upstream RADV/VideoOut claims are not console results from this project. Do not replace the working runtime SDK globally while evaluating this separate stack.

Next work is actual dependency platform support and native bindings, with a small native presentation test and Java-to-SDL/Vulkan bridge before attempting the client menu. LWJGL core/native invocation, SDL window/events/Vulkan surface creation, allocator integration, shaderc/SPIRV-Cross/VMA, text/image resources, OpenAL and controller input each require supported PS5 implementations and validation. Bundled JNI libraries must not silently fall back to desktop binaries. Preserve the official game JAR and keep compatibility in the Java port, dependency ports or external harness.

No PS5 client app, graphics frame, menu, world or controller result is claimed yet. Server endurance and remaining lifecycle checks remain pending separately.
