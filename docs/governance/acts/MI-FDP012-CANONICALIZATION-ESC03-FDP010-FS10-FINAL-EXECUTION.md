# Master Founder Execution Instruction — FDP-012 Canonicalization → ESC-03 Implementation → FDP-010 Completion → FS-10 Final Reconciliation (as received)

**Received:** from the Founder, 2026-10-01, in the message body; extracted byte-exactly from the session transcript. Authority: `FDP-012` (Register `§124`); receipt and result at Register `§125`.

````text
# MASTER FOUNDER EXECUTION INSTRUCTION
# FDP-012 — CANONICALIZATION → ESC-03 IMPLEMENTATION → FDP-010 COMPLETION → FS-10 FINAL RECONCILIATION

Document Type:
Founder Final Execution Instruction

Authority:
Founder Decision FDP-012

Purpose:
Mempercepat AIOS FS-10 dari kondisi governance-resolution menuju
implementasi nyata, menyelesaikan ESC-03, menyelesaikan FDP-010,
dan membawa FS-10 sampai Founder Release Gate tanpa proliferasi
Micro-Acts.

============================================================
0. FOUNDER DIRECTIVE
============================================================

Founder instructs Claude Code to proceed with one continuous bounded
execution workstream under FDP-012.

DO NOT CREATE ANOTHER MICRO-ACT.

DO NOT CREATE ANOTHER FOUNDER DECISION FOR ORDINARY IN-SCOPE WORK.

DO NOT RETURN TO THE PREVIOUS RECONCILIATION LOOP.

Use the authority already granted by FDP-012.

The execution objective is:

FDP-012 CANONICALIZATION
→ AUTHORITY ACTIVATION
→ ESC-03 IMPLEMENTATION
→ FDP-010 COMPLETION
→ FS-10 FINAL RECONCILIATION
→ FOUNDER RELEASE GATE

Founder Release and LIVE remain outside the execution authority.

============================================================
1. CURRENT KNOWN STATE
============================================================

Expected current state:

FD-2:
IMPLIED / OPEN / NOT GLOBALLY RATIFIED

FD-2 Reconciliation:
COMPLETE

FDP-012:
FOUNDER DECIDED
PERSISTED
VALIDATED
NOT YET CANONICALLY REGISTERED

FDP-011:
CANONICAL
O-A AUTHORIZED
NOT IMPLEMENTED

ESC-03:
UNRESOLVED

FDP-010:
CANONICAL
NOT COMPLETE

FS-10:
NOT READY

Production:
UNCHANGED

X2:
ACTIVE

B3:
ACTIVE

Production Release:
NOT AUTHORIZED

LIVE:
NOT ACTIVE

Re-discover all of the above before modifying anything.

If actual state differs, record the difference and continue only if
the difference remains inside FDP-012 authority.

============================================================
2. PHASE A — FDP-012 CANONICALIZATION
============================================================

First objective:

Make FDP-012 properly canonical and operative.

Perform:

1. Re-read the exact Founder-issued FDP-012.
2. Verify byte/hash integrity.
3. Verify no higher-precedence Founder Decision conflicts with it.
4. Verify the scope is bounded to FS-10 / ESC-03.
5. Verify Founder Release / LIVE remain reserved.
6. Register FDP-012 in the canonical Governance Decision Register.
7. Register the execution record according to the existing registration
   convention.
8. Update current authority documents to reflect the now-operative
   FDP-012 authority.
9. Re-run authority integrity tests.
10. Re-discover.

IMPORTANT:

The previous repository safety hook blocked the combined registration/
current-authority mutation.

DO NOT bypass or disable the safety mechanism.

Instead:

- determine exactly which permission/control blocked the legitimate
  canonicalization;
- use the repository's existing authorized governance-registration
  workflow if available;
- if a permission must be granted by the Founder/account owner,
  identify exactly what permission is required;
- do not route around the control.

