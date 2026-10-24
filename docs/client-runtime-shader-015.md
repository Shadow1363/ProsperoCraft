# Client Runtime Shader Compilation 01.000.015

Client015 adds actual runtime GLSL compilation through the original LWJGL
shaderc3.4.3 bindings and a resident shaderc v2026.2 library. Shaderc, matching
glslang, SPIRV-Tools and SPIRV-Headers revisions are pinned in
client/ports/shaderc/sources.json. These are real compiler implementations;
no precompiled fixture SPIR-V is used by the new compiler row.

Three compiler/options lifecycles compile a deliberately invalid compute shader
and require non-success status, errors and a nonempty diagnostic. Each then
compiles valid GLSL for Vulkan1.1/SPIR-V1.3, checks bounded length/magic, copies
the actual compiler result, releases compiler/result/options and passes those
bytes to vkCreateShaderModule. RADV builds a compute pipeline and executes six
workloads per cycle. Java verifies all returned/guard words:18dispatches total.
Optimization alternates between zero and size. Includes/callbacks/HLSL are not
validated; HLSL build support remains enabled because upstream shaderc links it.

The compiler's actual retained constructors, including the exact SDK libc++
iostream member newly required by the compiler, are staged in a separate linker
range and executed once by its genuine resident JNI_OnLoad after VM creation.
Compiler references bind to available existing scoped graphics providers;
process-wide JVM resolution and the SDK remain unchanged. Global module
teardown and low-memory behavior are unvalidated. Individual shaderc result,
options and compiler handles are released during the test.

## PS5 run

Install **PPSA99874 01.000.015** from `dist/client-runtime_shader/PPSA99874.zip`,
also copied to the runtime workspace's current `dist/PPSA99874.zip`. Installing
replaces the shared-ID client/server app. Frozen014 and earlier milestones remain
unchanged; server two-hour endurance stays deferred.

1. Wait for **Client015 ready**, release X, then press X once.
2. Thirteen checks run automatically. At the SDL **Input ready** prompt, briefly hold X, Circle and D-pad Left, then move the left stick strongly, as in014.
3. After SDL accepts input, the new runtime compiler row runs. The existing full-screen tiles remain visible while it compiles/checks offscreen GPU output.
4. Wait for **Client015 automatic checks PASS**, then confirm tiles remain visible. Keep the app open for logs; after a crash reopen without pressing X.

The new compiler row is check12, followed by DestroyJavaVM at13. Console compiler
time has not been measured. If it stalls for several minutes or fails, preserve
its report by reopening without pressing X and request log retrieval. The SDL
input phase retains its two-minute limit; GPU fence waits are five seconds.

## Host evidence and limitations

The host builds the same pinned shaderc/glslang/SPIR-V dependencies and runs
actual original Java shaderc bindings, pairing only the host library digest
resource to the actual built binary. Three invalid/valid compile cycles pass,
then18 real MoltenVK GPU dispatches pass all output/guard checks with Java25
Xint/XcheckJNI/verification and actual LWJGL core UBSan. A separately loaded
upstream macOS dlopen/dlsym JNI provider is used by the host library loader.
Host success does not validate target resident initialization or PS5 compiler
execution. The compiler itself is a normal release build, not UBSan-instrumented.

```sh
python3 tools/package_client_vulkan.py --runtime-shader --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline
python3 tools/test_client_vulkan_host.py --runtime-shader --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25
python3 tools/test_client_vulkan_package.py --runtime-shader --runtime-workspace /path/to/PS5_Homebrew
```

Source caches must contain the exact pins for offline builds. Compiler licenses
are included with the app. Original game/SDL/Vulkan/shaderc JARs and runtime
implementation/SDK are unchanged. All thirteen PS5 checks and final visual
confirmation remain pending; status/hash/checks are in client/runtime_shader/status.json.
Textures/depth/blending, missing input/renderer features and Minecraft startup
are separate upcoming steps. No new passing milestone is created yet.
