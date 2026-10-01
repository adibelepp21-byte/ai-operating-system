# `FDP-010` — FS-10 Operational Access, Rollback & Governance Reconciliation: Founder Decision Record (as received)

**Received:** from the Founder, 2026-10-01, in the message body.
**Stated status:** *"FOUNDER DECIDED — PENDING CANONICAL REGISTRATION"*. Its `§21` makes canonical status depend on the established registration process; Register `§109` records that registration.
**Answers:** `ESC-01` and `ESC-02` (FS-10 authority record; Register `§106`–`§108`), the stale FS-09 rollback wording (`FS-10-RELEASE-PACKAGE.md` `§16` U-9) and the empty Production `AIOS_OPERATOR_TOKENS` (U-5).

Reproduced below as received.

````text
# FDP-010
# FS-10 OPERATIONAL ACCESS, ROLLBACK & GOVERNANCE RECONCILIATION
# FOUNDER DECISION RECORD

Document Type: Founder Decision Record
Decision Family: FS-10 Operational Access / Rollback / Governance Reconciliation

Decision IDs:
- ESC-01
- ESC-02
- FDP-010-01 — Permanent Production Operational Access
- FDP-010-02 — Post-Release Rollback Authority
- FDP-010-03 — Historical Gate / Current Governance Reconciliation
- FDP-010-04 — Production Operator Token Residual Cleanup

Status: FOUNDER DECIDED — PENDING CANONICAL REGISTRATION

Founder: Moriarty
Delegated Executive: Claude Code — AIOS Co-Founder + Delegated CEO

Parent Authority:
- FDP-009
- ACT-CC-POST-P13-AIOS-FULL-STACK-009
- FS-10 Production Verification

Related Governance:
- AIOS Co-Founder Delegation Charter V2.0
- AIOS CEO Operating Mandate & Execution Protocol

Related FS-10 Records:
- docs/fullstack/FS-10-ACT-009-AUTHORITY-BOUNDARY-RECORD.md
- docs/fullstack/FS-10-DEPLOYMENT.md
- docs/fullstack/FS-10-RELEASE-PACKAGE.md
- Register §107 — FDP-009
- Register §108 — FS-10 Production Verification / Release Package


---

# 1. FOUNDER DECLARATION

I, Moriarty, as Founder and holder of ultimate human governance authority
for AIOS, issue this Founder Decision Record to resolve the remaining
FS-10 operational and governance boundaries identified after successful
Production Verification.

This record resolves:

1. ESC-01 — permanent Production operational access;
2. ESC-02 — post-release rollback authority;
3. the stale FS-09 rollback wording identified during FS-10 execution;
4. the remaining empty Production `AIOS_OPERATOR_TOKENS` configuration.

This record operates under FDP-009.

This record does NOT replace FDP-009.

This record does NOT authorize Production Release or LIVE.

Production Release and LIVE remain separate Founder-controlled states.


---

# 2. CURRENT VERIFIED STATE

The preceding FS-10 execution established:

    Release Candidate
        = d05261c

    Production Deployment
        = completed

    Production Verification
        = PASS

    Release Package
        = READY

    Temporary Verification Access
        = REVOKED

    Temporary Verification Principal
        = REVOKED

    Production Public Release
        = NOT AUTHORIZED

    LIVE
        = NOT AUTHORIZED

    Operational AIOS
        = NOT ACTIVATED

Production verification established:

- Production persistence;
- Preview/Production separation;
- security behavior;
- audit behavior;
- request correlation;
- health;
- integration behavior;
- backup/export integrity;
- temporary-access revocation.

The verified Production deployment currently does not have a healthy
previous application deployment available as an immediate rollback target.

The previous deployment `22c0b49` predates the current application and
would not constitute a valid application rollback target.

This fact is material to ESC-02.


---

# 3. GOVERNING PRINCIPLE

