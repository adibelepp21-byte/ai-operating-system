# Continue FS-10 — O-A Credential Reported Installed: Founder Execution Instruction (as received)

**Received:** from the Founder, 2026-10-02, in the message body; extracted byte-exactly from the session transcript. Authority: `FDP-012` (Register `§124`), `AD-FS10-ESC03-R1` (Register `§125`); receipt and result at Register `§127`.

````text
## CONTINUE AIOS FS-10 — O-A CREDENTIAL NOW INSTALLED

The Vercel `Protection Bypass for Automation` secret for `aios-platform` has now been created by the account holder.

Do NOT ask for or print the secret value.

Start a NEW SESSION so the provider-side credential injection becomes available.

Then resume the already-authorized execution from the current canonical state:

- FDP-012 = canonical + operative
- O-A = selected + implementation authorized
- ESC-03 = unresolved only because the credential was previously absent
- FDP-010 = incomplete
- FS-10 = blocked at O-A credential

Execute:

1. `preflight`
   - Verify O-A credential injection without exposing its value.
   - Verify the expected `x-vercel-protection-bypass` behavior.
   - Verify all authorized Production hosts.

2. If preflight PASS:
   - run the prepared O-A session runner;
   - execute P1–P5;
   - verify B3 authentication;
   - verify workflow execution;
   - verify persistence;
   - verify trace;
   - verify audit correlation via `X-Request-Id`;
   - verify `aios.agent.register` remains 403;
   - verify environment/host isolation.

3. Verify rollback target through O-A.

4. Do NOT revoke the Vercel bypass yet.
   Stop and report when the session reaches the explicit revocation step.

5. Do NOT:
   - Release
   - LIVE
   - change X2
   - create a permanent bypass
   - create another Act/Micro-Act
   - create another Founder Decision
   - modify P12/P13
   - modify certified roots
   - expose or print the credential.

Expected intermediate state:

O-A CREDENTIAL AVAILABLE
→ O-A PRE-FLIGHT PASS
→ PRODUCTION VERIFICATION IN PROGRESS
→ ESC-03 NOT YET CLOSED UNTIL REVOCATION TEST IS COMPLETED

Do not claim ESC-03 resolved until the complete O-A lifecycle, including revocation verification, has passed.
````
