# ProsperoCraft client042 — consistent supported SDL/display surface mode

041run client-01.000.041-1792936853-896206858 was observed RUN before the human
reported a crash and reopened. Saved original Minecraft exceptions.log shows
Vulkan/PS5 GPU and SDL window initialization,resource reload and the renderFrame
loop,repeatedly failing swapchain creation at3840x2160/FIFO. Previous4MiB native
allocation refusal is absent. VM trace ends in completed shader compilation;
no fatal signal/abort report was captured. The crash instruction and precise
internal driver rejection remain unresolved;render-loop progress is not a
visible menu or successful presentation.

The SDL port currently chooses advertised native4K/highest refresh and its
upstream Vulkan display helper independently chooses a native mode. This forces
4K despite the1280x720 original launch request. The driver actually enumerates
1080p,1440p and4K,so a720p scanout cannot be claimed.

042implements one shared enumerated mode policy for SDL display inventory and
its Vulkan surface:prefer actual1080p <=60Hz;fallback to another actual usable
mode when unavailable. No dimensions/refresh/handles are fabricated. Surface
creation uses the chosen mode handle and extent,queries supported displays and
plane alpha/transform/extent support,and preserves plane stack index. SDL logs
chosen display/surface resolution,refresh and queried surface capabilities.
This lowers the forced startup output and removes independent selection paths;
it is a compatibility retry,not a proven fix for the later native crash.

Original game JARs,JVM global allocation,256MiB heap,041's paired scoped LWJGL
allocator and other accepted native components remain unchanged. The approved
v3 icon is retained. Exact041package/symbols/status and frozen passes preserved.

Checks:

```sh
python3 tools/test_sdl_display_mode_host.py
python3 tools/test_sdl_loader_identity_host.py
python3 tools/test_client_startup_host.py --java-home /path/to/jdk25
python3 tools/package_client_vulkan.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline --startup
python3 tools/test_client_startup_package.py --runtime-workspace /path/to/PS5_Homebrew
```

The display host regression compiles the actual SDL surface hook and shared
policy under UBSan against explicitly synthetic Vulkan inventory callbacks:
4K/1080p and119.88/59.94 selection,fallback,bounds,plane/display/stack propagation,
alpha/incomplete enumeration rejection. It does not exercise a GPU. The separate
loader check uses real MoltenVK;allocation preflight uses real original LWJGL
JNI/host libc. Target packaging checks actual SDL source/header and object,
paired native allocators,all54original JARs/5147assets,exact runtime,retained
constructors,other accepted native components,branding and SELF integrity.

Install dist/client-startup/PPSA99874.zip or runtime dist/PPSA99874.zip,launch
and press X once. Observe the real screen/menu;report failure promptly. After a
crash,reopen without X for logs. Original Main returning is not a menu PASS.
PS5 selected1080p extent,presentation/swapchain/menu,crash resolution,memory and
performance/network/teardown remain pending. Server2H endurance stays deferred.

Host display-policy/loader/allocation/launch and full-package checks pass.
Full local ZIP SHA-256:`0bfa7f9d36b1882e36b9d53f79e4f025b197cf2ec1a022cc0aa8202c56a7c280`. PS5 validation pending.