The following states remain permanently distinct:

    OPERATIONAL ACCESS
          ≠
    PRODUCTION DEPLOYMENT
          ≠
    PRODUCTION VERIFICATION
          ≠
    PRODUCTION ROLLBACK
          ≠
    PRODUCTION RELEASE
          ≠
    LIVE
          ≠
    FINAL FOUNDER ACCEPTANCE

Possession of Production operational access does NOT grant:

- Production Release authority;
- LIVE authority;
- Founder Release Authorization;
- authority to change AIOS governance;
- authority to modify certified architecture.

Likewise:

    Founder Release Authorization
        ≠
    permanent operational access.

These are separate authority surfaces.


---

# 4. ESC-01
# PERMANENT PRODUCTION OPERATIONAL ACCESS

## 4.1 Founder Decision

Permanent Production operational access is authorized as an
**operational capability**, not as Release or LIVE authority.

The operational access model shall be:

    Human Founder
         │
         │ ultimate authority
         ▼
    Production Access Control
         │
         ├───────────────┐
         ▼               ▼
    Founder Access   Delegated Operational Access
                         │
                         ▼
                     CEO / AIOS
                     Operational Scope


## 4.2 Production Access Ownership

The Production provider account remains controlled by the account holder.

Provider-level credentials, account ownership, billing ownership and
provider security controls remain external/account-holder controls.

Claude Code MUST NOT require the Founder to paste provider secrets into
ChatGPT or another conversational channel.

Provider credentials remain stored in the provider's appropriate secret
mechanism.


## 4.3 AIOS Operational Principal

A permanent AIOS operational principal MAY exist for the delegated CEO /
operational runtime.

Its purpose is:

    OPERATE AIOS

not:

    AUTHORIZE AIOS RELEASE


The permanent operational principal MUST be:

- dedicated to AIOS operation;
- server-side;
- represented only by secure credential material;
- least-privilege;
- scope-limited;
- auditable;
- revocable;
- separate from Founder identity;
- separate from Vercel/provider account ownership;
- separate from Release Authorization.


## 4.4 Scope Principle

The permanent operational principal MUST receive only the minimum scopes
required for legitimate operational duties.

It MUST NOT automatically receive:

- Founder authority;
- Release authority;
- LIVE authority;
- governance mutation authority;
- certified-root modification authority;
- unrestricted administrative authority.

Any exact scope set must be derived from the existing canonical operator
scope model.

Claude Code MUST NOT invent new scopes merely to simplify deployment.


## 4.5 Founder Emergency Access

Founder retains the ability to obtain or exercise Production access through
the provider/account-holder control plane.

Founder access is not required for every ordinary operational action.

Founder authority remains the upper governance boundary.


## 4.6 Operational Access ≠ LIVE

The existence of a permanent Production operational principal does NOT mean:

    AIOS = LIVE

and does NOT mean:

    Production Release = APPROVED

It only means:

    Operational access exists.

### Decision

    ESC-01 = RESOLVED

    FDP-010-01 = APPROVED


---

# 5. ESC-02
# POST-RELEASE ROLLBACK AUTHORITY

## 5.1 Founder Decision

After Production Release, rollback is classified as an
**operational reliability action** within the CEO delegated authority,
subject to strict conditions.

The CEO MAY execute rollback when:

1. the system is already Released;
2. rollback is operationally necessary;
3. the target deployment is a verified known-good deployment;
4. the rollback does not require changing governance;
5. the rollback does not modify certified architecture;
6. evidence is preserved;
7. the rollback remains within the existing deployment architecture.

This confirms the FDP-009 operational rollback boundary.


---

# 6. ROLLBACK SAFETY CONDITION

Rollback authority does NOT mean:

    "CEO may select any older deployment."

It means:

    "CEO may restore the service to an already verified
     known-good deployment when operationally required."

Therefore:

    UNKNOWN / UNVERIFIED TARGET
        =
    NOT AN AUTHORIZED ROLLBACK TARGET


    KNOWN-GOOD / VERIFIED TARGET
        =
    POSSIBLE ROLLBACK TARGET


