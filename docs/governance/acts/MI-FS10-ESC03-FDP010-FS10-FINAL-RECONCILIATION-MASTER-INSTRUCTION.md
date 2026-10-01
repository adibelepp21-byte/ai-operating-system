# Master Instruction — AIOS FS-10: ESC-03 Authority Resolution → Founder Decision → FDP-010 Completion → FS-10 Final Reconciliation (as received)

**Received:** from the Founder, 2026-10-01, in the message body.
**Stated status:** *"FOUNDER-ISSUED EXECUTION INSTRUCTION"*. A conditional state machine (S0–S9, its `§4`): a later state runs only when its entry condition holds; a required Founder Decision is prepared and **not** manufactured (`§1` item 2, `§10`).

Reproduced below as received.

````text
# MASTER INSTRUCTION
# AIOS FS-10 — ESC-03 AUTHORITY RESOLUTION → FOUNDER DECISION → FDP-010 COMPLETION → FS-10 FINAL RECONCILIATION

Document Type:
Master Execution / Resolution / Reconciliation Instruction

Status:
FOUNDER-ISSUED EXECUTION INSTRUCTION

Purpose:
Resolve the remaining FS-10 Production Operational Access authority problem, prepare and obtain any required Founder Decision without manufacturing it, execute only after authority is established, complete all remaining obligations of FDP-010, perform full integration verification and FS-10 reconciliation, and stop at the Founder Release Gate.

---

# 0. PRIMARY OBJECTIVE

The objective of this Master Instruction is to bring the current AIOS FS-10 state from:

    ESC-03 = UNRESOLVED
    FDP-010 = CANONICAL / DECIDED / IMPLEMENTATION PARTIALLY COMPLETE
    Production Operational API Usability = BLOCKED
    Release = NOT AUTHORIZED
    LIVE = NOT ACTIVE

to:

    ESC-03 = RESOLVED
    FDP-010 = FULLY EXECUTED / VERIFIED
    Production Operational Access = VERIFIED
    Rollback Readiness = VERIFIED
    FS-10 = RECONCILED / READY
    Release Package = READY
    Founder Release Authorization = REQUIRED
    LIVE = NOT ACTIVE

This instruction MUST NOT exercise Founder Release Authority or LIVE Authority.

---

# 1. GOVERNING PRINCIPLES

The following principles are absolute:

1. UNKNOWN AUTHORITY is not AUTHORIZED.

2. Founder Decision may be prepared completely, but MUST NOT be manufactured, inferred, or self-issued by Claude Code.

3. Technical capability does not create governance authority.

4. Implementation does not constitute Founder approval.

5. Verification does not constitute Release Authorization.

6. Production Deployment does not constitute Production Release.

7. Production Release does not constitute LIVE unless Founder authorization and all applicable release conditions are satisfied.

8. Operational Access ≠ Release Authority ≠ LIVE Authority.

9. Silence is not approval.

10. "Obvious choice", "only practical option", technical preference, convenience, or implementation momentum MUST NOT be treated as Founder intent.

11. Existing canonical decisions MUST be preserved unless a later valid Founder Decision or higher-precedence canonical authority explicitly changes them.

12. Historical certified artifacts MUST NOT be modified in place.

13. No Phase 14 exists.

14. No Native Core #12 may be created.

15. P12/P13 certified roots remain protected.

16. Platform Organization closure remains protected.

17. The historical FS-09 gate remains historical evidence and MUST NOT be silently rewritten to change history.

18. Current FS-10 authority is governed by the applicable current Founder Decisions and canonical authority records.

19. Every material construction must be followed by re-discovery.

20. NO EVIDENCE → NO CLOSURE.

21. NO VERIFICATION → NO CLAIM OF SUCCESS.

---

# 2. AUTHORITY ORDER

Use the established AIOS authority precedence:

1. Constitution
2. Founder Authority / Founder Decisions
3. Governance Baseline
4. Canonical Architecture
5. Master Program / Phase
6. Platform Organization / Canonical Volumes
7. Co-Founder Delegation Charter
8. CEO Operating Mandate
9. Authority / Escalation Matrix
10. Execution Instruments / Acts / Instructions
11. Implementation

Do not allow a lower-level artifact to silently override a higher-level artifact.

If two sources conflict and precedence does not explicitly resolve the conflict:

    STOP
    IDENTIFY CONFLICT
    PRESERVE EVIDENCE
    CLASSIFY AUTHORITY
    ESCALATE AS REQUIRED

