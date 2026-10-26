# Authentication rejection handling — candidate078

The user reports Microsoft approval followed by a return to "Not signed in" with
"Microsoft app setup needs attention. Check public client flow and service approval."
This establishes a rejected authentication attempt, not a completed Minecraft
session. The launcher commits the account only after Microsoft, Xbox, XSTS,
Minecraft token, entitlement and Java profile checks all succeed.

Earlier, a host request with the public app ID returned HTTP401/invalid_client/
AADSTS70002: the client needed to be marked mobile/public. The user enabled public
client flow and reported progress. That setting and the later rejection are separate
observations. The exact post-approval failing endpoint/status is not established
by077's generic message. A current077session identity was readable via Safari;
old077reports confirmed native UI/VM entry, but auth failures were not logged.
Further native browser capture failed during retrieval. Do not invent a current
Minecraft403, assume the user lacks the game, or claim full MSA acceptance.

## What changed

Small OAuth/JSON POSTs are now buffered rather than fixed-length streaming.
OpenJDK25's HTTP transport disconnects streaming requests on401 and loses the
OAuth error body; a real local TLS regression reproduces this. Error status/body
can now reach the auth parser. Non-JSON/empty HTTP failures retain their status.
Redirect following remains disabled; TLS certificate/hostname validation remains
active. Input/output bounds remain enforced.

The account panel prefixes failures with the endpoint and HTTP status, for example
`[TOKEN HTTP 401]` or `[MINECRAFT HTTP 403]`. DEVICE/AAD70002 identifies public-client
setup explicitly. Minecraft403 identifies a services denial with approval as a
possibility, not a proven cause. Tokens and raw responses are never displayed.

`PS5_AUTH` records in the existing Java exception report contain fixed endpoint
names, HTTP status, allowlisted OAuth error identifiers, bounded numeric AAD codes
and fixed transport-failure categories. No request/response text, exception text,
headers, codes, passwords, account names or tokens are logged by these diagnostics.
Generic network/parser exceptions are not printed with their causes.

## Test on PS5

Install local `dist/client-startup/PPSA99874.zip`, titlePPSA99874/version01.000.078.
Sign in and approve the code yourself. If it fails again, report only the endpoint/
HTTP prefix and message, or leave the app open for `/exceptions.log` retrieval.
Do not share live authorization codes or tokens. A genuine Minecraft Services
application rejection may need separate registration/approval work; don't change
the client ID to another launcher's or skip entitlement checks to bypass it.

[Public-client flow setup](https://learn.microsoft.com/en-us/entra/identity-platform/scenario-desktop-app-configuration#enable-public-client-flow).
The setting is Authentication → Advanced settings → Allow public client flows →
Yes → Save. No client secret is used.

078keeps077native-first UI/threading, user icons, original game files and074audio/
performance policies. The exact077 package/symbols remain preserved locally.
Real HTTPS host tests cover401body preservation, distinct403, non-JSON errors,
redirect refusal, size bounds, CA/hostname rejection and diagnostic redaction.
They do not prove PS5 login or service approval. No release or Store update.

[Build record](validation/client078-auth-errors-build-2026-10-26.json).
