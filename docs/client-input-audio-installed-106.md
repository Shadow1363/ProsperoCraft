# Development106: audio, input and installed content

105 starts Fabric again and renders BSL through Vitrail, but the human reports
physical keyboard/mouse failure and intermittent silence. Safari first records
AudioOut init0/open0x8026000d, followed by Minecraft disabling sounds. A later run
with Controlify has real PCM submissions; installing that mod is correlated with
the recovery, not a proven audio repair. Public [AudioOut error definitions](https://github.com/shadps4-emu/shadPS4/blob/main/src/core/libraries/audio/audioout_error.h) name
0x8026000d out-of-memory; these PS4 definitions do not prove the internal PS5 cause, which remains unmeasured.
See [105 observations](validation/client105-input-audio-observation-2026-10-27.json).

106 opens the real256frame/48kHz/stereoS16SYSTEM audio port before JVM heaps and
Vulkan allocation. OpenAL adopts it exactly once under its existing mutex and
uses its real mixer/output/drain/close lifecycle. If early reservation fails, the
existing bounded initialization/open recovery remains. No silent/null sink is
introduced. Host tests include adopting a pre-opened port when a late open fails
with the observed error; subsequent device opens can still fail and require PS5
reload/lifecycle testing. This is a candidate, not an audible console pass.

The HID backend now has real keyboard/mouse import declarations in the console
ELF, as the public device-tested reference uses. The generated Mouse import file
is a link-time declaration; no stub implementation or system library is shipped
in the app. Named module export lookup remains a fallback. Preloading and opening
all supported device indexes happens early inside captured logging. SDL claims
the prepared handles once. Device discovery, reads and close still use genuine
console APIs; USB/Bluetooth ABI, import resolution and game input require PS5
validation. Text supports US ASCII and optional missing icons/devices stay
nonfatal. The native launcher remains controller driven.

Controlify3.5.3 reports `no SDL3 in java.library.path`. The [Java repository update](https://github.com/mateo-cogeanu/ps5-java25-homebrew/commit/42fe3a5709beb65b5f54470aabb169a376ccbdc3)'s
explicit resident-library alias option maps SDL3 to the same ps5sdl symbol table,
JNI initializer and retained implementation already used by Minecraft. It adds
no desktop SDL download, platform spoof or game/mod class rewrite. The runtime
FFM system linker selects the existing x86-64SystemV path. Actual PS5 FFM calls,
controller discovery/configuration and Controlify gameplay remain unvalidated.
The temporary controller adapter now yields only after a mod actually opens a
PS5 gamepad, not merely after SDL subsystem initialization. If manager creation
fails, existing controller controls remain available.

Mods, shaders and resource packs now each have Installed/Browse views. Installed
reads the selected instance's actual folders, including manually added JAR/ZIP
files and dependencies, excluding symlinks. The human found their content and
retracted the disappearance report. No missing-file restore, deletion or new
content migration was implemented. Browse distinguishes installed items from
queued items. Selecting an installed item explains its state instead of queuing
another copy. Installed is a read-only inventory; disabling/removing/updating
mods is not added.

Selection boxes use the same toolkit checkbox as the startup notice. Search,
Installed and download-all retain spatial controller navigation. PNG project
icons are bounded, decoded in pure Java, cached per instance and shown in rows
and beside the active download. Every actual downloaded mod/dependency/shader/
resource pack sets its own current icon, even across mixed-category queues.
Missing, invalid, non-PNG or unsupported icons fall back to the Modrinth icon;
icon failures do not fail content downloads. HTTPS host restrictions and bounded
PNG dimensions/CRC/inflate lengths remain enforced. No AWT/game initialization
is introduced into the launcher to decode thumbnails.

## Shader performance

Human steady feedback is approximately60FPS moving/80still. Logs show BSL shadow
maps3072x3072 redrawn each frame, not a measured GPU bottleneck diagnosis. The
Shaders browser offers a reversible Shadows100%/50% button. It changes only
Vitrail's supported `vitrail/pack.txt` shadowmapscale setting for next launch,
with a first-edit backup. At50%, a3072map becomes1536on each axis, one quarter
of its pixels, with reduced shadow detail. Pack selection, enabled state, main
render scale, distance and other settings are preserved. Full shadows restore100.
Default quality is unchanged until selected. No120FPS shader promise or measured
performance improvement is made. Compare the same scene after compilation.

## Console checks

Install exact106 then check audio with and without Controlify, sound after
resource reload and quit/relaunch;physical keyboard typing/WASD and mouse
look/click/wheel/reconnect;Controlify controller discovery/configuration and
mapping without double input;temporary controls if Controlify fails;Installed
across all three categories and restart;checkboxes/icons/mixed queue downloads;
Shaders shadow-scale toggle with the same BSL scene. Save/reload and103EMFILE
remain pending. Preserve101release and103/104/105/frozen packages. Store/public
binary release stays unchanged. Development source is published to both repos
under their ownership rules.

[106 build validation](validation/client106-input-audio-content-build-2026-10-27.json).
Package SHA-256: `4c99efb9ebce399a1f262577bc77a17aa95f57d43bfe55fb31497b57a9703a60`.