Do not select a side by inference.

---

# 3. CURRENT KNOWN STATE

Begin from the following known state, but RE-DISCOVER and verify it before relying on it:

    ESC-01 Permanent Production Operational Principal
        = RESOLVED

    ESC-02 CEO Rollback Authority
        = RESOLVED WITH BOUNDARY

    FDP-009
        = CANONICAL

    FDP-010
        = FOUNDER DECIDED / CANONICAL

    B3 Operator Authentication
        = ESTABLISHED

    X2 Production Deployment Protection
        = PRESERVED

    ESC-03 Principal → X2 Operational API Access
        = UNRESOLVED

    Production Operational API Usability
        = BLOCKED BY ESC-03

    Production Release
        = NOT AUTHORIZED

    LIVE
        = NOT ACTIVE

These are starting assertions only.

They MUST be re-discovered against the repository and canonical records before execution proceeds.

---

# 4. STATE MACHINE

The execution MUST follow this state machine.

    S0 — CURRENT STATE RE-DISCOVERY
       ↓
    S1 — ESC-03 AUTHORITY ANALYSIS
       ↓
    S2 — FOUNDER DECISION PREPARATION
       ↓
    S3 — FOUNDER DECISION HARD STOP
       ↓
    S4 — FOUNDER DECISION CANONICALIZATION
       ↓
    S5 — AUTHORIZED IMPLEMENTATION
       ↓
    S6 — FDP-010 COMPLETION
       ↓
    S7 — INTEGRATION VERIFICATION
       ↓
    S8 — FINAL FS-10 RECONCILIATION
       ↓
    S9 — FOUNDER RELEASE GATE

The state machine is conditional.

Do not execute a later state when its entry condition is not satisfied.

---

# 5. S0 — CURRENT STATE RE-DISCOVERY

Before changing anything, inspect and reconcile:

- FDP-009
- FDP-010
- ESC-03 Authority Resolution
- AD-FS10-ESC03
- FS-10 Current Authority
- FS-10 Deployment documentation
- FS-10 Release Package
- X2 canonical authority
- B3 operator authentication architecture
- Production operator principal state
- Production deployment state
- rollback target(s)
- historical FS-09 gate
- relevant governance register entries
- relevant evidence and execution records

Also inspect current repository state and git status.

Determine:

- what is canonical;
- what is historical;
- what is current;
- what is implementation;
- what is verified;
- what remains unresolved;
- what is Founder-reserved;
- what is Architect-reserved;
- what is CEO-authorized.

Produce an internal current-state map before construction.

DO NOT make architectural selections during S0.

DO NOT modify implementation during S0 except strictly necessary non-semantic evidence capture.

### S0 Exit Conditions

Proceed only if:

    CURRENT STATE VERIFIED
    +
    NO UNRESOLVED PRECEDENCE CONFLICT

If a genuine authority conflict remains:

    HARD STOP

---

# 6. S1 — ESC-03 AUTHORITY ANALYSIS

Determine exactly what authority is required for delegated CEO operational access to the protected Production AIOS API through X2.

The question is NOT:

    "Which technology is best?"

The question is:

    "What operational capability and access authority are actually authorized,
     and what mechanism may lawfully implement it?"

Analyze the previously identified candidate mechanisms:

- E-A — Per-session X2 bypass
- E-B — Standing X2 bypass
- E-C — Trusted Sources OIDC
- E-D — Vercel identity / provider identity
- E-E — Runtime inside the protected boundary
- E-F — No new mechanism / provider control plane only

Do not rank candidates.

Do not recommend a candidate.

Do not select a candidate unless the applicable authority explicitly allows selection.

For every candidate classify:

    CANONICAL AUTHORITY
    DIRECT EVIDENCE
    PROVIDER EVIDENCE
    IMPLEMENTATION EVIDENCE
    TEST EVIDENCE
    UNKNOWN
    AUTHORITY REQUIRED
    SECURITY IMPLICATION
    RELEASE/LIVE IMPLICATION
    IMPLEMENTATION REQUIREMENT

Maintain strict separation between:

    CAPABILITY AUTHORITY
    ACCESS MECHANISM
    IMPLEMENTATION
    VERIFICATION
    RELEASE
    LIVE

---

# 7. CAPABILITY AUTHORITY CHECK

