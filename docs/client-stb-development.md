# Client030 failure and031 STB acceptance

Safari-saved reports identify run client-01.000.030-1792920868-564011535.
Original Main reaches NativeLibrariesBootstrap and exits-3 while loading STB:
UnsatisfiedLinkError for liblwjgl_stb.so. STB is index0in this randomized order;
this run therefore does not corroborate the original Main OpenGL path. Saved
startup and exception reports remain local;the source-controlled failure record
contains checksums and scope. No underlying native VM fault or heap OOM is
identified in those reports. Frozen029provider acceptance remains separate.

031builds the original LWJGL3.4.3 STB implementations and generated JNI at commit
30fac9b95f99cda97312232be25ba55297bf9951. All source/header files are pinned by
path,size and SHA256. Eleven generated C units compile with the actual embedded
STB implementations,producing224JNI exports. The standalone stb_vorbis.c is
included by its generated binding and is not separately compiled. The module
uses the existing PS5 native core;no game classes or driver-success stubs exist.

Original LibSTB.setupMalloc initializes private clientstb_org_lwjgl_* allocator
pointers. Compile-time symbol naming keeps these separate from the core's
allocator globals while retaining actual upstream setup/free behavior. The PS5
build uses compiler-managed emulated TLS for STB's per-thread decoder state;
there are no native .tdata/.tbss segments or module constructors. No runtime,
SDK implementation,original game JAR or frozen milestone is modified.

The same fixture bytecode executes real PNG encode-to-file/read/decode/free
cycles under Java25 Xint/XcheckJNI/verification and UBSan-instrumented host STB.
Three changing8x8RGBA images each verify256exact bytes and128input guard bytes,
plus dimension/channel queries,truncated-PNG rejection/failure reason,invalid
Vorbis rejection/error code,finite Perlin output and native struct sizes. Both
normal Mac and forced PS5 enum dispatch pass the3cycles each. The host selector
uses Unsafe (expected deprecation warnings) and is excluded from the app. A
host-only paired JAR adjusts only its native SHA1 resource. Actual original game
and downloaded library artifacts remain intact.

Target checks verify real STB exports/private allocator slots,the original54JARs,
exact runtime image/native libraries,359+4+5+15staged constructors/no automatic
constructors,8resident groups,matching host/console fixture bytecode,signatures
and CRC. Exact029passing and030failed packages remain preserved.031does not
invoke Minecraft. Full valid Vorbis decoding,font rasterization,resize,DXT,
callbacks,concurrent/large-image workloads and broad codec coverage are not
validated by these controls. Actual PS5 codec/JNI/cleanup and JVM shutdown
remain pending;do not freeze a milestone from host/package success.

Reproduce component builds with tools/build_lwjgl_stb_native.py using
--runtime-workspace and --java-home;--host selects macOS. --offline requires all
pinned sources in cache. Run tools/test_stb_bootstrap_host.py --java-home for
actual host codecs and both dispatch controls. Build the acceptance app with
 tools/package_client_vulkan.py --stb-bootstrap and the existing workspace/JDK
arguments;check it with tools/test_client_stb_package.py --runtime-workspace.
The local app includes original STB implementation source and license notices.
Public OpenAL-linked binary distribution still requires matching source/relink
materials;031is local development,not a published passing binary release.

Install031and press X once. It automatically runs five checks,ending in ALL5
PASS or a failing-row notification;no game window or sound is expected. Keep
it open afterward for logs. Once this real native component is accepted on the
console,the next original Main attempt can include it alongside029's genuine
OpenGL provider. Other game native libraries and server endurance remain pending.


## Client031 console acceptance

Human ALL5 PASS and saved session client-01.000.031-1792921801-581678467
establish the passing Client_STB_Codecs milestone. The saved session explicitly
reports STB PNG/codecs/JVM stop. The large startup download was incomplete and
contains historical text only in its partial local file;no independent detailed
current-run stage verification is claimed. Preserve that limitation in any
follow-up evidence. Frozen source/package/symbols/validation and app-only release
are retained. Original54JAR reprovisioning reproduces every accepted file and
rejects corrupt retained files;matching OpenAL relink reproduces the exact native
ELF. Continue new work outside the snapshot. Valid Vorbis/font/resize/DXT/callback
coverage,Minecraft startup and server endurance remain unvalidated.
