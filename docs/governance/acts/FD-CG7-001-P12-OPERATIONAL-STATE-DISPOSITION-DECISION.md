# FD-CG7-001 — Founder Decision Record: FQ-CG7-1 & FQ-CG7-2 (P12 Operational State Disposition & Live Escalation Resolution)

**Received:** from the Founder (Moriarty), 2026-10-03, in the message body; extracted byte-exactly from the session transcript. Decides the two Founder Questions of CG-7 (Register `§144`). Registered at Register `§145`; remediation result at `§146`.

````text
AIOS — FOUNDER DECISION RECORD

FQ-CG7-1 & FQ-CG7-2

P12 Operational State Disposition & Live Escalation Resolution

Document Type: Founder Decision Record
Gate: CG-7 — P12 Operational State Reconciliation
Decision Scope: P12 operational state only
Founder: Moriarty
Delegated CEO: Claude Code — AIOS Co-Founder + Delegated CEO
Date: 2026-10-03
Status: FOUNDER DECISION REQUIRED

⸻

1. PURPOSE

This Founder Decision Record resolves the two unresolved Founder Questions produced by CG-7:

FQ-CG7-1
Should A2 operational disposition authority be extended
from P11 to P12, and how should the nine historical
P12 grants be dispositioned?
FQ-CG7-2
How should live escalation 9cb90fa0 be answered,
and what disposition should be applied to live grant 2494015d?

This record also authorizes narrowly bounded remediation R-1–R-4 only after the Founder decisions are recorded and registered.

⸻

2. SOURCE OF DECISION

CG-7 established the following state:

P12
│
├── 10 grants
│   ├── 1 LIVE / VALID
│   │    └── 2494015d
│   │
│   └── 9 HISTORICAL ONLY
│
└── 3 OPEN ESCALATIONS
    ├── 1 OPEN / LIVE
    │    └── 9cb90fa0
    │
    └── 2 OPEN / HISTORICAL
        ├── 0991300404
        └── 9d6bc0ad

CG-7 additionally established:

* certified P12 evidence remained unchanged;
* the nine historical grants are proof-run remnants;
* the recipient instances for those historical grants were not persisted for current execution;
* 2494015d is the only currently live P12 grant;
* 9cb90fa0 is the only currently live P12 escalation;
* P12 currently mixes certified historical state with operational state;
* the existing S-1 separation pattern can be reused;
* R-1–R-4 are remediation findings, not previously granted implementation authority.

⸻

3. FQ-CG7-1 — FOUNDER DECISION

Question

Should the A2 operational-disposition authority previously established for P11 be extended to P12, and what disposition should be applied to the nine historical P12 grants?

RECOMMENDATION

OPTION B — EXTEND A2 + TERMINAL REVOKED/CLOSED DISPOSITION

Recommended.

Rationale:

The nine grants have already served their proof-run purpose.

They are not current executable work:

historical proof-run
        ↓
execution already occurred
        ↓
recipient no longer persisted
        ↓
no current execution path
        ↓
historical state

Leaving them represented as ACTIVE creates a false operational interpretation even though their historical evidence is valid.

Therefore the clean separation is:

CERTIFIED HISTORY
        ↓
UNCHANGED / IMMUTABLE
OPERATIONAL STATE
        ↓
REVOKED / CLOSED

This does not rewrite history.

It only establishes the current operational disposition.

⸻

FQ-CG7-1 — FOUNDER DECISION

Decision:
B — EXTEND A2 TO P12 + REVOKED/CLOSED HISTORICAL DISPOSITION
Founder Authorization:
YES
Scope:
The nine historical P12 proof-run grants identified by CG-7.
Authorized Disposition:
REVOKED / CLOSED
Constraints:
1. Certified P12 evidence MUST remain byte-identical.
2. Historical grant records MUST NOT be rewritten.
3. Operational disposition MUST be stored separately from certified history.
4. No historical execution may be falsely represented.
5. No new authority is created.
6. No new delegation is created.
7. No grant may become executable merely because its state is reconciled.
Founder:
Moriarty
Date:
2026-10-03
Decision Status:
APPROVED

⸻

4. FQ-CG7-2 — FOUNDER DECISION

Question

How should live escalation 9cb90fa0 be answered, and what disposition should be applied to live grant 2494015d?

RECOMMENDATION

