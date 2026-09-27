# `FS-DP-05-ARCHITECT-DECISION` — FS-DP-05 Architect Decision Record: Concurrency / Run Identity (as received)

**Identifier:** `FS-DP-05-ARCHITECT-DECISION` (the text's *"Decision ID: FS-DP-05"*
names the package it decides, which holds the identifier `FS-DP-05`).
**Received:** from the Architect (Moriarty), 2026-09-27, in the message body,
under `ACT-CC-POST-P13-AIOS-FULL-STACK-003`.
**Stated decision:** *"ARCHITECT DECISION: RATIFY"*, selected option *"C1 —
Runtime-derived Run Identity"* (`§5`, `§16`). It decides FS-DP-05 only: not
FS-DP-02, and it does not close FS-08 (`§13`, `§14`).

Register `§79` records the decision.

Reproduced below as received. The message's formatting is kept as sent,
including a code fence opened in `§1` and not closed.

````text
# FS-DP-05 — ARCHITECT DECISION RECORD
## Concurrency / Run Identity

**Decision ID:** FS-DP-05  
**Decision Subject:** Concurrency / Run Identity  
**Decision Status:** ARCHITECT DECISION — READY FOR RECORDING  
**Act Authority:** `ACT-CC-POST-P13-AIOS-FULL-STACK-003`  
**Proposal:** C1 — Runtime-derived Run Identity  
**Architect:** Moriarty  
**Date:** 27 September 2026

---

## 1. Decision Context

FS-DP-05 addresses the concurrency and run-identity behavior of the
AIOS Full Stack runtime.

The current discovery identified a concurrency condition in which two
concurrent requests could both mint:

```text
run-00001
with the result that the first run could become unreachable by the expected run identity.
The architectural question is therefore:
What is the authoritative identity source for an individual Runtime execution/run such that concurrent executions do not depend on shared positional or allocation assumptions?
 
⸻
 
2. Current Proposal
C1 — Runtime-derived Run Identity
The proposed architecture is:
Request
   ↓
Runtime Instance
   ↓
Runtime-derived Run Identity
   ↓
Trace / Execution Association
The Runtime that owns an execution is the source from which the run identity is derived.
The run identity must therefore identify the Runtime execution itself, rather than relying on a shared positional allocation mechanism whose correctness depends on request ordering.
 
⸻
 
3. Problem Being Addressed
The discovered failure mode was:
Concurrent Request A ──┐
                       ├── run-00001
Concurrent Request B ──┘
This can produce an identity collision.
The resulting condition is:
Run A → run-00001
Run B → run-00001

        ↓

identity collision
        ↓
incorrect / ambiguous association
        ↓
one execution may become unreachable by expected run identity
C1 addresses the identity source rather than attempting to serialize concurrent requests merely to preserve the existing allocation behavior.
 
⸻
 
4. Architectural Principle
Under C1:
RUNTIME
   │
   └── owns execution identity
          │
          ▼
      RUN IDENTITY
          │
          ├── Execution association
          └── Trace association
The run identity is therefore derived from the Runtime execution that owns the run.
The implementation must not make run identity depend on:
* list position;
* insertion position;
* request arrival ordering;
* mutable shared counters whose correctness depends on serialization;
* the assumption that concurrent requests execute sequentially.
 
⸻
 
5. Decision
ARCHITECT DECISION: RATIFY
The Architect ratifies:
C1 — Runtime-derived Run Identity
for FS-DP-05.
The ratification authorizes implementation of C1 within the boundaries specified by this decision record.
This decision does not authorize unrelated changes to Runtime, Execution, Trace, Persistence, Authentication, or other architecture outside the FS-DP-05 boundary.
 
⸻
 
6. Rationale
The discovered concurrency condition demonstrates that the existing run-number allocation behavior can produce duplicate run identity under concurrent execution.
C1 establishes the identity at the Runtime execution boundary itself.
This preserves the architectural relationship:
Runtime
   ↓
Execution
   ↓
Run Identity
   ↓
Trace
and avoids making identity correctness dependent on request ordering or shared positional allocation.
The decision is therefore specifically directed at the identified concurrency/run-identity problem.
 
⸻
 
7. Architectural Boundary
C1 is limited to:
Runtime-derived Run Identity
Concurrency-safe run identification
Run-to-Runtime association
Run-to-Trace association
C1 does not by itself authorize:
Authentication redesign
Authorization redesign
Multi-user identity architecture
New persistence schema unrelated to run identity
New Planner architecture
New Scheduler architecture
New Execution Orchestrator
New Agent architecture
New Trace architecture outside the required identity association
New governance authority
Any such requirement discovered during implementation must be separately classified and routed through the applicable authority boundary.
 
⸻
 
8. Identity Requirements
The implementation shall establish the following properties.
8.1 Uniqueness
Two concurrent Runtime executions must not receive the same run identity.
Runtime A → Run ID A
Runtime B → Run ID B

Run ID A ≠ Run ID B
8.2 Runtime Ownership
Every run identity must be attributable to the Runtime execution that owns it.
Run ID → Runtime
must be deterministic within the applicable execution lifetime.
8.3 Trace Association
Trace records associated with a run must remain attributable to the correct Runtime execution.
Runtime
   ↓
Run ID
   ↓
Trace
8.4 Concurrency Safety
Correctness must hold under concurrent requests.
The implementation must not rely on:
request serialization
global positional allocation
shared mutable state whose correctness depends on ordering
unless such behavior is explicitly part of the ratified implementation and does not violate the identity requirement.
 
⸻
 
9. Implementation Authority
Claude Code is authorized to implement C1 only within the boundaries of this decision.
Implementation may include:
* modification of the relevant run-identity implementation;
* modification of the relevant execution/trace association;
* concurrency tests;
* regression tests;
* necessary adapter changes;
* necessary documentation/evidence records.
Claude Code shall not interpret this decision as authorization to redesign unrelated AIOS architecture.
 
⸻
 
10. Required Verification
After implementation, Claude shall verify at minimum:
V1 — Sequential Identity
Multiple sequential executions produce distinct valid identities.
V2 — Concurrent Identity
Multiple concurrent executions produce distinct identities.
V3 — Trace Association
Each execution’s trace resolves to the correct Runtime/run identity.
V4 — No Positional Dependency
Run lookup does not depend on collection position or insertion order.
V5 — No Duplicate Identity
A concurrency test must demonstrate:
N concurrent executions
        ↓
N valid execution identities
        ↓
no duplicate run identity
for the tested concurrency population.
V6 — Regression
Existing Full Stack and relevant AIOS regression suites remain valid.
V7 — Failure Safety
A failed execution must not leave behind an identity that can be incorrectly associated with another execution.
 
⸻
 
11. Verification Evidence
The implementation record shall report:
Implementation commit:
[recorded after implementation]

Concurrency test:
[PASS / FAIL]

Unique run identities:
[measured result]

Trace association:
[PASS / FAIL]

Regression:
[PASS / FAIL / CLASSIFIED]

Existing known failures:
[classified separately]

Protected artifacts:
[UNCHANGED / exception with authority]
Evidence must distinguish:
ARCHITECT DECISION
        ≠
IMPLEMENTATION
        ≠
VERIFICATION
 
⸻
 
12. Negative Controls
The implementation shall verify that C1 did not:
create Native Core #12
modify certified P12 evidence
modify certified P13 roots
create Phase 14
expand Founder authority
expand Architect authority
modify authentication architecture
modify authorization architecture without authority
introduce unrelated persistence architecture
silently redesign Trace
silently redesign Runtime
Any discovered requirement outside the FS-DP-05 boundary must be escalated rather than silently absorbed.
 
⸻
 
13. Relationship to FS-DP-02
FS-DP-05 is independently decided from FS-DP-02.
This decision:
FS-DP-05 = RATIFY C1
does not imply:
FS-DP-02 = RATIFY B3
FS-DP-02 remains subject to its own Architect decision record.
 
⸻
 
14. Relationship to FS-08
This decision does not itself close FS-08.
The required sequence remains:
FS-DP-05
   ↓
Architect Decision
   ↓
Implementation
   ↓
Verification
   ↓
FS-DP-02
   ↓
Architect Decision
   ↓
Implementation
   ↓
Verification
   ↓
External Dependencies
   ↓
FS-08 Final Gate
FS-08 may only be declared PASS when all required gate conditions are independently satisfied.
 
⸻
 
15. Decision State
FS-DP-05
    = DECIDED

DECISION
    = RATIFY

SELECTED PROPOSAL
    = C1 — Runtime-derived Run Identity

IMPLEMENTATION
    = AUTHORIZED WITHIN FS-DP-05 BOUNDARY

VERIFICATION
    = REQUIRED

FS-08
    = NOT YET PASSED
 
⸻
 
16. Architect Signature / Decision Authority
ARCHITECT:
Moriarty

DECISION:
RATIFY

DATE:
27 September 2026

AUTHORITY:
ACT-CC-POST-P13-AIOS-FULL-STACK-003

DECISION SUBJECT:
FS-DP-05 — Concurrency / Run Identity

SELECTED OPTION:
C1 — Runtime-derived Run Identity
 
⸻
 
17. Final Decision Statement
The Architect ratifies C1 — Runtime-derived Run Identity for FS-DP-05. Claude Code is authorized to implement and verify the runtime-derived run-identity architecture within the boundaries of this decision. This ratification does not authorize unrelated architectural changes, does not decide FS-DP-02, and does not close FS-08.
 
⸻
 
Decision Boundary
ARCHITECT
    │
    │ RATIFY C1
    ▼
CLAUDE CODE
    │
    ├── IMPLEMENT
    ├── TEST
    ├── VERIFY
    └── RECORD EVIDENCE
            │
            ▼
       FS-08 GATE
No further authority is inferred from this decision.
````
