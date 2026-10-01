# FDP-011 — Founder Decision Submission & S4 Resume Instruction (as received)

**Received:** from the Founder, 2026-10-01, in the message body: the Founder's decision text, then the submission and resume instruction. The decision instrument designated in its `§0` is persisted separately as `FDP-011-FS-10-ESC03-PER-SESSION-X2-OPERATIONAL-ACCESS.md`.

````text
FDP-011 — FOUNDER DECISION

D-1 — Mechanism:
O-A

D-1 Decision:
Founder authorizes E-A per-session bypass as the mechanism for carrying the delegated CEO Production operational principal (`aios-operator`) through X2 to the Production AIOS API.

The authorization is limited to a per-session automation-bypass mechanism. It does not authorize a standing bypass, permanent bypass, public exposure, Production Release, LIVE activation, traffic activation, or any change to Founder Release Authority.

The bypass exists only for an explicitly authorized operational session and must be revoked at the end of that session.

D-2 — Terms:

T1 — Environment:
Production only.

The mechanism is not authorized for Preview unless a separate authority is established.

T2 — Deployments:
The serving Production deployment and the designated verified rollback target.

Access to other Production deployments is not authorized unless they become the serving deployment or are explicitly designated as the verified rollback target within the existing FDP-010 authority.

T3 — Purpose:
All operational duties already authorized under FDP-010 §13, including:

- Production health verification;
- Production smoke verification;
- integration verification;
- post-deployment verification;
- post-rollback verification;
- authorized workflow execution;
- state and trace verification;
- audit verification;
- observability verification;
- operational rollback execution where already authorized by FDP-010;
- other directly related operational verification duties within the existing CEO authority envelope.

The mechanism does not expand the CEO's underlying capability or authority.

T4 — Duration:
Per session.

The bypass must not become standing access.

It must be revoked when the authorized operational session ends.

If the provider supports automatic expiry, the shortest practical expiry compatible with the authorized session should be used.

If automatic expiry behavior is not supported or cannot be verified, explicit end-of-session revocation and verification are mandatory.

T5 — Creation and custody:
The automation-bypass credential must be created through the provider-supported control plane by the authorized account holder.

The credential must be used only for the authorized operational session and must not be:

- committed to the repository;
- written into source code;
- written into documentation;
- written into evidence files;
- written into logs;
- exposed in chat;
- exposed in normal tool output;
- retained after the authorized session.

Credential custody must remain within an authorized secure execution/secret-handling path.

The credential value must never be included in Founder Decision records, Governance Register entries, execution records, evidence artifacts, or chat.

Whether direct credential transmission through tool output is permissible must remain subject to FDP-010 §11.4. If that path is not explicitly permitted, it must not be used.

T6 — Rotation:
Rotate for every new operational session.

Immediately rotate if:

- exposure is suspected;
- custody is uncertain;
- the credential is accidentally disclosed;
- the provider reports compromise;
- the authorized session boundary is violated.

T7 — Revocation:
Revoke:

1. at the end of every authorized operational session;
2. immediately upon suspected exposure;
3. immediately when the operational purpose is complete;
4. immediately if the mechanism is no longer required;
5. before any transition to an unauthorized access state.

Revocation must be independently verified.

Verification must include confirmation that the previously authorized path no longer passes X2, including the applicable 302/no-access control where supported by the provider.

T8 — Evidence:
For every operational session record, without recording the credential value:

- session identifier;
- operator subject;
- purpose;
- start time;
- end time;
- deployment targeted;
- designated rollback target if applicable;
- operations performed;
- relevant request/run identifiers;
- verification results;
- audit evidence;
- revocation event;
- revocation verification;
- final access state.

Credential values, secrets, tokens, or bypass values must never be recorded.

T9 — Relation to FDP-009-03:
Extended.

FDP-009-03 remains the governing temporary-access principle.

FDP-011 provides the specific Founder authorization and operational terms for the per-session X2 access mechanism.

Nothing in FDP-011 authorizes permanent bypass or overrides FDP-009-03's security and revocation requirements.

D-3 — Founder Principal:
P-2

Scopes:

- `aios.observe`
- `aios.workflow.run`
- `aios.audit`

No `aios.agent.register`.

The Founder principal is a separate human operational principal and must not be conflated with the delegated CEO `aios-operator` principal.

Release / LIVE:
Remain Founder-reserved.

Additional Founder Constraints:

