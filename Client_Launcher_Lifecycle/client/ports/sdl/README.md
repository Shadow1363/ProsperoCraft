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
