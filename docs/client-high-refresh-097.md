# 120 Hz output candidate — 01.000.097

The user reports Minecraft remaining at60/61FPS with VSync disabled and a120FPS
target. Two consumer restrictions prevent the existing high-refresh path: the
startup manifest has attribute3=0, and SDL explicitly prefers modes<=60Hz.
The pinned Mesa VideoOut backend exposes only FIFO presentation, so the game's
VSync switch cannot select immediate/mailbox presentation on this port.

097 sets the existing VideoOut high-frame-rate declaration bit0x40 in the startup
manifest and chooses the fastest actual enumerated mode up to120Hz for the
requested resolution. The default remains1080p; requested resolution matching
and logical/physical input scaling retain their existing behavior. SDL display
reporting and surface creation share the same selection helper.

The pinned backend already checks OS output support, requests high-frame-rate
mode, measures six vblank intervals and offers119.88Hz only when that succeeds.
Unsupported/configuration-error/wait-error/still60Hz output retains or restores
the existing59.94Hz fallback. No mode is fabricated, no extra output is opened,
and neither the native WSI implementation nor game JARs are changed. This patch
does not implement true VSync-off immediate/mailbox presentation. Rendering120FPS
also depends on the game workload and Minecraft's separate maximum-framerate
setting. The launcher's own animation rate is independent of game presentation.

## Verification

- `python3 tools/test_sdl_display_mode_host.py`: actual SDL surface hook with
 119.88Hz selection,59.94Hz fallback,120Hz ceiling,unordered/invalid inventories
 and retained plane/alpha/extent checks under UBSan.
- `python3 tools/test_videoout_high_refresh_host.py`: actual generated private
 WSI manifest parser,open path and vblank measurement under ASan/UBSan; positive
 admission/handle retention and unsupported/error/slow-output/wait-error cases.
 Synthetic OS responses establish policy behavior only.
- `python3 tools/test_sdl_fixed_resolution.py`: logical/framebuffer coordinate
 regression under ASan/UBSan.
- Target build and package audits are recorded in the matching validation JSON.

## PS5 test still required

Install the complete097 folder, including its manifest; refresh loader metadata
if the installed manifest is cached. Use a120Hz-capable display/output configuration.
Set Minecraft's maximum framerate to120or higher, turn VSync off and compare the
same scene to096. Check the display's refresh readout and F3 FPS, then test controls,
audio, game Quit returning to the launcher and relaunch. Retrieve current-run
native stderr/SDL logs if it stays at60: selected119.88Hz versus59.94Hz separates
output negotiation from rendering performance. Do not infer that the user's
HDMI/display configuration is the cause before those reports are available.
A60Hz-only output should remain usable. No console120Hz/FPS pass is claimed.

096release/candidate and older frozen packages remain preserved. Development
continues on main with the existing temp_gametest channel; no public binary release
or Store update is requested. Home, hosting and extended endurance stay deferred.