Explicitly determine whether the Founder Decision required for ESC-03 is:

A. authorization of the delegated CEO operational-access capability itself;

OR

B. selection/authorization of a mechanism implementing an already-authorized capability;

OR

C. both.

Do NOT assume A or B.

If the canonical sources already establish this, follow them.

If they do not, classify the unresolved matter as Founder Decision Required.

Do not manufacture a capability authority from implementation requirements.

---

# 8. S1 EXIT STATES

S1 may exit only through one of these states:

### S1-A — EXISTING AUTHORIZED MECHANISM

A mechanism already exists and is clearly authorized.

Then:

    S1 → S5

provided no additional Founder or Architect authority is required.

### S1-B — FOUNDER DECISION REQUIRED

The capability or access mechanism requires Founder authority.

Then:

    S1 → S2

### S1-C — ARCHITECT DECISION REQUIRED

The matter is genuinely Architect-reserved and Founder authority is not required under current canonical governance.

Then prepare the Architect Decision Package and STOP if no authorized Architect decision path exists.

Do not manufacture Architect authority.

### S1-D — INSUFFICIENT / CONFLICTING EVIDENCE

If evidence cannot establish authority:

    HARD STOP

---

# 9. S2 — FOUNDER DECISION PREPARATION

If Founder Decision is required, prepare a complete Founder Decision Record / Decision Package.

The package MUST contain:

1. Decision ID
2. Context
3. Existing canonical authority
4. Current verified state
5. Evidence inventory
6. Directly verified facts
7. Provider-documented facts
8. Implementation-observed facts
9. Unknowns
10. Authority classification
11. Candidate mechanisms
12. Security implications
13. Governance implications
14. Operational implications
15. Release/LIVE boundary implications
16. Exact Founder Decision Question
17. Decision options
18. Consequences of each option
19. Required implementation scope after decision
20. Explicit non-decisions
21. Negative controls
22. Evidence references
23. Canonicalization requirements

Every candidate must remain UNSELECTED unless Founder authority already exists.

Do not use:

    recommended
    preferred
    best
    optimal
    obvious
    natural choice

to steer the Founder toward a candidate.

Facts and consequences may be stated.

Founder choice must remain Founder choice.

---

# 10. S3 — FOUNDER DECISION HARD STOP

Once the Founder Decision Package is complete and the decision is required:

    STOP.

The following actions are prohibited:

- selecting an option;
- implementing an option;
- configuring an option;
- canonicalizing an option;
- treating silence as approval;
- treating user intent inferred from conversation as a formal decision;
- treating technical necessity as Founder authorization;
- treating the remaining candidate as automatically selected;
- treating "no objection" as approval.

The required terminal state is:

    FOUNDER DECISION REQUIRED
    EXECUTION PAUSED
    NO IMPLEMENTATION AUTHORIZED

Wait for an explicit Founder Decision.

---

# 11. S4 — FOUNDER DECISION CANONICALIZATION

Only after an explicit Founder Decision exists:

1. Verify the decision record.
2. Verify its identity.
3. Verify the exact decision text.
4. Persist it according to canonical governance.
5. Register it in the canonical Decision Register.
6. Record content hash where applicable.
7. Re-discover the registered record.
8. Confirm no later/higher authority conflicts with it.
9. Determine the exact implementation envelope.

Do not silently reinterpret the Founder Decision during canonicalization.

If the Founder Decision is ambiguous:

    STOP

Do not fill the ambiguity by inference.

---

# 12. S5 — AUTHORIZED IMPLEMENTATION

After authority is established, implement only what is necessary to execute the authorized decision.

Implementation may include:

- provider configuration within authority;
- access mechanism;
- X2-compatible identity/trust path;
- AIOS B3 integration;
- scoped credentials;
- revocation;
- auditability;
- configuration;
- operational documentation;
- tests;
- evidence.

Implementation MUST preserve:

    X2
    B3
    least privilege
    environment isolation
    auditability
    revocability
    Release/LIVE separation

Do not weaken X2 merely to make the API reachable.

Do not create permanent bypass unless explicitly authorized.

Do not create public exposure unless explicitly authorized.

Do not expand into unrelated architecture.

---

# 13. S6 — COMPLETE FDP-010

Treat FDP-010 as an EXISTING CANONICAL FOUNDER DECISION.

Do NOT create "FDP-010 v2" merely to finish implementation.

Complete its remaining obligations.

