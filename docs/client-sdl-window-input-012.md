# Client SDL Window/Input 01.000.012

This candidate builds actual SDL3 release3.4.2 (683181b47cfabd293e3ea409f838915b8297a4fd)
as a resident library and uses the original LWJGL SDL3.4.3 Java JAR. The public
PS5 video/joystick backend originates in griches/PS5_Dusklight at
72d6885cc8b4ff4c5f6be23682ab11578ec926c4. Only its independently licensed SDL
backend and input platform code are used; no game, artwork, audio or Dawn is
included. Zlib/MIT attribution and source pins are retained in client/ports/sdl.

Consumer adaptations register the backend, use the statically resident Vulkan
ICD, query actual display dimensions and connect SDL Vulkan extension/surface/
presentation hooks to SDL's upstream VK_KHR_display helper. Rumble/LED are not
advertised in this input-only profile. The target uses SDL’s own wchar/string and locale fallbacks where SDK header
checks would otherwise assume missing libc exports. SDL dynamic API replacement, desktop
window backends, audio, process spawn and other unused features are disabled.
Original game/SDL/Vulkan Java JARs and JVM/SDK implementation remain unchanged.
SDL libc/thread references use the existing scoped graphics-provider map;
global JVM resolution is unchanged. No libffi callback support is claimed.

## PS5 run

Install **PPSA99874 01.000.012** from `dist/client-sdl/PPSA99874.zip`, also copied
to the runtime workspace's current `dist/PPSA99874.zip`. The app identity is shared
with prior clients/server: installation replaces it. Frozen000–004/008–011 remain
preserved; server two-hour endurance remains deferred.

1. Wait for **Client012 ready**. The initial screen can be blank; there is no CPU menu.
2. Release X, then press X once to start twelve checks automatically.
3. When the SDL pattern and input notification appear, release all controls and center the left stick.
4. After **Input ready**, press and briefly hold **X**, **Circle**, **D-pad Left**, then move the **left stick strongly**. The input deadline is two minutes.
5. Wait for **Client012 automatic checks PASS** and confirm the full-screen pattern remains afterward. Keep it open for reports. After a crash reopen without pressing X.

The final fixture requires event and polled-state evidence for all four controls,
from the selected real SDL gamepad. It creates a real fullscreen SDL Vulkan
window and surface, then uses the earlier graphics/swapchain workload with at
least90 frames,36 readback samples and256 guard bytes per frame. Frames continue
while waiting for controller input. The palette repeats every90 frames.

SDL/native window, gamepad and GPU display resources are intentionally retained
until app close, including through DestroyJavaVM. Teardown, SDL_Quit/window close,
resizing, reconnect/focus behavior, timeout recovery, callbacks, audio and game
startup are unvalidated. This is not a claim of complete SDL or Minecraft support.

## Host and build limits

`tools/test_sdl_host.py` uses real macOS SDL3 and the original Java bindings
(with only the host library digest resource paired to the actual host binary).
A small host-only C helper creates a genuine virtual joystick because the
Java virtual-descriptor path initializes currently unported libffi callbacks.
Java verifies gamepad button/axis state, SDL_Event ABI, event receipt, release
and cleanup with Xint/XcheckJNI/verification and native UBSan. This does not
exercise PS5 pad hardware, SDL PS5 window/surface hooks or display/input lifecycle.
The PS5 candidate uses real hardware polling and no virtual inputs.

```sh
python3 tools/package_client_vulkan.py --sdl --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25 --offline
python3 tools/test_sdl_host.py --runtime-workspace /path/to/PS5_Homebrew --java-home /path/to/jdk25
python3 tools/test_client_vulkan_package.py --sdl --runtime-workspace /path/to/PS5_Homebrew
```

The first SDL dependency build requires the pinned source in its ignored cache
or network access. Package/hash/check status is recorded in client/sdl/status.json.
All twelve PS5 checks and explicit visual/input acceptance are pending.
