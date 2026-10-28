# Iris download dependency resolution, development109

Build108 could report `Required mod versions conflict` on an empty instance when
Sodium was queued before Iris. A direct selection chose the newest Sodium build,
while Iris required a specific older Modrinth version. Queue order determined
whether that requirement was honored or rejected.

Development109 rebuilds the complete download plan using discovered exact required
versions until the selected graph agrees. Exact required versions take precedence
over an unpinned popular/search selection. Every pass discards the previous plan
and metadata so dependencies of discarded versions are not installed. Two actual
incompatible exact requirements remain an error, now naming the project and both
version IDs. Resolution is cancellable and bounded; repeated constraints and
excessive passes stop before publication. Existing installed files remain protected.
No mod or game JAR is rewritten.

The regression reproduces the user's Iris/Sodium/Fabric API queue in both orders:
Iris1.11.7 (`vTN4NRGW`) requires Sodium0.9.2 (`bAZQdGpg`), while the separately
selected Sodium release is0.9.3-beta.1 (`g6ju16VJ`). Host tests download and
hash-verify the real original JARs and validate their Fabric manifests with
upstream Fabric Loader0.20.1 predicates. Both orders produce exactly Iris,
Sodium0.9.2 and Fabric API0.165.0+26.3 (`EQKgpeKu`). Synthetic regressions also
cover discarded dependencies and conflicting exact requirements without partial
installation or queue loss. Existing Vitrail/Fabric API repair tests remain passing.

The candidate is01.000.109. PS5 download, launch and shader rendering remain pending.
This fixes launcher download planning; it does not establish Iris graphics support
or compatibility with another installed shader loader. Store108 and all frozen
milestones remain unchanged. No reusable Java runtime change is needed.

Candidate ZIP SHA-256:
`75acfafe14ee9aa01ecfc5e9c6ec0d63fed981d75d37d9e6a2648e1d02ea5372`.
