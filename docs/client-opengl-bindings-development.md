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
