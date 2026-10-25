# Client036 — real SPIRV-Cross translation/reflection acceptance

035 established actual VMA allocation/transfers on PS5. SPIRV-Cross is the next
known missing native bootstrap component before another original Main retry.
036 builds the pinned official SPIRV-Cross vulkan-sdk-1.4.363.0 sources with
C API0.68.0,matching the original LWJGL3.4.3 bindings. GLSL,HLSL,MSL,CPP and JSON
reflection backends are compiled. No implementation stubs or game transformations
are added. All54 downloaded Java/game JARs remain unchanged;no Java runtime or
SDK implementation changes are made.

The native C API is exported through resident ps5spvc. The harness sets
Configuration.SPVC_LIBRARY_NAME to System.mapLibraryName("ps5spvc") before
original Spvc initializes. A future Main retry must apply that same supported
configuration and combine the accepted VMA,FreeType,STB,GL and other providers.
The original Spvc default is spirv-cross;no Java dependency overlay is needed.

The target SDK lacks nl_langinfo in the current provider bindings. A single
reviewable dependency source patch selects SPIRV-Cross's existing localeconv
fallback using SPIRV_CROSS_PS5_LOCALECONV. It reads the real native decimal
separator;no constant value or fake locale API is substituted. Host builds test
the same branch against real host libc. Real C++ exceptions/RTTI stay enabled
so malformed SPIR-V returns real C API error codes/messages rather than asserting.
C++ namespace override clientspvc avoids private dependency name collisions;
C API names remain unchanged. Heap/thread providers use existing scoped graphics
bindings. Source archives stay intact;the patch applies to a private copy.

CMake Git discovery is disabled and SOURCE_DATE_EPOCH=0 makes its metadata stable,
preventing accidental consumer-parent Git identity/timestamps in native code.
The real source revision is recorded in the source pin and packaged audit.

The five rows initialize runtime/128MiB VM,verify54original artifacts,run shader
checks and destroy the VM. Three contexts parse the existing independently
validated compute SPIR-V fixture. Each translates to GLSL450/Vulkan semantics,
HLSL5 and MSL. Reflection must report compute/local_size_x64,one storage buffer
at set0/binding0 and an8-byte push-constant block. Exact translated-source Java
fingerprints are265161891(GLSL),657299176(HLSL),956349156(MSL). Malformed SPIR-V
must return SPVC_ERROR_INVALID_SPIRV with a diagnostic;input remains unchanged
with128guard bytes per cycle. Context allocations are released and contexts
actually destroyed. No game window or background music opens.

```sh
python3 tools/build_spvc_native.py --runtime-workspace /path/to/PS5_Homebrew --offline
python3 tools/build_spvc_native.py --runtime-workspace /path/to/PS5_Homebrew --offline --host
python3 tools/test_spvc_bootstrap_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --spvc-bootstrap
python3 tools/test_client_spvc_package.py --runtime-workspace /path/to/PS5_Homebrew
```

Omit --offline for the first verified source fetch. Host tests use the exact
fixture bytecode,real SPIRV-Cross under UBSan,Xcheck:jni and Xverify:all,normal
Mac and a host-only PS5 enum selector. The host validation JAR pairs only its
native hash metadata with the host library;original cached/target JARs remain
intact. Generated GLSL/HLSL outputs independently recompile with glslangValidator
and pass spirv-val for Vulkan1.1. MSL is generated/fingerprint checked,not Metal
compiler validated or executed. None of these host checks establish PS5 behavior.

Install local dist/client-spvc_bootstrap/PPSA99874.zip or runtime workspace
dist/PPSA99874.zip. Same PPSA99874 identity replaces the existing probe/server app.
Launch,press X once,and report all five checks. If it fails,leave it open for
reports;after app closure,reopen without pressing X. No preset device IP/filter
is embedded. Frozen035/033/031/029/026/023 and earlier packages remain preserved.

Actual PS5 C API,localeconv,exception/error handling,translations/reflection and
cleanup are pending. Executing translated shaders on PS5 GPU,other shader
stages/resources/features,CPP/JSON backend workloads,callbacks/concurrency/large
inputs,non-C/changing locales/floating-literal formatting,global teardown and
combined original Minecraft startup/menu remain unvalidated. Server two-hour
endurance remains deferred. No036 passing milestone/release is inferred yet.

Original SPIRV-Cross Apache-2.0 source/archive/license,the locale patch and LWJGL
BSD notice are packaged. A public OpenAL-linked release must include matching
corresponding-source and exact relink materials before publication.

Host/native build/full package checks pass. Full local package SHA-256:
`e4ff7cfe2464e7f218e4b518e1dfe77cca90e67fec531f9314aeb3e1191773ac`.
Actual PS5 five-row validation remains pending.