## ESC-01

Verify:

    permanent Production operator principal exists
    correct scopes
    server-side/hash-only credential storage
    auditable identity
    revocability
    least privilege
    no unnecessary Agent registration authority

Verify that the principal is operationally usable only through the authorized X2 path.

## ESC-02

Verify:

    CEO rollback authority remains bounded
    rollback requires known-good verified target
    invalid/unverified target is prohibited
    22c0b49 is NOT treated as valid rollback target
    rollback does not imply Release
    rollback does not imply LIVE

Establish and verify a valid rollback target where required by the current FS-10 authority.

## ESC-03

Resolve:

    Permanent Principal
        ↓
    X2
        ↓
    B3
        ↓
    Production AIOS API
        ↓
    Operational capability

The access path must be genuinely usable, not merely documented.

---

# 14. SECURITY VERIFICATION

Perform positive and negative controls.

At minimum verify:

### Positive

- authorized operational identity can access authorized Production API;
- authorized operational action succeeds;
- audit/trace records are generated;
- state persistence remains correct;
- environment isolation holds.

### Negative

Verify denial for:

- missing scope;
- wrong scope;
- wrong environment;
- Preview principal → Production;
- Production principal → Preview where prohibited;
- Agent registration scope when not authorized;
- unauthorized bypass;
- unauthorized identity;
- unauthenticated request;
- Release action;
- LIVE action.

Do not weaken a negative control merely to make a positive test pass.

---

# 15. RELEASE / LIVE FIREWALL

The following are ALWAYS Founder-reserved unless a later valid canonical Founder Decision explicitly changes the boundary:

    Production Release
    LIVE activation
    public operational activation
    traffic activation
    declaration of LIVE
    declaration of Founder Release Authorization

The following do NOT automatically constitute Release or LIVE:

    Production Deployment
    Production Verification
    Operational API Access
    Smoke Test
    Health Check
    Integration Test
    Rollback
    Temporary Verification Access

Do not conflate these states.

---

# 16. S7 — INTEGRATION VERIFICATION

Verify the complete operational chain:

    CEO
      ↓
    Operational Identity
      ↓
    X2
      ↓
    B3
      ↓
    AIOS API
      ↓
    Runtime / Workflow
      ↓
    Persistent State
      ↓
    Trace / Audit
      ↓
    Evidence

Verify:

- authentication;
- authorization;
- execution;
- persistence;
- trace;
- audit;
- failure handling;
- environment isolation;
- concurrency where relevant;
- revocation;
- rollback readiness;
- observability;
- secret handling.

Use fresh evidence.

Do not rely only on previous evidence when the current implementation/configuration has changed.

---

# 17. S8 — FINAL FS-10 RECONCILIATION

Perform final rediscovery after all material work.

Reconcile:

- FDP-009
- FDP-010
- ESC-03
- AD-FS10-ESC03
- X2
- B3
- current FS-10 authority
- FS-10 deployment documentation
- release package
- Production state
- rollback state
- access state
- evidence
- governance register
- historical FS-09 record

Search specifically for:

- stale authority;
- contradictory documentation;
- outdated access instructions;
- stale tests;
- stale gate language;
- undocumented configuration;
- unauthorized capability;
- credential leakage;
- bypass residue;
- unresolved rollback dependency;
- unresolved Founder/Architect boundary.

Historical documents may be annotated or superseded only according to governance.

Do not rewrite historical facts.

---

# 18. GLOBAL HARD-STOP CONDITIONS

STOP immediately if any of the following occurs:

### H1 — Founder Decision Required

Required Founder authority is absent.

### H2 — Authority Conflict

Canonical sources conflict without explicit precedence resolution.

### H3 — Insufficient Evidence

The decision cannot be established from evidence.

### H4 — Canonical Conflict

Implementation conflicts with protected canonical architecture.

### H5 — Scope Expansion

Work requires:

- Constitution modification;
- Mission/Identity modification;
- Governance Model redesign;
- Founder authority modification;
- Native Core #12;
- Phase 14;
- reopening P12/P13 certified roots;
- reopening closed Platform Organization;
- unrelated architectural expansion.

### H6 — Release Boundary

Action would constitute Release or LIVE.

### H7 — Permanent Bypass

A permanent X2 bypass is required without explicit authority.

### H8 — Credential Boundary

Required credentials are unavailable or outside authorized control.

