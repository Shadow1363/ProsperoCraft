# ProsperoCraft client039 — shared SDL/LWJGL Vulkan loader

038was not still loading:the live PS5 session reported FAIL/codeFFFFFAE5. Full
saved console/native startup identify VulkanBackend rejecting different
vkGetInstanceProcAddr addresses. SDL returned raw vk_icdGetInstanceProcAddr while
LWJGL resolved the consumer's public vkGetInstanceProcAddr wrapper. The original
game explicitly compares the two pointers. It then tried OpenGL,which this SDL
PS5 video driver does not expose,and could not display its error dialog because
no SDL message system is implemented. Original Main returned;the harness
correctly reports that as failure. This is not evidence of a system-wide hang.

256MiB heap reservation/VM startup worked in038;GC diagnostics progressed to
124.349seconds with247MiB committed/130MiB used after the last logged collection.
No heap OOM is captured. Full game memory adequacy remains unvalidated. Network
service warnings are present but are separate from the recorded Vulkan rejection.
The small session/exception reports were read through Safari UI;complete console
and startup files are saved locally and hashed in the public failure record.

039changes only the development SDL PS5 port to use the same public resident
Vulkan entry as LWJGL for loader address,extension/display/surface queries. That
entry delegates every call to the real static ICD;no fake Vulkan functions or
game-check bypass is added. Original Minecraft's pointer comparison is unchanged.
The256MiB heap,all other native components and game JARs remain intact. The
consumer SDL object changes;frozen passing SDL/native milestones stay untouched.
ProsperoCraft title and user-provided512RGBA icon are applied to this candidate,
with unchanged PPSA99874/content identity and independent version01.000.039.

Host regression check:

```sh
python3 tools/test_sdl_loader_identity_host.py
```

It compiles the exact development PS5_Vulkan_LoadLibrary body with minimal host
SDL data/error declarations and the exact public loader wrapper with host symbol
adaptation. Real MoltenVK supplies the underlying driver calls. It checks pointer
identity,extension enumeration,instance/physical-device lookup/destruction and
explicit-path rejection under UBSan. A negative control returning the raw actual
host driver pointer reproduces038's mismatch. This isolates loader identity;
it does not establish the full PS5 SDL video/event/surface stack or game rendering.

Build/test:

```sh
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

Package checks verify ProsperoCraft name/icon,all54original JARs/5147assets,
exact runtime image/native libraries,13real resident groups,retained constructors,
signatures,accepted GL/STB/FreeType/VMA/SPIRV-Cross inputs and corrected SDL source
identity. Old archived failure packages are verified by streaming their compact
archive;they are not expanded unnecessarily. Exact failed038package/symbols and
all prior frozen milestones are preserved.

Install local dist/client-startup/PPSA99874.zip or runtime dist/PPSA99874.zip.
Launch and press X once. Observe whether a real Minecraft window/menu appears.
If black or failed,report promptly;the last run's initialization stopped around
two minutes,so do not wait30minutes. Keep the app open for reports,or reopen
without pressing X after closing. The four harness rows/Main return do not imply
menu success. Original offline demo/Vulkan/1280x720 arguments/options remain.

Actual PS5 corrected-pointer/native renderer/window/menu/gameplay,broader Vulkan
feature support,network services,game heap adequacy/performance/global teardown
and server two-hour endurance remain unvalidated;endurance remains deferred.

Host loader regression/launch policy and full-package checks pass. Full local
ZIP SHA-256:`a034ae37f7d5c40026f0c7163b812aaeda6fb7811936b516ed1bd87baaad13a6`.
PS5 corrected-loader/renderer/window/menu validation remains pending.
