# Continue authentication candidate078

User could request/approve Microsoft sign-in after enabling public-client flow,
but returned to Not signed in with generic REGISTRATION text. Earlier host public
app DEVICE request returned401/invalid_client/AAD70002 requiring mobile/public
registration. User's "works now" accepted only progress past that setting; it did
not establish Xbox/XSTS/Minecraft/profile success. Do not infer full auth pass.

Current077session via Safari: client-01.000.077-1793030265-346553867. Earlier saved
reports belong to client-01.000.077-1793029898-424370611. Raw reports stay ignored.
Shell LAN reads failed No route to host, Safari worked; later native capture failed.
Old code did not log auth phase/status. Exact post-approval rejection is unresolved.

[078guide](client-auth-078.md) · [build record](validation/client078-auth-errors-build-2026-10-26.json).
078buffers smallPOST requests to retain OAuth401error bodies, distinguishes
DEVICEpublic-client failure/Minecraft403denial, prefixes UI errors with endpoint/
HTTP status and adds fixed/allowlisted PS5_AUTH diagnostics to exceptions.log.
Real localTLS tests reproduce oldstreaming401and test newhandling, HTTP403nonJSON,
no redirects,1MiBbodybound, CA/hostname rejection and nosecretlogging. Use these
logs to establish the actual endpoint/error before changing service setup.

Public app ID f0c7635e-8d50-4d7e-afa3-d15db4a0a3d3 remains; no clientsecret, other
launcher's app ID, rawresponse/token logging or entitlement bypass. RealMinecraft
Services approval may require a separate human step, but has not been confirmed
as the exact rejection. Keep077native-first UI and accepted074performance/audio.
Preserve exact077 and earlier candidates/packages. No release or Store update.
Consumer-only changes; runtime stays de339155ba78e54be1ddc903e7df0904c866fbdb.