## 6.1 Current State

The current historical deployment:

    22c0b49

is classified as:

    NOT A VALID APPLICATION ROLLBACK TARGET

because the current verification established that it predates the current
application and would result in an unavailable/non-functional application
state.

Therefore Claude MUST NOT use `22c0b49` as a Production rollback target
merely because it is technically available in Vercel.


---

# 7. ROLLBACK TARGET REQUIREMENT

Before Production Release, AIOS must establish:

    CURRENT RELEASE
          │
          ▼
    VERIFIED KNOWN-GOOD TARGET
          │
          ▼
    ROLLBACK PROCEDURE
          │
          ▼
    EVIDENCE

The rollback target must be:

- deployable;
- compatible with the current Production state;
- verified;
- identifiable by immutable commit/deployment identity;
- documented;
- tested or otherwise evidenced according to the FS-10 rollback
  requirements.

If no valid rollback target exists, Claude MUST NOT fabricate one.

Instead:

    ROLLBACK READINESS
        =
    BLOCKED / CLASSIFIED

until a valid target is established.


---

# 8. EMERGENCY ROLLBACK

If Production has been Released and a severe operational failure occurs
while no valid rollback target exists:

Claude MUST NOT use an invalid historical deployment merely because
rollback is operationally desirable.

Claude must instead:

1. preserve evidence;
2. classify the incident;
3. use the existing failure/containment procedures;
4. determine whether a verified recovery target exists;
5. escalate if the recovery action exceeds delegated authority.

Rollback authority does not override evidence requirements.


---

# 9. ROLLBACK ≠ RELEASE

Rollback does NOT:

- authorize a new Release;
- authorize LIVE;
- change Founder Release Authority;
- change governance;
- certify a new version.

Rollback is an operational state transition.

Founder Release Authority remains separate.


---

# 10. FDP-010-03
# HISTORICAL FS-09 GATE / CURRENT GOVERNANCE RECONCILIATION

## 10.1 Problem

FS-10 verification identified that the closed FS-09 readiness gate still
contains wording stating that Production rollback is Founder-only.

FDP-009 subsequently established that operational rollback may be executed
by the delegated CEO within its defined boundary.

The historical FS-09 gate is closed and therefore MUST NOT be silently
rewritten to make history conform to later decisions.


## 10.2 Founder Decision

The historical FS-09 gate remains immutable historical evidence.

It MUST NOT be edited merely to remove the historical wording.

The current authoritative operational rule shall instead be represented
through a successor/current governance layer that explicitly states:

    FDP-009 / FDP-010
        supersede the historical rollback interpretation
        for CURRENT FS-10 operational execution.

The historical gate remains evidence of its state at the time it was
closed.


## 10.3 Current Authority

For current FS-10 operation:

    FDP-009
        +
    FDP-010

govern the current Production rollback boundary.

The closed FS-09 gate is historical.

Therefore:

    HISTORICAL GATE
        ≠
    CURRENT AUTHORITY


## 10.4 Required Reconciliation

Claude Code is authorized to:

- update current FS-10 operational documentation;
- update current readiness/authority documentation where necessary;
- add an explicit successor/current-authority reference;
- preserve the historical FS-09 gate unchanged;
- add tests that ensure current authority is represented correctly.

Claude Code MUST NOT:

- rewrite historical FS-09 evidence;
- alter historical test results;
- change closed-phase records;
- pretend that the old wording never existed.


## 10.5 Closure Condition

The inconsistency is considered reconciled when:

1. historical FS-09 wording remains preserved;
2. current FS-10 authority explicitly points to FDP-009/FDP-010;
3. no current execution path incorrectly interprets the historical wording
   as overriding FDP-009/FDP-010;
4. the distinction is documented;
5. governance/citation checks pass.


### Decision

    ESC-02 GOVERNANCE RECONCILIATION = RESOLVED

    FDP-010-03 = APPROVED


---

