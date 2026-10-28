# SDL3 public PS5 dependency port

SDL3 release3.4.2 source is pinned in sources.json. PS5 video/joystick and input
platform code derive from griches/PS5_Dusklight at the recorded commit, under
Zlib/MIT. Original author notices and license texts are preserved. Altered files
are marked: video gains resident-ICD Vulkan hooks/actual mode query; joystick
removes unvalidated rumble/LED claims; platform-input.c extracts controller-only
support. No game/artwork/audio code is used. The SDL registration/filesystem/
static-dynapi/process-build changes are an explicit dependency patch.

Build with tools/build_sdl_native.py. The generated source/cache/build outputs
remain ignored. SDL is statically resident; no arbitrary ELF loading or desktop
window provider is claimed. Java SDL/Vulkan and game JARs remain original.

Development112 adds native joystick gyro and a primary DualSense actuator-only
SDL audio endpoint for Controlify. The four-channel logical stream sends only
channels2/3 to the actual type10 stereo haptic port. Main game speaker audio
remains OpenAL. One silent actuator output is reserved before the JVM and retained
across logical audio reloads. Capabilities require successful native probes.
Hardware motion values/axis signs,HD haptic feel,hotplug and simultaneous sound
remain pending PS5 checks. Standalone SDL sensors,standard rumble,adaptive
triggers and LEDs remain unsupported;controller identity alone is not acceptance.

Development113 adds native compatible two-motor rumble after a successful zero-output capability probe. SDL owns duration/stop timing. HD audio selects advanced mode only for actual nonzero actuator samples, sharing mode state with compatible rumble. LED/adaptive triggers remain unsupported. Physical effects and mode arbitration require PS5 validation.
