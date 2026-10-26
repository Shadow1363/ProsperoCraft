# Client063 — temporary controls and idle menu policy

The user confirmed the Minecraft menu on 062, then reported no button controls
and a menu that starts normally and becomes laggier. 063 is a development candidate
for those two issues. The accepted 062 release and its exact bytes remain preserved.

## Temporary controls

Vanilla Minecraft processes keyboard/mouse events. The existing PS5 port exposed
joystick/gamepad input, but its video event pump was empty. The new adapter reads
player 0's buffered DualSense samples and calls SDL's normal internal event/state
functions; it never patches Minecraft classes or calls game methods.

| Control | Menu action | When the game captures the mouse |
| --- | --- | --- |
| D-pad | Arrow keys / navigation | Arrow keys |
| Left stick | Arrow keys / navigation | WASD movement |
| X | Enter / select | Space / jump |
| Circle | Escape / back | Escape / pause |
| Triangle | Tab / focus navigation | E / inventory |
| Square | Backspace | Backspace |
| R2 / L2 | Left / right mouse button | Left / right mouse button |
| Right stick | No pointer movement | Relative mouse look |

These are temporary keyboard-like mappings, not a completed controller UX.
Use D-pad/Tab focus navigation in menus; a visible virtual pointer, text-entry
keyboard, full inventory management, rebinding, hotbar controls, rumble and gyro
are not supplied. Captured-mode mappings exist but world gameplay remains untested.

The bridge consumes buffered button edges, suppresses buttons/triggers still held
from launch, repeats navigation keys without repeating confirmation, releases
held inputs on disconnect/system interception/focus loss, and caps look movement
after a long frame. It generates no idle keepalive events. Pad initialization is
idempotent so the existing raw joystick driver shares the same handles.

Only the startup harness opts in with the SDL hint `PS5_TEMPORARY_CONTROLS=1`.
`-Dps5.temporaryControls=0` disables that opt-in. Initializing SDL's gamepad subsystem
also disables the bridge and releases its inputs. A future controller mod must
explicitly disable it too, rather than producing duplicate mappings.

## Gradual menu slowdown

Retained 062 samples frequently put the render thread in the original frame limiter.
Read-only inspection of the original game shows that the default `AFK` policy
reduces the limit to 30 FPS after one minute without input and 10 FPS after ten
minutes. Without a working input path, real controller activity never resets it.
This is a source-informed likely contributor; the exact applied throttle reason
and before/after FPS were not directly measured.

063 sets the supported vanilla option:

```text
inactivityFpsLimit:"minimized"
```

That preserves minimized-window throttling and removes the AFK timers. It does
not remove vanilla's 60 FPS out-of-level menu limit. An existing options file is
backed up once as `/download0/mc-client/options.before-menu063.txt`; only this
setting changes. Other option bytes and existing audio settings are preserved.
New profiles get the setting directly. The actual original Minecraft enum codec
accepts the JSON string `"minimized"` in host testing.

There is also a separate measured source of stutter: late full SerialGC pauses
of roughly 286–403 ms, approximately every 16.3 seconds in the retained logs.
The post-full-GC live size is roughly 172 MiB. This does not establish a memory
leak. The 256 MiB heap, SerialGC, interpreter, SDK, renderer and diagnostic logging
remain unchanged in this candidate. This fix makes no general FPS guarantee.

[Hashed console observations](validation/client062-menu-analysis-2026-10-26.json).
Raw logs remain local.

## Controlify later

The user prefers [upstream Controlify](https://github.com/isXander/Controlify).
Its [official documentation](https://controlify.isxander.dev/) describes SDL3 input
and Fabric/NeoForge support. Select exact game/loader/mod/dependency versions when
the modded client is ready. Desktop compatibility does not establish PS5 support:
native loading, SDL ABI/API coverage, initialization ownership, input release and
optional hardware features still need validation. No loader or Controlify JAR is
installed in 063. The raw SDL gamepad path remains available for that future work.

## Checks and console acceptance

Host ASan/UBSan exercises the actual adapter with deterministic SDL/OS boundary
fixtures: enable/disable, launch-held suppression, buffered tap, repeats, captured
mapping, trigger/look limits, interception/disconnect/focus release and mod handoff.
Actual platform adapter tests cover shared initialization and read/release state.
The original game codec and actual startup options migration are tested separately.
Host fixtures are not PS5 controller acceptance.

On PS5, install 063 and press X once. Release X during loading. Navigate Options
with D-pad or left stick, select with X, return with Circle, and test Triangle/Tab.
Leave the menu idle for at least two to three minutes and compare its animation
with the initial menu. Check that navigation becomes responsive immediately after
idle and that held keys release when the system takes focus. Note any remaining
periodic hitch, crash or stuck input. World play, audio, saves and stability remain
separate pending tests. No new GitHub release or Store submission is made here.

## Checked candidate

PPSA99874, version **01.000.063**. Native compile/link/SELF and full package checks
passed, including all 54 original JARs, 5,147 assets and accepted062 preservation.
Full local ZIP SHA-256:

```text
a1c62a8a6ccc8554c77ea3166633545fd08da6ca2b8e1ebffaf0c843677545f0
```

[Build/check record](validation/client063-build-2026-10-26.json). Console acceptance
for063 remains pending.