1. X2 deployment protection remains enforced.
2. No standing or permanent bypass is authorized.
3. No public exposure is authorized.
4. The CEO operational principal does not acquire Release or LIVE authority.
5. Production Release remains subject to separate Founder Release Authorization.
6. LIVE activation remains subject to separate Founder authorization.
7. B3 remains unchanged and continues to govern operator authentication, scopes, hash-only credential storage, fail-closed behavior, auditability, and environment isolation.
8. No change is authorized to the Constitution, Governance Model, Founder Authority, Native Core, P12, P13, Platform Organization, or Phase structure.
9. The Founder principal and CEO delegated principal remain separate identities and separate authority subjects.
10. Any mechanism behavior not established by the current evidence must be verified before implementation rather than inferred.

# FDP-011 — FOUNDER DECISION SUBMISSION & S4 RESUME INSTRUCTION

## 0. FOUNDER DECISION

The Founder has now explicitly issued the following FDP-011 decision.

Do NOT reinterpret, optimize, rank, replace, or silently modify the Founder Decision.

Treat the following text as the Founder Decision instrument to be validated and canonicalized.

---

FDP-011 — FOUNDER DECISION

D-1 — Mechanism:
O-A

D-1 Decision:
Founder authorizes E-A per-session bypass as the mechanism for carrying the delegated CEO Production operational principal (`aios-operator`) through X2 to the Production AIOS API.

The authorization is limited to a per-session automation-bypass mechanism. It does not authorize a standing bypass, permanent bypass, public exposure, Production Release, LIVE activation, traffic activation, or any change to Founder Release Authority.

The bypass exists only for an explicitly authorized operational session and must be revoked at the end of that session.

D-2 — Terms:

T1 — Environment:
Production only.

The mechanism is not authorized for Preview unless a separate authority is established.

T2 — Deployments:
The serving Production deployment and the designated verified rollback target.

Access to other Production deployments is not authorized unless they become the serving deployment or are explicitly designated as the verified rollback target within the existing FDP-010 authority.

T3 — Purpose:
All operational duties already authorized under FDP-010 §13, including:

- Production health verification;
- Production smoke verification;
- integration verification;
- post-deployment verification;
- post-rollback verification;
- authorized workflow execution;
- state and trace verification;
- audit verification;
- observability verification;
- operational rollback execution where already authorized by FDP-010;
- other directly related operational verification duties within the existing CEO authority envelope.

The mechanism does not expand the CEO's underlying capability or authority.

T4 — Duration:
Per session.

The bypass must not become standing access.

The bypass must be revoked when the authorized operational session ends.

If the provider supports automatic expiry, the shortest practical expiry compatible with the authorized session should be used.

If automatic expiry behavior is not supported or cannot be verified, explicit end-of-session revocation and verification are mandatory.

T5 — Creation and custody:
The automation-bypass credential must be created through the provider-supported control plane by the authorized account holder.

The credential must be used only for the authorized operational session and must not be:

- committed to the repository;
- written into source code;
- written into documentation;
- written into evidence files;
- written into logs;
- exposed in chat;
- exposed in normal tool output;
- retained after the authorized session.

Credential custody must remain within an authorized secure execution/secret-handling path.

The credential value must never be included in Founder Decision records, Governance Register entries, execution records, evidence artifacts, or chat.

Whether direct credential transmission through tool output is permissible must remain subject to FDP-010 §11.4. If that path is not explicitly permitted, it must not be used.

T6 — Rotation:
Rotate for every new operational session.

Immediately rotate if:

- exposure is suspected;
- custody is uncertain;
- the credential is accidentally disclosed;
- the provider reports compromise;
- the authorized session boundary is violated.

T7 — Revocation:
Revoke:

1. at the end of every authorized operational session;
2. immediately upon suspected exposure;
3. immediately when the operational purpose is complete;
4. immediately if the mechanism is no longer required;
5. before any transition to an unauthorized access state.

Revocation must be independently verified.

Verification must include confirmation that the previously authorized path no longer passes X2, including the applicable 302/no-access control where supported by the provider.

T8 — Evidence:
For every operational session record, without recording the credential value:

- session identifier;
- operator subject;
- purpose;
- start time;
- end time;
- deployment targeted;
- designated rollback target if applicable;
- operations performed;
- relevant request/run identifiers;
- verification results;
- audit evidence;
- revocation event;
- revocation verification;
- final access state.

Credential values, secrets, tokens, or bypass values must never be recorded.

T9 — Relation to FDP-009-03:
Extended.

FDP-009-03 remains the governing temporary-access principle.

FDP-011 provides the specific Founder authorization and operational terms for the per-session X2 access mechanism.

Nothing in FDP-011 authorizes permanent bypass or overrides FDP-009-03's security and revocation requirements.

