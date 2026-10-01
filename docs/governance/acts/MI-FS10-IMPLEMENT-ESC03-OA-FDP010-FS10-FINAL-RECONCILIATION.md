# Master Execution Instruction — FS-10: Implement ESC-03 O-A Now → Complete FDP-010 → FS-10 Final Reconciliation (as received)

**Received:** from the Founder, 2026-10-01, in the message body; extracted byte-exactly from the session transcript. Authority: `FDP-012` (Register `§124`), `AD-FS10-ESC03-R1` (Register `§125`); receipt and result at Register `§126`.

````text
# MASTER EXECUTION INSTRUCTION
# AIOS FS-10 — IMPLEMENT ESC-03 O-A NOW → COMPLETE FDP-010 → FS-10 FINAL RECONCILIATION

## 0. EXECUTION DIRECTIVE

Proceed with implementation NOW.

Do NOT create another Act.
Do NOT create another Micro-Act.
Do NOT open another governance loop for ordinary in-scope implementation work.

The required authority already exists:

- FDP-012 is CANONICAL and OPERATIVE.
- Register §124 = FDP-012 canonical registration.
- Register §125 = FDP-012 execution result.
- AD-FS10-ESC03-R1 selected O-A.
- O-A implementation is AUTHORIZED.
- Release/LIVE authority remains Founder-reserved.

The objective is now execution, not further governance discovery.

---

# 1. CURRENT AUTHORITY STATE

Before changing anything, perform one concise re-discovery of:

1. FDP-009
2. FDP-010
3. FDP-011
4. FDP-012
5. AD-FS10-ESC03-R1
6. Register §§124–125
7. FS-10 Current Authority
8. FS-10 Deployment documentation
9. FS-10 Release Package
10. X2 deployment protection
11. B3 operator authentication
12. Current Production deployment
13. Current rollback target
14. Current Production credential state

Confirm:

- FDP-012 = canonical + operative
- O-A = selected
- O-A = implementation authorized
- ESC-03 = not yet resolved
- FDP-010 = not yet complete
- FS-10 = not yet ready
- Release = NOT authorized
- LIVE = NOT active

Do not reinterpret already-decided authority.

If no genuine canonical conflict is discovered, proceed immediately.

---

# 2. OBJECTIVE

Execute the already-authorized architecture:

## O-A — PER-SESSION VERCEL PROTECTION BYPASS

The purpose is:

Allow the delegated CEO/Claude Code execution environment to reach the protected Production AIOS API during an authorized operational session while preserving:

- X2 protection architecture
- B3 authentication
- least privilege
- auditability
- revocation
- environment isolation as far as the selected mechanism supports
- Release/LIVE separation
- Founder Release Authority

This is an OPERATIONAL ACCESS mechanism.

It is NOT:

- Production Release
- LIVE activation
- public exposure
- permanent bypass
- governance authority expansion
- new product authority
- new AIOS capability
- Phase 14
- Native Core #12
- reopening P12/P13
- reopening Platform Organization

---

# 3. ACCOUNT-HOLDER / PROVIDER BOUNDARY

If a provider-side action genuinely requires the account holder:

- identify the exact action,
- execute only what is already authorized,
- do not request or expose the secret value in chat,
- do not paste credentials into repository files,
- do not put credentials into documentation,
- do not put credentials into evidence artifacts,
- do not print credentials in command output,
- do not place credentials into logs,
- do not create a permanent bypass.

The provider credential mechanism already investigated may be used ONLY if it conforms to the selected O-A architecture and the existing FDP-012 / AD-FS10-ESC03-R1 constraints.

Do not silently substitute M1 environment-variable injection for the selected provider-side credential path.

If the provider-side credential capability is unavailable, do not invent another mechanism.

Use only an already-authorized equivalent mechanism that remains within FDP-012.

---

# 4. IMPLEMENTATION SEQUENCE

Execute continuously.

## STEP 1 — Establish O-A access path

Implement the selected per-session Protection Bypass mechanism.

Required characteristics:

- Production only
- session-bounded
- no permanent bypass
- no public exposure
- no X2 redesign
- no weakening of deployment protection
- no change to B3 authentication
- no expansion of operator scopes
- no Release/LIVE capability

The existing `aios-operator` principal remains governed by B3.

The bypass only solves the X2 edge-access problem.

It must NOT replace B3.

Therefore:

X2 → O-A access mechanism → B3 authentication → AIOS API

remains the intended security chain.

---

# 5. VERIFY SECRET / CREDENTIAL SAFETY

Before making Production requests, verify that the chosen provider credential path satisfies the already-authorized security envelope.

At minimum verify:

1. Secret value is never printed.
2. Secret value is never committed.
3. Secret value is never written to repository files.
4. Secret value is never written to evidence files.
5. Secret value is never written to logs.
6. Secret value is never included in test output.
7. Secret value is not exposed to ordinary Claude commands if provider architecture claims proxy-side injection.
8. Bypass is restricted to the intended Production hosts.
9. Credential is not attached to unrelated hosts.
10. Credential can be revoked.
11. Revocation can be verified.
12. No permanent bypass remains after the authorized session.

