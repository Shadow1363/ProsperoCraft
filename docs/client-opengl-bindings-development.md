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

A real available PS5 provider/context integration remains necessary. Existing
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
