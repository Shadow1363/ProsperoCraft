# Shared Demo / Offline fixes — candidate01.000.086

The user requests centered native top-bar labels and a real CPU description in
Minecraft's debug screen. Both are shared changes for `main`, `codex/demo` and
`codex/offline`. Existing channel selection, signed Offline profile, recoverable
instance deletion,1080p/input/audio and process-replacement lifecycle remain.
No new Store release or console pass is inferred from this request.

## Native top bar

Add Instance, Settings and Account previously used a fixed24pixel left inset and
fixed text Y within differently sized buttons. The new consumer UI helper measures
the actual Inter glyph ink bounds, including side bearings and descenders, and
centers each label horizontally and vertically in its existing rectangle.
Button positions, focus animation and controller hit targets are unchanged.

[Actual native host-rendered preview](launcher/086/centered-topbar.png).
The pixel check measures all three rendered labels across home, Settings and
Account states; their ink centers are within one pixel of their button centers.
This checks the rendered font, not just the positioning formula.

## CPU identity through OSHI

Inspection of the pinned, unmodified26.3game shows that
`DebugEntrySystemSpecs.getCpuInfo()` asks OSHI for a logical processor count and
processor identifier name. It catches any failure and leaves `<unknown>`.
The normal OSHI FreeBSD path relies on desktop JNA dispatch/sysctl facilities
that are not provided by this client. GPU text comes through the independent
RenderPearl device-info path, explaining why GPU identity can already work.

086adds a narrowly scoped **OSHI dependency port**, not a Minecraft class hook or
replacement. Pinned6.9.0upstream source and its MIT license are recorded in
`client/ports/oshi/sources.json`. A small source patch selects the PS5 hardware
provider before desktop JNA initialization. Other platforms keep their original
factory selection. The original downloaded OSHI/game JARs remain intact.

The consumer startup JNI callback reads actual x86 CPUID vendor, brand and CPU
signature/family/model/stepping, plus `hw.ncpu` when available. If the kernel count
cannot be read, the reported CPUID topology/count is used. A missing/invalid brand
falls back to the actual CPUID vendor/family/model values, never an invented
marketing name. Missing identity/count data is rejected instead of substituting
PS5 specs. No clock, temperature, load or physical-core measurement is fabricated.
The JVM's existing ActiveProcessorCount4worker policy is unchanged.

After a game is selected and verified, startup publishes this bounded snapshot
as `ps5.cpu.*` properties and enables the scoped OSHI provider. The startup log
records `PS5_CPU identity=READY` with count/source, or a bounded unavailable code.
No account data, serial number or credential is read or logged. Unsupported OSHI
telemetry methods explicitly throw rather than report fake zero readings.
GPU identity/reporting remains unchanged.

The bundled `oshi-6.9.0-ps5-platform.jar` precedes the selected26.3cache classpath.
It contains only OSHI dependency classes. The game's original debug entry still
formats the line through its original OSHI calls. A host fixture invokes that
actual game method and checks the original game's code source/JAR checksum;
valid input displays the supplied native identity, missing input remains unknown,
and the working PS5 provider path never initializes desktop JNA native dispatch.
This host result does not establish actual PS5CPUID output.

## Validation and install

Actual native decoding fixtures cover real field layout, kernel-count preference,
CPUID count fallback, invalid/missing brand and failed identity. Java tests check
the original game debug entry, honest unsupported metrics, unchanged desktop
selection and unmodified original game bytes. Existing instance/delete/undo,
Demo/Offline proof and rendering checks are retained. Both target packages and
complete package audits must pass before calling the local candidates ready.

Install the full chosen086folder, including the new platform JAR and license
sources, while retaining `/download0/ProsperoCraft`. Offline keeps the same public
verification key, so the existing unexpired personal record can be reused.
Demo stays demo-only and ignores that record. Both use the same title ID and
replace one another, as before. Separate ZIP/symbol outputs and candidate copies
are preserved for the two channels. Published083/082,084and085candidate bytes and
all frozen milestones remain unchanged.

On each exact086PS5build, check the three top-bar labels in their normal and focused
states, then launch and enable the debug system-specs display to check the CPU
name/count and unchanged GPU line. Check world/audio/controls, Delete/Undo and
Quit/library/relaunch. These physical console checks remain pending; no measured
CPU performance, new milestone or public086availability is claimed.
