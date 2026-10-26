# ProsperoCraft AppID review request draft

Official form: [AppID Review](https://aka.ms/mce-reviewappid). Verified2026-10-26;
the short link redirects to Microsoft's AppID Review form. The current form says
submissions are reviewed weekly; duplicate submissions do not accelerate review.
Approval and timing are not guaranteed.

This is a draft for the project owner. No form fields have been filled or submitted.
Read the linked EULA/Usage Guidelines yourself before answering its first question.

## Form values

| Field | Suggested value |
| --- | --- |
| Request type | New AppID for Approval |
| Application name | ProsperoCraft |
| Application (client) ID | `f0c7635e-8d50-4d7e-afa3-d15db4a0a3d3` |
| Directory (tenant) ID | Copy from the same app registration's Overview page. |
| Contact | Use the contact email associated with this Azure registration; the form says it cross-checks that contact. |
| Associated website | https://github.com/mateo-cogeanu/ProsperoCraft |

Keep the existing app ID. Do not submit a client secret, password, live device
code, access token or refresh token.

## Justification draft

ProsperoCraft is an open-source, unofficial Minecraft Java Edition launcher and
native Java25port for PlayStation5homebrew. We request Minecraft Services access
for our own application ID so users can authenticate their Microsoft account,
verify JavaEdition entitlement, retrieve their Minecraft profile, and launch the
original, unmodified client using their authenticated session.

The launcher uses Microsoft's public-client device-code flow and Xbox/XSTS token
exchange. The authenticated full-game launch path is gated on the Minecraft token,
entitlement and profile checks. Tokens remain in memory in the current version;
passwords are entered only on Microsoft's site. No client secret is embedded, and
no token or live code is published in diagnostics. End-to-end authenticated launch
is still pending: Microsoft/Xbox/XSTS reaches Minecraft login, which returns403
for this app. We seek review of this application's access rather than reusing
another launcher's ID or bypassing service checks.

The development build also offers a separate restricted upstream demo path using
the original client's --demo option, with multiplayer and chat disabled. It does
not create an authenticated session or unlock the full game. Public release
packages omit the original game JARs and assets and document separate provisioning.
Source and reproduction details are available in the linked repository.

## Optional context

Application ID: f0c7635e-8d50-4d7e-afa3-d15db4a0a3d3.
Observed failure: Minecraft Services login HTTP403 after Microsoft/Xbox/XSTS.
Public client flow has been enabled. Full authenticated Minecraft launch remains
unvalidated. We can provide further non-sensitive implementation details if needed.

Only the project owner should make the form's EULA/Usage Guidelines attestation
and submit the request after checking the registration contact and tenant ID.