OPTION A — ANSWER / CLOSE ESCALATION WITHOUT NEW AUTHORITY

Recommended.

The live grant exists as a P12 proof-run artifact and is blocked by an escalation concerning an out-of-scope proof action.

The appropriate disposition is not to manufacture additional work merely to preserve an old proof-run grant.

Therefore:

9cb90fa0
    ↓
Founder acknowledges / answers
    ↓
NO NEW AUTHORITY
    ↓
CLOSE ESCALATION
2494015d
    ↓
REVOKED / CLOSED

The Founder response must not be invented by Claude Code.

The Founder-authorized semantic response is:

The escalation is acknowledged and closed without granting additional authority or widening the original delegation scope. The associated proof-run grant is therefore not continued as live operational work.

The original escalation and grant evidence remain preserved.

⸻

FQ-CG7-2 — FOUNDER DECISION

Decision:
A — ANSWER / CLOSE ESCALATION WITHOUT NEW AUTHORITY
Founder Authorization:
YES
Founder Response:
Acknowledge and close escalation 9cb90fa0.
No new authority is granted.
No scope expansion is authorized.
The associated proof-run grant 2494015d is not continued.
Grant Disposition:
REVOKED / CLOSED
Constraints:
1. Do not widen the original grant.
2. Do not create a replacement grant.
3. Do not reinterpret the escalation as authorization.
4. Preserve original certified evidence.
5. Store the operational response outside certified historical state.
6. Record the disposition against the exact grant/escalation identities.
Founder:
Moriarty
Date:
2026-10-03
Decision Status:
APPROVED

⸻

5. HISTORICAL ESCALATIONS

The following remain historical:

0991300404
9d6bc0ad

No operational work is required for them.

Their historical records remain preserved.

Do not fabricate Founder responses for them.

Do not modify certified evidence merely to make the historical reader appear clean.

Their operational treatment may be included in the P12 reconciliation implementation only if supported by the same authorized A2 separation model.

⸻

6. AUTHORITY EFFECT

These decisions DO NOT create:

* new capability;
* new Agent;
* new delegation authority;
* new organizational authority;
* new executive authority;
* new runtime authority;
* new workflow authority;
* new deployment authority.

The decisions only establish lifecycle/disposition for already-existing P12 operational records.

The existing authority model remains unchanged.

⸻

7. REMEDIATION AUTHORIZATION

Following successful registration of FQ-CG7-1 and FQ-CG7-2, the following remediation is AUTHORIZED:

R-1 — Full-Path Ledger Identity
R-2 — P12 State Reader Visibility
R-3 — Proof-Run vs Current Grant Distinction
R-4 — Plan Completion Evidence Compatibility

These are authorized as bounded integration / state-reconciliation remediation.

They must not expand into architecture redesign.

⸻

8. R-1 — FULL-PATH LEDGER IDENTITY

Objective

Correct the S-1 ledger identity defect where operational ledger folders are identified only by their final path segment.

Current collision:

p11/w4-operations
p12/w4-operations

must no longer resolve to the same operational identity.

Authorized action

Change ledger identity to use an unambiguous path-based identity.

The implementation may:

* modify the ledger identity function;
* update affected operational readers;
* add regression tests;
* prove P11/P12 separation.

The implementation may NOT:

* rewrite certified P11/P12 history;
* alter delegation authority;
* create a new ledger subsystem;
* silently migrate historical state without evidence.

Required verification

Prove:

P11 W4 ≠ P12 W4

and:

same basename
≠
same ledger identity

⸻

9. R-2 — P12 STATE READER VISIBILITY

Objective

Extend existing state readers only as necessary to correctly expose P12 operational state.

The reader must distinguish:

P11
P12
CERTIFIED HISTORY
OPERATIONAL CURRENT STATE

Required behavior

Historical ACTIVE records must not automatically be presented as currently executable.

Operational disposition must be read from the operational ledger when available.

Existing P11 behavior must remain unchanged.

Prohibited

Do not create a second competing state model.

Do not redefine lifecycle semantics.

Do not alter certified historical evidence.

⸻

10. R-3 — PROOF-RUN VS CURRENT GRANT

Objective

Make the distinction explicit between:

historical proof-run artifact

and:

current operational grant

The implementation must use existing evidence and the newly authorized operational disposition.

Preferred semantic model:

