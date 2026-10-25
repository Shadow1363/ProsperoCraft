# ProsperoCraft client054 — policy/direct memory and denser transition samples

Human reported restarting the app after the053crash. Matching run:
client-01.000.053-1792953446-914697374. No new specific053screen/timing report was
provided;keep052's Mojang-near-complete/~1½minute observation separate.
[053hashed evidence](validation/client053-startup-failure-2026-10-25.json);
complete raw reports:runtime logs/client053-result-20261025/.

053has98complete Java snapshots and98native phase pairs. Last Java sample at
97185ms,last native record97186ms;no normal observer completion/error marker.
The earlier pipeline wait resolves:by about96s Main is in Minecraft.run/Main292,
then at97.185s it applies LanguageManager/ClientLanguage JSON resources through
SimpleReloadInstance/Minecraft.runTick. Worker-Main-1 is idle in the final sample.
This demonstrates constructor/main-loop progress and rules out calling that
previous join a permanent deadlock. It does not establish a working menu or place
a fatal instruction in Gson/StringLatin1 merely because those are sampled last.

All196native records report getrusage/flexible query success and four matching
fault handlers (mask0xf,error0). Flexible available minimum/last339738624bytes
(324MiB). Raw maxrss rises509584to1162304,with a marked increase after95s;units and
applicable process policy remain unverified. Do not equate it with bytes,apply
an assumed1GiB limit,or call it total-memory exhaustion. Java heap last/max-used
241813728,max heap259522560. Scoped direct allocator counters are not total GPU/
console memory.390shader entries/390returns and first8successful fences/accepted
flips remain;no captured fatal signal,VM abort,driver error or Java OOM. Cause is
unknown. Four initial metadata null results632/752/240/88bytes still require the
same per-request retry-result caveats documented in052investigation.

Before changing binaries,exact053ZIP/symbols/status/source commit1790aaf89c53b93bbe2f4fcae5fae9a6bb5a6596/build+failure
validation were retained in ignored dist/failures/Client_Original_Startup-01.000.053.
Exact053full ZIP SHA256cea95dcd5ef98f851a1f66e023a6e3323914d589df29cff6452f3f858cb1e65d.
Earlier failed/frozen artifacts stay intact.

054 fills two remaining evidence gaps. The native observer now queries raw
RLIMIT_DATA,RLIMIT_AS,RLIMIT_RSS soft/hard values,result/errno and explicit infinity
flags;these are process policy observations,not current physical availability or
proof of enforcement. It also records total direct memory and the largest
available direct range/start using the existing16KiB target alignment. A nonpositive
total skips the range query with result-1 and sentinels;query failures invalidate
associated values. No rlimit,allocation pool,heap or graphics setting is changed.
Existing raw RSS/flexible/handler records and build/run/phase identity remain.
Unique per-limit key prefixes support machine parsing. Records remain bounded to
2048stack bytes and direct append IO;errno is preserved. No extra observer thread.

The same optional daemon now takes240samples. Sleeps after completed samples:
1..89=1000ms,90..169=250ms,170..179=1000ms,180..239=5000ms. Nominal sample90is89s,
170is109s,180is119s,last240is419s,plus all query/stack/output/scheduling overhead.
Thus actual dense observations can drift beyond90–110s. This targets the observed
post95s transition without imposing a game timeout.32thread/64frame output bounds,
256KiB requested stack,native-failure fallback and close serialization remain.
Extra queries/safepoints/allocations/IO/mutex contention can perturb timing and
memory;missing records alone do not locate the crash or prove process death.

Original54JARs/5147assets,runtime image,heap/executor properties,graphics behavior
and fault-handler installation/delegation remain intact. Consumer observer helper,
launcher/cadence and version labels change. No speculative crash repair or menu
acceptance. No new passing milestone/client release/Store download. Server2H stays
deferred;eventual accepted binary needs the full051handoff provisioning/license/
exact-source/OpenAL relink and Store requirements.

Host checks exercise actual helper formatting/raw query failures/infinity/invalid
direct-total skip/append errors/errno under ASan/UBSan,and actual Java blocked/deep
stacks/cadence boundaries/bounds/absent-native fallback/finite lifecycle. Target
and full-package checks verify new diagnostic strings,matching observer bytecode,
all original JAR/assets,native/runtime/SELF audits and exact preserved053.
Host/target checks cannot establish PS5 policy/query correctness or a working menu.

Install054,press X once and note screen/timing. After failure,reopen without X,
then retrieve process-usage/build/session/exceptions/VM/native-stderr/startup-tail/
abort/fatal reports before launching again. Keep actual version/run identity.

Host/native-helper tests,target build and full-package checks passed.
[Build validation](validation/client054-build-2026-10-25.json). PS5 validation pending.