The objective is to complete legitimate canonicalization, not to
defeat a governance safeguard.

Do NOT commit a partially canonicalized state.

============================================================
3. PHASE B — AUTHORITY ACTIVATION
============================================================

Once FDP-012 is canonically registered:

Treat FDP-012 as operative.

The following authority becomes active:

BOUNDED ARCHITECT AUTHORITY
FOR FS-10 / ESC-03

Claude Code / Co-Founder may now:

- resolve architecture ambiguity;
- select implementation architecture;
- select operational access mechanism;
- reconcile FD-2 / AA-001 implications for this workstream;
- implement;
- deploy;
- verify;
- rollback;
- modify current operational documentation;
- create ADRs/evidence records;
- complete FDP-010;
- perform final FS-10 reconciliation.

Do NOT interpret this as global ratification of FD-2.

Do NOT interpret this as permanent global Architect appointment.

Do NOT expand authority beyond FDP-012.

============================================================
4. PHASE C — STOP THE RECONCILIATION LOOP
============================================================

After FDP-012 becomes operative:

DO NOT:

- create another FD-2 reconciliation;
- create another AA-001 reconciliation gate;
- create FDP-013 for ordinary work;
- ask Founder to decide ordinary technical alternatives;
- reopen completed reconciliation records;
- repeatedly re-audit the same authority question unless new
  material evidence actually changes the authority state.

The existing evidence is sufficient to proceed under FDP-012.

If an ordinary technical ambiguity appears:

RESOLVE IT.

Do not escalate merely because multiple technical alternatives
exist.

============================================================
5. PHASE D — ESC-03 ARCHITECTURE EXECUTION
============================================================

Use:

AD-FS10-ESC03-R1

as the current architecture decision candidate.

Revalidate it under operative FDP-012.

The current selected design is:

O-A
Per-session Vercel Protection Bypass

Delivery:
Claude Code environment API credentials feature

Header:
x-vercel-protection-bypass

Scope:
ONLY:

- Production alias
- current Production serving deployment
- verified rollback target

No other hosts.

No Preview.

No unrelated Vercel resources.

The credential value must never enter:

- Claude session;
- tool output;
- chat;
- repository;
- documentation;
- logs;
- evidence;
- commits.

============================================================
6. PHASE E — PROVIDER CAPABILITY CHECK
============================================================

Immediately verify whether the current Claude Code environment/
account actually supports the API credentials feature.

Do NOT ask Founder to decide this.

This is an operational/provider capability check.

If available:

→ proceed with O-A.

If unavailable:

→ evaluate the already documented alternatives within FDP-012.

Do NOT create another Founder Decision merely because the first
implementation mechanism is unavailable.

Select the safest mechanism that satisfies:

- X2;
- B3;
- least privilege;
- revocability;
- auditability;
- environment isolation;
- credential non-disclosure;
- Release/LIVE separation.

============================================================
7. PHASE F — ACCOUNT-HOLDER BOUNDARY
============================================================

Only actions that genuinely require Founder/account-holder access
remain outside Claude's execution capability.

These may include:

- creating the Vercel Protection Bypass;
- configuring provider API credentials;
- provider-side account configuration;
- creating the Founder-side Production operator token.

If such an action is required:

STOP ONLY AT THAT SPECIFIC EXTERNAL-CREDENTIAL BOUNDARY.

Do NOT create another Act.

Do NOT stop the entire architecture/implementation workstream.

Prepare an exact minimal account-holder action list.

The list must contain:

- exact UI/action;
- exact host;
- exact header;
- exact scope;
- exact lifetime;
- exact revocation action.

Never request the secret value in chat.

============================================================
8. PHASE G — IMPLEMENT ESC-03
============================================================

Once the provider-side prerequisite exists:

Implement O-A.

Requirements:

