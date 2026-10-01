# Master Instruction — AIOS FS-10 — FDP-011 Founder Decision Completion & Resume Gate (as received)

**Received:** from the Founder, 2026-10-01, in the message body. Its final hard stop limited the response to presenting the FDP-011 decision surface, so it is persisted here on the arrival of FDP-011 (Register `§117`).

````text
# MASTER INSTRUCTION — AIOS FS-10 — FDP-011 FOUNDER DECISION COMPLETION & RESUME GATE

## 0. PURPOSE

Lanjutkan AIOS FS-10 dari kondisi terakhir setelah:

MASTER INSTRUCTION —
AIOS FS-10 — ESC-03 AUTHORITY RESOLUTION →
FOUNDER DECISION →
FDP-010 COMPLETION →
FS-10 FINAL RECONCILIATION

Execution terakhir berhenti secara benar pada:

STATE A — EXECUTION COMPLETE — FOUNDER DECISION REQUIRED

Current state:

- S0 COMPLETE
- S1 COMPLETE
- S2 COMPLETE
- S3 ACTIVE / HARD STOP
- S4 NOT ENTERED
- S5 NOT ENTERED
- S6 NOT ENTERED
- S7 NOT ENTERED
- S8 NOT ENTERED
- S9 NOT ENTERED

ESC-01 = resolved
ESC-02 = resolved
ESC-03 = unresolved

FDP-009 = canonical
FDP-010 = canonical but NOT COMPLETE because ESC-03 remains unresolved

X2 = preserved
B3 = preserved
Production = deployed and verified
Release Package = ready
Production Release = NOT AUTHORIZED
LIVE = NOT ACTIVE

The Founder Decision Package has already been prepared at:

docs/fullstack/decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE-COMPLETE.md

The package contains the complete decision surface for FDP-011.

Your task is NOT to choose the access mechanism.

Your task is to:

1. Read the complete Founder Decision Package.
2. Present the exact decision surface to the Founder.
3. Allow the Founder to make FDP-011.
4. Do not infer, recommend, rank, or silently select any option.
5. Only after an explicit Founder Decision exists, enter S4.
6. Canonicalize and resume execution only within the exact authority granted by FDP-011.

---

# 1. ABSOLUTE GOVERNANCE RULE

The current authority state is:

UNKNOWN / UNDECIDED MECHANISM
→ NOT AUTHORIZED.

The following are prohibited before explicit Founder Decision:

- selecting E-A through E-F;
- selecting O-A through O-H;
- selecting a combination;
- choosing terms T1–T9;
- choosing Founder principal P-1/P-2/P-3;
- implementing any Production X2 access mechanism;
- changing X2;
- changing B3;
- creating a permanent bypass;
- creating a new credential mechanism;
- changing deployment protection;
- modifying Release/LIVE authority;
- declaring ESC-03 resolved;
- completing FDP-010;
- entering S4;
- entering S5;
- entering S6;
- entering S7;
- entering S8;
- entering S9.

Technical feasibility is NOT authorization.

Provider capability is NOT authorization.

Founder silence is NOT authorization.

Claude recommendation is NOT authorization.

---

# 2. FIRST ACTION — READ THE COMPLETE PACKAGE

Before asking the Founder for a decision:

READ:

docs/fullstack/decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE-COMPLETE.md

Do not rely only on the previous execution summary.

Extract the exact:

- evidence basis;
- canonical constraints;
- decision questions;
- O-A through O-H definitions;
- T1 through T9 terms;
- P-1 through P-3 Founder principal choices;
- consequences of each choice;
- unresolved evidence limitations;
- security constraints;
- X2 constraints;
- B3 constraints;
- Release/LIVE firewall;
- implementation boundaries.

Do not rewrite the options in a way that changes their meaning.

Do not add new options unless the package itself explicitly permits "another mechanism/combination".

Do not remove options.

Do not rank options.

Do not label an option as best, preferred, recommended, safer, simpler, or optimal.

---

# 3. RECONFIRM THE DECISION SCOPE

Before the Founder decides, explicitly establish:

## D-1 — PRODUCTION OPERATIONAL ACCESS MECHANISM

The Founder decides whether and how delegated CEO operational access may pass through X2.

This decision is about the ACCESS MECHANISM.

It does not automatically authorize:

- Production Release;
- LIVE;
- public exposure;
- permanent deployment bypass;
- changes to Founder authority;
- changes to B3 scopes;
- changes to AIOS Governance;
- Phase 14;
- Native Core #12;
- reopening P12/P13;
- modification of certified roots.

---

## D-2 — TERMS / BOUNDARIES

The Founder decides the applicable terms required by the selected mechanism, using the package's T1–T9 structure.

Preserve the exact package terminology.

