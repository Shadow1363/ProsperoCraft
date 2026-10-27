# Toolkit motion and backgrounds — candidate01.000.088

[Build/checksum record](validation/client088-motion-build-2026-10-27.json).

The user wants the existing ProsperoCraft layout with the visual polish of
PS5_VKHomebrewUI, including Aurora Shelf's motion.087 adopted the renderer but
retained too much of the flat presentation.088 adds the actual toolkit's
backgrounds, glass composition and animated collection/modal components while
preserving the four-column library, top bar, page layout and Java model.

[Native Vulkan motion preview](launcher/088/motion.webp) ·
[Library](launcher/088/home.png) · [All page states](launcher/088/contact-sheet.png) ·
[All ten backgrounds](launcher/088/backgrounds.png).
These are scripted host Vulkan readbacks using synthetic library/account text.
The motion clip uses a fixed24Hz clock; it is not a PS5 FPS measurement.

## What changed

- All ten pinned toolkit background modes are available: Gradient, Aurora,
  Grid, Stars, Waves, Bokeh, Phosphor, Paper, Dots and Vista. In **Settings,
  press Square** to cycle them. The selected name appears on the left panel.
  Selection persists with the existing library settings. Older libraries and
  invalid preference values default to Aurora. Instance UUIDs/worlds/cache and
  account records are unaffected.
- Background colours follow the selected icon through toolkit SpringColor
  interpolation. Background changes crossfade; the time-driven modes keep
  moving while the launcher is idle. Static modes retain their intended look.
- The Vulkan compositor now requests the toolkit's real blurred glass copy.
  Top bar, panels, controls and dialogs sample it with dark green tinting,
  hairlines, shadows and focus halos. Footer shading keeps hints readable.
- The instance library uses the actual GridView/Card implementation: staggered
  arrivals, spring-driven moving focus, card lift/growth, glow, shaded artwork
  and status badges. Its four-by-two page geometry and authoritative Java
  selection remain; no independent component mutates the model.
- Page content enters with a fade/rise. The real Dialog component handles the
  Delete confirmation's scale/rise, scrim, frosted panel and opening/closing
  motion. Java still decides Cancel-first selection, busy protection and
  deletion/undo. No worlds are deleted by presentation code.
- Settings switches and the welcome checkbox use toolkit Painter controls
  with animated saved values. Download progress uses the real ProgressBar,
  eased progress and a moving sheen. Actions keep their component press/focus
  response. Headings now load the upstream Montserrat display face.

Reduced Motion freezes backdrop time, snaps palette/preference changes, removes
card lift/scale and page travel, and settles controls immediately. The rendered
fixture checks repeated settled frames byte-for-byte, not just the flag value.
No toolkit music, mixer or audio backend is started. Gameplay audio is unchanged.

This applies the toolkit features that fit the launcher. It does not transplant
the sample app, gallery controls, fake products or unrelated sample animations.
The dependency revision remains2188642afbcc8d84d36149124f3d9e39dc1b1a05, with no
upstream source/shader patches. BlackBearReloaded's toolkit, Mihawk's Vulkan work
and font/third-party notices remain credited and packaged.

## Graphics and model boundaries

The087 private offscreen RADV device, native VideoOut presenter, one frame slot,
fence/readback ordering, attached-thread JNI mailbox, cleanup/join gate and
original-Main clean return plus LoadExec boundary are retained. Glass resources
belong to the toolkit renderer and are released before game handoff. There is
no competing SDL/WSI display owner or game-JAR/class transformation.

The native mailbox remains80 fields. Previously unused75/76 carry the validated
background number/name. Java adds only the additive saved background preference
and Settings-only Square action. Existing keyboard Square/Done, auth, downloads,
version guard, channel restrictions, verified Offline lease, Delete/Undo, locked
1080p, OSHI provider and original game data remain covered by regression checks.

## Checks and remaining console work

Host checks cover persisted background cycling/default migration/world retention,
all ten Vulkan backgrounds with glass, the180-frame motion tour, pixel-identical
Reduced Motion, unchanged centered labels, all launcher pages and the actual
native controller/JNI/display-join fixtures. Vulkan resource tests exercise
glass banks across repeated one-slot submissions/device cycles, partial startup
failure and timeout retention. Both target builds and complete package/source/
license/constructor/allocator/channel audits must pass before delivery.

Continuous motion requests redraws at about30Hz. The offscreen readback and tiled
upload remain, and blur adds GPU work. **Actual PS5 smoothness, memory headroom
and responsiveness are unmeasured.** Host lavapipe uses the real Vulkan backend
through the direct ICD, without Khronos validation layers. Neither the preview
clip nor compilation establishes console success.

On each exact088 channel: check cold startup, background cycling and persistence,
card/page/dialog transitions, readable focus, Reduced Motion, busy downloads and
cancellation. Then check Demo/Offline separation, Delete/Cancel/restart Undo,
preserved worlds/options, game handoff,1080p clicks, controls/audio/CPU debug text,
save/reload and at least three Quit/library/relaunch cycles. Retain087/086 as
reinstall fallbacks. No public release or ProsperoStore update is made.
