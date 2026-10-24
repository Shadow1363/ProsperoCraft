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