### H9 — Evidence Destruction

Action would destroy or materially obscure historical evidence.

### H10 — Self-Authorization

Claude would need to expand its own authority.

### H11 — Ambiguous Founder Decision

The Founder Decision exists but its operative meaning is ambiguous.

### H12 — Security Regression

The proposed implementation weakens an already-established security control without explicit authority.

---

# 19. NEGATIVE CONTROL FIREWALL

Before declaring completion, prove:

    NO SELF-AUTHORIZATION
    NO FOUNDER DECISION MANUFACTURED
    NO SILENT ARCHITECTURE SELECTION
    NO PERMANENT BYPASS
    NO PUBLIC EXPOSURE
    NO RELEASE
    NO LIVE
    NO NATIVE CORE #12
    NO PHASE 14
    NO CERTIFIED ROOT MODIFICATION
    NO HISTORICAL RECORD REWRITE
    NO UNAUTHORIZED CREDENTIAL DISCLOSURE
    NO UNAUTHORIZED SCOPE EXPANSION

---

# 20. EVIDENCE REQUIREMENTS

Every completion claim must identify:

- artifact;
- source;
- verification method;
- timestamp where relevant;
- environment;
- result;
- limitations;
- residuals;
- authority basis.

Do not use "PASS" without evidence.

Do not use "COMPLETE" when only implementation is complete.

Distinguish:

    Task Complete
    Component Complete
    Integration Complete
    Verification Complete
    FS-10 Ready
    Founder Release Authorized
    LIVE

These are different states.

---

# 21. FDP-010 COMPLETION CRITERIA

FDP-010 may be declared FULLY EXECUTED only when:

1. ESC-01 is implemented and verified.
2. ESC-02 is implemented/operationally supported and verified.
3. ESC-03 is resolved under canonical authority.
4. Operational Production API access is genuinely usable.
5. X2 remains intact.
6. B3 remains intact.
7. Least privilege is verified.
8. Revocation is verified.
9. Auditability is verified.
10. Environment isolation is verified.
11. Valid rollback target exists and is verified where required.
12. Historical FS-09 gate remains preserved.
13. Current FS-10 authority is internally consistent.
14. Release/LIVE remain Founder-reserved.
15. Final rediscovery finds no unresolved in-scope blocker.

If any mandatory item fails:

    FDP-010 = NOT COMPLETE

Do not downgrade the requirement merely to obtain closure.

---

# 22. FS-10 FINAL READY STATE

The target terminal state before Founder Release is:

    FS-09
        = CLOSED

    FS-10
        = READY FOR FOUNDER RELEASE GATE

    FDP-009
        = CANONICAL

    FDP-010
        = CANONICAL + FULLY EXECUTED + VERIFIED

    ESC-01
        = RESOLVED

    ESC-02
        = RESOLVED

    ESC-03
        = RESOLVED

    X2
        = PRESERVED

    B3
        = PRESERVED

    Operational Production Access
        = VERIFIED

    Rollback Readiness
        = VERIFIED

    Release Package
        = READY

    Founder Release Authorization
        = REQUIRED

    Production Release
        = NOT AUTHORIZED

    LIVE
        = NOT ACTIVE

---

# 23. S9 — FOUNDER RELEASE GATE

When the final ready state is reached:

STOP.

Do NOT:

- Release;
- declare LIVE;
- activate traffic;
- infer Founder Release Authorization;
- create a new Act merely to cross the Release Gate;
- treat verification as release approval.

The final execution state MUST be reported as:

    PRODUCTION VERIFIED
    OPERATIONALLY READY
    RELEASE PACKAGE READY
    FOUNDER RELEASE AUTHORIZATION REQUIRED

---

# 24. DOCUMENTATION REQUIREMENTS

Update only current living documentation required by the authorized work.

Maintain clear distinction between:

    HISTORICAL
    CURRENT
    CANONICAL
    VERIFIED
    PREPARATION
    PROPOSED
    UNKNOWN

Do not rewrite historical records to make the current state appear cleaner.

If an old document is inconsistent with a later valid decision:

    preserve historical artifact
    record supersession/reconciliation
    update current operational documentation
    preserve provenance

---

# 25. GOVERNANCE REGISTER

Every Founder Decision, Architect Decision, material execution result, and required reconciliation must be registered according to existing governance.

Do not fabricate a register number.

Do not reuse a previous decision ID.

