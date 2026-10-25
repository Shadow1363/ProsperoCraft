# Client027 OpenGL failure and native binding work

The human reported027 exited and reopened it. Safari's current session identified
run client-01.000.027-1792854115-898280003 at original Main. The full saved
exceptions.log identifies Loading library OpenGL:
`UnsatisfiedLinkError: Failed to locate library: liblwjgl_opengl.so`,from
org.lwjgl.opengl.GL class initialization. Its randomized load order starts
OpenGL,vma,freetype,STB,SDL,shaderc,OpenAL,spvc;the failure is at index0.
The heap report shows46MiB used of123MiB;no heap OOM is reported. OSHI's
caught unsupported-OS report warnings are not the fatal cause. The game JAR
signature/brand remains untouched. Startup-tail saving was unavailable in Safari;
no complete startup/native termination trace or raw native crash is claimed.

This has two distinct requirements:a genuine LWJGL OpenGL JNI module and a real
OpenGL implementation/function provider. Development now builds193 original
pinned LWJGL3.4.3 generated C units and2,270JNI exports as a PS5 relocatable
object. The OpenGL header/platform macros use the existing native core ABI;
WGL/GLX native units are excluded. Sources are pinned by commit,size and SHA256.
No driver-success stub or replacement game class is added. The native binding
is built separately and has not been packaged/accepted on PS5. This is not a
028 app or milestone.

Host validation loads those actual rebuilt bindings with the real macOS CGL
provider/Apple M4 GPU. Three real contexts execute texture/framebuffer setup,
clear/readback and destruction. Each verifies64RGBA pixels and128guard bytes
(192pixels/384guards total). Java25 Xint/XcheckJNI/verification and native UBSan
pass without JNI/UBSan warnings. The host-only paired JAR changes only its
native-library SHA1 resource;the original downloaded Java/game artifacts remain
intact. These host controls do not establish a PS5 OpenGL provider or rendering.

The existing PS5 SDK libSceGLSlimVSH.so contains import declarations,not a driver
implementation;its symbol presence does not establish desktop OpenGL/context
availability. Search results advertised blackbearreloaded/ps5-opengl as a Mesa-
based candidate,but direct GitHub page,API and git access returned404/repository
not found on2026-10-24. No source,SDK artifact or binary identity could be
retrieved/verified;it is not adopted. Cached search claims are not validation.

A real PS5 resident provider/context integration remains necessary. Existing
RADV/Vulkan acceptance is preserved. Further native libraries STB,FreeType,VMA,
SPIRV-Cross and remaining SDL paths are also incomplete. No additional027
console rerun or bindings-only app is requested while the provider is unresolved.
Continue development outside frozen026 and keep all game/runtime artifacts intact.
The two-hour server run stays deferred. Raw reports remain local.

Reproduce this component build with tools/build_lwjgl_opengl_native.py using
--runtime-workspace and --java-home;--host builds the host JNI library. Then run
tools/test_lwjgl_opengl_host.py --java-home. The actual host core/loader helpers
from preceding native tests must be built first. Generated outputs/logs/caches
are ignored;no game/desktop native binary is substituted into the PS5 package.


## OSMesa provider development — 2026-10-25

The original client accepts `--graphicsBackend vulkan` (already supplied by
ClientStartup25),and Options contains `preferredGraphicsBackend` with the enum
value `vulkan`. NativeLibrariesBootstrap nevertheless loads OpenGL unconditionally
before the Minecraft instance processes its options. Changing options.txt cannot
supply its missing native binding/provider. This conclusion comes from local
inspection of the pinned,unmodified client classes,not a new console result.

Development now pins original Mesa24.3.4 and zlib1.3.1 archives plus the Meson
zlib adapter,with verified sizes/SHA256. The build disables Vulkan,LLVM,EGL,GLX,
window platforms and shared GLAPI and selects genuine OSMesa/softpipe. This is a
software OpenGL bootstrap path;it does not replace RADV or establish hardware GL
performance. Minecraft's selected rendering backend remains Vulkan.

Three explicit dependency patches produce a static OSMesa target,use the SDK's
actual file-description field type instead of unavailable kvaddr_t,and select
compiler-generated x86 dispatch for PS5 emulated TLS. The last patch adds an
opt-in Meson option,default false;host builds keep upstream dispatch selection.
The PS5 component build combines real OSMesa,XML option-query support (XML parsing
disabled upstream),and zlib into a relocatable object. Internal GLAPI,OSMesa and
DRI query references must resolve. External SDK/provider references deliberately
remain unresolved at this component boundary;this is not a final executable link.

The host test uses the same pinned softpipe implementation and original generated
LWJGL OpenGL JNI,not macOS CGL. It creates/destroys three OpenGL3.3 core contexts,
executes texture/FBO setup and distinct red/green/blue clears,then verifies192RGBA
pixels and768guard bytes. Non-direct and undersized context buffers are rejected.
Java25 Xint,XcheckJNI,full bytecode verification and UBSan-instrumented JNI helpers
are enabled;Mesa itself is built in release mode without UBSan instrumentation.
The host-only paired LWJGL JAR changes only its native SHA1 resource. Optional
SPIRV-Tools autodetected by host Meson is linked from Homebrew;the PS5 component
has no host SPIRV-Tools dependency. These checks do not establish PS5 GL behavior.

Reproduce with `python3 tools/build_osmesa_native.py --offline` for PS5 and add
`--host` for macOS. The existing graphics SDK/cross-file and graphics-python
Meson environment are prerequisites. Offline mode verifies all three archives,
preloads Meson's package cache and forbids further wrap downloads. Source/patch
changes invalidate the export and Meson configuration;separate generated host
and target output directories contain build audits. Run
`python3 tools/test_osmesa_host.py --java-home /path/to/jdk25` after the host Mesa,
LWJGL OpenGL,libffi/core and host-loader builds described above.

