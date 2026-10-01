# `AD-FS10-ESC03` — Production Operational Edge Access: Architecture Decision (as received)

**Received:** from the Founder, 2026-10-01, in the message body.
**Stated status:** *"ARCHITECTURAL DECISION — EVIDENCE REQUIRED"*. An Architect Decision Record that, by its own `§5`, `§19`–`§22` and `§24`, opens an evidence phase: no candidate is selected and nothing is implemented before the evidence is complete and the decision authority is exercised.
**Answers:** the Architect Decision Package `docs/fullstack/decision-packages/FS-DP-03-R3-ESC-03-OPERATIONAL-EDGE-ACCESS.md` (Register `§112`).

Reproduced below as received. The message's formatting is kept as sent, including a code fence opened in `§33` and not closed.

````text
# AD-FS10-ESC03
# PRODUCTION OPERATIONAL EDGE ACCESS
# ARCHITECTURE DECISION

Document Type:
Architect Decision Record

Decision ID:
AD-FS10-ESC03

Status:
ARCHITECTURAL DECISION — EVIDENCE REQUIRED

Parent Resolution:
ACT-CC-POST-P13-AIOS-FS10-ESC03
ESC-03 Authority Resolution

Related Founder Decisions:
- FDP-009
- FDP-010

Related Architecture:
- FS-DP-02
- FS-DP-03
- X2 Deployment Protection Decision
- B3 Operator Authentication
- FS-10 Current Authority

Primary Question:

> How may the delegated CEO obtain operational access to the protected
> Production AIOS API through X2 without creating a permanent bypass,
> changing the protected-edge architecture without authority, or acquiring
> Production Release / LIVE authority?

---

# 1. DECISION PURPOSE

This ADR exists to resolve the architectural question identified by
ESC-03.

The purpose is NOT to maximize convenience.

The purpose is to determine whether the existing AIOS architecture and
X2 protection model provide an authorized, secure and operationally viable
path for delegated CEO access to the protected Production AIOS API.

The decision must preserve:

    X2 Protection
        +
    Application Authentication
        +
    Least Privilege
        +
    Auditability
        +
    Revocability
        +
    Release Separation
        +
    LIVE Separation


---

# 2. CURRENT VERIFIED STATE

The following state has already been established by ESC-03 discovery.

Production:

    DEPLOYED
    VERIFIED
    NOT RELEASED
    NOT LIVE

FDP-009:

    CANONICAL

FDP-010:

    CANONICAL

Permanent operational principal:

    aios-operator

Current application scopes:

    aios.observe
    aios.workflow.run
    aios.audit

Application-level bearer authentication:

    VERIFIED WORKING

X2:

    PROTECTED

Temporary verification bypass:

    NONE

Permanent bypass:

    NONE

Production Release:

    FOUNDER RESERVED

LIVE:

    FOUNDER RESERVED

Operational AIOS:

    NOT ACTIVATED


---

# 3. KNOWN ACCESS PROBLEM

Current observed path:

    CEO / delegated execution environment
            │
            ▼
           X2
            │
            ▼
      Vercel SSO boundary
            │
            X
    Connector cannot complete
    the required SSO path

Whereas:

    Authorized request
            │
            ▼
           X2
            │
            ▼
       AIOS application
            │
            ▼
           B3
            │
            ▼
      aios-operator
            │
            ▼
       Authorized API


Therefore the current issue appears to be an
**edge access-path problem**, not an application authorization problem.

This distinction MUST be preserved unless new evidence disproves it.


---

# 4. GOVERNING PRINCIPLE

Technical capability does not establish architectural authority.

A mechanism is not authorized merely because:

- Vercel supports it;
- the connector can technically invoke it;
- a token can be generated;
- a bypass can be created;
- the endpoint can be reached;
- the implementation is easy.

Every mechanism must be classified against canonical authority.


---

# 5. NO-SELECTION-BEFORE-EVIDENCE RULE

This is the primary rule of this ADR.

Claude MUST NOT select:

- E-A;
- E-B;
- E-C;
- E-D;
- E-E;
- E-F;

until the evidence requirements in this ADR have been completed.

Before evidence completion:

    DECISION = UNSELECTED

not:

    E-A
    E-B
    E-C
    E-D
    E-E
    E-F


No implementation may begin before selection is authorized.

No recommendation may be disguised as an evidence finding.


---

# 6. CANDIDATE SET

The candidate mechanisms inherited from ESC-03 are:

## E-A — Per-Session Bypass

A temporary, explicitly authorized X2 bypass used for a specific
operational session.

## E-B — Standing Bypass

A persistent mechanism that allows access around X2.

## E-C — Trusted Sources OIDC

A machine/service identity mechanism operating through Vercel's supported
trusted-source/OIDC capability.

## E-D — Vercel Identity for CEO

A provider-level identity capable of satisfying the X2 access requirement
for the delegated CEO.

## E-E — Runtime Inside Protected Boundary

An operational execution/runtime path located inside the protected
deployment boundary, allowing authorized service-to-service access without
requiring the external CEO execution environment to cross X2 directly.

## E-F — No New Mechanism

Do not create a new CEO-to-API access path.

CEO operational responsibilities remain executable through the existing
authorized provider control plane and other existing operational surfaces.


---

# 7. EVIDENCE CLASSES

Every finding MUST be classified as one of:

    CANONICAL
    DIRECTLY VERIFIED
    PROVIDER-DOCUMENTED
    IMPLEMENTATION OBSERVED
    TEST EVIDENCE
    CONFIGURATION OBSERVED
    INFERRED
    UNKNOWN

Do not present:

    INFERRED

as:

    CANONICAL

Do not present:

    UNKNOWN

as:

    NOT SUPPORTED

Do not present:

    TECHNICALLY POSSIBLE

as:

    AUTHORIZED


---

# 8. SOURCE PRECEDENCE

Use the existing AIOS authority hierarchy.

At minimum inspect:

1. Constitution / Founder Authority where relevant;
2. Founder Decisions;
3. Governance Baseline;
4. canonical architecture;
5. FS-DP-02;
6. FS-DP-03;
7. X2 decision / ratification;
8. FDP-009;
9. FDP-010;
10. Co-Founder Delegation Charter V2;
11. CEO Operating Mandate;
12. current FS-10 authority layer;
13. B3 implementation and contract;
14. current deployment/security runbook;
15. provider documentation only for provider capability facts.

If sources conflict:

    DO NOT RESOLVE BY CONVENIENCE.

Identify:

- source;
- authority level;
- conflict;
- later decision;
- whether supersession is explicit;
- required decision owner.


---

# 9. EVIDENCE PACKAGE — E-A

## E-A — Per-Session Bypass

Determine:

1. exact X2 authority allowing temporary bypass;
2. whether FDP-009-03 covers the intended operational use;
3. whether it is verification-only or may support ordinary operations;
4. whether each session requires Founder authorization;
5. whether the bypass can be automatically revoked;
6. whether audit evidence exists;
7. whether bypass changes public accessibility;
8. whether bypass changes Release/LIVE semantics;
9. whether the bypass can be safely used by the delegated CEO;
10. whether using it for routine operations would effectively create
    standing access through repetition.

Required classification:

    AUTHORIZED
    AUTHORIZED WITH BOUNDARY
    FOUNDER DECISION REQUIRED
    PROHIBITED
    UNKNOWN


---

# 10. EVIDENCE PACKAGE — E-B

## E-B — Standing Bypass

Determine:

1. exact canonical authority for any standing bypass;
2. whether X2 explicitly permits it;
3. whether any current decision explicitly authorizes it;
4. whether it weakens the deployment protection boundary;
5. whether it creates permanent access independent of X2;
6. whether it creates a new trust boundary;
7. whether it changes public/private exposure;
8. whether it affects security ownership.

Do not implement.

Do not create a test bypass.

Do not create configuration.

The purpose of E-B analysis is classification only.

If no explicit authority exists, classify according to evidence.

---

# 11. EVIDENCE PACKAGE — E-C

## E-C — Trusted Sources OIDC

This candidate requires especially careful verification.

Determine from provider documentation and current environment:

1. whether the relevant Vercel feature exists;
2. whether the current Vercel plan supports it;
3. whether the current project supports it;
4. whether it is compatible with the current X2 configuration;
5. whether it supports machine/service identities;
6. whether it can authenticate the delegated CEO execution environment;
7. whether an OIDC token can actually be obtained from the execution
   environment;
8. whether the token can be presented through the existing connector/tool
   path;
9. whether X2 will accept it;
10. whether application B3 remains unchanged;
11. whether any new AIOS identity architecture is required;
12. whether implementation changes the trust boundary;
13. whether it requires provider-side account changes;
14. whether provider/account credentials are required;
15. whether Founder authority is required for those provider changes.

