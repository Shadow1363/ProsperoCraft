# 101: account navigation, clearer tabs, cursor menus and skin stream repair

Successful sign-in or saved-account restoration now selects Instances before
optional avatar work, clears the old device code/link and resets content focus.
The account page has one action: Sign in when disconnected, Sign out when an
account is present. Its row bound matches that single action. Failed/canceled
sign-in does not take the success path. Ownership/profile/session checks remain.

New libraries default snapshots to off. Existing saved preferences are preserved;
the switch remains available. Resolution changes only through its X-opened
confirm/cancel dropdown; left/right on the Settings row no longer changes it.
The active header tab has a brighter fill and persistent light underline even
when focus is in page content. Controller focus retains its own selection ring.

Uncaptured game menus receive no synthetic arrow-key events from the D-pad or
left stick: the right-stick cursor and mouse clicks select items. Captured
movement, hotbar/gameplay bindings, touchpad utility layer and the in-game text
keyboard retain their controls. The text keyboard still uses directional input
inside its own overlay. The menu controls guide now describes cursor selection.
Launcher controller navigation is unchanged.

Saved console skin failures identify Net.available/FIONREAD Permission denied
inside HttpURLConnection -> SkinTextureDownloader.readAllBytes. Java patch0124
provides a conservative zero estimate only for a confirmed TCP stream when that
query is unsupported/denied; normal reads remain real. The reusable fix, exact
native/JVM/TCP/fragmented-HTTP/error tests and target build evidence are published
in ps5-java25-homebrew at c7d6601.101 integrates its rebuilt Net.o/libnio.so and
resident nio group. No game JAR, texture URL policy or authentication bypass is
added. This addresses the captured failure; actual custom-skin display on PS5
remains pending and later independent failures may still need investigation.

Host checks exercise successful account navigation/sign-out/code clearing,
snapshot default and saved opt-in, resolution confirm/cancel/no left-right change,
credential redaction, the actual SDL adapter under ASan/UBSan and keyboard/input
handoff. Native and real-Vulkan UI previews are inspected, with top-bar text
centering checked. Preview fixtures now set the appropriate tab for account
screens. Host unchanged Main reaches expected native bootstrap; this is not a
console or game-menu pass. Full package audits check exact rebuilt libnio while
other baseline native libraries retain their existing comparisons.

Preserve exact100release/Store assets,all prior candidates and frozen milestones.
101 is a local development candidate,not a Store update or public binary release.
Console checks: sign in/restore -> Instances, correct account action, snapshots,
active tab, dropdown resolution/coordinate alignment, cursor-only menus, text
keyboard, owned custom skin, retained100smoothness/audio and Quit/relaunch.
