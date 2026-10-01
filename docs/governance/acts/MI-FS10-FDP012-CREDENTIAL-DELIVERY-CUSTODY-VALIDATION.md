# Master Instruction — AIOS FS-10 — FDP-012 Credential Delivery & Custody Validation (as received)

**Received:** from the Founder, 2026-10-01, in the message body; extracted byte-exactly from the session transcript. The instruction refers to an *"FDP-012 Founder Decision"*; **the FDP-012 decision text itself was not part of the message** and is not reproduced or inferred here (Register `§120`).

````text
# MASTER INSTRUCTION — AIOS FS-10 — FDP-012 CREDENTIAL DELIVERY & CUSTODY VALIDATION

## 0. PURPOSE

Process FDP-012 as a strict Founder Decision validation and custody-feasibility gate.

FDP-011 is already canonical.

FDP-011 remains unchanged.

FDP-011 D-1 remains:

O-A — E-A per-session bypass.

This instruction does NOT select another X2 mechanism.

This instruction does NOT convert O-A into O-B.

This instruction exists only to determine whether the Founder-authorized
M1 environment-variable delivery path can satisfy the credential-custody
requirements necessary to implement the already-authorized O-A mechanism.

The governing principle is:

AUTHORITY ≠ TECHNICAL CAPABILITY ≠ SAFE CREDENTIAL CUSTODY.

No implementation may begin merely because FDP-012 exists.

---

# 1. CURRENT CANONICAL STATE

Re-discover before doing anything:

- FDP-009
- FDP-010
- FDP-011
- ESC-03
- AD-FS10-ESC03
- FS-10-ESC-03 Founder Decision Package
- FS-10-FDP011-T5-SECRET-CUSTODY-FEASIBILITY.md
- current FS-10 authority
- X2
- B3
- Production deployment
- designated rollback target
- Release Package
- Governance Decision Register
- FDP-012 Founder Decision

Confirm:

O-A = AUTHORIZED
O-A = NOT IMPLEMENTED
ESC-03 = NOT RESOLVED
FDP-010 = NOT COMPLETE
FS-10 = NOT READY
RELEASE = NOT AUTHORIZED
LIVE = NOT ACTIVE

Do not alter this state during the validation phase.

---

# 2. FOUNDER DECISION STATUS

The Founder has issued FDP-012 as a proposed supplemental decision governing
credential delivery and custody for O-A.

Before canonicalization:

- validate the decision;
- identify conflicts;
- identify ambiguity;
- identify missing authority;
- identify technical impossibility;
- identify security impossibility.

Do not silently rewrite FDP-012.

Do not reinterpret it in a way that weakens its conditions.

If FDP-012 conflicts with higher canonical authority:

STOP.

If FDP-012 is internally ambiguous:

STOP.

If FDP-012 is valid:

canonicalize it exactly as issued before any implementation activity.

---

# 3. ABSOLUTE SECURITY RULE

During feasibility and validation:

DO NOT:

- create a real Vercel automation bypass;
- obtain a real bypass secret;
- revoke a real bypass secret;
- set a real bypass secret into an environment variable;
- print a secret;
- echo a secret;
- transmit a secret through chat;
- transmit a secret through tool output;
- store a secret in the repository;
- store a secret in evidence;
- store a secret in logs;
- store a secret in telemetry;
- store a secret in source code;
- create a permanent bypass;
- create a standing bypass;
- weaken X2;
- weaken B3.

A real credential must NOT be used until every FDP-012
feasibility condition has passed.

---

# 4. FDP-012 SCOPE

FDP-012 governs ONLY:

- M1 environment-variable credential delivery;
- custody;
- session isolation;
- credential lifecycle;
- telemetry/logging exposure;
- revocation;
- removal;
- evidence.

FDP-012 does NOT modify:

- O-A;
- FDP-011 D-1;
- FDP-011 T1–T4;
- FDP-011 T6–T9 except where FDP-012 explicitly supplements custody;
- B3 scopes;
- X2 architecture;
- Release authority;
- LIVE authority;
- Founder Authority;
- Governance Model;
- P12/P13;
- Platform Organization;
- Phase structure.