# 11. FDP-010-04
# PRODUCTION `AIOS_OPERATOR_TOKENS` RESIDUAL

## 11.1 Current State

Production currently retains:

    AIOS_OPERATOR_TOKENS = empty list

The execution established that:

- no operator token is currently active;
- Production is effectively without an operator token;
- temporary verification credentials have been revoked;
- no credential material was found in Production records.


## 11.2 Founder Decision

The empty `AIOS_OPERATOR_TOKENS` configuration is classified as:

    CONFIGURATION RESIDUAL

and NOT:

    ACTIVE ACCESS.


## 11.3 Cleanup

Claude Code is authorized to remove the empty Production variable if the
provider control plane permits deletion.

If the connector cannot delete it, the account holder may remove it
manually through the provider dashboard.

Deletion is preferred for configuration cleanliness but is NOT equivalent
to granting or revoking operational authority.


## 11.4 Security Boundary

The following remains mandatory:

    EMPTY TOKEN LIST
        =
    NO ACTIVE OPERATOR TOKEN

The variable MUST NOT be populated with a token merely to eliminate the
configuration residual unless that token is part of the approved permanent
operational-access model established by this Founder Decision.

No plaintext token may be placed in:

- repository;
- documentation;
- evidence;
- logs;
- chat.


### Decision

    FDP-010-04 = APPROVED


---

# 12. PERMANENT OPERATIONAL ACCESS MODEL

The resulting model is:

                         FOUNDER
                            │
                            │
              ┌─────────────┴─────────────┐
              │                           │
              ▼                           ▼
      Provider Account             Release Authority
      / Credentials                / LIVE Authority
              │                           │
              │                           │
              ▼                           ▼
      Production Access          Founder Release Gate
              │                           │
              ▼                           ▼
       Operational CEO             Production Release
       / AIOS Principal                    │
                                           ▼
                                          LIVE


These are separate authority domains.

Possessing:

    Production Access

does not grant:

    Release Authority.


---

# 13. OPERATIONAL CEO BOUNDARY

Within the established delegation, the CEO may:

- observe Production;
- operate Production;
- execute authorized operational procedures;
- perform incident response;
- perform authorized rollback;
- perform recovery;
- rotate operational credentials according to existing controls;
- maintain operational configuration;
- preserve evidence;
- update current operational documentation.

The CEO may NOT:

- release a new Production version without Founder Release Authorization;
- activate LIVE;
- modify Founder Authority;
- modify Governance Model;
- modify Constitution;
- modify Mission;
- reopen P12;
- reopen P13;
- reopen Platform Organization;
- create Phase 14;
- alter certified roots;
- expand Native Core;
- create authority through implementation.


---

# 14. FOUNDER RELEASE BOUNDARY

The Founder remains the authority for:

    Production Release

and:

    LIVE Activation

Therefore:

    OPERATIONAL ACCESS
        ↓
    does not imply
        ↓
    RELEASE


    ROLLBACK AUTHORITY
        ↓
    does not imply
        ↓
    RELEASE AUTHORITY


    PRODUCTION VERIFICATION PASS
        ↓
    does not imply
        ↓
    RELEASE AUTHORIZATION


    RELEASE AUTHORIZATION
        ↓
    does not automatically imply
        ↓
    future autonomous architectural authority


---

# 15. PRE-LIVE REQUIREMENTS

Before Founder Release Authorization is requested, Claude must ensure:

1. permanent operational access model is configured;
2. required operational scopes are verified;
3. temporary verification credentials remain revoked;
4. no unintended operator token remains active;
5. rollback target is valid and documented;
6. current rollback authority is reconciled;
7. historical FS-09 evidence remains immutable;
8. current FS-10 documentation points to FDP-009/FDP-010;
9. Production Release Package remains valid;
10. no unresolved blocking security or operational condition exists.

If the rollback target is not yet valid, the Release Package must explicitly
state:

    RELEASE READINESS
        =
    BLOCKED BY ROLLBACK READINESS

