# Development117: consistent controls and adaptive-trigger fallback

User reports adaptive triggers do not work in116 and requests Settings-style controls throughout the launcher, plus a 2×2 instance action grid. Public release and ProsperoStore remain108. Previous candidates and frozen passing snapshots are preserved. Java runtime source and its existing0126integration are unchanged.

## Launcher controls

Instance Settings places Mods / Shaders above Resource Packs / Duplicate Instance, with Done / Delete below. Directional navigation follows these columns and rows. The duplicate operation and its recovery/isolation behavior remain unchanged.

Consumer toolkit adapters now share the Settings dark glass face, animated focus border, focus tint and press pulse across action buttons, Settings rows and content result controls. Done uses a distinct green filled face with the same focus and press animations. Other primary actions use readable accent text and destructive actions use muted red text. Dialog actions use the same dark theme. The common controls retain their size while page entrance slides run; focus and press motion settle between inputs. Press pulses are bound to their page/row and current press window, preventing old events from replaying after navigation. Reduced Motion snaps focus and suppresses pulses. No vendored toolkit implementation was changed.

## Observed trigger failure and repair

Safari retrieved preserved116reports from the console log server. The previous gameplay log records native OFF with result0, then per-zone resistance mode4 repeatedly returning0x80920001. Haptic audio separately reports first nonzero PCM success. This establishes a native command rejection, not a physical success for the new fallback. Raw reports remain local.

The SDL consumer adapter now submits each enabled trigger independently. Accepted per-zone commands retain full native behavior. Only the observed invalid-argument result enables a cached per-mode fallback. Rejected per-zone resistance/vibration profiles are approximated with basic resistance/vibration commands selected from actual trigger travel. Hysteresis reduces boundary chatter; identical commands are skipped. Both triggers retain independent profiles and masks. Failure of a basic command stops its polling fallback. Close, disconnect and intercepted input clear requested effects and reset active output. Other native errors remain failures rather than being silently treated as compatibility success.

This travel-following approach is also used by the [Jelly5 PS5 implementation](https://github.com/02dnot/Jelly5/blob/333e393b7f1a5b98d88099b4782dab97bd10fa5d/app/src/nuvio_input.c). It is an approximation of a hardware per-zone effect. Physical resistance, vibration, release/reset and coexistence with Controlify haptic audio still require PS5 testing. No mod/game JAR is transformed and no arbitrary HID report is forwarded.

## Validation

- Actual input adapter fixture: native mode4 rejection, analog zone changes, cached rejection, deduplicated updates, independent trigger sides and interception/disconnect resets. Mode6 frequency, hysteresis and inactive zones are checked too.
- Original Controlify packet serialization and native decoder checks pass with the original mod JAR.
- Instance duplication/isolation/recovery and asynchronous navigation checks pass with the new grid routing.
- Actual Vulkan launcher render and motion checks pass, including stable Reduced Motion frames and all ten backdrops. The 2×2 page was visually inspected.
- Startup host policy and package/native toolkit checks pass. Console behavior remains pending.

Candidate117 ZIP SHA-256: `52198449e6a623995e261b636a06ec847669af5321c9919a3932afbb1df804c5`. Console validation is pending; this is not a Store release.

Preserved local startup-tail report SHA-256: `b53e258d5b6e8a8557675d8c993816622bae390f56b1f2eccbbbbd53eb9aadbd`. Native stderr SHA-256: `f7272f27d5d0ae91cefb251f58182d728d25953e02629f47670a235592c4de2e`. Reports are not included in Git.