If any of these cannot be verified, STOP the implementation at that specific security boundary and report the exact blocker.

Do not weaken the requirement.

---

# 6. PRODUCTION ACCESS VERIFICATION

Once O-A is established:

Verify that:

### Without O-A
Protected Production endpoint remains blocked by X2.

Expected behavior:

- anonymous request → blocked
- operator token without X2 → blocked

### With O-A + B3
Authorized operator request reaches AIOS.

Expected:

X2 PASS
→ B3 PASS
→ scope enforcement PASS
→ API request PASS

Test both:

- valid authorized request
- unauthorized scope request

---

# 7. REQUIRED POSITIVE TESTS

Run the minimum complete operational verification suite.

### P1 — Health / Smoke

Verify:

- Production reachable through authorized O-A path
- service healthy
- response valid

### P2 — Read

Use `aios.observe`.

Verify:

- authorized read succeeds
- unauthorized read fails appropriately

### P3 — Workflow Execution

Use `aios.workflow.run`.

Verify:

- authorized workflow execution succeeds
- execution state is persisted correctly
- trace exists
- audit exists

### P4 — Audit

Verify:

- request is attributed to correct subject
- audit record exists
- no credential material appears

### P5 — Negative Scope

Attempt an operation requiring:

`aios.agent.register`

using `aios-operator`.

Expected:

`403`

No scope expansion.

### P6 — X2 Negative Control

Remove/disable the O-A access path for the test request.

Expected:

`302` / X2 protection behavior.

This proves O-A did not silently disable X2.

### P7 — Environment Isolation

Verify:

- Production credential/path does not authorize Preview unintentionally.
- Preview credential/path does not authorize Production.
- old deployments do not receive unintended authorization.

### P8 — Revocation

Revoke the O-A access mechanism.

Then verify:

- Production API access through that mechanism fails.
- X2 protection returns.
- B3 token alone cannot bypass X2.

---

# 8. COMPLETE ESC-03

ESC-03 may be declared RESOLVED only when all are true:

- O-A is implemented.
- Production access works through O-A + B3.
- X2 remains intact.
- B3 remains intact.
- least privilege holds.
- negative controls pass.
- credential safety verified.
- revocation verified.
- no permanent bypass exists.
- no public exposure exists.
- Release/LIVE remain unavailable.
- evidence is captured without secrets.

Then update:

`docs/fullstack/FS-10-ESC-03-AUTHORITY-RESOLUTION.md`

and the current FS-10 authority state.

Do not rewrite historical records.

---

# 9. COMPLETE FDP-010

After ESC-03 is resolved, complete the EXISTING FDP-010.

Do NOT create FDP-010 v2.

Verify all three operational components:

### ESC-01
Permanent Production operational principal:

`aios-operator`

Scopes:

- `aios.observe`
- `aios.workflow.run`
- `aios.audit`

Must NOT have:

- `aios.agent.register`

Verify hash-only storage.

### ESC-02
Rollback authority:

CEO may rollback to a verified known-good target under FDP-010.

Verify:

- valid rollback target exists
- target is deployable
- target has been smoke-tested
- rollback path is operationally documented
- `22c0b49` remains excluded as invalid legacy target

Do not falsely claim rollback resilience against an untested defect.

### ESC-03
Operational access through X2 is now usable.

Once all three are verified:

FDP-010 = COMPLETE / EXECUTED / VERIFIED.

---

# 10. ROLLBACK READINESS

Establish the currently authorized rollback target.

Verify:

- target deployment exists
- target commit identified
- target is known-good
- target smoke test passes
- Production can technically be rolled back
- O-A + B3 access remains usable after rollback
- rollback does not imply Release/LIVE

If a full destructive rollback is unnecessary, do not perform one merely for theater.

Evidence of rollback readiness is sufficient if the governing requirement does not require a live destructive drill.

Do not claim a rollback drill was performed if it was not.

---

# 11. UPDATE CURRENT DOCUMENTATION

Update only CURRENT/LIVING documents.

At minimum reconcile:

- `docs/fullstack/FS-10-CURRENT-AUTHORITY.md`
- `docs/fullstack/FS-10-CURRENT-AUTHORITY.json`
- `docs/fullstack/FS-10-DEPLOYMENT.md`
- `docs/fullstack/FS-10-RELEASE-PACKAGE.md`
- `docs/fullstack/FS-10-ESC-03-AUTHORITY-RESOLUTION.md`
- FDP-010 execution/evidence record if one exists
- relevant execution record

Preserve historical records.

Do not rewrite:

- historical FS-09 gate
- P12 certified records
- P13 certified roots
- closed Platform Organization records
- prior Founder Decision records
- historical deployment records

---

# 12. RELEASE PACKAGE

Update the Release Package with the final verified FS-10 state.

