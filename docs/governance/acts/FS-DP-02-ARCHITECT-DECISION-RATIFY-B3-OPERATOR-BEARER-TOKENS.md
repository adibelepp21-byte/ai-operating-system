# `FS-DP-02-ARCHITECT-DECISION` — FS-DP-02 Architect Decision: B3 Operator Bearer Tokens (as received)

**Received:** from the Architect (Moriarty), 2026-09-27, in the message body,
under `ACT-CC-POST-P13-AIOS-FULL-STACK-003`.
**Stated decision:** *"Decision: RATIFY"*, *"Option: B3 — Operator Bearer
Tokens"*, *"Authority: Architect"*. It authorizes authentication only: not an
authorization redesign, not multi-user identity, not production release
(`§5`, `§6`).

Register `§81` records the decision.

Reproduced below as received. The message's formatting is kept as sent,
including a code fence opened in `§3.6` and not closed.

````text
# FS-DP-02 — ARCHITECT DECISION
## B3 — OPERATOR BEARER TOKENS

Document Type:
Architect Decision Record

Decision ID:
FS-DP-02-ARCHITECT-DECISION

Parent Package:
FS-08-ACT-003-EXECUTION-RECORD.md

Parent Decision Surface:
FS-DP-02 — Authentication Architecture

Status:
RATIFIED

Authority:
Architect

Decision:
RATIFY

Option:
B3 — Operator Bearer Tokens


---

# 1. ARCHITECT DECISION

The Architect hereby RATIFIES:

> **B3 — Operator Bearer Tokens**

as the authentication architecture for the current AIOS Full Stack FS-DP-02 boundary.

This decision authorizes implementation and verification of an operator bearer-token authentication boundary for protected Full Stack API access.

The decision is intentionally bounded.

It does not authorize a general identity architecture redesign, multi-user identity system, authorization redesign, or production release.


---

# 2. ARCHITECTURAL CONTEXT

The current Full Stack console already uses a bearer-token request model.

The FS-DP-02 discovery identified that:

1. protected API access requires an explicit authentication boundary;
2. the existing console flow already provides a bearer-token surface;
3. Supabase Auth / ES256 verification would introduce an additional cryptographic/dependency path not presently established by the current Python stdlib implementation;
4. B3 provides a bounded operator authentication mechanism compatible with the existing Full Stack boundary;
5. multi-user identity can remain an evolutionary concern and is not required to resolve the present FS-DP-02 requirement.

Therefore the Architect selects B3 as the current bounded authentication architecture.


---

# 3. AUTHORIZED ARCHITECTURAL SCOPE

The following are AUTHORIZED under this decision:

### 3.1 Operator Authentication

Implement operator authentication using bearer tokens.

### 3.2 Token Verification

The backend MUST verify the supplied bearer credential before allowing access to protected endpoints.

### 3.3 Credential Storage

The server-side representation MUST use token hashes rather than storing plaintext operator bearer tokens.

Plaintext bearer tokens MUST NOT be persisted as server-side credential records.

### 3.4 Existing Console Contract

The existing console bearer-token request model may remain the client-side authentication mechanism.

No unnecessary frontend authentication redesign is authorized.

### 3.5 Protected API Boundary

Protected Full Stack API routes MUST enforce authentication.

Authentication MUST occur before protected operation is permitted.

### 3.6 Fail-Closed Authentication

The authentication boundary MUST fail closed.

At minimum:

