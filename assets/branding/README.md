# ProsperoCraft artwork

The user selected ProsperoCraft and supplied ProsperoCraft.png from Downloads
on2026-10-25. ProsperoCraft-original.png preserves those360x360PNG bytes.
The initial icon0.png was a512x512RGBA nearest-neighbour resize of that artwork.
The active icon was subsequently updated to the selected v3 source below;
branding.json records current source and packaged-icon checksums.
The supplied artwork is used under the user's explicit project publication
instruction;no new third-party asset license is asserted here.

Future development client/server packaging applies this name/icon while retaining
PPSA99874,content identity and each build's version. Frozen snapshots/releases
and already-built038 are unchanged;the next build will carry the branding.

## Standalone icon source v2

On2026-10-25 the user selected the generated concept sheet's small app tile and
requested a standalone source file for direct use. ProsperoCraft-icon-v2-source.png
is the original high-resolution square raster master from the built-in image_gen
tool. icon-v2-source.json records actual dimensions,checksum,provenance and exact
prompt. This is a flattened PNG rather than layered/vector artwork. A matching
copy was delivered to Downloads as ProsperoCraft-icon-source.png. The existing
icon0.png and compiled packages have not been replaced;future integration can
use this source while preserving frozen milestones.

## Outline correction v3

ProsperoCraft-icon-v3-source.png is the user-requested correction to v2:
continuous dark-green pixel outlines follow both letters,including the P hole.
The built-in image_gen edit and visual inspection are recorded in
icon-v3-source.json with exact prompt,dimensions and checksum. Original v2 is
preserved. Delivered in Downloads as ProsperoCraft-icon-outline-fixed.png.
Packaging icon0.png and compiled/frozen packages remain unchanged.

## Active artwork for the next build

The user approved v3 on2026-10-25 and requested it in the next build. icon0.png
now derives from ProsperoCraft-icon-v3-source.png as512x512RGBA with Lanczos
resampling for packaging. The high-resolution master and earlier source versions
are preserved. Both client and server packaging already use branding.json via
tools/apply_branding.py. No existing040/frozen/release package was rebuilt.

## Selected-app and launch banner —096

The user supplied prosperocraft-banner.png and chose the banner alone with the
system-rendered ProsperoCraft title. prosperocraft-banner-source.png preserves
those exact PNG bytes. The separately supplied title PNG remains in Documents;
it is not copied into the package or composited. Existing icon0.png is unchanged.

presentation.json pins the source, output and host encoder. The image is center-fit
with Lanczos to3840x2160RGB, then encoded as one BC7_UNORM DX10 DDS surface without
mipmaps. apply_branding.py installs the same DDS as sce_sys/pic0.dds(selection) and
pic1.dds(launch), including when branding an existing ZIP. A PNG renamed to DDS is
not used. The user's Minecraft-themed artwork retains its original rights; the
project's GPL grant does not relicense Minecraft artwork or trademarks.

Reproduction uses Python/Pillow11.3.0 and the portable C++ encoder from
https://github.com/richgel999/bc7enc_rdo at
b9438627eef73a1157e84201b6fa6eb2ffd6d9f0 (MIT/Unlicense options; upstream
LICENSE and LodePNG notices apply to the converter). The encoder is a host tool,
not linked into the app. Clone/check out that exact revision under an ignored
dependency directory. Build with clang++ -std=c++11 -O2 -fno-strict-aliasing using
bc7enc.cpp,bc7decomp.cpp,bc7decomp_ref.cpp,lodepng.cpp,test.cpp,rgbcx.cpp,utils.cpp,
ert.cpp,rdo_bc_encoder.cpp. Run tools/prepare_presentation_assets.py with --banner,
--bc7enc and --encoder-source paths. The committed DDS means ordinary app packaging
does not need to build or run the converter. Changes to either source or encoder
must update the asset pins and decoded-image/packaging checks.

PS5 display remains pending. The shell/loader can retain older presentation files
after an app update; verify the selected-title background on the actual console.
Do not modify shell catalog databases to imitate retail title-logo metadata.
