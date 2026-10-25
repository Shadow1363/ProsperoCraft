# Runtime GLSL compiler dependency

Actual shaderc v2026.2 and matching glslang/SPIRV-Tools/Headers pins are in
sources.json. Build with tools/build_shaderc_native.py. Upstream sources remain
unchanged in ignored caches. Compiler C++ Release builds disable exceptions;
HLSL support remains on to satisfy upstream shaderc linkage but is not tested.
Target x86-64/SSE2 excludes AVX/AVX2/FMA. Individual compiler/result handles are
released by Java; native global teardown is not validated.

Actual compiler constructors are retained in a dedicated linker range and run
once through lifecycle.c's resident JNI_OnLoad after VM creation. Only actual
available graphics-provider definitions are used for scoped compatibility.
JVM/SDK and official Java shaderc/game JARs remain unchanged. The app packages
upstream component license texts; source pins identify reproducible sources.

018 exports the exact pinned shaderc source into the ignored target build tree
and applies `0001-compile-checkpoints.patch`. This observational native dependency
patch logs actual compile API, diagnostic stringstream and glslang parser
boundaries; it does not replace compiler results or change a Java/game JAR.
The host compiler uses the original sources, without these target checkpoints.
The patch SHA-256 is recorded in the package audit and checked against source.

019 additionally exports pinned glslang and applies `0002-parser-checkpoints.patch`.
`fault.c` scopes a signal-context recorder around actual compilation, forwarding
unchanged faults to previous handlers and restoring handlers on normal return.
It records96 raw context words using the pinned SDK probe range, without assuming
desktop register offsets. Native patch/source hashes are packaged and verified;
this does not establish PS5 signal capture or a repaired parser. Host delegation/
restoration tests are in `tools/test_shaderc_fault.py`.
