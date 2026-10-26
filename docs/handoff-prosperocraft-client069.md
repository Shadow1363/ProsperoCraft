# ProsperoCraft069 continuation

The user reports two068stutters, then many more and a complete freeze. Three
read-only snapshots identify run client-01.000.068-1793018012-623066325. The first
shows two plausible recent pauses640.757/713.728ms. Later/frozen captures show
GCthrash, retained live data growing toward499MiB, JavaheapOOM and failed chunk
save. Final collections repeatedly499M->499M; capture ends duringGC711. This is
heap exhaustion evidence, not proof of a native renderer deadlock. User was told
to close/reopen without X to preserve logs. Do not assume save success.

[Investigation](client-heap-069.md) · [Evidence](validation/client068-stutters-2026-10-26.json) ·
[Build checks](validation/client069-heap-build-2026-10-26.json).

069 keeps C1level1/onecompiler/32MiBcodecache/cleanup and working audio/input,
but requests768MiBheap/NewRatio3 (576MiBold/192MiByoung reservation). Runtime0119
raises the separate direct-heap ceiling only;256MiBnativebudget and ownership/
error/uncompressed/unhinted/nonexec gates unchanged. Runtime source/push verified
atbb013f533e14f01f0d93d5f4133dad8232385e3e. Physical backing remains kernel-checked
and PS5reservation is pending. Do not promise unlimited memory or no pauses.

Host actual768MiBalignedreservation ASan/UBSan passes rollback/protection/release
controls. Host realJava retained472MiB+48MiBring controlOOMs at512,passes768; C1
checksum40960/negativecontrols/startup/migration checks pass. TargetHotSpot and
appcompile/link/SELF/package checks pass. Game54JARs/5147assets stay intact.

Install package:dist/client-startup/PPSA99874.zip,01.000.069,titlePPSA99874, SHA256
59b20b2434071485c5211ff6b61bd1ccff3010ee71d6b219c0bd66f02a90fd11.
Exact068package/symbols preserved underdist/accepted/Client_GC-01.000.068; it is
a failed GC candidate, not a passing milestone.067audio/066public/server fallback
packages remain. No new GitHub release or Store publication requested.

Next obtain actual069startup/reservation, same-world extendedplay/pause/audio
feedback and freshGC/JIT reports. Track live-setgrowth;768is not proof of no leak
or sufficient memory for all worlds/settings. Save/reload/endurance still pending.
After crash reopenwithoutX before retrieval. Safari current AX report links work
when shellLANfails. Keep raw logs local; publish hashes/interpretation only.

README stays concise; build history in CHANGELOG.md. Publish consumer source here;
reusable runtime fixes separately through runtime sync script. Preserve accepted
bytes and official game files; no gameclass replacements or bytecode hooks.

## Superseded by070

069starts with768MiBonPS5but user reports stutters again. Logs show40captured
fullGCs(up to950.997ms),609MiBretained, and integrated-server view16/simulation12.
Next070caps supported distances6/5once with exactoptionsbackup; no more heap
increase. See[070handoff](handoff-prosperocraft-client070.md) and
[evidence](validation/client069-stutters-2026-10-26.json). Exact069bytes retained.
