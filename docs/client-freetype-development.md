# Client033 — real FreeType fonts,PS5 ALL5 PASS

Original Minecraft startup032 exits at NativeLibrariesBootstrap,loading
`libfreetype.so` first. The game crash report identifies UnsatisfiedLinkError;
the native report ends VM EXIT -3. This does not establish a native VM fault,
heap exhaustion,or successful STB/OpenGL loading in original Main. Its exact
full ZIP,symbols and candidate metadata remain in local ignored dist/failures.
Saved reports are recorded by hash in the032 validation JSON;raw logs stay local.

033 supplies real FreeType2.14.1 from the pinned upstream commit in
client/ports/freetype/sources.json. No FreeType source changes or fabricated
functions are used. CMake disables optional zlib,bzip2,PNG,HarfBuzz and Brotli;
built-in drivers/rasterization remain real. A static resident group named
freetype exposes the real FT functions. Its allocations use the existing
scoped graphics heap;JVM allocation wrappers stay unchanged. Original LWJGL
Java methods call those real addresses through existing JNI/libffi paths.
No additional Java dependency overlay is required. All54 downloaded Java/game
JARs stay intact. The test uses pinned Abel Regular under OFL,not a game asset.

Build:

```sh
python3 tools/build_freetype_native.py --runtime-workspace /path/to/PS5_Homebrew --offline
python3 tools/build_freetype_native.py --runtime-workspace /path/to/PS5_Homebrew --offline --host
python3 tools/test_freetype_bootstrap_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --freetype-bootstrap
python3 tools/test_client_freetype_package.py --runtime-workspace /path/to/PS5_Homebrew
```

Omit --offline for the first verified source/font fetch. Host tests use the
exact fixture bytecode,real FreeType under UBSan,Xcheck:jni and Xverify:all,
normal Mac and a host-only PS5 enum selector. Only the host validation JAR's
native hash resource is paired with the host-built library;original cached JARs
and target package remain unchanged. The existing host loader supplies real
dlopen/dlsym. Host dispatch controls are excluded from the console package.

The five console rows initialize the runtime,create128MiB VM,verify the original
54-JAR inventory,execute real font checks,then destroy the VM. Three library/
face lifecycles verify version2.14.1,Abel metadata,FT struct access,and A/g/@
at16/24/32px. Each glyph is rendered twice and compared exactly. Nine bitmaps
have expected FNV64 `fc260d7c9d8a2036`. Space must have zero bitmap rows with
positive advance;invalid font input must fail. The font input remains unchanged
with128guard bytes per cycle. Face/library cleanup uses the actual FT APIs.
There is no application music or visible game window. Font/raster results are
automated checks,not a visual glyph preview or Minecraft menu pass.

Install the local full dist/client-freetype_bootstrap/PPSA99874.zip or the
runtime workspace dist/PPSA99874.zip. Same title PPSA99874 replaces the existing
app. Launch,press X once,and report the five-row outcome. If it fails or closes,
reopen without pressing X and leave it open for report retrieval.

Human ALL5 PASS on2026-10-25 and matching saved session/detailed startup establish the tested
PS5 font ABI,rasterization,controls and cleanup workload. Other font formats,
hinting/kerning/shaping,color/compressed fonts,callbacks,concurrent/large inputs,
full native teardown and Minecraft startup/menu remain unvalidated. VMA,
SPIRV-Cross and remaining SDL paths are still incomplete. Server two-hour run
remains deferred. Preserve frozen031/029/026/023 and all earlier milestones.
Client_FreeType_Fonts preserves the accepted source/package/validation and
public release. Continue development outside that frozen snapshot.

FreeType is included under the FreeType Project License;portions are copyright
The FreeType Project. Its LICENSE.TXT and complete docs directory are packaged,
with Abel's OFL notice. A future public OpenAL-linked binary must include matching
OpenAL corresponding source and exact relink materials before publication.

Host/source-integrity/full-package checks pass. All210 required LWJGL FreeType
function addresses and its optional Bzip2 entry have real exports. Optional
compressed-font functionality remains disabled as disclosed above. Full local
package SHA-256:
`e7666f17dedda986507f9ba19fa11183bf89baf07971044659dcee2416022afc`.
PS5 five-row human ALL5 PASS and matching saved session/detailed startup recorded
on2026-10-25. All3cycles,9glyphs/FNV64,guards/controls/cleanup and DestroyJavaVM
are independently corroborated in the saved current-run report.