Do not fill unspecified terms by inference.

If the Founder leaves a term unresolved, classify it as unresolved rather than inventing a value.

---

## D-3 — FOUNDER'S OWN PRODUCTION PRINCIPAL

The Founder decides among the exact P-1/P-2/P-3 choices in the package.

Do NOT conflate:

Founder operational access

with:

CEO delegated operational access.

They are separate authority subjects.

---

# 4. FOUNDER DECISION INTERFACE

Present the Founder with the exact decision surface from the package.

Use this structure:

## FDP-011 — FOUNDER DECISION

### D-1 — Mechanism
Founder selection:
`[exact O-A–O-H choices from package]`

### D-2 — Terms
Founder decisions:
- T1:
- T2:
- T3:
- T4:
- T5:
- T6:
- T7:
- T8:
- T9:

### D-3 — Founder Principal
Founder selection:
`[exact P-1/P-2/P-3 choices from package]`

### Additional Founder Constraints
Any additional explicit Founder condition must be recorded verbatim.

---

# 5. NO MANUFACTURED DECISION

If the Founder has not explicitly supplied the decision:

STOP.

Do NOT:

- create FDP-011 as decided;
- register FDP-011;
- hash FDP-011 as canonical;
- implement;
- modify Production;
- modify X2;
- modify B3;
- declare ESC-03 resolved.

The correct state remains:

STATE A — FOUNDER DECISION REQUIRED

---

# 6. IF FOUNDER PROVIDES A DECISION

Only when the Founder explicitly provides D-1, D-2 and D-3:

Enter:

S4 — FOUNDER DECISION CANONICALIZATION

Then:

1. Compare the Founder response against the exact package.
2. Detect ambiguity.
3. Detect contradictory terms.
4. Detect missing mandatory decisions.
5. Detect scope expansion.
6. Detect any instruction that conflicts with higher canonical authority.

If ambiguous:

STOP and identify the ambiguity.

If contradictory:

STOP and identify the conflict.

If complete and valid:

Persist FDP-011 exactly as decided.

Do not improve the Founder wording in a way that changes meaning.

---

# 7. FDP-011 CANONICALIZATION

After a valid Founder Decision:

- persist the decision record;
- preserve exact Founder decision semantics;
- generate content hash;
- register it in the Governance Decision Register;
- record the canonical registration;
- preserve the original Founder Decision Package;
- link the package to FDP-011;
- update current FS-10 authority documentation;
- perform mandatory re-discovery.

Do not modify historical Founder Decisions.

Do not rewrite FDP-009.

Do not rewrite FDP-010.

Do not modify historical FS-09.

Do not modify P12/P13 certified roots.

---

# 8. ESTABLISH THE IMPLEMENTATION ENVELOPE

After FDP-011 becomes canonical:

derive the implementation envelope ONLY from:

1. higher canonical authority;
2. FDP-009;
3. FDP-010;
4. FDP-011;
5. existing X2;
6. existing B3;
7. the exact Founder terms.

Explicitly classify:

- AUTHORIZED
- AUTHORIZED WITH BOUNDARY
- REQUIRES FOUNDER DECISION
- CONFLICT
- OUTSIDE AUTHORITY
- UNKNOWN AUTHORITY

Anything not clearly authorized remains unauthorized.

---

# 9. ONLY THEN ENTER S5

If and only if FDP-011 is canonical and implementation authority is clear:

S5 — AUTHORIZED IMPLEMENTATION

Implement ONLY the mechanism explicitly authorized by FDP-011.

Mandatory preservation:

### X2
- deployment protection remains intact unless FDP-011 explicitly and validly authorizes an architecture change;
- no standing bypass unless explicitly authorized and compatible with canonical authority;
- no public exposure;
- no silent protection weakening.

### B3
- hash-only credentials;
- least privilege;
- existing scope boundaries;
- fail-closed behavior;
- auditability;
- revocability;
- environment isolation.

### Release/LIVE firewall
Operational access MUST NOT become:

- Release authority;
- LIVE authority;
- Founder Release Authorization;
- public traffic authority.

---

# 10. FDP-010 COMPLETION

After ESC-03 mechanism is implemented and verified:

Complete the EXISTING FDP-010.

Do NOT create "FDP-010 v2".

Verify:

### ESC-01
Permanent Production operational principal exists and works within its authorized boundary.

### ESC-02
Rollback authority exists according to FDP-010.

A rollback target must be:

- known-good;
- verified;
- reachable through authorized operational access;
- compatible with current AIOS architecture.

Do not use `22c0b49` merely because it is historical.

### ESC-03
Authorized Production operational access through X2 is demonstrably usable.

ESC-03 is not resolved merely because a mechanism exists.

It must be:

- implemented;
- reachable;
- authenticated;
- authorized;
- auditable;
- revocable;
- least-privileged;
- environment-correct;
- tested.

---

# 11. SECURITY VERIFICATION

Run both positive and negative controls.

At minimum verify:

- authorized operational access succeeds;
- unauthorized access fails;
- wrong environment fails;
- insufficient scope fails;
- unauthorized Agent registration fails;
- Release authority cannot be obtained through operational access;
- LIVE cannot be activated through operational access;
- X2 remains enforced;
- B3 remains enforced;
- credentials are not exposed;
- audit records identify the operational principal;
- revocation works;
- temporary access, if any, is removed;
- no public exposure is introduced.

Do not claim success from implementation alone.

---

# 12. ROLLBACK VERIFICATION

Verify the currently authorized rollback path.

The rollback verification must establish:

- current deployment;
- known-good rollback target;
- target availability;
- target identity;
- target verification evidence;
- authorization boundary;
- rollback procedure;
- post-rollback verification procedure;
- recovery path.

Do not claim rollback readiness if the target cannot actually be reached or verified.

---

# 13. S6 — FDP-010 COMPLETION GATE

Declare FDP-010 complete only when:

- ESC-01 PASS;
- ESC-02 PASS;
- ESC-03 PASS;
- all required evidence exists;
- all required authority is canonical;
- no unresolved Founder Decision remains inside FDP-010;
- no unresolved X2 conflict remains;
- no security regression exists;
- final re-discovery passes.

Otherwise:

STOP and classify the remaining blocker.

---

# 14. S7 — INTEGRATION VERIFICATION

After FDP-010 completion:

Verify the complete chain:

Founder Authority
→ FDP-011
→ X2
→ Operational Access
→ B3
→ Production API
→ Runtime
→ Execution
→ State
→ Trace
→ Audit

Also verify negative paths.

The verification must distinguish:

- technical capability;
- operational authorization;
- governance authorization;
- Release authority;
- LIVE authority.

---

# 15. S8 — FINAL FS-10 RECONCILIATION

Perform final re-discovery.

Verify:

- FDP-009 canonical;
- FDP-010 complete;
- FDP-011 canonical;
- ESC-01 resolved;
- ESC-02 resolved;
- ESC-03 resolved;
- X2 preserved;
- B3 preserved;
- Production verified;
- rollback ready;
- Release Package current;
- historical records preserved;
- current authority documents reconciled;
- no stale contradictory operational rule remains.

Any contradiction must be classified and resolved before declaring FS-10 ready.

---

# 16. S9 — FOUNDER RELEASE GATE

If all FS-10 requirements pass:

Final state MUST be:

FS-10 READY
+
PRODUCTION VERIFIED
+
RELEASE PACKAGE READY
+
FOUNDER RELEASE AUTHORIZATION REQUIRED

Do NOT:

- Release;
- activate LIVE;
- declare Operational AIOS;
- infer Founder Release Authorization;
- open public traffic;
- create Phase 14;
- reopen P12/P13;
- modify certified roots.

The final Release/LIVE decision remains a separate Founder action.

---

# 17. NO MICRO-ACT RULE

Do not create additional Micro-Acts merely to perform work already authorized by canonical FDP-011/FDP-010.

Use the established execution envelope.

Create a new Founder Decision only if a genuinely Founder-reserved matter remains unresolved.

---

# 18. FINAL REPORT

At the end report exactly:

### STATE
One of:

A. FOUNDER DECISION REQUIRED
B. FOUNDER DECISION CANONICALIZED — IMPLEMENTATION AUTHORIZED
C. FDP-010 COMPLETED — FS-10 RECONCILIATION IN PROGRESS
D. FS-10 READY — FOUNDER RELEASE AUTHORIZATION REQUIRED
E. BLOCKED — AUTHORITY / SECURITY / EVIDENCE / CANONICAL CONFLICT

### Include

- FDP-011 status
- D-1 decision
- D-2 terms
- D-3 Founder principal
- canonical hash
- Register section
- ESC-01
- ESC-02
- ESC-03
- X2 status
- B3 status
- Production status
- rollback status
- security verification
- negative controls
- Release Package status
- Release status
- LIVE status
- remaining Founder-reserved decisions, if any
- commit
- evidence files
- regression results
- citation audit

Do not compress unresolved matters into "non-blocking" if they prevent the required state transition.

---

# FINAL HARD STOP

If Founder Decision has not yet been explicitly supplied:

DO NOTHING BEYOND PRESENTING THE EXACT FDP-011 DECISION SURFACE.

NO SELECTION.
NO IMPLEMENTATION.
NO CANONICALIZATION.
NO FDP-010 COMPLETION.
NO RELEASE.
NO LIVE.

The Founder must decide first.
````
