# Normal add card and PS5 banner — 01.000.096

The user requests the final artwork/card update before a later merge. This build
remains on Temp_gametest; it does not merge main, publish Store/release assets or
establish a console milestone. Preserve095 and all older exact candidates.

Empty Instances now uses the same grid renderer and420x242card layout as the
add card in a populated library. Its plus artwork, focus animation and position
match normal cards. The former1770x550empty-state panel is removed. Instances,
Settings and Account remain the only top-level pages; Home stays deferred.

The supplied prosperocraft-banner.png is retained byte-for-byte as
assets/branding/prosperocraft-banner-source.png. The separately supplied
prosperocraft_title.png was inspected; the user chose the banner alone and normal
system-rendered ProsperoCraft text. No title-logo image or composition is packaged.
The existing app icon stays active.

The banner is Lanczos center-fit to3840x2160RGB and encoded to BC7_UNORM DX10 DDS,
one2Dsurface without mipmaps. The same image ships as sce_sys/pic0.dds(selected-app
background) and pic1.dds(launch background). Asset sources, dimensions, exact hashes,
encoder revision and reproducible conversion instructions are in
assets/branding/presentation.json and its README. No AI redraw is used. Normal
packaging reads the committed DDS and does not require a host encoder.

apply_branding.py validates the image header, payload size and pinned hash before
copying both assets into an app. Its ZIP rewrite also inserts/replaces both
backgrounds without duplicate entries and preserves unrelated files. Package
audits compare both embedded DDS files byte-for-byte to the pinned source.

Host checks include real BC7 decoding at4K,48.83dBPSNR against the resized original,
application/ZIP insertion and idempotence, plain text title, existing icon and
unrelated-byte preservation. The native and actual Vulkan UI previews show the
normal empty add card; three-header pixel-centering and joined UI teardown/JNI
checks pass. Original Minecraft JARs, authentication/network settings and runtime
patch0123 are unchanged; hosting remains deferred.

Actual PS5 selected-title and launch banner display, visual framing, title text
and ordinary launcher/game lifecycle still need validation. The shell/loader can
cache old presentation files after an app update. Check current installed assets
and loader registration if old artwork remains; this change does not modify shell
catalog databases or cached metadata automatically.

Exact package/symbol hashes and tests are in the [096 validation record](validation/client096-presentation-build-2026-10-27.json).