Separate:

    Vercel capability exists

from:

    AIOS can use it

from:

    Current execution environment can use it

from:

    Current X2 configuration accepts it

from:

    Current delegated authority permits deployment.


No conclusion may be drawn from provider documentation alone.


---

# 12. EVIDENCE PACKAGE — E-D

## E-D — Vercel Identity for CEO

Determine:

1. what "Vercel identity" means technically;
2. whether it is a human identity, service identity or machine identity;
3. whether it can satisfy X2;
4. whether it requires a new Vercel member/account;
5. whether it requires Founder-controlled provider administration;
6. whether it changes account ownership;
7. whether it creates a permanent access path;
8. whether it is revocable;
9. whether it is auditable;
10. whether it creates any Release/LIVE authority;
11. whether it requires Founder Decision.

Do not create the identity during evidence gathering.


---

# 13. EVIDENCE PACKAGE — E-E

## E-E — Runtime Inside Protected Boundary

Determine:

1. whether an existing runtime inside the protected boundary already exists;
2. whether it can legitimately perform the required operational actions;
3. whether it can use the existing `aios-operator` identity;
4. whether it preserves B3;
5. whether it requires a new service-to-service trust boundary;
6. whether it requires new credentials;
7. whether it requires new infrastructure;
8. whether it changes Runtime architecture;
9. whether it changes Security architecture;
10. whether it changes X2;
11. whether it creates a new operational authority surface;
12. whether existing delegated architecture authority covers it.

Do not build the runtime merely to test whether it works.

Architecture first.

Implementation only after decision.


---

# 14. EVIDENCE PACKAGE — E-F

## E-F — No New Mechanism

Determine:

1. what operational responsibilities the CEO actually needs;
2. which of those responsibilities are already executable through:
   - provider control plane;
   - deployment tools;
   - rollback tools;
   - logs;
   - store/read interfaces;
   - existing authorized operational surfaces;
3. which responsibilities genuinely require direct AIOS API access;
4. whether those responsibilities are mandatory or merely convenient;
5. whether absence of direct API access actually blocks Operational AIOS;
6. whether a future mechanism can be added as a successor architecture
   without blocking current Release/LIVE decisions.

Do not assume that direct API access is mandatory.

Do not assume that direct API access is unnecessary.

Measure the requirement.


---

# 15. OPERATIONAL REQUIREMENT MATRIX

Build:

| Operational Responsibility | Required? | Existing Path | Direct API Required? | Evidence | Authority |
|---|---|---|---|---|---|
| Observe Production | | | | | |
| Run workflow | | | | | |
| Read audit | | | | | |
| Deployment | | | | | |
| Rollback | | | | | |
| Recovery | | | | | |
| Configuration | | | | | |
| Incident response | | | | | |
| Health verification | | | | | |
| Release | | | | | |
| LIVE activation | | | | | |

The last two rows MUST remain:

    Production Release = Founder Reserved

    LIVE = Founder Reserved

They are not candidates for CEO operational access.


---

# 16. SECURITY EVALUATION

For every candidate mechanism evaluate:

### S1 — X2 Preservation

Does X2 remain enforced?

### S2 — Least Privilege

Does the mechanism preserve:

    aios.observe
    aios.workflow.run
    aios.audit

without adding unrelated authority?

### S3 — Revocability

Can access be revoked?

### S4 — Auditability

Can actions be attributed to the correct principal?

### S5 — Credential Safety

Are credentials protected from:

- repository;
- logs;
- evidence;
- chat;
- client-side exposure?

### S6 — Public Exposure

Does the mechanism change public accessibility?

### S7 — Trust Boundary

Does it create a new trust boundary?

### S8 — Identity Boundary

Does it create a new identity model?

### S9 — Security Ownership

Does it move security authority between PDs or owners?

### S10 — Failure Behavior

What happens if the mechanism fails?


---

# 17. GOVERNANCE EVALUATION

For every candidate determine:

### G1

Does it require Founder Decision?

### G2

Does it require Architect Decision?

### G3

Does it fall inside CEO delegated authority?

### G4

Does it alter X2?

### G5

Does it alter application authorization?

### G6

Does it create a new authority surface?

### G7

Does it affect certified roots?

### G8

Does it affect P12/P13?

### G9

Does it affect Native Core?

### G10

Does it affect Release/LIVE?

If G10 is anything other than:

    NO

STOP and classify the candidate as outside this ADR's allowed scope.


