# AIOS FS-10 — Provider-Side Credential Injection Evidence & Compatibility Gate (as received)

**Received:** from the Founder, 2026-10-01, in the message body; extracted byte-exactly from the session transcript. Evidence discovery and compatibility analysis only; selects, authorizes and configures nothing (Register `§121`).

````text
# AIOS FS-10 — PROVIDER-SIDE CREDENTIAL INJECTION EVIDENCE & COMPATIBILITY GATE

## PURPOSE

A new provider capability has been discovered during FDP-012/M1 feasibility
analysis:

Provider-side API credential injection.

The provider documentation reportedly states that:

- a credential can be stored outside the sandbox;
- the provider proxy attaches it to matching outbound requests;
- the credential does not reach Claude;
- the credential does not reach commands run by Claude;
- the credential does not enter the session's environment variables;
- the credential remains active until deleted.

This mechanism was NOT previously evaluated.

It has NOT been selected.

It has NOT been authorized.

It has NOT been implemented.

It must NOT be treated as O-A automatically.

The purpose of this instruction is evidence discovery and architectural
compatibility analysis only.

---

# 1. CURRENT STATE

Re-discover:

- FDP-009
- FDP-010
- FDP-011
- ESC-03
- AD-FS10-ESC03
- FS-10-ESC-03 Founder Decision Package
- FS-10-FDP011-T5-SECRET-CUSTODY-FEASIBILITY.md
- FS-10-FDP012-M1-CUSTODY-VALIDATION.md
- current FS-10 authority
- X2
- B3
- Production state
- designated rollback target
- Release Package
- Governance Decision Register

Confirm:

O-A = AUTHORIZED
O-A = NOT IMPLEMENTED
M1 = FAILED
ESC-03 = NOT RESOLVED
FDP-010 = NOT COMPLETE
FS-10 = NOT READY
RELEASE = NOT AUTHORIZED
LIVE = NOT ACTIVE

Do not change this state.

---

# 2. ABSOLUTE NO-SELECTION RULE

The provider-side credential injection mechanism is:

UNSELECTED.

Do NOT:

- select it;
- implement it;
- configure it;
- create a credential;
- upload a credential;
- store a credential;
- change provider settings;
- change X2;
- change B3;
- change FDP-011;
- create FDP-012;
- create a new Founder Decision;
- declare ESC-03 resolved.

This is evidence collection only.

---

# 3. PROVIDER DOCUMENTATION

Locate and preserve the exact provider documentation supporting the
credential-injection capability.

Determine:

1. exact feature name;
2. supported plans;
3. availability on the current account;
4. account/team/project scope;
5. credential storage location;
6. credential visibility;
7. whether credential reaches Claude;
8. whether credential reaches shell commands;
9. whether credential reaches session environment;
10. proxy injection behavior;
11. matching-host configuration;
12. custom-header support;
13. request methods covered;
14. HTTPS/TLS boundary;
15. deletion/revocation behavior;
16. caching behavior;
17. persistence across sessions;
18. persistence across deployments;
19. persistence across environment rebuilds;
20. auditability;
21. provider logging behavior;
22. telemetry behavior;
23. secret exposure risks;
24. whether multiple credentials are supported;
25. whether credential values can be rotated safely.

Every item must be classified:

- VERIFIED FROM PROVIDER DOCUMENTATION
- DIRECTLY VERIFIED
- UNKNOWN
- NOT APPLICABLE

Do not infer missing facts.

---

# 4. CURRENT ACCOUNT / PLAN ENTITLEMENT

Determine whether the current AIOS environment/account actually supports
the feature.

This must be established from authoritative account/provider evidence.

If plan information cannot be read:

classify:

PLAN ENTITLEMENT = UNKNOWN

Do not assume Pro, Max, Enterprise, or any other plan.

Do not upgrade the account.

Do not spend money.

Do not change subscription.

Do not create billing changes.

If an account-holder action is required, classify it as:

PROVIDER / ACCOUNT-HOLDER DEPENDENCY.

---

# 5. TARGET REQUEST ANALYSIS

Determine whether provider-side credential injection can technically
carry the O-A bypass credential to the exact required request.

Target chain:

Claude operational environment
        ↓
provider proxy
        ↓
matching outbound request
        ↓
Vercel X2 protected Production endpoint
        ↓
X2
        ↓
B3
        ↓
AIOS Production API

Determine:

- target hostname;
- target path;
- protocol;
- HTTP method;
- custom header requirement;
- whether the provider proxy can attach the required header;
- whether the Vercel endpoint accepts that header;
- whether X2 uses that header to permit O-A;
- whether B3 then receives the request;
- whether any existing proxy behavior interferes.

Do not send a real credential.

Do not configure the real mechanism.