CERTIFIED GRANT RECORD
        │
        ├── Historical truth
        │
        └── Operational disposition
                │
                ├── LIVE
                ├── REVOKED
                └── CLOSED

Do not create a new lifecycle model unless discovery proves that the existing one cannot express the required state.

⸻

11. R-4 — PLAN COMPLETION EVIDENCE COMPATIBILITY

Objective

Determine whether the existing plan-completion/provenance mechanism can recognize the P12 evidence form.

Use:

existing contract
        ↓
existing evidence model
        ↓
existing reader
        ↓
minimal compatibility extension

The implementation must not create a new completion subsystem.

If the existing mechanism already contains sufficient semantics, adapt the reader rather than creating new semantics.

⸻

12. REMEDIATION EXECUTION PROTOCOL

Claude Code is authorized to execute the remediation autonomously within the following boundary:

DISCOVER
    ↓
CLASSIFY
    ↓
BASELINE
    ↓
MINIMAL CHANGE
    ↓
TEST
    ↓
VERIFY
    ↓
RE-DISCOVER

Claude Code may determine the implementation method.

Claude Code may NOT:

* expand the scope;
* create new authority;
* create new capabilities;
* create new Agent instances;
* alter canonical governance;
* alter Founder authority;
* activate deployment;
* modify certified historical evidence.

⸻

13. MANDATORY PRE-REMEDIATION BASELINE

Before modifying code:

1. Record current HEAD.
2. Record relevant file hashes.
3. Record certified P12 byte hashes.
4. Record P11 reader baseline.
5. Record P12 reader baseline.
6. Record current state counts.
7. Record the exact 10 grants and 3 escalations.
8. Record 2494015d and 9cb90fa0 as the live pair being resolved.

No implementation begins without this baseline.

⸻

14. MANDATORY POST-REMEDIATION VERIFICATION

After R-1–R-4:

A. Certified Evidence

P12 certified bytes
BEFORE == AFTER

B. Historical State

All original historical records remain reconstructable.

C. Operational State

Expected disposition:

9 historical grants
→ REVOKED / CLOSED
2494015d
→ REVOKED / CLOSED
9cb90fa0
→ ANSWERED / CLOSED
0991300404
9d6bc0ad
→ historical only

D. Ledger Identity

P11/W4
≠
P12/W4

E. Reader Behavior

Readers must distinguish:

historical
vs
current

F. Regression

Existing P11/S-1/S-2/S-3 tests must remain passing.

G. Negative Controls

Verify that remediation does NOT permit:

* unauthorized delegation;
* scope widening;
* agent-issued delegation;
* historical-state mutation;
* certified-evidence mutation;
* authority expansion.

⸻

15. FAILURE / STOP CONDITIONS

Immediately stop remediation if:

certified bytes change unexpectedly
        OR
authority semantics change
        OR
new capability is required
        OR
new canonical entity is required
        OR
new delegation authority is required
        OR
P11 behavior regresses
        OR
historical state becomes unreconstructable
        OR
implementation requires Founder-reserved decision

In those cases:

STOP
↓
PRESERVE STATE
↓
REPORT
↓
ESCALATE

Do not improvise a governance solution.

⸻

16. COMPLETION CRITERIA

The CG-7 remediation is complete only when:

FQ-CG7-1 REGISTERED
        +
FQ-CG7-2 REGISTERED
        +
R-1 VERIFIED
        +
R-2 VERIFIED
        +
R-3 VERIFIED
        +
R-4 VERIFIED
        +
CERTIFIED BYTES INTACT
        +
P11 REGRESSION CLEAN
        +
P12 STATE RECONSTRUCTABLE
        +
NO NEW AUTHORITY

Only then may the system return to the next Agency construction frontier.

⸻

17. RETURN PACKAGE

Claude Code must return:

1. Founder Decision registration IDs
2. Commit(s)
3. R-1 result
4. R-2 result
5. R-3 result
6. R-4 result
7. Before/after state table
8. Certified-byte integrity result
9. Regression test result
10. Negative-control result
11. Remaining gaps
12. Whether S-4 is now unblocked

The final report must clearly distinguish:

DECISION
AUTHORIZATION
IMPLEMENTATION
EVIDENCE
VERIFICATION
REMAINING BLOCKER

No implementation result may be represented as Founder-approved unless the corresponding decision was actually recorded and registered.
````
