# ProsperoCraft 01.000.096 — sign in, pick an instance, play

Minecraft Java on PS5, with a native Vulkan launcher, working account login and a refreshed instance library. This release brings the `Temp_gametest` work into `main` and publishes the user's exact096 candidate, without rebuilding it.

## What's new since083

- Sign in with an owned Java Edition account, restore your saved sign-in and see your player name/head. Full-game launch checks entitlement and profile; access tokens stay in memory.
- A native Vulkan GUI with animated backgrounds, glass panels, focused instance cards and a saved Waves background default.
- MultiMC/Prism-style instance artwork, version/snapshot download choices, dropdown settings and a normal-sized add-instance card.
- In-game controller keyboard, controller glyphs, shoulder-button navigation and clearer PLAY/OPTIONS control guides.
- Optional launcher vibration and Reduced Motion settings.
- PS5 selected-title and launch banners using the supplied ProsperoCraft artwork.
- Instance deletion with a No/Yes confirmation. Confirmed deletion permanently removes that instance and its worlds; there is no Undo.

## Credits

**GUI:** [mihawk-99/PS5_VKHomebrewUI](https://github.com/mihawk-99/PS5_VKHomebrewUI), based on BlackBearReloaded's ps5-homebrew-ui. Thank you to Mihawk and the upstream UI contributors.

**Instance icons:** [MultiMC](https://github.com/MultiMC/Launcher) and [Prism Launcher](https://github.com/PrismLauncher/PrismLauncher) contributors. Original SVG authors, CC BY-SA4.0 artwork notices and upstream licenses remain included. The ProsperoCraft logo is separate project artwork.

**Runtime:** [PS5 Java25](https://github.com/mateo-cogeanu/ps5-java25-homebrew), with OpenJDK, Mesa/RADV, SDL, LWJGL, OpenAL Soft and the other upstream projects credited in the packaged notices.

## Install or update

Download **PPSA99874.zip**, extract its complete PPSA99874 folder and update it through your existing homebrew installation workflow. ProsperoStore will offer096 after its catalog update is approved and deployed.

Preserve `/download0/ProsperoCraft` and back up worlds before updating. The app requests the same4GiB storage and keeps the existing title/content identity. Client and server share PPSA99874, so installing the client replaces the server app; keep server packages separately.

New installs start with an empty library. Download game files through the launcher; the app ZIP contains no official Minecraft game JARs or asset objects. Authentication requires an owned Java Edition account. Sign out clears saved credentials. Saved refresh credentials use app-local encryption with an adjacent local key; this is not hardware-backed storage.

## Validation and limits

The user reports Minecraft running and login working on PS5 and selected this exact096 package for release. This is scoped human feedback, not a formal ALL PASS, measured FPS or an endurance result. Host package/auth/channel/ownership checks, artwork validation and exact OpenAL relinking are recorded separately.

The packaged channel remains **temp_gametest**. Authentication is an experimental legacy flow; it does not establish approval of a separate ProsperoCraft Microsoft application registration. Only26.3is the playable native baseline. Other26.xreleases/snapshots may download but are not claimed launchable. Client mod loaders/Controlify/shaders remain future work. Server joining has earlier console confirmation; **LAN hosting is deferred**. Home/favorites remain deferred. Resolution combinations, account expiry/recovery, save/reload, reconnect, lifecycle regressions and long sessions need broader testing.

Official game JARs remain unmodified. The scoped OSHI CPU provider is a separately disclosed dependency port. Source, original notices and matching OpenAL corresponding-source/relink materials accompany this release. Do not replace old082/083release assets or infer new frozen milestones.