Use documentation and existing architecture evidence only.

---

# 6. O-A COMPATIBILITY

This is a critical architectural question.

Determine whether provider-side credential injection would merely be:

A. a credential-delivery implementation of already-authorized O-A,

or:

B. a materially different X2 access mechanism requiring new authority.

Do NOT choose between A and B by preference.

Derive the classification from:

- FDP-011;
- FDP-010 §11.4;
- FDP-009-03;
- AD-FS10-ESC03;
- canonical X2 authority;
- the exact provider behavior.

If classification is ambiguous:

HARD STOP — ARCHITECTURE / AUTHORITY AMBIGUITY.

Do not assume it is O-A.

---

# 7. FDP-011 T5 COMPATIBILITY

Evaluate the mechanism against every T5 condition.

### T5 requirements

The credential must not:

- enter chat;
- enter normal tool output;
- enter repository;
- enter source code;
- enter documentation;
- enter evidence;
- enter logs;
- enter normal session environment;
- remain exposed after the operational session.

The credential must have:

- controlled creation;
- controlled custody;
- controlled delivery;
- controlled use;
- rotation;
- revocation;
- evidence without value disclosure.

Create a matrix:

| T5 Requirement | Evidence | PASS/FAIL/UNKNOWN |
|---|---|---|

UNKNOWN is not PASS.

---

# 8. SESSION / LIFETIME ANALYSIS

The provider documentation reportedly says the injected credential
remains active until deleted.

Therefore determine:

- whether it can be created only for one session;
- whether it is environment-wide;
- whether all sessions can use it;
- whether unrelated sessions can use it;
- whether routine tasks can use it;
- whether it can be restricted to a single execution;
- whether deletion is immediate;
- whether already-running sessions retain access;
- whether proxy caches it;
- whether deletion invalidates it immediately.

This is critical.

Do not confuse:

"credential does not reach Claude"

with:

"credential is session-isolated."

Those are different properties.

If the mechanism is environment-wide until deleted, record that fact.

Do not call it per-session merely because we manually create/delete it
around a session.

---

# 9. TELEMETRY / LOGGING

Determine whether provider-side credential injection prevents the secret
from appearing in:

- Claude transcript;
- shell;
- process environment;
- AIOS logs;
- Vercel logs;
- request logs;
- tracing;
- telemetry;
- provider proxy logs;
- provider diagnostic logs;
- error reporting;
- network debugging.

Provider documentation is sufficient only where explicit.

If provider telemetry behavior is undocumented:

UNKNOWN.

UNKNOWN is a hard stop for implementation.

Do not infer safety from the absence of historical leakage.

---

# 10. REVOCATION / DELETION

Determine:

- who can delete the credential;
- how deletion is performed;
- whether deletion requires the plaintext value;
- whether deletion can be done through provider dashboard;
- whether deletion can be done without exposing the credential;
- whether deletion is immediate;
- whether cached credentials survive;
- how deletion can be verified;
- whether a subsequent request is rejected.

Do not delete or create any real credential during this phase.

---

# 11. SECURITY MODEL

Evaluate:

- least privilege;
- host restriction;
- header restriction;
- credential scope;
- environment scope;
- session scope;
- rotation;
- revocation;
- auditability;
- credential exposure;
- replay risk;
- cross-session access;
- unrelated-task access;
- provider compromise boundary.

Do not provide a qualitative ranking.

Do not say "best", "safest", "preferred", or equivalent.

Only report evidence and classification.

---

# 12. B3 COMPATIBILITY

If provider-side injection reaches AIOS:

verify conceptually:

X2
→ injected O-A credential
→ protected request
→ B3
→ `aios-operator`
→ existing scopes

Confirm B3 remains unchanged.

No scope expansion.

No bypass of B3.

No `aios.agent.register`.

No Founder authority change.

---

# 13. X2 COMPATIBILITY

Determine whether X2 recognizes the injected credential in the same way
as the already-authorized O-A mechanism.

Do not assume.

If X2 would need a new trust source, new identity provider, new header
contract or architecture change:

classify it explicitly.

Potential classifications:

- Existing O-A implementation path
- O-A with bounded implementation change
- Architect Decision Required
- Founder Decision Required
- Provider Dependency
- Incompatible
- Insufficient Evidence

---

# 14. RELEASE / LIVE FIREWALL

Regardless of the result:

Provider-side credential injection must NOT grant:

- Production Release;
- Founder Release Authorization;
- LIVE;
- public traffic;
- deployment authorization beyond existing FDP-009/FDP-010;
- governance authority.

If any implementation would create such authority:

HARD STOP.

---

# 15. ACCOUNT-HOLDER BOUNDARY

Determine which actions require the Founder/account holder:

- enabling the feature;
- selecting plan;
- creating credential;
- deleting credential;
- changing host rules;
- changing header rules;
- viewing credential;
- auditing credential;
- rotating credential.

Do not perform any account-holder action.

Do not request secret material.

Do not request payment.

---

# 16. NO REAL CREDENTIAL

This entire instruction is read-only.

The following are prohibited:

- create real credential;
- upload real credential;
- configure real credential;
- send real request using credential;
- delete real credential;
- rotate real credential.

Synthetic/non-secret tests may be used only to verify plumbing behavior,
and must not be represented as proof of real-secret behavior unless
the underlying mechanism is deterministic and documented.

---

# 17. DECISION MATRIX

Produce:

| Property | Evidence | Classification |
|---|---|---|
| Provider feature exists | | |
| Current plan supports it | | |
| Credential never reaches Claude | | |
| Credential never reaches shell | | |
| Credential never enters environment | | |
| Host restriction | | |
| Header restriction | | |
| Session isolation | | |
| Cross-session isolation | | |
| Routine isolation | | |
| Lifetime control | | |
| Revocation | | |
| Deletion verification | | |
| Telemetry safety | | |
| Logging safety | | |
| B3 compatibility | | |
| X2 compatibility | | |
| FDP-011 T5 compatibility | | |
| O-A compatibility | | |
| Release/LIVE separation | | |

Do not select the mechanism.

---

# 18. FINAL CLASSIFICATION

Classify the provider-side mechanism as exactly one:

A. EXISTING AUTHORIZED O-A DELIVERY PATH

B. O-A DELIVERY PATH — AUTHORIZED WITH BOUNDARY

C. ARCHITECT DECISION REQUIRED

D. FOUNDER DECISION REQUIRED

E. PROVIDER DEPENDENCY

F. INSUFFICIENT EVIDENCE

G. INCOMPATIBLE WITH FDP-011 T5

H. INCOMPATIBLE WITH X2

Do not rank these classifications.

---

# 19. DOCUMENTATION

Create:

docs/fullstack/FS-10-PROVIDER-CREDENTIAL-INJECTION-EVIDENCE.md

Include:

1. Scope
2. Canonical sources
3. Provider documentation
4. Plan entitlement
5. Exact feature behavior
6. Target request analysis
7. O-A compatibility
8. T5 compatibility
9. Session/lifetime analysis
10. Telemetry analysis
11. Logging analysis
12. Revocation analysis
13. Security boundary
14. B3 compatibility
15. X2 compatibility
16. Account-holder dependency
17. Release/LIVE separation
18. Decision matrix
19. Final classification
20. Remaining unknowns
21. Exact next authorized action

Do not include credential values.

---

# 20. REGISTER / GOVERNANCE

This is an evidence/architecture discovery action.

Do not create a Founder Decision merely because the mechanism is promising.

Do not canonicalize a mechanism selection.

If an architecture decision is genuinely required, create only an
Architect Decision Package describing the evidence.

If a Founder Decision is genuinely required, prepare the decision surface
but do not manufacture the decision.

---

# 21. RE-DISCOVERY

After documentation/test construction:

Re-discover:

- FDP-011;
- FDP-012 status if present;
- provider evidence;
- X2;
- B3;
- Production;
- current authority;
- Release Package.

Confirm:

- no credential created;
- no credential configured;
- no X2 modification;
- no B3 modification;
- no Production change;
- no Release;
- no LIVE.

---

# 22. HARD STOP CONDITIONS

STOP if:

- plan entitlement is unknown and implementation would require it;
- provider behavior is undocumented where security depends on it;
- telemetry behavior is unknown;
- logging behavior is unknown;
- deletion behavior is unknown;
- credential remains accessible to unrelated sessions and no compensating
  canonical control exists;
- X2 requires architectural change;
- B3 must change;
- FDP-011 interpretation is ambiguous;
- new Founder authority is required;
- new Architect authority is required.

Do not resolve these by inference.

---

# 23. FINAL STATE

Report exactly one:

STATE A — EXISTING AUTHORIZED O-A DELIVERY PATH

STATE B — O-A DELIVERY PATH WITH BOUNDARY

STATE C — ARCHITECT DECISION REQUIRED

STATE D — FOUNDER DECISION REQUIRED

STATE E — PROVIDER DEPENDENCY

STATE F — INSUFFICIENT EVIDENCE

STATE G — INCOMPATIBLE WITH FDP-011 T5

STATE H — INCOMPATIBLE WITH X2

Until a valid implementation path is established:

O-A AUTHORIZED — NOT IMPLEMENTED
ESC-03 NOT RESOLVED
FDP-010 NOT COMPLETE
FS-10 NOT READY
RELEASE NOT AUTHORIZED
LIVE NOT ACTIVE
````