```text
missing credential
        ↓
REJECT

invalid credential
        ↓
REJECT

malformed credential
        ↓
REJECT

valid operator credential
        ↓
ALLOW
The implementation MUST NOT silently treat authentication failure as anonymous authorization.
3.7 Preview Verification
The implementation may be deployed to the authorized Preview environment for verification.
Preview verification is part of FS-08 evidence.
It does NOT constitute Production Release Authorization.
 
⸻
 
4. AUTHENTICATION MODEL
The intended bounded model is:
Operator
   │
   │ bearer token
   ▼
Full Stack API
   │
   ▼
Authentication Boundary
   │
   ├── missing → REJECT
   ├── invalid → REJECT
   └── valid
          │
          ▼
       Protected API
Credential persistence:
Operator Token
      │
      ▼
Server-side credential representation
      │
      ▼
Token Hash
Do NOT persist the plaintext bearer token as the server-side credential record.
 
⸻
 
5. AUTHORIZATION BOUNDARY
This decision authorizes AUTHENTICATION.
It does NOT redesign AUTHORIZATION.
Maintain the distinction:
Authentication
    =
Who/what supplied a valid credential?

Authorization
    =
Is that authenticated actor permitted to perform this action?
Any existing authorization boundary must remain intact.
Do not introduce a new role/permission model merely to implement B3 unless an existing contract explicitly requires it.
If implementation discovers that B3 cannot be correctly implemented without a material authorization redesign, STOP at that boundary and escalate rather than silently expanding scope.
 
⸻
 
6. EXPLICITLY NOT AUTHORIZED
This decision does NOT authorize:
1. Multi-user identity architecture
2. Supabase Auth adoption
3. General identity-provider integration
4. Role architecture redesign
5. Permission architecture redesign
6. Authorization policy redesign
7. Agent identity architecture
8. Founder identity architecture
9. Capability expansion
10. New Native Core component
11. Native Core #12
12. New Planner architecture
13. Scheduler architecture
14. Execution Orchestrator architecture
15. Runtime architecture redesign outside the authentication boundary
16. Generic persistence redesign
17. Database schema redesign unrelated to B3
18. Production release
19. Founder Release Authorization
20. Modification of certified P1–P13 roots
21. Reopening P13
22. Phase 14
23. Reopening closed Platform Organization
Unknown requirements MUST NOT be treated as implicitly authorized.
 
⸻
 
7. IMPLEMENTATION BOUNDARY
Implementation MUST remain limited to the smallest surface required to satisfy B3.
Before modifying code:
1. read the current FS-DP-02 package;
2. inspect the current authentication/request path;
3. inspect existing protected-route behavior;
4. inspect existing token handling;
5. identify the minimum implementation surface;
6. preserve existing public contracts unless a contract change is strictly required.
Do not perform unrelated refactoring.
Do not redesign the Full Stack architecture while implementing B3.
 
⸻
 
8. REQUIRED SECURITY PROPERTIES
The implementation MUST demonstrate:
S1 — Missing Credential Rejection
A protected endpoint without a bearer credential is rejected.
S2 — Invalid Credential Rejection
A protected endpoint supplied with an invalid credential is rejected.
S3 — Malformed Credential Rejection
Malformed authentication input is rejected safely.
S4 — Valid Credential Acceptance
A valid operator credential is accepted.
S5 — No Plaintext Credential Persistence
Server-side persistent credential material is represented by a hash, not plaintext bearer-token storage.
S6 — Protected Route Enforcement
Authentication cannot be bypassed by directly invoking a protected route.
S7 — Fail Closed
Authentication failures do not fall through to protected execution.
S8 — Existing Console Compatibility
The existing bearer-token console flow continues to function.
S9 — No Authentication Side Door
No alternate unauthenticated path may provide equivalent protected access.
S10 — Secret Boundary
Secrets MUST NOT be committed into source control, logs, test fixtures, generated artifacts, or public responses.
 
⸻
 
9. VERIFICATION CONTRACT
The implementation is not complete merely because code exists.
The following verification matrix MUST be executed:
ID	Verification	Required Result
V1	Missing bearer token	PASS — rejected
V2	Invalid bearer token	PASS — rejected
V3	Malformed bearer token	PASS — rejected
V4	Valid operator bearer token	PASS — accepted
V5	Protected route enforcement	PASS
V6	No plaintext token persistence	PASS
V7	Authentication fail-closed behavior	PASS
V8	Existing console authentication flow	PASS
V9	No unauthenticated bypass	PASS
V10	Existing Full Stack regression	PASS
V11	Existing governance regression	PASS
V12	Certified-root integrity	PASS
V13	Security negative controls	PASS
V14	Preview authentication verification	PASS, once authorized Preview access exists
All failures MUST be recorded.
Do not convert an unresolved failure into PASS by changing the test expectation without architectural justification.
 
⸻
 
10. NEGATIVE CONTROLS
Verification MUST explicitly demonstrate that the implementation did NOT:
NC-01  Create Native Core #12
NC-02  Modify Native Core #11
NC-03  Modify certified P1–P13 roots
NC-04  Reopen P13
NC-05  Create Phase 14
NC-06  Expand Architect authority
NC-07  Expand Founder/CEO authority
NC-08  Introduce multi-user identity architecture
NC-09  Introduce Supabase Auth without separate authority
NC-10  Redesign authorization
NC-11  Introduce unrelated persistence architecture
NC-12  Create an unauthenticated protected-route bypass
NC-13  Persist plaintext bearer tokens
NC-14  Expose bearer credentials through logs or responses
NC-15  Modify unrelated Full Stack contracts
NC-16  Convert Preview verification into Production Release
Expected result:
HELD = all applicable controls
FAILED = 0
If a control cannot be exercised, report it as NOT EXERCISED rather than claiming PASS.
 
⸻
 
11. TESTING REQUIREMENT
Run targeted FS-DP-02 tests first.
Then run the required regression suites applicable to the changed surface.
At minimum report:
FS-DP-02 targeted tests
Full Stack regression
Governance regression
Security-related tests
Citation / governance index checks where applicable
Certified-root integrity checks
If an unrelated pre-existing failure appears, classify it explicitly rather than silently changing it.
 
⸻
 
12. EXTERNAL / PREVIEW BOUNDARY
The following external dependency remains separate from this Architect Decision:
EXT-03
Preview access / Vercel deployment protection
This decision does NOT authorize bypassing Vercel authentication or deployment protection.
If Preview access remains blocked:
LOCAL IMPLEMENTATION
        ↓
LOCAL VERIFICATION
        ↓
PREVIEW VERIFICATION = BLOCKED
Record the dependency honestly.
Do not claim Preview PASS without actual Preview evidence.
 
⸻
 
13. SUPABASE / SECRET BOUNDARY
If the implementation requires:
AIOS_OPERATOR_TOKENS
or equivalent operator-token configuration, determine the exact required configuration from the existing package and implementation.
Do not invent a new secret format if an existing contract already defines one.
Any required operator-token hashes may be supplied/configured through the authorized Preview environment.
Do NOT:
* place plaintext production/operator tokens in Git;
* place tokens in source files;
* place tokens in test fixtures;
* expose tokens in logs;
* expose tokens in API responses.
If Founder-side configuration is required, report it as an external dependency.
Do not infer the secret value.
 
⸻
 
14. RELATION TO FS-08
B3 implementation and verification are one prerequisite for the FS-08 Final Gate.
The lifecycle is:
ARCHITECT DECISION
        │
        ▼
B3 IMPLEMENTATION
        │
        ▼
LOCAL VERIFICATION
        │
        ▼
PREVIEW VERIFICATION
        │
        ▼
FS-DP-02 VERIFIED
        │
        ▼
FS-08 FINAL RECONCILIATION
Do not declare FS-08 PASS solely because B3 is ratified.
The following remain distinct:
Architect Decision
≠
Implementation
≠
Verification
≠
FS-08 Gate
≠
FS-09 Readiness
≠
Deployment
≠
Production Verification
≠
Founder Release Authorization
 
⸻
 
15. REQUIRED RECORDING
Persist this Architect Decision in the canonical FS-08 decision/evidence location.
The implementation record MUST contain:
Decision ID:
FS-DP-02-ARCHITECT-DECISION

Parent:
FS-08-ACT-003

Option:
B3 — Operator Bearer Tokens

Decision:
RATIFY

Authority:
Architect

Implementation:
[commit/hash]

Verification:
[exact test results]

Security verification:
[results]

Preview verification:
[results or BLOCKED + reason]

External dependencies:
[EXT-03 / other applicable dependency]

Negative controls:
[results]

Final status:
VERIFIED / BLOCKED / FAILED
The original decision text MUST remain preserved.
Do not rewrite the decision after implementation merely to match the implementation.
 
⸻
 
16. RE-DISCOVERY REQUIREMENT
After implementation:
IMPLEMENT
   ↓
VERIFY
   ↓
RE-DISCOVER
   ↓
CHECK AUTHORITY / BOUNDARY
   ↓
INTEGRATE
   ↓
EVIDENCE
Re-discovery MUST determine whether implementation introduced:
* a new dependency;
* a new authority question;
* a new security boundary;
* an architectural conflict;
* a scope expansion;
* a regression;
* an external dependency affecting FS-08.
Any newly discovered Architect- or Founder-reserved matter MUST be escalated rather than inferred.
 
⸻
 
17. COMPLETION CONDITION
FS-DP-02 B3 is complete only when:
Architect Decision
        = RATIFIED
             │
             ▼
Implementation
        = COMPLETE
             │
             ▼
Verification
        = PASS
             │
             ▼
Security controls
        = PASS
             │
             ▼
Regression
        = PASS
             │
             ▼
Re-discovery
        = CLEAR
             │
             ▼
Evidence
        = RECORDED
If Preview verification is blocked by EXT-03, distinguish:
B3 LOCAL IMPLEMENTATION
        = COMPLETE

B3 LOCAL VERIFICATION
        = PASS

B3 LIVE PREVIEW VERIFICATION
        = BLOCKED
Do not collapse these states.
 
⸻
 
18. EXECUTION INSTRUCTION
Proceed now with:
READ
→ DISCOVER
→ CLASSIFY
→ IMPLEMENT B3
→ VERIFY
→ SECURITY TEST
→ REGRESSION
→ RE-DISCOVER
→ RECORD EVIDENCE
→ REPORT
Do not wait for another micro-approval for work that is explicitly authorized by this decision.
If a new Founder-reserved or Architect-reserved matter is discovered, stop only at that boundary and escalate the specific matter.
Do not expand the scope to unrelated architecture.
 
⸻
 
FINAL ARCHITECT STATEMENT
The Architect has RATIFIED:
FS-DP-02 — B3 Operator Bearer Tokens
within the bounded scope defined above.
This is an Architect Decision, not a Production Release Authorization.
Proceed with implementation and verification within the stated boundary.
````