unless Founder explicitly decides otherwise through a later Founder
Decision.


---

# 16. NO AUTOMATIC LIVE AUTHORIZATION

Nothing in FDP-010 authorizes:

- Production Release;
- LIVE;
- public traffic;
- Operational AIOS activation.

The state remains:

    PRODUCTION DEPLOYED
    PRODUCTION VERIFIED
    RELEASE PACKAGE READY
    FOUNDER RELEASE AUTHORIZATION REQUIRED


---

# 17. REQUIRED EXECUTION AFTER REGISTRATION

After FDP-010 is canonically registered, Claude Code shall:

### Step 1
Re-discover FDP-009 and FDP-010.

### Step 2
Reconcile the current FS-10 operational documents.

### Step 3
Establish the permanent operational-access model.

### Step 4
Verify its scopes and negative controls.

### Step 5
Remove the empty `AIOS_OPERATOR_TOKENS` variable if the provider permits.

### Step 6
Preserve the historical FS-09 gate unchanged.

### Step 7
Create/update the current successor authority representation so that
FDP-009/FDP-010 are authoritative for current FS-10 operation.

### Step 8
Establish a valid known-good rollback target.

### Step 9
Verify rollback readiness against that target.

### Step 10
Run the required governance, citation and regression checks.

### Step 11
Update the Release Package with the resolved operational-access and
rollback state.

### Step 12
STOP.

The execution MUST NOT automatically continue to Production Release or LIVE.


---

# 18. FOUNDER DECISION SUMMARY

| Decision | Founder Resolution | Authority Result |
|---|---|---|
| ESC-01 | Permanent operational access permitted | CEO operational access, least privilege |
| ESC-02 | CEO may rollback after Release within bounded conditions | Operational authority |
| FDP-010-03 | Historical FS-09 gate remains immutable; current FDP-009/FDP-010 governs | Governance reconciled |
| FDP-010-04 | Empty Production operator-token variable classified as residual and authorized for cleanup | No active token implied |

Critical separation:

    Operational Access
        ≠
    Rollback Authority
        ≠
    Production Release
        ≠
    LIVE


---

# 19. FOUNDER RATIONALE

The purpose of this decision is to allow AIOS to operate safely after
Production Release without requiring Founder intervention for every
ordinary operational event.

At the same time, operational capability must not silently become release
authority.

The Founder therefore delegates bounded operational access and rollback
authority while retaining final control over:

    Production Release
    LIVE
    AIOS operational activation


---

# 20. FOUNDER AUTHORIZATION

Founder:

    Moriarty

Decisions:

    ESC-01
    RESOLVED

    ESC-02
    RESOLVED

    FDP-010-01
    APPROVED

    FDP-010-02
    APPROVED

    FDP-010-03
    APPROVED

    FDP-010-04
    APPROVED

Founder Authorization:

    GRANTED

Date:

    2026-10-01

Status:

    FOUNDER DECIDED
    PENDING CANONICAL REGISTRATION


---

# 21. CANONICALIZATION

This Founder Decision Record becomes authoritative only after completion
of the established canonical registration process.

Required:

    Persist verbatim
        ↓
    Compute content hash
        ↓
    Register
        ↓
    Re-discover
        ↓
    Reconcile current FS-10 authority
        ↓
    Verify hash
        ↓
    Canonical


---

# 22. FINAL AUTHORITY STATE

After canonical registration:

    PRODUCTION DEPLOYMENT
        = CEO AUTHORIZED

    PRODUCTION VERIFICATION
        = CEO AUTHORIZED

    OPERATIONAL ACCESS
        = CEO AUTHORIZED WITH BOUNDARY

    ROLLBACK
        = CEO AUTHORIZED WITH BOUNDARY

    PRODUCTION RELEASE
        = FOUNDER RESERVED

    LIVE
        = FOUNDER RESERVED

    FINAL SYSTEM ACCEPTANCE
        = FOUNDER RESERVED


No authority may be inferred beyond these classifications.
````