---

# 18. PROVIDER / CONNECTOR SEPARATION

Explicitly determine whether each limitation belongs to:

    AIOS architecture

    X2 architecture

    Vercel provider capability

    Vercel account configuration

    ChatGPT connector capability

    Claude execution environment

    Current application implementation

These categories MUST NOT be conflated.

In particular:

    "Connector cannot send Authorization header"

does NOT by itself prove:

    "AIOS needs a new authentication architecture."


---

# 19. DECISION MATRIX

After evidence is complete, create:

| Candidate | Evidence Complete | Authority Class | X2 Preserved | Least Privilege | Revocable | Auditable | New Trust Boundary | Founder Decision | Architect Decision | Selection State |
|---|---|---|---|---|---|---|---|---|---|---|
| E-A | | | | | | | | | | |
| E-B | | | | | | | | | | | |
| E-C | | | | | | | | | | | |
| E-D | | | | | | | | | | | |
| E-E | | | | | | | | | | | |
| E-F | | | | | | | | | | | |

Until every required evidence field is populated:

    Selection State = UNSELECTED


---

# 20. STRICT NO-RANKING RULE

Do not produce:

- best option;
- worst option;
- preferred option;
- recommendation;
- score;
- ranking;
- winner;
- "most suitable";
- "least risky" as an overall selection.

The ADR may state factual consequences.

It may state:

    "This candidate requires Founder Decision."

It may state:

    "This candidate conflicts with X2."

It may state:

    "This candidate preserves X2."

It may NOT convert those facts into a selected winner before the decision
authority has been properly exercised.


---

# 21. ARCHITECT DECISION STATES

After evidence is complete, the Architect may record exactly one state
for each candidate:

    ACCEPTABLE FOR ARCHITECTURAL IMPLEMENTATION

    ACCEPTABLE WITH BOUNDARY

    FOUNDER DECISION REQUIRED

    PROVIDER ACTION REQUIRED

    REJECTED BY CANONICAL AUTHORITY

    INCOMPATIBLE WITH CURRENT ARCHITECTURE

    INSUFFICIENT EVIDENCE


These are classifications, not rankings.


---

# 22. SELECTION RULE

Only after:

1. evidence complete;
2. authority classified;
3. security implications documented;
4. operational requirements measured;
5. Release/LIVE separation verified;

may the Architect record a selection.

If the selected mechanism requires Founder authority:

    DO NOT IMPLEMENT.

Instead produce:

    FOUNDER DECISION PACKAGE


If the selected mechanism falls inside existing Architect authority:

    IMPLEMENTATION MAY PROCEED

subject to all stated boundaries.


---

# 23. FOUNDER DECISION PACKAGE TRIGGER

A Founder Decision Package MUST be generated if the selected architectural
path requires:

- permanent security-boundary modification;
- permanent X2 modification;
- Founder-controlled provider identity;
- permanent access mechanism explicitly reserved to Founder;
- provider/account ownership change;
- any other Founder-reserved authority.

The package must contain:

1. exact decision question;
2. evidence;
3. current architecture;
4. proposed architectural effect;
5. security effect;
6. authority effect;
7. Release/LIVE non-effect;
8. implementation boundary;
9. rollback/recovery effect.

Do not make the Founder Decision inside this ADR.


---

# 24. NO IMPLEMENTATION DURING EVIDENCE PHASE

During evidence collection:

    NO X2 CHANGE
    NO BYPASS
    NO NEW IDENTITY
    NO NEW TOKEN
    NO NEW SERVICE
    NO NEW TRUST BOUNDARY
    NO PUBLIC EXPOSURE

Allowed:

    READ
    INSPECT
    VERIFY
    DOCUMENT
    TEST EXISTING BEHAVIOR
    CONSULT PROVIDER DOCUMENTATION


---

# 25. IF EXISTING AUTHORITY ALREADY SOLVES ESC-03

If evidence establishes an existing authorized mechanism:

1. record the source;
2. record the exact authority;
3. verify implementation;
4. run security tests;
5. run negative controls;
6. document revocation;
7. confirm Release/LIVE separation.

Do not create a new architectural mechanism.


---

# 26. IF NO AUTHORIZED MECHANISM EXISTS

The valid result may be:

    ESC-03
    = ARCHITECTURALLY UNRESOLVED

with:

    DECISION REQUIRED

This is not a failure of execution.

Do not create an unauthorized mechanism merely to eliminate the unresolved
state.