---

# 5. CANONICALIZATION

If validation passes:

1. Persist FDP-012 exactly as issued.
2. Compute content hash.
3. Register it at the next available Governance Decision Register position.
4. Preserve the Founder Decision verbatim.
5. Link it to FDP-011.
6. Mark FDP-012 as supplemental custody authority.
7. Re-discover the persisted record.
8. Verify hash equality.
9. Update current FS-10 authority documentation.
10. Preserve the earlier T5 feasibility record as historical evidence.

Do NOT modify FDP-011.

Do NOT rewrite FDP-011 T5.

---

# 6. M1 FEASIBILITY GATE

The M1 environment-variable mechanism must pass ALL of the following
before a real O-A credential may be used.

Required gates:

M1-G1 — Creation Boundary
M1-G2 — Delivery Boundary
M1-G3 — Secret Visibility
M1-G4 — Telemetry Isolation
M1-G5 — Logging Isolation
M1-G6 — Process Isolation
M1-G7 — Session Isolation
M1-G8 — Routine Execution Isolation
M1-G9 — Lifetime Control
M1-G10 — Removal
M1-G11 — Revocation
M1-G12 — Revocation Verification
M1-G13 — Evidence Safety
M1-G14 — B3 Compatibility
M1-G15 — X2 Compatibility
M1-G16 — No Release/LIVE Expansion

ALL MUST PASS.

No partial approval.

No "probably safe".

No inference from absence of previous leakage.

---

# 7. M1-G1 — CREATION BOUNDARY

Determine:

- who creates the environment variable;
- where it is created;
- who has access to the settings;
- whether the value can be viewed later;
- whether creation itself exposes the secret to any system;
- whether the Founder remains the credential custodian.

Do NOT create the real bypass secret.

Evidence must be obtained from:

- provider documentation;
- existing configuration;
- provider UI behavior;
- already available configuration metadata;
- existing canonical AIOS documentation.

Classify unknowns explicitly.

---

# 8. M1-G2 — DELIVERY BOUNDARY

Determine exactly how the secret travels:

Founder
→ provider environment setting
→ new execution session
→ process environment
→ O-A execution.

Determine whether the secret ever passes through:

- chat;
- tool output;
- connector output;
- source code;
- shell command output;
- logs;
- telemetry;
- tracing;
- browser console;
- request headers exposed to diagnostics;
- error reports.

If the secret necessarily passes through a prohibited channel:

FAIL.

---

# 9. M1-G3 — SECRET VISIBILITY

Determine whether Claude can:

- print it;
- inspect it;
- enumerate it;
- accidentally expose it;
- receive it through tool output;
- cause it to appear in diagnostics.

Do not perform a test with a real secret.

Use architecture inspection and non-secret synthetic values only where such testing does not create misleading evidence.

A synthetic-value test may establish plumbing behavior,
but MUST NOT be treated as proof that production secret values
cannot leak unless the underlying mechanism is deterministic and
the evidence supports that conclusion.

---

# 10. M1-G4 — TELEMETRY ISOLATION

THIS IS A HARD GATE.

The absence of a secret in historical telemetry is NOT sufficient evidence.

Determine whether an environment variable introduced through M1 can appear in:

- application logs;
- access logs;
- debug logs;
- tracing;
- telemetry;
- crash reports;
- environment diagnostics;
- provider deployment logs;
- shell history;
- process inspection;
- request diagnostics;
- error messages;
- monitoring systems.

Required outcome:

PASS only if there is sufficient evidence that the secret is not
automatically exposed through these paths.

If the platform behavior cannot be established:

M1-G4 = UNKNOWN.

UNKNOWN = HARD STOP.

Do NOT convert UNKNOWN into PASS.

---

# 11. M1-G5 — LOGGING ISOLATION

Determine whether any existing AIOS component logs:

- environment variables;
- configuration snapshots;
- process environment;
- request headers;
- authentication credentials;
- exception context containing environment values.

Search:

- application logging;
- backend logging;
- middleware;
- diagnostics;
- smoke tools;
- tracing;
- test instrumentation.

Do not print the actual environment value.

If the logging behavior cannot be proven safe:

FAIL or UNKNOWN.

Both are HARD STOP states.

---

# 12. M1-G6 — PROCESS ISOLATION

Determine:

- which processes inherit the variable;
- which functions inherit it;
- whether child processes inherit it;
- whether unrelated scripts inherit it;
- whether test runners inherit it;
- whether routine automation inherits it.

The target requirement is:

ONLY the explicitly authorized operational execution context
may have access to the credential.

If the entire environment receives the variable and unrelated
processes cannot be prevented from inheriting it:

M1-G6 = FAIL.

Do not rationalize environment-wide inheritance as session isolation.

---

# 13. M1-G7 — SESSION ISOLATION

FDP-012 treats the current M1 mechanism as environment-scoped.

Therefore establish:

- exactly when a session begins;
- exactly when it ends;
- whether another session can start while the secret exists;
- whether routine sessions can run;
- whether the same secret is accessible to a later session;
- whether session termination removes access.

Required invariant:

ONE AUTHORIZED O-A SESSION
=
ONE ACTIVE CREDENTIAL AVAILABILITY WINDOW

If another session can automatically inherit the credential:

M1-G7 = FAIL unless an enforceable control prevents that session.

---

# 14. M1-G8 — ROUTINE EXECUTION ISOLATION

This is separate from session isolation.

Determine whether any:

- scheduled automation;
- background task;
- routine task;
- unrelated agent execution;
- maintenance process;
- test;
- deployment hook;

can run while the M1 secret exists.

If yes, determine whether that execution can access the secret.

If unrelated execution can receive the credential:

FAIL.

If it cannot be determined:

UNKNOWN → HARD STOP.

---

# 15. M1-G9 — LIFETIME CONTROL

Establish:

- creation time;
- activation time;
- operational window;
- revocation time;
- environment-variable removal time.

Because provider automatic expiry is not established:

DO NOT assume automatic expiry.

The required lifecycle is:

CREATE
→ INSTALL
→ NEW SESSION
→ OPERATE
→ STOP
→ REVOKE
→ VERIFY REVOKE
→ REMOVE VARIABLE
→ VERIFY REMOVAL

If any stage cannot be executed reliably:

HARD STOP.

---

# 16. M1-G10 — REMOVAL

Determine whether the Founder can remove the environment variable after
the operational session.

Verify:

- removal is possible;
- removal is complete;
- subsequent sessions do not receive the variable;
- cached/previous process environments do not remain active.

Do not claim removal if the old session remains alive with the variable.

If the environment retains the value after removal:

HARD STOP.

---

# 17. M1-G11 — REVOCATION

Determine the exact provider procedure for revoking the O-A bypass.

No automatic expiry may be assumed.

The mechanism must support explicit revocation.

Revocation must be possible without requiring the secret to appear
in:

- chat;
- tool output;
- logs;
- repository;
- evidence.

If revocation itself requires prohibited secret transmission:

HARD STOP unless FDP-012 explicitly and validly authorizes another
secure custody path.

---

# 18. M1-G12 — REVOCATION VERIFICATION

After revocation, verify:

- X2 rejects the previously authorized request;
- expected 302/no-access behavior occurs;
- no bypass remains active;
- no alternate access path was created.

The test must NOT expose the credential.

If revocation cannot be independently verified:

HARD STOP.

---

# 19. M1-G13 — EVIDENCE SAFETY

Evidence may contain:

- session ID;
- subject;
- timestamps;
- deployment ID;
- operation;
- result;
- request/run ID;
- revocation status;
- revocation verification;
- variable removal confirmation.

Evidence MUST NOT contain:

- secret value;
- token value;
- bypass value;
- environment dump;
- credential-bearing headers.

