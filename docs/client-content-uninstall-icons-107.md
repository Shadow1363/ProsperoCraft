# Development107: uninstall and actual project icons

Installed now offers an Uninstall button beside each file in Mods, Shaders and
Resource packs. Move right from a file to its button, press Cross, then choose
Cancel or Uninstall. Cancel has initial focus. The dialog identifies the exact
file and explains that other mods can depend on it. The action removes only
that selected file from that instance, updates its installed receipt and
refreshes the list. Worlds, configuration, other content and shared game files
are preserved. Dependencies are not automatically removed.

The file is moved to private uninstall staging before receipt publication. If
metadata cannot commit, it is moved back. After the receipt commits, its bytes
are reclaimed. A cleanup error can leave staged bytes outside the game's
content folders and is reported as storage cleanup pending. This is not an Undo
feature or crash-recovery guarantee. Unmanaged JAR/ZIP files can also be removed.
Symlink targets, traversal paths and unavailable files are refused. No real
console files were removed during development; tests use isolated host fixtures.

106 used a small pure-Java8bitPNG thumbnail decoder. Live Modrinth metadata shows
Sodium and Vitrail serving WebP and Fabric API serving4bitindexedPNG, so they
fell back to the Modrinth logo.107 adds a bounded consumer-specific native image
library with pinned[libwebp1.6.0](https://github.com/webmproject/libwebp/tree/4fa21912338357f89e4fd51cf2368325b59e9bd9)
and the existing pinned upstream STB header. It decodes PNG, including indexed
formats, JPEG and WebP for launcher project thumbnails. The[WebP decoding API](https://developers.google.com/speed/webp/docs/api)
checks dimensions before pixel allocation. Input is capped at1MiBand dimensions
at1024peraxis. Thumbnails now contain32x32pixels and render72pixels wide in four larger rows
per page, replacing the small44pixel icons and six cramped rows. Only dedicated
image slots have larger native buffers; ordinary UI text remains bounded. Transparent pixels are composited onto the launcher background.

The JNI library is a new resident consumer group,ps5contentimages,with no
constructors. It uses existing scoped graphics allocation and emulated TLS,
including STB's failure-reason TLS, without changing the JVM or original LWJGL
STB group. It does not initialize Minecraft,SDL,AWT or ImageIO. This is not an
ImageIO JPEG implementation or a complete desktop image API. Reusable Java
runtime source is unchanged from42fe3a5. Genuine title startup/native-library
lookup/codec behavior still needs PS5 validation. Upstream licenses are included.

Project thumbnails remain instance-cached and are used in Browse,Installed,
confirmation and current-download displays for mods,shaders and resource packs.
Unavailable/invalid/unknown artwork uses a neutral placeholder,notModrinth's
logo. Manually added content without a known project has no remote project
artwork lookup. No downloaded icon images are published with source or packages.

Host tests run the actual JNI codec with real Sodium/VitrailWebP,Fabric4bitPNG,
RGBPNG,alphaPNG and JPEG,comparing every thumbnail pixel against a reference.
They check truncated/oversized input and the Modrinth decode/cache pipeline.
UI tests exercise right-button navigation,Cancel,confirmed removal,receipt
cleanup,selected category only,world/other-file preservation,unsafe-path/symlink
rejection and exact-file rollback on receipt-write failure. Native and actual
Vulkan toolkit previews render real project icons and the uninstall confirmation.
Target packaging checks verify the real decoder/JNI symbols,source/audit/license
files and preserved core/older package identities.

Test exact107 on PS5:real icons in all three content categories and during a
mixed download queue;Installed and right-side Uninstall buttons;Cancel;uninstall
a disposable mod/pack and confirm it stays absent after restart while worlds,
settings and other files remain. Check106audio/HID/Controlify and shader-quality
comparison separately;those remain unconfirmed. Preserve101Store/publicrelease,
106candidate and frozen snapshots. No Store/public binary release is made.

[107 build validation](validation/client107-uninstall-large-icons-build-2026-10-27.json).
Package SHA-256: `2d046a985b2cabc4e79af3599dc100038130600d1cb20a91644e2c26c6c44086`.
