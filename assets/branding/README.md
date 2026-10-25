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