---

# 27. NEGATIVE CONTROLS

Any implemented candidate MUST prove:

    NC-01
    Operational access cannot authorize Production Release.

    NC-02
    Operational access cannot activate LIVE.

    NC-03
    Operational access cannot permanently bypass X2.

    NC-04
    Operational access cannot modify Founder Authority.

    NC-05
    Operational access cannot modify Governance Model.

    NC-06
    Operational access cannot modify certified P12/P13 roots.

    NC-07
    Operational access cannot expand Native Core.

    NC-08
    Operational access cannot create new operator scopes.

    NC-09
    Preview credentials cannot operate Production.

    NC-10
    Production credentials cannot operate Preview outside authorization.

    NC-11
    No credential material appears in repository/evidence/logs/chat.


---

# 28. RELEASE / LIVE FIREWALL

This ADR MUST NOT:

- authorize Production Release;
- authorize LIVE;
- activate Operational AIOS;
- modify Founder Release Authority;
- modify LIVE Authority.

Regardless of architectural outcome:

    Production Release
        = FOUNDER RESERVED

    LIVE
        = FOUNDER RESERVED

This firewall is absolute.

A successful ESC-03 resolution does NOT constitute:

    Production Release Authorization

and does NOT constitute:

    LIVE Authorization.


---

# 29. RE-DISCOVERY AFTER DECISION

If an architectural decision is made and implementation is authorized:

perform complete re-discovery.

Verify:

- X2 state;
- FDP-009 hash;
- FDP-010 hash;
- current authority layer;
- operator scopes;
- authentication;
- authorization;
- audit;
- revocation;
- security controls;
- negative controls;
- Release separation;
- LIVE separation;
- no credential leakage.

Any material discrepancy:

    STOP
    CLASSIFY
    ESCALATE


---

# 30. REQUIRED ARTIFACTS

Create/update only the artifacts necessary for this ADR.

Primary:

    docs/fullstack/FS-10-ESC03-ARCHITECTURE-DECISION.md

Evidence:

    docs/fullstack/evidence/FS-10-ESC03-ARCHITECTURE-EVIDENCE.json

If Founder decision is required:

    docs/fullstack/decision-packages/FS-10-ESC03-FOUNDER-DECISION-PACKAGE.md

If implementation is authorized:

    docs/fullstack/FS-10-ESC03-IMPLEMENTATION-RECORD.md


Do not create a Founder Decision Record unless the evidence establishes
that Founder authority is required.


---

# 31. REGISTER

If this ADR reaches a genuine architectural decision, register it in the
AIOS Governance Decision Register.

The Register entry must distinguish:

    DISCOVERY
    EVIDENCE
    ARCHITECT DECISION
    IMPLEMENTATION
    VERIFICATION

Do not collapse these into a single "approved" status.


---

# 32. FINAL ADR STATUS

Allowed final states:

    ARCHITECTURE RESOLVED — IMPLEMENTATION AUTHORIZED

    ARCHITECTURE RESOLVED — FOUNDER DECISION REQUIRED

    ARCHITECTURE UNRESOLVED — INSUFFICIENT EVIDENCE

    ARCHITECTURE CONSTRAINED — NO AUTHORIZED MECHANISM

    EXISTING AUTHORIZED MECHANISM VERIFIED


Do not use:

    RELEASED

    LIVE

    OPERATIONAL AIOS

as the status of this ADR.


---

# 33. FINAL REPORT

Return the following:

```text
AD-FS10-ESC03
PRODUCTION OPERATIONAL EDGE ACCESS ARCHITECTURE DECISION

Evidence Status:
[COMPLETE / INCOMPLETE]

X2 Canonical Authority:
[...]

Current AIOS Authentication:
[...]

Connector Limitation:
[...]

Operational Requirements:
[...]

Candidate Matrix:
E-A [...]
E-B [...]
E-C [...]
E-D [...]
E-E [...]
E-F [...]

Architectural Trust Boundary Impact:
[...]

Security Impact:
[...]

Authority Impact:
[...]

Release Authority:
FOUNDER RESERVED

LIVE Authority:
FOUNDER RESERVED

Selection:
[UNSELECTED / SELECTED AFTER EVIDENCE]

Architect Decision:
[...]

Founder Decision Required:
[YES / NO]

Implementation:
[AUTHORIZED / NOT AUTHORIZED]

Final ADR State:
[...]

Next Authorized Action:
[...]
````