1. X2 remains enabled.
2. B3 remains enabled.
3. Protected Production remains protected.
4. API requests reach AIOS only through the authorized path.
5. Unauthorized requests remain 302/401 as appropriate.
6. Operator scope remains least privilege.
7. Preview remains isolated.
8. Agent registration remains denied unless explicitly authorized.
9. Credential is not exposed to Claude.
10. Credential is not written anywhere in the repository.
11. Credential is not written to logs.
12. Credential is revocable.
13. Revocation can be verified without reading the secret.
14. No public bypass exists.

============================================================
9. PHASE H — COMPLETE FDP-010
============================================================

Complete all remaining FDP-010 obligations.

### ESC-01

Verify:

- permanent operational principal;
- correct scopes;
- hash-only storage;
- Production-only boundary;
- auditability;
- revocation.

### ESC-02

Verify:

- rollback authority;
- valid known-good rollback target;
- rollback execution path;
- post-rollback verification;
- restoration to serving deployment.

Do NOT use obsolete 22c0b49 as a rollback target unless independently
proven valid.

### ESC-03

Verify:

- protected Production access;
- operational API access;
- X2 preservation;
- B3 preservation;
- revocation;
- negative controls.

============================================================
10. PHASE I — SECURITY VERIFICATION
============================================================

Run positive and negative tests.

At minimum verify:

POSITIVE:

- authorized Production operator reaches API;
- allowed workflow execution works;
- observe works;
- audit works;
- required operational path works.

NEGATIVE:

- anonymous access blocked;
- invalid operator token blocked;
- Preview credential cannot access Production;
- Production credential cannot access Preview;
- insufficient scope denied;
- agent.register denied;
- old/unauthorized deployment denied;
- revoked bypass denied;
- revoked credential denied;
- no permanent bypass;
- no public access.

============================================================
11. PHASE J — ROLLBACK VERIFICATION
============================================================

Verify the designated rollback target.

Perform a bounded rollback drill if required to establish operational
readiness.

Record:

- source deployment;
- target deployment;
- verification;
- resulting state;
- restoration.

Rollback does NOT authorize Release or LIVE.

============================================================
12. PHASE K — DOCUMENTATION RECONCILIATION
============================================================

Update CURRENT documents only.

Required where applicable:

- FS-10-CURRENT-AUTHORITY
- FS-10-DEPLOYMENT
- ESC-03 authority/architecture record
- AD-FS10-ESC03-R1
- FDP-010 execution record
- Release Package
- current runbook
- current governance register

Do NOT rewrite historical records merely to make them look as though
FDP-012 existed earlier.

Historical records remain historical.

============================================================
13. PHASE L — REGRESSION
============================================================

Run:

- native_core
- consumers
- bounded_exception
- fullstack
- relevant governance tests
- relevant security tests
- citation audit
- secret/credential scan
- boundary scan

Run the full tools suite if required by the existing verification
standard.

Existing classified P12-W6 failure remains classified and must not be
silently altered or gamed.

Do not modify P12 to make the test pass.

============================================================
14. PHASE M — FINAL REDISCOVERY
============================================================

After all material construction:

RE-DISCOVER EVERYTHING.

Verify:

- FDP-012 canonical;
- authority active;
- ESC-03 resolved;
- FDP-010 complete;
- Production operational access works;
- X2 preserved;
- B3 preserved;
- rollback ready;
- credentials secure;
- temporary access revoked where no longer required;
- current documentation reconciled;
- historical roots intact;
- no unexpected Production state;
- no public bypass;
- no Release;
- no LIVE.

============================================================
15. FOUNDER RELEASE FIREWALL
============================================================

ABSOLUTE:

Claude may NOT:

- declare Production Release;
- declare LIVE;
- activate LIVE;
- infer Founder Release Authorization;
- perform Final System Acceptance.

When all technical and governance work is complete, stop at:

PRODUCTION VERIFIED
+
FDP-010 COMPLETE
+
ESC-03 RESOLVED
+
FS-10 READY
+
RELEASE PACKAGE READY
+
FOUNDER RELEASE AUTHORIZATION REQUIRED

