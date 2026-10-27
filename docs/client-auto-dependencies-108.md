# Development108: required mod dependencies

The user confirms keyboard input works and requests automatic mod dependencies
after a Fabric API omission caused startup failure. Safari identifies current
build107/runclient-01.000.107-1793129940-944961850. Its native report has working
keyboard API bindings/handles and real AudioOut PCM submissions; human keyboard
feedback does not establish mouse,Controlify,audible audio or full lifecycle
acceptance. The retained previous Fabric exception names Vitrail0.13.0-beta's
missing `fabric-key-mapping-api-v1` requirement. The previous exception has no
build identity,so it is not presented as the current run's failure. Current
output includes Fabric API0.165.0+26.3 following manual installation.

The downloader already followed Modrinth's recursive required-dependency graph,
but Vitrail marks Fabric API optional there while its actual Fabric manifest
requires a bundled API module.108 checks both sources before publishing newly
downloaded mods. It reads original `fabric.mod.json` manifests and declared
nested JARs,including `provides` aliases. For missing Fabric API modules it adds
the game-filtered Fabric API projectP7dR8mSH,then verifies that the downloaded
JAR really supplies the required module and satisfies the declared versions.
Optional mods are not all installed indiscriminately. Required pack dependencies
remain outside this mod-only repair path.

Version conditions use the original pinned Fabric Loader0.20.1's public Version
and VersionPredicate APIs in an isolated,closed URLClassLoader. Minecraft,Java
and Fabric Loader are accounted for as builtins. Multiple versions of nested
libraries are allowed and checked together;Sodium and full Fabric API can bundle
different versions of the same API base. Top-level conflicting versions are
not replaced. These bounded checks supplement Fabric's final resolver;they do
not claim complete equivalence with every Fabric metadata/resolution feature.

Checks and repair also run on the download/verification worker before PLAY,
including existing instances. The launcher stays responsive. Healthy instances
return after a local inventory check without dependency-network requests. A
missing dependency in offline mode produces a clear launcher message. Online
repair retains exact installed Modrinth version pins,adds required files and
keeps unrelated queued downloads. Unknown dependencies without usable Modrinth
metadata/mapping are named in the launcher rather than guessed. Incompatible
existing files must be resolved by the user;there is no forced mod upgrade or
removal. Manually installed mods can benefit from the known Fabric API-module
repair,while arbitrary unlisted dependencies may still need manual installation.

All planned bodies retain the existing HTTPS host restrictions,version/loader
filters and hash/size verification. The expanded graph is scanned before new
files are published. Failed resolution/checks retain queues and verified staging
for retry. Worlds,settings and original game/mod JAR contents are preserved;
no class replacements,bytecode transformations or game hooks are added. Nested
metadata has per-entry,total-byte,depth and module-count bounds. Dependency
checks run only before launching/downloading,not per frame.

Host fixtures exercise the actual upstream predicates,manifest-only API
requirements,nested module providers,duplicate compatible bundled versions,
old-instance repair,no-network healthy launch,offline failure,version conflicts,
unmapped requirements,queue preservation and unchanged worlds/files. A live
test uses original pinned Vitrail0.13.0/Sodium/Fabric API JARs,verifies all download
hashes,installs the previously missing module,removes API only in an isolated
host test instance,and repairs it again. No game execution or PS5 pass is inferred
from these tests. Java runtime source is unchanged from42fe3a5;all code and
validation belong in ProsperoCraft.

Test exact108 on PS5:open the existing Fabric instance,press PLAY with a required
Fabric API module missing,and check that repair downloads it before Minecraft
starts. Test a fresh Vitrail download without manually queuing Fabric API. Verify
Installed lists the dependency,worlds/settings remain,subsequent launch is healthy
and keyboard still works. Store/public release stays at101 until the user tests
and confirms release readiness. Preserve exact107/106 and frozen milestones.

[108 build validation](validation/client108-auto-dependencies-build-2026-10-27.json).
Package SHA-256: `545678bd4801cbf9e00b7209c25a89a9dfb0b3be7b645e3cd98f75633e455560`.
