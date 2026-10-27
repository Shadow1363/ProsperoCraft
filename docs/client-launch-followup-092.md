# Launch follow-up, wording and Waves — 01.000.092

Temp_gametest development only. User reports091crashes after choosing PLAY FULL
GAME and requests PLAY, Coming soon labels and Waves as the default background.
No new Store/release or passing milestone is authorized or inferred.
Preserve091and earlier candidates with their exact symbols.

## UI changes

Unimplemented versions say Coming soon in the version selector, instance grid,
detail action and explanatory messages. They remain downloadable but launch-blocked;
only26.3SDLcan launch. The authenticated ready action is PLAY. Existing Demo
behavior remains isolated. Waves(mode5) is the new, absent/invalid and pre-model
native fallback. A one-time backgroundDefaultsRevision migration sets Waves for
existing libraries too, preserving instances/worlds/account data and every later
explicit background choice. Nothing changes the available ten backgrounds.

## Retrieved console evidence

Direct FTP and log HTTP requests from the tool process failed with No route to
host. At the user's direction, Cyberduck computer use connected to the PS5.
The first browser listing was stale; refresh showed the current files under
/mnt/sandbox/download/PPSA99874. Some transfers returned FTP550Permission denied,
but the current/previous Java exceptions, previous native stderr and startup log
were successfully downloaded. The first retrieval was preserved before collecting
the next run after the user reopened the launcher. Raw reports remain local.

The recorded091launch completed the legacy device flow, Xbox/XSTS, Minecraft
login, entitlement and profile checks. It closed the launcher display/GPU,
passed TCP_LISTEN/UDP_BIND preflight and JIT warmup, and entered original Main.
It reached the original Vulkan backend selection after SDLdisplay inventory.
The previous exception log stops there; native stderr confirms launcher handoff
and driver initialization. No fault PC/backtrace was obtained. OSHI unsupported
metric/storage warnings are caught by original SystemReport and are not established
as the cause of the native launch failure. The socket probe completed, so092
retains it rather than treating it as the crash cause.

The reopened091run logs TOKEN HTTP400invalid_scope during account restoration.
092explicitly supplies the same legacy Xbox MBI_SSL service scope on refresh
requests. The mock transport regression requires it and verifies the normal
ownership/profile pipeline still follows refresh. A dummy invalid-refresh network
probe returned invalid_grant both with and without scope; that probe does not
establish actual credential restoration success. Re-sign in once if091cleared the
saved credential, then check restoration on the next launch. Actual092refresh
with the owning account remains pending.

## Graphics regression repair candidate

091introduced a requested-resolution override that selected the first matching
width/height from the inventory. That discarded the established normal-refresh
ranking. With119.88Hz listed before59.94Hz, SDLdisplay inventory selected59.94Hz
but Vulkan surface creation could select119.88Hz.092ranks matching requested modes
with the same <=60Hz preference, using the fastest normal-refresh mode when one
exists. Unknown resolutions keep the existing valid fallback. A null-window guard
also preserves the original surface-hook harness behavior. Actual pixel-size
reporting/logical coordinates remain separate, as introduced in091.

The actual surface-hook regression verifies1080p59.94beats1080p119.88 and4K,
4Krequested selection similarly prefers59.94, unenumerated sizes return no match,
and selected display/mode/plane/alpha/extent/stack reach real surface-creation
arguments. Existing failure checks remain. Added native logging records requested
size and selected extent/refresh before surface creation; Java logging marks
instance preparation and binding setup without printing credentials/arguments.

This is a concrete mode-selection bug repair on the observed graphics-startup
path, not proof that the console crash is resolved. Exact092PS5PLAY, display mode,
menu/world/quit, pointer alignment, saved login and LAN checks remain pending.
No original game classes or downloaded JAR bytes are changed.

The [validation record](validation/client092-launch-followup-build-2026-10-27.json)
contains matching package/symbol checksums, host/target checks and the scoped
console evidence. Install replaces the same PPSA99874title and preserves the
/download0/ProsperoCraft library/cache/world paths and4GiBstorage request.

## User startup confirmation — 2026-10-27

After receiving the092candidate above, the user reports “MC starts now!”.
Record this as scoped console startup confirmation for package SHA256
f9c1cd0a67c1229fdd08b29295acddaf2f0b79e3d0162dc199a1f8ef55e64610.
The prior immediate launch blocker is no longer observed in this report. It does
not prove the precise native fault cause, gameplay stability, menu/world/quit
lifecycle, saved-login restoration, resolution alignment or multiplayer/LAN.
No ALL PASS, new frozen milestone or public release is inferred.