Remaining work is to isolate this Mesa provider's symbols from the separately
pinned RADV Mesa,bind scoped PS5 libc/thread providers,stage constructors for
resident JNI initialization,and package a real OpenGL acceptance app. No028
installer has been produced;027 remains a failed startup build and must not be
presented as the new candidate. PS5 context/JNI/readback/shutdown acceptance and
original Minecraft menu startup remain pending. No original game JAR,server
configuration,frozen milestone or runtime implementation was changed.


## Client028 resident acceptance candidate

028 now packages the genuine OpenGL JNI and private Mesa OSMesa implementation.
13,241 Mesa definitions,including TLS descriptors and internal C++ definitions,
are isolated from the existing RADV Mesa. Existing scoped graphics providers
supply libc/thread services. One real Mesa constructor is retained in an explicit
ordered linker range and invoked by resident JNI_OnLoad after the VM exists.
The automatic constructor table remains empty. The original game/runtime code
is unchanged;this fixture does not call Minecraft Main.

A fourth dependency patch uses `__thread` for the constant-initialized GL TLS
slots when the explicit PS5 Meson option is enabled. This matches upstream's
Apple declaration strategy and avoids Clang's optional C++ TLS-init thunk,which
our native conversion tool otherwise treats as an import. No fake initializer
or zero-call shim is linked. The platform still uses compiler-managed emulated
TLS. Prior component build records remain historical evidence,not028 validation.

The exact packaged ClientOpenGL25 bytecode passes the real host provider test.
Target checks verify original54JAR hashes,unchanged runtime libraries,image and
shared application identity,all real provider/JNI exports,private GLAPI symbols,
359JVM+4graphics+5shaderc+15OpenAL+1Mesa staged constructors,signatures and ZIP
CRC. Frozen026 and preceding validation packages are preserved. The local app
includes the original pinned Mesa source archive and all four dependency patches
so upstream per-file copyright/license notices are retained.

Build with tools/package_client_vulkan.py --opengl-bootstrap plus the existing
--runtime-workspace,--java-home and --offline arguments. Check with
 tools/test_client_opengl_package.py --runtime-workspace and run the same
fixture on host with tools/test_opengl_bootstrap_host.py --java-home. The new
build is PPSA99874 01.000.028;see client/opengl_bootstrap/status.json and
 docs/validation/client028-candidate-2026-10-25.json for its exact checksum.

Install028,open it and press X once. It runs five rows automatically;no game
window,visible RGB sequence or sound is expected. Wait for ALL5 PASS or the
failed-row notification and keep the app open for logs. Console context creation,
original JNI function-table dispatch,readback/guards and VM shutdown remain
pending until the actual PS5 result. Do not freeze a milestone or infer game
startup from host/package checks. A future public OpenAL-linked release still
requires matching corresponding-source/relink materials;028 is local development.


## Client028 failure and029 dispatch repair — 2026-10-25

Saved startup and VM reports identify028run
client-01.000.028-1792918591-814097997. VM creation,54artifact checks,graphics
constructors and the real retained Mesa initializer complete. Row4then reports
ClientOpenGL25 ExceptionInInitializerError (-1307);no readback or VM shutdown
pass follows. The session was observed in Safari;exceptions.log was unavailable.
The complete underlying PS5 exception chain was not captured. Raw reports stay
local;docs/validation/client028-failure-2026-10-25.json records these limits.

Local source inspection and a real-provider host regression identify a concrete
PS5 dispatch defect:GL.loadOSMesa passes both the configured name and eagerly
computed Configuration.OPENGL_OSMESA_LIBRARY_NAME_DEFAULTS to Library.loadNative.
The defaults method has no PS5 case and throws even when a provider name is
configured. Original GL catches it and ultimately reports no available context
management API. The normal Mac host test passed because that platform is
supported. The PS5-enum test fails with original GL and passes after the repair.
This supports the029fix;it does not independently establish that this was the
sole underlying PS5 failure.

029extends the separate dependency platform overlay with the original,pinned
LWJGL GL unit and a PS5-only loadOSMesa branch. It opens the actual configured
resident OSMesa library through the existing real PS5Library resolver,keeping
missing-provider errors real and avoiding desktop defaults. Native JNI loading,
GL capabilities/function calls,and desktop branches remain upstream. No game
classes or original game JARs change. The fixture now records nested exceptions
and stack frames before rethrowing the failure;diagnostic lines do not trigger
repeated notifications.

The actual029fixture passes three contexts/192RGBA pixels/768guards under normal
host dispatch and again under actual PS5 enum dispatch with real Mesa and native
JNI (six contexts/384pixels/1536guards total). An original-GL control without the
overlay fails the PS5 check as expected. The host-only enum selector uses Unsafe
and produces expected deprecation warnings;there are no JNI-check/UBSan failure
reports. It is excluded from the package. This is a loader/dispatch regression
check,not PS5 hardware validation.

029passes package integrity,signature,identity,54original JAR/runtime preservation,
9resident groups,GL overlay/diagnostic fixture checks,unchanged native constructor
counts and exact frozen026/failed028 package preservation. Failed028source,
package and symbols remain recoverable. See client/opengl_bootstrap/status.json
and docs/validation/client029-candidate-2026-10-25.json for the checksum. Install029,
press X once,and leave it open after its result for logs. ALL5on actual PS5,
full game startup and the deferred server endurance run remain pending.
