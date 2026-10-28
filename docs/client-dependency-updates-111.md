# Required dependency updates, development111

When a selected mod resolves to a newer version of an already-installed dependency,
the launcher can now update that dependency instead of requiring manual uninstall.
This also applies to pre-Play repair when a required Fabric manifest condition
identifies an outdated dependency whose Modrinth project is known from the receipt.
Missing or outdated bundled Fabric API modules can select a newer Fabric API.
Healthy instances still need no dependency network requests;offline instances with
missing/outdated requirements stop with a connection message.

Exact required Modrinth version IDs take precedence over the installed root-version
preferences during repair. Download planning retains109's queue-order behavior.
Known manifest-only requirements can request the project's current Minecraft/Fabric
candidate and recheck the complete prospective manifest graph. Candidate expansion
is bounded to16 passes, with unchanged plans rejected. This is not a general search
through all historical mod combinations. Unsupported/unmapped requirements still
stop with the owning mod, required ID and version predicate.

Updates apply to receipt-managed Fabric mods with unchanged original bytes and the
same Fabric root mod ID. The upstream Fabric version comparator must establish that
the replacement is newer. Automatic downgrades, equal-version repacks, edited files
and untracked/manual duplicate JARs are preserved for manual resolution. Shader and
resource-pack version replacement remains separate from this mod dependency work.
Receipt filenames, project IDs and hashes are validated before automatic file moves.

All new files are downloaded and publisher-hash verified before replacement. The
prospective mod scan excludes only verified old JARs scheduled for replacement and
includes the other installed mods, so an incompatible required version blocks the
change. Exact conflicting Modrinth pins and incompatible metadata remain errors.
Manifest checks supplement rather than replace the full upstream Fabric resolver.

Publication moves old JARs into a private per-instance backup, installs the complete
plan and saves the installed receipt once. A pre-commit cancellation or I/O failure
removes newly placed files and restores the old JARs;the queue remains available.
Successful updates remove the old JAR from the game folder even when filenames
change, preventing duplicate versions. World/config/resource-pack data is untouched.
After receipt commit, cleanup or queue-save failures do not roll back committed
files. Failed cleanup retains private backups outside mods. Power-loss recovery
across the file/receipt commit window remains unvalidated;do not claim a durable
filesystem transaction or an Undo feature.

Host regression tests cover same/different filenames, exact-pin upgrades,
manifest-only pre-Play repair, no-network healthy launch, offline rejection,
conflicting installed requirements, modified files, rejected downgrades, bad hashes,
cancellation after the old JAR was staged and receipt-write failure. Failures retain
the old file bytes, receipt and queue. Existing108-110 dependency and Iris launch
guard checks remain passing.

The original-JAR test installs Sodium0.9.3-alpha.1 (`v4PSXean`), then queues
Vitrail0.13.0 (`Q3nKuPKJ`). Vitrail's unpinned required Sodium project resolves to
0.9.3-beta.1 (`g6ju16VJ`);the alpha JAR is removed and the receipt updated. Fabric
API0.165.0 (`EQKgpeKu`) is also added as required by Vitrail's manifests. Original
hashes, upstream predicates and a world marker are checked. Vitrail's declared
Sodium predicate is0.9.x;this fixture tests a newer resolved required dependency,
not a claim that Vitrail itself rejects every older0.9.x version.

Build111 PS5 dependency update, pre-Play repair, launch and save/reload tests remain
pending. Public108 release/Store and all frozen passing milestones are preserved.
This is consumer launcher policy;the Java runtime source is unchanged.

Candidate ZIP SHA-256:
`7ee993f95c1ec897b4e61d893a01dc001202a8e7c8d58c43fb3e94ba6e2243e7`.
