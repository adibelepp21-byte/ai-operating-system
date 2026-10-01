# `FDP-011` — FS-10 ESC-03 Production Operational Edge Access: Founder Decision Record (as issued)

**Issued:** by the Founder, 2026-10-01, in the message body, together with the *"FDP-011 — Founder Decision Submission & S4 Resume Instruction"*, whose `§0` designates the text below as *"the Founder Decision instrument to be validated and canonicalized"*.
**Answers:** `docs/fullstack/decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE-COMPLETE.md` (kept unchanged).
**Variance:** the same message also opens with an undesignated copy of the decision. It differs in one line only (T4: *"It must be revoked…"* against *"The bypass must be revoked…"*), with the same meaning. The designated text is reproduced here, as issued.

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
````