D-3 — Founder Principal:
P-2

Scopes:

- `aios.observe`
- `aios.workflow.run`
- `aios.audit`

No `aios.agent.register`.

The Founder principal is a separate human operational principal and must not be conflated with the delegated CEO `aios-operator` principal.

Release / LIVE:
Remain Founder-reserved.

Additional Founder Constraints:

1. X2 deployment protection remains enforced.
2. No standing or permanent bypass is authorized.
3. No public exposure is authorized.
4. The CEO operational principal does not acquire Release or LIVE authority.
5. Production Release remains subject to separate Founder Release Authorization.
6. LIVE activation remains subject to separate Founder authorization.
7. B3 remains unchanged and continues to govern operator authentication, scopes, hash-only credential storage, fail-closed behavior, auditability, and environment isolation.
8. No change is authorized to the Constitution, Governance Model, Founder Authority, Native Core, P12, P13, Platform Organization, or Phase structure.
9. The Founder principal and CEO delegated principal remain separate identities and separate authority subjects.
10. Any mechanism behavior not established by the current evidence must be verified before implementation rather than inferred.

---

# 1. ENTER S4 — FOUNDER DECISION VALIDATION

First re-discover:

- FDP-009
- FDP-010
- ESC-03
- AD-FS10-ESC03
- FS-10-ESC03 Founder Decision Package
- current FS-10 authority
- X2
- B3
- current Production state
- current rollback target
- Governance Decision Register

Then validate the Founder Decision against the decision package.

Do NOT immediately implement.

---

# 2. VALIDATION REQUIREMENTS

Verify that:

1. D-1 is one of the package-authorized choices.
2. O-A corresponds exactly to E-A.
3. D-2 T1–T9 are explicitly populated.
4. D-3 is explicitly populated.
5. Release/LIVE remains Founder-reserved.
6. No term silently expands the underlying CEO capability.
7. No term silently changes B3.
8. No term silently changes X2 architecture beyond the authorized per-session mechanism.
9. No term conflicts with higher canonical authority.
10. No term contradicts FDP-009 or FDP-010 except where explicitly intended by T9.

If any contradiction or ambiguity is found:

STOP.

Report the exact conflict.

Do not modify the Founder Decision to resolve it yourself.

---

# 3. FDP-011 CANONICALIZATION

If validation passes:

1. Persist FDP-011 exactly as issued.
2. Do not rewrite its semantics.
3. Compute its content hash.
4. Register it at the next Governance Decision Register position.
5. Preserve the Founder Decision Package unchanged.
6. Link FDP-011 to the package.
7. Record canonical registration evidence.
8. Re-discover FDP-011 after registration.
9. Confirm hash consistency.
10. Update current FS-10 authority documentation.

The current expected next Register position is §117 unless re-discovery shows another canonical entry has legitimately occupied that position.

Do not overwrite existing Register content.

---

# 4. DERIVE THE IMPLEMENTATION ENVELOPE

Derive the implementation envelope from:

- higher canonical authority;
- FDP-009;
- FDP-010;
- FDP-011;
- existing X2;
- existing B3.

Classify every implementation action.

Anything not explicitly authorized remains:

UNKNOWN AUTHORITY / NOT AUTHORIZED.

---

# 5. S5 — IMPLEMENT O-A ONLY

Only after FDP-011 is canonical:

Implement E-A / O-A:

- per-session;
- Production only;
- serving deployment and designated verified rollback target only;
- no standing bypass;
- no permanent bypass;
- no public exposure;
- no Release;
- no LIVE.

Do not implement O-B, O-C, O-D, O-E or O-G.

Do not create any alternative access path.

---

# 6. CREDENTIAL SAFETY

The bypass credential must never appear in:

- repository;
- source code;
- Markdown;
- JSON evidence;
- Governance Register;
- logs;
- terminal output;
- chat;
- commit messages.

Do not read or print the secret merely to prove that it exists.

Use secure provider-supported handling.

If the available execution environment cannot safely handle the credential without violating FDP-010 §11.4:

STOP.

Do not improvise another mechanism.

---

# 7. VERIFY O-A

Positive controls:

- anonymous request remains blocked by X2;
- `aios-operator` without bypass remains blocked;
- authorized per-session bypass permits the intended request;
- B3 authenticates the operator;
- authorized scopes work;
- unauthorized scopes fail;
- Agent registration remains denied;
- Production API access works only during the authorized session.

Negative controls:

- Preview credential/path rejected;
- unauthorized principal rejected;
- expired/revoked bypass rejected;
- bypass alone does not bypass B3;
- B3 alone does not bypass X2;
- operational principal cannot Release;
- operational principal cannot activate LIVE;
- public access is not created.

---

# 8. SESSION REVOCATION

At the end of verification:

1. Revoke the session bypass.
2. Verify revocation.
3. Confirm the same previously authorized request is blocked again by X2.
4. Confirm no temporary bypass remains.
5. Confirm no permanent bypass exists.
6. Confirm no credential remains in repository, logs, evidence or working artifacts.
7. Record only metadata/evidence, never the secret.

---

# 9. FOUNDER PRINCIPAL — P-2

Establish the Founder Production principal only according to the exact FDP-011 terms.

Required scopes:

- `aios.observe`
- `aios.workflow.run`
- `aios.audit`

Must NOT have:

- `aios.agent.register`

Founder principal must remain distinct from:

- CEO `aios-operator`;
- Release Authorization;
- LIVE authority.

Verify:

- correct environment;
- correct scopes;
- authentication;
- authorization;
- audit identity;
- negative controls;
- revocation.

Do not use the Founder principal as a substitute for the CEO delegated principal.

---

# 10. S6 — COMPLETE FDP-010

After O-A is implemented and verified:

Re-evaluate FDP-010.

ESC-01:
PASS only if permanent operational access is usable within its authorized boundary.

ESC-02:
PASS only if verified rollback target and rollback authority are operationally reachable.

ESC-03:
PASS only if O-A is demonstrably usable through X2 and all required security/revocation evidence exists.

Do not declare FDP-010 complete merely because O-A was implemented.

---

# 11. S7 — INTEGRATION VERIFICATION

Verify:

Founder Authority
→ FDP-011
→ X2
→ O-A per-session access
→ B3
→ Production API
→ Runtime
→ Execution
→ State
→ Trace
→ Audit

Verify both successful and denied paths.

---

# 12. S8 — FINAL FS-10 RECONCILIATION

Re-discover everything.

Confirm:

- FDP-009 canonical;
- FDP-010 complete;
- FDP-011 canonical;
- ESC-01 PASS;
- ESC-02 PASS;
- ESC-03 PASS;
- X2 preserved;
- B3 preserved;
- Production verified;
- rollback ready;
- Release Package current;
- historical records preserved;
- no stale authority wording;
- no contradictory current rule;
- no credential leakage;
- no standing bypass;
- no permanent bypass.

---

# 13. S9 — FINAL FOUNDER RELEASE GATE

If all requirements pass:

Set final state to:

FS-10 READY
PRODUCTION VERIFIED
RELEASE PACKAGE READY
FOUNDER RELEASE AUTHORIZATION REQUIRED

Do NOT:

- Release;
- activate LIVE;
- open public traffic;
- infer Founder Release Authorization;
- declare Operational AIOS;
- create Phase 14;
- modify P12/P13;
- modify certified roots.

---

# 14. HARD STOP CONDITIONS

STOP immediately if:

- FDP-011 conflicts with higher authority;
- O-A cannot be safely implemented;
- provider behavior differs from evidence;
- credential custody cannot satisfy FDP-010 §11.4;
- X2 must be permanently weakened;
- a standing bypass is required;
- public exposure is required;
- B3 must be weakened;
- Release/LIVE authority would be affected;
- Founder principal requires scopes outside FDP-011;
- rollback cannot be verified;
- evidence cannot be produced;
- credential leakage occurs;
- any action requires authority not contained in FDP-011 or existing canonical authority.

Do not solve any of these by inference.

---

# 15. FINAL REPORT

Report:

- FDP-011 validation result;
- canonical hash;
- Register section;
- O-A implementation result;
- X2 result;
- B3 result;
- Founder principal result;
- ESC-01;
- ESC-02;
- ESC-03;
- security controls;
- negative controls;
- revocation evidence;
- rollback evidence;
- FDP-010 status;
- FS-10 status;
- Release Package status;
- Release status;
- LIVE status;
- evidence files;
- commits;
- regression results;
- citation audit;
- any remaining Founder-reserved matter.

The only acceptable final states are:

A. BLOCKED — AUTHORITY / SECURITY / EVIDENCE / CANONICAL CONFLICT

B. FDP-011 CANONICALIZED — IMPLEMENTATION IN PROGRESS

C. FDP-010 COMPLETED — FS-10 RECONCILIATION IN PROGRESS

D. FS-10 READY — FOUNDER RELEASE AUTHORIZATION REQUIRED

Never report Release or LIVE as active unless a separate Founder Release Authorization explicitly exists.
````