It must explicitly distinguish:

1. Production Deployment
2. Production Verification
3. Operational Access
4. Rollback Readiness
5. Founder Release Authorization
6. Production Release
7. LIVE

These are NOT the same state.

The final state must NOT say:

- Released
- LIVE
- Operational AIOS

unless Founder Release Authorization has separately been issued.

---

# 13. FINAL FS-10 GATE

FS-10 may be marked READY only if:

### Governance
- FDP-009 canonical
- FDP-010 complete
- FDP-011 canonical
- FDP-012 canonical + operative
- no unresolved authority conflict affecting FS-10
- no unauthorized authority expansion

### ESC-03
- O-A implemented
- Production access verified
- X2 preserved
- B3 preserved
- least privilege verified
- revocation verified
- no permanent bypass
- no public exposure

### ESC-01
- permanent operator principal verified
- correct scopes
- hash-only storage
- auditability verified

### ESC-02
- valid rollback target established
- rollback readiness verified

### Verification
- smoke PASS
- health PASS
- integration PASS
- persistence PASS
- trace PASS
- audit PASS
- security PASS
- negative controls PASS
- credential leak scan PASS

### Documentation
- current authority reconciled
- deployment docs reconciled
- Release Package reconciled
- evidence complete
- historical records preserved

### Regression
Run the relevant regression suites.

Classify failures accurately.

Do NOT manipulate P12 population or tests.

Known pre-existing/classified failures may remain classified exactly as already established, but no NEW unexplained failure may be silently accepted.

---

# 14. FINAL REDISCOVERY

After all material construction:

STOP modifying first.

Then perform a fresh re-discovery.

Verify:

- repository clean
- correct commit
- Production state
- X2 state
- B3 state
- O-A state
- temporary access state
- permanent operator state
- rollback target
- evidence
- current authority
- Release Package
- governance register
- no secrets
- no bypass residue

Confirm that implementation did not create an unintended authority expansion.

---

# 15. ABSOLUTE RELEASE FIREWALL

This instruction DOES NOT authorize:

- Founder Release Authorization
- Production Release
- LIVE
- public launch
- public access expansion
- removal of X2
- permanent bypass
- new Founder authority
- new governance authority
- Phase 14
- Native Core #12
- reopening P12
- reopening P13
- reopening Platform Organization
- changing constitutional authority
- changing the AIOS Mission/Identity

When FS-10 becomes ready, STOP.

The final state must be:

> FS-10 READY
> PRODUCTION DEPLOYED
> PRODUCTION VERIFIED
> OPERATIONAL ACCESS VERIFIED
> ROLLBACK READY
> FDP-010 COMPLETE
> RELEASE PACKAGE READY
> FOUNDER RELEASE AUTHORIZATION REQUIRED
> RELEASE NOT AUTHORIZED
> LIVE NOT ACTIVE

---

# 16. NO MORE GOVERNANCE MICRO-ACTS

Do NOT create:

- ACT-013
- ESC-04
- another Micro-Act
- another authority reconciliation gate
- another Founder Decision

for ordinary implementation issues already covered by FDP-012.

Only stop and escalate if a genuinely Founder-reserved matter appears that is NOT already bounded by FDP-012, FDP-009, FDP-010, or the existing governance baseline.

Technical implementation ambiguity inside the authorized O-A envelope must be resolved through the already-granted bounded Architect authority.

Do not reopen FD-2.

Do not attempt to globally ratify FD-2.

FDP-012 deliberately grants bounded authority for this exact FS-10/ESC-03 work.

Use it.

---

# 17. EXECUTION STYLE

This is an EXECUTION instruction.

Do not merely produce a plan.

Do not tell me what you could do.

Do not stop after documentation.

Execute the authorized implementation.

For every action:

DISCOVER
→ CLASSIFY
→ EXECUTE
→ VERIFY
→ INTEGRATE
→ EVIDENCE
→ RE-DISCOVER

Construction-first.

No silent authority expansion.

No unsupported completion claims.

No secret exposure.

No Release/LIVE.

---

# 18. FINAL REPORT

At completion provide:

## A. Authority
- FDP-012 status
- O-A status
- FDP-010 status
- ESC-03 status

## B. Implementation
- mechanism actually implemented
- exact bounded architecture
- Production hosts affected
- credential handling model
- revocation model

Never print secret values.

## C. Verification
- X2 tests
- B3 tests
- positive tests
- negative tests
- audit/trace/persistence
- rollback readiness

## D. Regression
- native_core
- consumers
- fullstack
- tools
- citation audit
- exact classification of any failures

## E. Final State

One of:

### STATE A
`FS-10 READY — FOUNDER RELEASE AUTHORIZATION REQUIRED`

or

### STATE B
`FS-10 BLOCKED — <exact blocker>`

Do not use vague status language.

If STATE A:

> RELEASE NOT AUTHORIZED
> LIVE NOT ACTIVE

remains mandatory.
````
