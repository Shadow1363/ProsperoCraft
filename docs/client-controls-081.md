# Controller and launcher candidate 01.000.081

081 expands the temporary controller adapter, adds an SDL menu pointer and text
picker, and polishes the launcher. It remains a development candidate awaiting
PS5 checks. Controlify integration is still on the roadmap. The official game
JARs and assets are unmodified.

[Build record](validation/client081-controls-build-2026-10-26.json) · [Notice preview](launcher/081/intro.png) · [Controller guide preview](launcher/081/controls.png)

## Launcher

The library heading is **Instances**, with the old subtitle removed. The full
**01.000.081** version appears at bottom right. Routine startup checkpoints no
longer produce system notifications; diagnostic files and fatal alerts remain.

A startup notice explains application-ID review, demo availability and the full
roadmap. Select **OK** with X to continue. The **Show next time** switch is saved
in the existing library settings and can be restored through Settings → Startup
notice. It defaults on, including for libraries created before081.

Only exact **26.3** is currently allowed to launch, with an SDL receipt required.
Other versions can download, but show **NOT YET** in the grid and **LAUNCH NOT
AVAILABLE YET** in detail. Play stays in the launcher and explains the restriction.
This conservative guard includes unvalidated snapshots and future versions;
sharing Java25 does not establish native-library compatibility.

Press **Options** in the launcher to read the controller guide; Circle returns.

## Gameplay layout

These mappings use vanilla default key bindings. Existing custom key bindings
are preserved; changing them can change the corresponding controller actions.

| Controller | Action |
| --- | --- |
| Left stick / right stick | Move / look |
| X | Jump; double tap for creative flight |
| Circle held | Sneak / descend in creative flight |
| L3 held | Sprint |
| Triangle | Inventory / close inventory |
| R2 / L2 | Attack or mine / use or place |
| L1 / R1 | Previous / next hotbar slot |
| Square | Swap main and offhand |
| R3 | Cycle camera perspective |
| D-pad down | Drop one item |
| D-pad up | Player list |
| D-pad left / right | Hotbar slot1 / slot9 |
| Options | Pause / back |
| Hold touchpad + R3 | Pick block |
| Hold touchpad + left / right | Toggle HUD / screenshot |
| Hold touchpad + up / down | Debug display / advancements |
| Hold touchpad + Triangle / Square | Chat / command key (demo launch still disables chat) |
| Hold touchpad + X / Circle | Enter / backspace |
| Hold touchpad + Options | Fullscreen key |

The touchpad **click** is a modifier. Touch-surface pointer tracking is not
implemented in this candidate.

## Menus and inventory

Right stick moves a visible pointer. **X or R2** holds the left mouse button;
**L2** holds the right button; **R3** is middle click. Holding the button while
moving the stick supports dragging. Hold **Square** while clicking for Shift
quick move. **L1/R1** scroll, **Circle** goes back, and D-pad/left stick also
provide keyboard navigation. Triangle sends the inventory key.

Click **touchpad + R3** in a menu to toggle the compact text picker. A glyph at
the pointer shows the selected character; an underline indicates lowercase.

| Text picker | Action |
| --- | --- |
| D-pad left/right or L1/R1 | Previous/next character |
| D-pad up/down | Move eight characters |
| X | Type selected character |
| Square | Space |
| Triangle | Backspace |
| R2 | Toggle letter case |
| Options | Enter and close picker |
| Circle | Close picker |

Click the text field before opening the picker. This is a compact Latin ASCII
picker, not a system keyboard, clipboard, Unicode input or a complete future
Controlify replacement. Some mod-specific shortcuts and arbitrary key chords
remain outside this temporary layout.

## Implementation and validation boundaries

The adapter supplies ordinary SDL keyboard/mouse/text events and state. It
releases held inputs when capture mode changes, focus is lost, the controller
disconnects or system input is intercepted, and suppresses launch-held buttons.
It hands off if SDL gamepads are initialized by a mod. Stick time steps remain
bounded after a stall. No game bytecode hooks or replacement classes are added.

The pointer uses the existing WSI-owned VideoOut handle and a retained64KiB
allocation, two64x64 ARGB images and OS cursor composition. It does not copy or
modify game framebuffers or open a second output. Character images change only
when the selected glyph changes. The cursor ABI was checked against the primary
[prospero-win implementation](https://github.com/mpereiraesaa/prospero-win/blob/main/wine/ps5/pw_vulkan_radv.c);
this is API-reference research, not a runtime dependency.

Host ASan/UBSan fixtures execute the actual input adapter and cursor patch;
OS/SDL boundaries remain simulated. Native UI previews exercise the actual draw
code, frontend-before-JVM, silent ready message and ordered display cleanup.
Java tests cover notice persistence, an old library's default, unsupported launch
rejection and supported original26.3demo arguments. Target builds and package
checks do not establish physical controller behavior or cursor-plane support.

On PS5, check pointer visibility/alignment at the chosen resolution, inventory
click/drag/right click/quick move, hotbar cycling, sprint/sneak, text-field entry,
pause/back, focus/disconnect recovery and retained sound/smoothness. Confirm the
notice switch survives relaunch and pending versions cannot leave the launcher.
Continue the080download-completion check; the user's downloading report alone
is not a completed download, gameplay or formal ALL PASS result.

Install the complete081folder, including param.json. The4096MiB request and
`/download0/ProsperoCraft` path remain. Keep existing instance/cache/world data.
The exact080package is preserved locally as a fallback. No release or Store
publication is created by this candidate.
