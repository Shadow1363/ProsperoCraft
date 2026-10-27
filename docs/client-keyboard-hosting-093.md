# Keyboard, launcher navigation and hosting diagnostics — 01.000.093

Temp_gametest development candidate, PPSA99874; no Store or release publication.
Same app identity,4GiB storage request, saved accounts/worlds/cache paths retained.
092 and older candidates remain preserved. Original downloaded game JARs are
unchanged. No ALL PASS or frozen milestone is inferred.

## Console evidence from092

The user confirms Minecraft starts and can join servers, but hosting still fails.
Cyberduck retrieved current/previous Java exception reports after a browser
refresh. Current-run saved-account restoration now completes TOKEN, Xbox, XSTS,
Minecraft login, entitlement and profile successfully. Socket preflight passes
TCP_LISTEN and UDP_BIND. These are scoped observations, not a full multiplayer,
LAN, account lifecycle or endurance pass. Raw reports remain local.

Inspection of original26.3 bytecode shows IntegratedServer.publishServer catches
IOException and returns false without logging it. Its path includes Netty listener
bind and the original LanServerPinger socket. Available logs do not identify the
hosting failure. Runtime patch0123 adds optional bounded native socket error
categories/class-method frames, enabled by the launcher, without game hooks or
changes to networking semantics. It is diagnosis, not a hosting fix. Reproduce
Open to LAN on093 and retrieve its current-run `PS5_HOST_IO` events. Absence of
events does not prove success; failures outside the traced operations may need
further investigation. Joining behavior is retained.

## Launcher

Signed-out account tab reads **Sign in**. A supported instance's signed-out action
reads **PLAY - Sign in** and starts the normal owning-account device flow. Pending
versions retain Coming soon. Signed-in tabs show the name and head. L1/R1 selects
Settings/Account and opens their content; selecting Add instance returns to the
library and requires X before opening creation. Down enters focused content.

Footer controls use font-independent controller shapes and button caps. Instance
count/page text and the visible TEMP GAMETEST label are removed, with Triangle
Undo given clear space. Channel identity and the personal legacy sign-in
restriction remain documented and packaged; the welcome screen uses ordinary
library/sign-in instructions. This does not authorize a Store/public binary
release or change the authentication/entitlement rules.

PLAY displays a two-column control guide during download verification and launch
preparation. OK waits for preparation to finish before handing the display to
Minecraft. Don't show again is persisted independently of the welcome preference;
OPTIONS still opens the guide in the launcher. This is before original Main's
loading screen, not an overlay rendered concurrently over Minecraft startup.
Cancel keeps verified downloads. The native frontend closes/joins before Main.

## In-game text keyboard

In Minecraft menus, press **L3** (or touchpad+R3) to open a visible50character grid
and6action keys. Choose using D-pad/left stick, X types, L1/Triangle deletes,
R1/Square inserts a space, R2 changes case, L2 switches symbols, Options sends
Enter and closes, Circle closes. L3 remains sprint in captured gameplay. D-pad
repeat is bounded; confirmation is edge-triggered. IP addresses, ports, names and
punctuation are available without cycling one letter at a time.

The preview contains text typed during this keyboard session, not the existing
contents of Minecraft's selected field. Text is sent directly through normal SDL
text events. Close does not undo text already entered. The user must first focus
a game text field. Input releases on focus/disconnect/gamepad-mod handoff remain.

The overlay draws into the existing tiled VideoOut buffer after its GPU fence
succeeds and before its owned flip, under the output lock. It allocates no second
display/swapchain. Only touched tile cache lines are flushed. Console checks must
still establish flicker-free updates/closing, input focus, mouse alignment and
acceptable frame cost across selected resolutions. Host raster and input tests
do not establish those GPU/console results.

Validation and exact checksums: [093 record](validation/client093-keyboard-hosting-build-2026-10-27.json).