============================================================
16. NO MICRO-ACT RULE
============================================================

This is one continuous execution workstream.

DO NOT create:

- Micro-Act for provider configuration;
- Micro-Act for credential rotation;
- Micro-Act for rollback;
- Micro-Act for security testing;
- Micro-Act for documentation;
- Micro-Act for architecture alternatives;
- Micro-Act for ordinary operational decisions.

Use FDP-012.

Escalate only genuine Founder-reserved matters.

============================================================
17. GENUINE STOP CONDITIONS
============================================================

STOP only if:

1. Constitution conflict cannot be resolved within FDP-012;
2. Founder Reserved Authority is directly implicated;
3. permanent authority expansion is required;
4. Release/LIVE is requested;
5. Final System Acceptance is reached;
6. irreversible external commitment outside authority is required;
7. security requirements cannot be satisfied by any in-scope design;
8. canonical authority conflict exists above FDP-012 and cannot be
   resolved under the existing precedence model.

Do NOT stop merely because:

- provider option A is unavailable;
- an implementation alternative is needed;
- an ADR is required;
- a technical ambiguity exists;
- documentation must be reconciled;
- a rollback target must be selected;
- a test fails and requires engineering repair.

Resolve those within FDP-012.

============================================================
18. EXECUTION PRIORITY
============================================================

Priority order:

P0 — Canonicalize FDP-012 legitimately
P1 — Activate bounded authority
P2 — Verify provider capability
P3 — Implement ESC-03
P4 — Complete FDP-010
P5 — Verify rollback/security/observability
P6 — Reconcile current documentation
P7 — Full regression
P8 — Final rediscovery
P9 — Stop at Founder Release Gate

Do not spend another execution cycle re-litigating FD-2 unless
new evidence creates a genuine higher-authority conflict.

============================================================
19. FINAL REPORT
============================================================

Return:

# FDP-012 / FS-10 FINAL EXECUTION REPORT

## A. FDP-012
- canonical status
- hash
- Register section
- activation status

## B. Authority
- bounded Architect authority active: YES/NO
- FD-2 global status
- AA-001 status
- authority reconciliation result

## C. ESC-03
- architecture selected
- implementation status
- access path
- X2 status
- B3 status
- security status

## D. FDP-010
- ESC-01
- ESC-02
- ESC-03
- overall status

## E. Production
- deployment
- operational access
- rollback target
- verification

## F. Security
- positive controls
- negative controls
- credential handling
- revocation

## G. Regression
- test results
- known classified failures

## H. Documentation
- current records updated
- historical records preserved

## I. Final State

Expected:

FDP-012 CANONICAL
FDP-012 OPERATIVE
ESC-03 RESOLVED
FDP-010 COMPLETE
FS-10 READY
RELEASE PACKAGE READY
FOUNDER RELEASE AUTHORIZATION REQUIRED
LIVE NOT ACTIVE

OR:

EXACT BLOCKER
+
AUTHORITY BASIS
+
REQUIRED FOUNDER ACTION ONLY IF GENUINELY REQUIRED

============================================================
20. FINAL FOUNDER DIRECTIVE
============================================================

Do not optimize for producing another governance document.

Optimize for completing the authorized engineering work.

The purpose of FDP-012 is to remove the need for repeated
Micro-Acts and allow bounded autonomous execution.

Therefore:

DISCOVER ONCE
→ CANONICALIZE
→ ACTIVATE AUTHORITY
→ IMPLEMENT
→ VERIFY
→ RECONCILE
→ RE-DISCOVER
→ STOP AT FOUNDER RELEASE GATE

Do not manufacture authority.

Do not manufacture approval.

Do not manufacture Release.

Do not manufacture LIVE.

EXECUTE ALL AUTHORIZED WORK.
============================================================
END OF INSTRUCTION
============================================================
````
