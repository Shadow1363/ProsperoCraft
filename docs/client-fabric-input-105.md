# Fabric launch recovery and input controls, development105

The user reports Fabric no longer launches on104 and requests issue3's mappable
keybinds and keyboard/mouse support. They also request two reply drafts in chat,
including issue1 and the fact they do not own a PSVR2. No issue/PR comment is posted.

## Fabric startup

Safari downloads identify open build104 and native run
`client-01.000.104-1793124119-372044561`. Fabric/Sodium/Mixin starts, then Java
output stops around graphics-card discovery before Minecraft rendering. The VM
trace is about36MiBand contains heavy repeated native allocation reports; the
JIT report continues compiling around340seconds. No new Java exception or JVM
fatal report establishes a crash cause. The downloaded session.txt still
identifies103, so it is stale and is not used to override the104 native header.
Downloaded gc.log likewise has an older timestamp and is not treated as104 proof.

104 disabled the global JAR URL resource cache to reduce retained descriptors.
105 restores normal cached JAR resource reads. Reopening archives for repeated
class/resource access is a plausible regression in this embedded runtime, but
PS5 causation and successful recovery are not yet confirmed. The actual host
Fabric/Knot/Mixin test reaches a fixture mod's preLaunch entrypoint with cached
reads, the intact original26.3game JAR and shared parent LWJGL providers.

The103 world-save `Too many open files` failure remains unresolved. This rollback
restores the retention tradeoff; it is not advertised as a descriptor/save fix.
Save/reload and descriptor headroom must be retested. The104 genuine ImageIO
raster/Disposer/LCMS subset,96MiBcode cache and concurrent explicit-GC changes
remain. No game/mod JAR is rewritten or deleted.

## Controller remapping

Settings -> Input & Controller Keybinds opens a paged list. Select a control,
choose a key or mouse button, then return. Preferences save to the existing
library and survive restarts; Restore Default resets them. Existing libraries
get defaults without moving worlds. Targets include letters, numbers,F1-F12,
Space/Enter/Escape/Tab/Backspace,modifier/arrows,slash,three mouse buttons and
Unbound. This permits assigning keys for mod screens, including Vitrail's I/R/K.

Mapping covers four left-stick directions,gameplay face/stick clicks,D-pad,
touchpad-layer shortcuts andL2/R2. Essential menu navigation,typing-overlay
controls,right-stick pointer/look and shoulder hotbar wheel behavior remain
fixed. Physical keyboard/mouse keybinds use Minecraft's own Controls screen.
Mappings feed standard SDL events/state; overlapping controls mapped to the same
key stay down until the last control releases. Modal/typing keys retain their
existing safety behavior. No Controlify compatibility is claimed.

## Physical keyboard and mouse

The optional native backend loads the known system modules libSceKeyboard and
libSceMouse and resolves their own init/open/read/close APIs. Missing modules or
hardware remain nonfatal and produce diagnostics. There is no arbitrary module
loader,downloaded native code or LAN input relay. It tries four device indexes
for the signed-in user; successful handles observe later connect/disconnect
reports. Keyboard/mouse adapters run in the SDL event pump after controller input
and independently of the controller/gamepad-mod handoff. Devices close at SDL
video shutdown. No physical input support in the native launcher is claimed.

Normal SDL scancodes preserve keys and modifiers. Text input currently translates
US ASCII only, including Shift/Caps Lock and common punctuation;international
layouts/IME are not implemented. Keyboard repeats occur for active text/editing,
not as repeated gameplay clicks. Mouse supports relative look,clamped menu
pointer,three main/two extra buttons and vertical/horizontal wheel. Buffered
short taps are retained. Focus loss,interception,disconnect/read failure release
held input;newly held inputs must release before activation. The in-game on-screen
keyboard remains unchanged, as does launcher QWERTY.

ABI research references public device-tested layouts in
[ZiZc3/Ruffle-Flash-PS5](https://github.com/ZiZc3/Ruffle-Flash-PS5/blob/1265f473e7479d6c0fcfb78cc160a0eea446bb08/src/hid.rs)
and its system-module lookup notes,commit1265f473e7479d6c0fcfb78cc160a0eea446bb08.
The local implementation and sanitizer tests live in client/ports/sdl and tools.
Matching ABI/documented device tests elsewhere do not establish a ProsperoCraft
PS5 hardware pass. Bluetooth is not separately validated.

## Tests and console checklist

Host tests exercise the actual native module-discovery/open/read/close code with
OS fixtures,including missing mouse APIs,and the actual SDL input adapter with
packet/event boundaries underASan/UBSan. They cover modifiers/text/caps,buffered
taps,relative/absolute motion,buttons,wheel,focus loss,rearm,interception,read
failure and owned device cleanup. Controller tests retain previous mappings,
add duplicate key and mouse-remap release checks. Actual Java model tests cover
migration,remap dropdown/save/reopen/reset/menu protection and hint serialization.
The real upstream Fabric bootstrap and vanilla/session/content regression checks
pass on host. Native and actual Vulkan toolkit previews show the new screen.
The target compiles and packages with current SDL native hashes;actual PS5 input
ABI,system-module loading and gameplay behavior remain pending.

Test exact105:
1. Launch the same Fabric instance with its existing mods;compare startup time.
2. Verify Vanilla still starts. Check stutters and world save/reload.
3. Change a controller key to I,confirm it reaches Minecraft/mod controls,then
   restart and verify persistence. Test reset and overlapping mapped keys.
4. Connect a keyboard/mouse before launch. In game,checkWASD,jump,keybind capture,
   menu typing,look,left/right clicks and wheel. Test disconnect/reconnect and
   leaving/resuming the system menu with a key held.
5. Retry Vitrail shader loading,audio,input and quit/relaunch. Leave app open for
   current-run diagnostics if it stalls or crashes.

Keep101/103/104 and all frozen snapshots. No public binary/Store release,new
milestone or ALLPASS is inferred. Keyboard/mouse support and startup recovery
are development candidates pending real console validation.

[104 launch observation](validation/client104-fabric-launch-observation-2026-10-27.json) ·
[105 build validation](validation/client105-fabric-input-build-2026-10-27.json).
Package SHA-256: `a4c51f25a4925f69acb2c8c0974c89a5c856c5a418f1e60645a76f3531409a75`.
