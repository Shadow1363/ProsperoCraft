# Client Native Graphics 01.000.003 — PS5 ALL PASS

This standalone native test is the next step after Client_LWJGL_Core002 ALL PASS. It checks the real Mesa/RADV PS5 GPU and VideoOut presentation path before combining it with the Java runtime. It launches no JVM, SDL, audio, shader pipeline or Minecraft code. Passing it will establish this transfer/readback/presentation path, not game rendering or full Vulkan conformance. On 2026-10-23 the human tester confirms all requested visible checks passed, with no crash or visual corruption. The source and exact compiled package are frozen in `Client_Native_Graphics/`. Logs were not reachable; acceptance is the direct human report.

Title `PPSA99874`, version `01.000.003`, same app/content identity as requested. Installing replaces the existing app. The exact frozen000/001/002 packages and Fabric094/Paper108 fallbacks remain preserved. Server two-hour endurance stays deferred.

## Run on PS5

1. Install the full `PPSA99874` folder from `dist/client-graphics/PPSA99874.zip` (also copied to the runtime workspace's current `dist/PPSA99874.zip`). No JAR provisioning is needed for this native-only app.
2. Open the app. The initial screen may be blank: a system notification says it is ready. Press **X once** to start. Until X is pressed, the app shares existing reports and does not rerun the GPU test.
3. Expect red, green and blue full-screen frames (30 each), followed by a blue/green card with **PS5 JAVA CLIENT 003**, **NATIVE GRAPHICS PASS** and **READBACK VERIFIED**. A system notification reports the automated result. Confirm that both the colour sequence and the final card are visible and legible, with no crash or corruption.
4. Leave the app open after success or failure for logs at `http://<PS5-IP>:8765/`. `build.txt` identifies the open app; `session.txt` identifies the recorded test; `startup.log` holds acceptance checkpoints and `vm-trace.log` holds the driver stderr stream. These are generic existing route names; this app does not execute a VM.
5. If the app crashes, reopen it and **do not press X** so the preceding reports remain available. Close via the PS menu when finished.

The test opens a Vulkan1.2 instance through the real statically linked RADV entry point, finds the physical GPU/graphics queue, queries display modes/surface capabilities and checks its format/usage support. It allocates a bounded swapchain and host-visible transfer buffer, runs actual GPU clear/copy/readback commands, compares first/last pixels and submits FIFO presents. A final CPU-generated bitmap card goes through a GPU buffer-to-image copy and another exact corner readback. The text is a test bitmap, not a shader renderer. Acquire/fence waits request five-second timeouts, although an internal driver/platform call can still hang or fault. Checkpoints are flushed before Vulkan calls.

One submission is in flight at a time. Fences and queue-idle waits protect command-buffer and semaphore reuse. Host writes are flushed; GPU readback is invalidated after its fence. The final swapchain/resources stay resident until the app is closed, preserving the visible result; teardown/recreation is not tested in003. A human display confirmation remains necessary even when automated readback passes.

## Dependencies and reproduction

`client/graphics/sources.json` pins the driver integration, Mesa and SDK fork, base SDK archive and actual compiler-rt CPU-model sources/licenses. Downloaded sources and binaries stay in ignored caches. No source changes are made to Mesa or the SDK fork.

- PS5_Vulkan integration: `f410e67a0241b3e8edcdbcd2a9b285dfc4a412ed`.
- Mesa/RADV: `1ba9874f478657ccf6da72ce55f0260164cc0bd0`.
- PS5 SDK platform fork: `b83202be73e930050e00de0f1b4d9ec46c0391bf`, layered over the SHA256-verified upstream SDKv0.42 **in a separate consumer cache**.
- LLVM22.1.7 compiler-rt CPU detection is compiled from pinned source, and the verified SDK supplies its real x86-64 emulated-TLS object. The generated copy of the upstream link recipe substitutes this target runtime archive for its Linux-host compiler-rt path; upstream heap/thread/libc binding rules are retained.
- The native app and target Mesa use explicit baseline x86-64/SSE2 flags without AVX/AVX2/FMA. SDK libraries retain their upstream bytes/profile.

The macOS build requires Homebrew LLVM22.1.7/lld, ninja, pkg-config, glslang, libclc and matching SPIR-V LLVM translator, plus Python3 and git. `prepare_client_graphics.py` creates an isolated pinned Python environment, builds the SDK platform archive and real Mesa host shader tools, then cross-compiles RADV. It compiles the pin's imported regex/dlmalloc units separately to avoid its make pattern-rule warning issue on this host; source remains unchanged. Mesa's upstream `_Generic` qualified-type warnings remain build warnings, not project fixes or runtime failures.

```sh
python3 tools/prepare_client_graphics.py --runtime-workspace /path/to/PS5_Homebrew
python3 tools/package_client_graphics.py --runtime-workspace /path/to/PS5_Homebrew
python3 tools/test_client_graphics.py --runtime-workspace /path/to/PS5_Homebrew
```

Native converter/signing tools and the existing clean-room libc companion come from the runtime workspace. Its SDK, HotSpot objects and boot image are unchanged. AGC `.so` link stubs declare real system-module imports for the converter; they are neither linked as implementations nor packaged/executed. Source/object/driver/platform hashes and dependency pins are embedded in `assets/graphics-audit.json`. Full component licenses and source copyright notices accompany the package.

Host checks cover actual target compilation, native conversion/signatures, real driver exports and AGC import providers, source/object audits, absence of game/JVM/audio/desktop libraries, exact frozen package hashes and the actual test-card pixel writer under ASan/UBSan from640x480 through8K. The result card is also visually inspected from that host writer. These checks do not execute PS5 GPU calls. The subsequent human console confirmation establishes this scoped ALL PASS milestone; it does not extend the host checks to untested graphics or game paths.
