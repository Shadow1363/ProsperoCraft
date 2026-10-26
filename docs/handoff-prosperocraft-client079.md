# Continue instance launcher079

Human requested a full native GUI redesign: top Add Instance/Settings/Account bar
with L1/R1navigation, instance grid, selected large icon left and Play/settings
right, rename/icon editing, resolution/global settings, fluid animation, and
on-console selected26.xdemo downloads instead of a bundled game. Use current
[guide/previews](client-instances-079.md) and [build record](validation/client079-instances-build-2026-10-26.json).

New ProsperoLibrary persists UUID instances/settings under /download0/ProsperoCraft,
with separate game/saves/options per instance. No preset instance or automatic
legacy world migration. ProsperoInstall resolves publisher catalog, checks Java25,
verifies client/libs/index/objects, skips desktop native classifiers, rejects URL/
path escapes, and commits a receipt only after complete verification. Cancellable
bounded workers retain valid cache, remove partials and stop before a new transfer.
ProsperoLauncher models80bounded native fields, UI/controller/text keyboard, async
catalog/install/auth tasks and demo-only selected-instance launch. Native UI is
still first-frame-before-VM on its own thread; JNI stays on the JVM caller thread.
Animations settle; Reduced Motion and held-direction repeat are supported.

Parent app classpath contains Gson/LWJGL bindings/port overlays only. Original
Minecraft and remaining Java libraries load from verified download URLs via a
separate URLClassLoader; thread context follows that loader. gamePreflight is now
Java receipt validation, not native legacy inventory run_test(2). Three JNI methods
remain for ClientStartup25. Instance audio/options setup happens after selection.
No game JAR changes. Preserve074audio/C1/G1andacceptedbytes;078exactpackage/symbols
preserved in dist/accepted/Client_Auth_Errors-01.000.078. No release or Store work.

IMPORTANT:26.1/26.2are Java25but GLFW3.4.1;26.3is SDL/LWJGL3.4.3. Downloads for26.2
are implemented and fixture-tested, but the GLFW native path is NOT implemented;
older gameplay remains unsupported. Do not claim all26.xgames work or silently
run26.3in place of another version. Start PS5download/launch tests with26.3. A
host real26.3inventory check verified54JARs/5147assets/index34anddownload-loader
identity. Console downloader/filesystem/network/loader/graphics/audio/pacing all
need validation. Runtime source unchanged; native dependency port versions remain
fixed at the existing accepted values. New metadata native classifiers were
reviewed: exclude netty OS classifiers but retain its Java unix-common artifact.

Account review is pending, human saw MINECRAFT403on078. Current Play always uses
upstream restricted demo, no full-session/ownership bypass or another AppID. Do
not log tokens/codes/headers/raw auth errors. Credentials remain memory-only.
Current screenshots are actual host native render with sample instances; real
new library is empty. Built-in8icons only; customPNG/removal/archive not present.
New package should contain no MinecraftJAR or game-assets subtree. Update all
checks/source/doc records and publish consumer changes; no Java runtime changes
should be mixed into this repository. Old validation snapshots remain frozen.