If evidence tooling can accidentally capture secrets:

HARD STOP.

---

# 20. M1-G14 — B3 COMPATIBILITY

O-A must not bypass B3.

Verify:

X2
→ O-A
→ B3
→ operator authentication
→ authorized scopes.

The following must remain true:

- `aios.observe` works where authorized;
- `aios.workflow.run` works where authorized;
- `aios.audit` works where authorized;
- `aios.agent.register` remains denied;
- malformed/invalid credentials fail;
- wrong environment fails;
- unauthorized principal fails.

No B3 scope expansion.

---

# 21. M1-G15 — X2 COMPATIBILITY

Verify:

Without O-A:
X2 blocks the operator.

With O-A:
X2 permits the request to reach B3.

After O-A revocation:
X2 blocks the operator again.

X2 protection must remain enabled.

No trusted IP.

No permanent bypass.

No public exposure.

No deployment protection weakening.

---

# 22. M1-G16 — RELEASE / LIVE FIREWALL

Regardless of M1 result:

O-A MUST NOT confer:

- Release authority;
- LIVE authority;
- Founder Release Authorization;
- traffic activation authority;
- public exposure authority.

Operational verification remains operational verification.

Release remains Founder-reserved.

LIVE remains Founder-reserved.

---

# 23. NO-SECRET TESTING POLICY

Before all gates pass:

Allowed:

- source inspection;
- configuration inspection;
- provider documentation;
- metadata inspection;
- synthetic non-secret values;
- static analysis;
- mutation tests;
- negative-control tests that do not require real credentials.

Not allowed:

- real bypass;
- real secret;
- real token;
- real environment injection;
- real revocation.

This distinction is mandatory.

---

# 24. HARD STOP MATRIX

Immediately STOP if any of the following occurs:

| Condition | Result |
|---|---|
| Telemetry behavior UNKNOWN | HARD STOP |
| Logging behavior UNKNOWN | HARD STOP |
| Process inheritance UNKNOWN | HARD STOP |
| Session isolation UNKNOWN | HARD STOP |
| Routine execution exposure UNKNOWN | HARD STOP |
| Removal behavior UNKNOWN | HARD STOP |
| Revocation cannot be verified | HARD STOP |
| Secret must enter tool output | HARD STOP |
| Secret must enter chat | HARD STOP |
| Secret appears in evidence | HARD STOP |
| Secret appears in logs | HARD STOP |
| Secret appears in telemetry | HARD STOP |
| Another session inherits secret uncontrollably | HARD STOP |
| B3 must be weakened | HARD STOP |
| X2 must be weakened | HARD STOP |
| Standing bypass required | HARD STOP |
| Public exposure required | HARD STOP |
| Release/LIVE authority affected | HARD STOP |
| New authority required | HARD STOP |

Do not bypass a HARD STOP.

Do not classify it as non-blocking.

Do not continue to S5.

---

# 25. IMPORTANT DISTINCTION

The following states are different:

### AUTHORITY PASS
FDP-012 authorizes the M1 custody path.

### FEASIBILITY PASS
M1 can technically satisfy FDP-012.

### SECURITY PASS
M1 has sufficient evidence of safe secret handling.

### IMPLEMENTATION PASS
O-A was actually implemented and verified.

Do not collapse these states.

FDP-012 canonicalization does NOT mean O-A is implemented.

---

# 26. IF ALL M1 GATES PASS

Only if:

M1-G1 through M1-G16 = PASS

may Claude proceed to:

S5 — O-A implementation planning.

Even then:

DO NOT create the real bypass immediately.

First produce an implementation plan identifying:

- exact provider action;
- exact Founder action;
- exact Claude action;
- session start;
- credential injection;
- operational verification;
- revocation;
- variable removal;
- evidence capture;
- final cleanup.

Then STOP for a final implementation readiness check.

Do not improvise.

---

# 27. IF ANY GATE IS UNKNOWN OR FAIL

Do NOT implement O-A.

Produce:

STATE — BLOCKED — CREDENTIAL CUSTODY FEASIBILITY

Include:

- failed gate;
- evidence;
- why evidence is insufficient;
- exact authority/dependency required;
- whether Founder Decision is required;
- whether Architect Decision is required;
- whether provider capability is required.

FDP-011 remains canonical.

FDP-012 remains canonical if already validated.

O-A remains authorized but not implemented.

ESC-03 remains unresolved.

FDP-010 remains incomplete.

FS-10 remains not ready.

---

# 28. DOCUMENTATION

Create:

docs/fullstack/FS-10-FDP012-M1-CUSTODY-VALIDATION.md

The document MUST contain:

1. Scope
2. Canonical authority
3. FDP-012 validation
4. M1 mechanism description
5. G1–G16 results
6. Evidence source for each gate
7. Telemetry analysis
8. Logging analysis
9. Process inheritance analysis
10. Session isolation analysis
11. Routine execution analysis
12. Lifetime analysis
13. Removal analysis
14. Revocation analysis
15. Evidence safety analysis
16. X2 compatibility
17. B3 compatibility
18. Release/LIVE separation
19. Hard-stop determination
20. Final state
21. Exact next authorized action

Never include any secret value.

---

# 29. REGRESSION / EVIDENCE

After documentation and test changes:

Run the applicable targeted tests.

Run regression suites according to existing project practice.

Run:

- secret scan;
- credential leakage scan;
- boundary scan;
- citation audit.

Do not claim a new regression baseline if the full tools suite was not rerun.

Clearly distinguish:

- fresh result;
- prior baseline;
- known pre-existing P12-W6 classification.

---

# 30. RE-DISCOVERY

After all material documentation/test construction:

Re-discover:

- FDP-011;
- FDP-012;
- X2;
- B3;
- Production;
- current authority;
- Release Package.

Confirm:

- FDP-011 unchanged;
- FDP-012 unchanged;
- X2 unchanged;
- B3 unchanged;
- Production unchanged;
- no secret created;
- no bypass created;
- no Release;
- no LIVE.

---

# 31. FINAL STATES

Use exactly one:

### STATE A
FDP-012 VALIDATED — M1 FEASIBILITY PASS — IMPLEMENTATION READY

Only if every mandatory gate passed.

### STATE B
BLOCKED — TELEMETRY / LOGGING / SESSION ISOLATION

If any relevant gate is UNKNOWN or FAIL.

### STATE C
BLOCKED — CREDENTIAL CUSTODY

If the secret cannot be safely delivered or controlled.

### STATE D
BLOCKED — AUTHORITY

If additional Founder/Architect authority is required.

### STATE E
BLOCKED — PROVIDER DEPENDENCY

If provider capability must change.

---

# 32. ABSOLUTE FINAL RULE

Do NOT create, obtain, transmit, install, use or revoke a real O-A bypass
credential during this feasibility validation.

The real credential may be used ONLY after:

FDP-012 canonical
+
M1-G1 PASS
+
M1-G2 PASS
+
M1-G3 PASS
+
M1-G4 PASS
+
M1-G5 PASS
+
M1-G6 PASS
+
M1-G7 PASS
+
M1-G8 PASS
+
M1-G9 PASS
+
M1-G10 PASS
+
M1-G11 PASS
+
M1-G12 PASS
+
M1-G13 PASS
+
M1-G14 PASS
+
M1-G15 PASS
+
M1-G16 PASS.

UNKNOWN ≠ PASS.

ABSENCE OF EVIDENCE ≠ SECURITY EVIDENCE.

TECHNICAL CAPABILITY ≠ AUTHORIZATION.

AUTHORIZATION ≠ IMPLEMENTATION.

VERIFICATION ≠ RELEASE.

RELEASE ≠ LIVE.

Final required state before any real credential use:

O-A AUTHORIZED
+
M1 SECURITY FEASIBILITY VERIFIED
+
IMPLEMENTATION READY

Otherwise STOP.
````