Do not alter an existing Founder Decision merely to make registration easier.

---

# 26. GIT / REPOSITORY CONTROL

Before work:

    inspect git status
    inspect current branch
    inspect relevant commits

After material changes:

    run relevant tests
    inspect diff
    inspect changed files
    inspect secrets
    preserve evidence
    commit
    push where current project practice requires

Never commit secrets.

Never place raw Production credentials in repository, documentation, logs, evidence, or chat.

---

# 27. TESTING REQUIREMENT

Run the relevant current regression suites.

At minimum reconcile the known baseline suites:

    native_core
    consumers
    bounded_exception
    fullstack
    tools

Existing classified historical failures must remain classified rather than silently reinterpreted.

New failures must be investigated.

Do not convert a new failure into "known" merely because an older similar failure exists.

---

# 28. RE-DISCOVERY LOOP

After every material construction:

    DISCOVER
    ↓
    UNDERSTAND
    ↓
    CLASSIFY
    ↓
    CHECK AUTHORITY
    ↓
    DECIDE
    ↓
    BUILD
    ↓
    VERIFY
    ↓
    INTEGRATE
    ↓
    EVIDENCE
    ↓
    RE-DISCOVER

Do not skip RE-DISCOVER after material construction.

---

# 29. NO MICRO-ACT PROLIFERATION

This Master Instruction is intended to cover the entire bounded resolution:

    ESC-03
    →
    Founder Decision preparation
    →
    Founder Decision canonicalization
    →
    authorized implementation
    →
    FDP-010 completion
    →
    verification
    →
    FS-10 reconciliation
    →
    Founder Release Gate

Do not create another Micro-Act for ordinary implementation work already authorized by this instruction.

Create/escalate a new governance instrument only when genuinely required by a new authority boundary, Founder-reserved matter, or canonical governance requirement.

---

# 30. EXPLICIT EXCLUSIONS

This instruction does NOT authorize:

- Constitution changes;
- Mission/Identity changes;
- Governance Model redesign;
- Founder authority changes;
- self-expansion of CEO authority;
- Native Core #12;
- Phase 14;
- reopening P12;
- reopening P13;
- modification of certified P13 roots;
- reopening closed Platform Organization;
- permanent X2 bypass without explicit authority;
- public exposure without explicit authority;
- Production Release;
- LIVE;
- Founder Release Authorization;
- unrelated application features;
- unrelated infrastructure expansion;
- speculative architecture construction.

---

# 31. REQUIRED FINAL REPORT

At completion, report exactly which state was reached.

Use one of:

### STATE A

    EXECUTION COMPLETE
    FOUNDER DECISION REQUIRED

### STATE B

    EXECUTION COMPLETE
    ARCHITECT DECISION REQUIRED

### STATE C

    EXECUTION BLOCKED
    INSUFFICIENT / CONFLICTING EVIDENCE

### STATE D

    FDP-010 FULLY EXECUTED
    FS-10 READY
    FOUNDER RELEASE AUTHORIZATION REQUIRED

Do not report STATE D unless every mandatory completion condition is actually verified.

The final report MUST include:

1. Current state.
2. State transition history.
3. Founder Decision status.
4. ESC-03 status.
5. FDP-010 status.
6. X2 status.
7. B3 status.
8. Production operational access status.
9. Rollback status.
10. Verification evidence.
11. Negative-control results.
12. Regression results.
13. Documentation reconciliation.
14. Governance Register changes.
15. Remaining blockers/residuals.
16. Exact Founder authority still required.
17. Explicit confirmation:

       RELEASE NOT AUTHORIZED
       LIVE NOT ACTIVE

---

# 32. FINAL GOVERNANCE RULE

The purpose of this instruction is NOT to force closure.

The purpose is to produce the strongest evidence-supported state that can legitimately be reached within current authority.

Therefore:

    DO NOT MANUFACTURE AUTHORITY.
    DO NOT MANUFACTURE EVIDENCE.
    DO NOT MANUFACTURE FOUNDER INTENT.
    DO NOT MANUFACTURE CLOSURE.

If authority exists:

    EXECUTE.

If evidence exists:

    VERIFY.

If a Founder Decision is required:

    PREPARE AND STOP.

If architecture is authorized:

    BUILD AND VERIFY.

If FS-10 is ready:

    STOP AT FOUNDER RELEASE GATE.

Never cross a boundary merely because the implementation is technically possible.
````
