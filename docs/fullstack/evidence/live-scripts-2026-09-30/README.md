# Live verification scripts, FS-09 final (2026-09-30)

The scripts that produced `../FS-09-LIVE-PREVIEW-2026-09-30-ACT-008.json`. They
read the operator token and the temporary bypass secret from files in a private
directory (`<dir>/token`, `<dir>/bypass09`) given as the first argument, never
print them, abort if a response echoes either, and hold no credential
themselves. They need a Preview base URL and, because Deployment Protection is
on, a valid `x-vercel-protection-bypass` secret, which exists only during an
authorized verification window (the ACT-008 window is closed and the secret
revoked).

| Script | Produces |
|---|---|
| `live_suite_09.py <dir> <base>` | the FS-08 checks 0-12 |
| `live_extra_09.py <dir> <base>` | transport headers, CORS, console CSP, repeated runs |
| `live_a_09.py <dir> <base> <stamp>` | Scenario A: definitions, 401, register, read back, failure paths, concurrency, audit |
| `rollback_final.py <dir> <base> <phase> <run id>` | one phase of the rollback / roll-forward drill |
| `obs_probe.py <base>` | a 12-request probe for the L1 log cross-check |
| `live_console.mjs <base>` | the console's Scenario A in Chromium (NOT run against the live Preview: the sandbox CA is not trusted by the browser, and TLS verification is not disabled) |
