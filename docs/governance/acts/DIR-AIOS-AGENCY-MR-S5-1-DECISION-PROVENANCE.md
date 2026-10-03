# AIOS — MR-S5-1: Minimal Decision Provenance Remediation (as received)

**Received:** from the Founder (Moriarty), 2026-10-03, in the message body; extracted byte-exactly from the session transcript. Origin S-5 (Register `§150`). Receipt at Register `§151`; result at `§152`.

````text
AIOS — MR-S5-1

MINIMAL DECISION PROVENANCE REMEDIATION

Document Type: Minimal Construction / Bounded Remediation
Origin: S-5 — Disposition Semantics Discovery & Exhaustion Gate
Predecessor: S-5 COMPLETE / VERIFIED / EXHAUSTED
Purpose: Remove the remaining representation ambiguity identified by G-S4-1 and G-S4-2 without introducing new lifecycle semantics, Plan states, authority, subsystems, or capabilities.

⸻

1. AUTHORIZATION

MR-S5-1 is authorized as the only remaining construction work from the S-5 frontier.

The remediation is strictly bounded to improving the provenance and deterministic reconstruction of CEO decisions already supported by existing AIOS semantics.

The construction target is:

CEO Decision
    ↓
Decision Provenance
    ├── decision
    ├── resulting plan
    └── rework target, when applicable

No new semantic category is being invented.

The remediation must make explicit information that S-5 proved already exists semantically but is currently recoverable only partly through structure and reason text.

⸻

2. SOURCE AUTHORITY

Treat the following as the governing evidence for this remediation:

1. S-4 — Agent Verification Evidence → CEO Decision → Plan Outcome
2. S-5 — Disposition Semantics Discovery & Exhaustion Gate
3. Existing delegation lifecycle and operational ledger implementation
4. Existing CEO authority and delegation governance
5. Existing Plan / Plan Revision mechanisms
6. Existing provenance and state readers
7. Existing certified-history protections

Do not reinterpret the findings of S-5.

The following classifications are fixed for this remediation:

G-S4-1 → Representation Gap
G-S4-2 → Partially Deterministic
G-S4-3 → Intentional Architecture

G-S4-3 is CLOSED and must not be changed by this remediation.

⸻

3. CONSTRUCTION OBJECTIVE

Make the following information explicitly persisted when the CEO records a decision:

1. Which decision was made.
2. Which resulting/revised Plan was produced, when applicable.
3. Which new Plan Step represents the rework target, when applicable.

The resulting record must allow a fresh process to reconstruct:

ACCEPT
REWORK
REJECT

without interpreting free-text reason fields.

⸻

4. IMPORTANT SEMANTIC BOUNDARY

Do NOT create new disposition semantics.

The following meanings were established during S-5:

ACCEPT

Existing semantic:

verified result
+
CEO accepts result
+
delegation may reach COMPLETED
+
Plan outcome can become completed

REWORK

Existing semantic:

result is not accepted
+
work is to be performed again
+
revised Plan exists
+
new step represents the work to be redone

REJECT

Existing semantic:

result is not accepted
+
the work is not being redone as the same work
+
the resulting Plan/path proceeds differently

or, where CEO authority is insufficient:

result/path requires escalation

Do not add new meanings beyond this.

⸻

5. REQUIRED DECISION RECORD INFORMATION

The CEO decision record must explicitly carry:

5.1 Decision

The decision must identify the existing semantic:

ACCEPT
REWORK
REJECT

Do not expand this set.

Do not add:

CANCEL
ABANDON
DROP
TERMINATE
FAILED
BLOCKED

or any other new disposition.

Those were explicitly investigated during S-5 and are outside this remediation.

⸻

5.2 Resulting Plan Reference

When a CEO decision produces or depends upon a revised Plan, persist a reference to that Plan/version.

The reference must be sufficient to distinguish:

original Plan

from:

resulting/revised Plan

without relying on reason text.

Do not create a new Plan state.

Do not alter existing Plan lifecycle semantics.

Use the existing Plan identity/version mechanism.

⸻

5.3 Rework Target

For:

decision = REWORK

persist the identity/reference of the new Plan Step that performs the rework.

The field must be absent, null, or equivalent for:

ACCEPT
REJECT

unless existing architecture requires another representation.

Do not create a new step-state model.

Do not modify Plan Step lifecycle semantics.

This is provenance only.

⸻

6. MINIMAL-CONSTRUCTION RULE

Before writing code:

1. Locate the existing CEO decision writer.
2. Locate the existing ledger record.
3. Locate existing Plan identity/version fields.
4. Locate existing Plan Step identity.
5. Locate existing provenance readers.
6. Determine the smallest existing record/location capable of carrying the three pieces of information.

Prefer extending an existing record over introducing a new record type.

Prefer existing identifiers over creating new identifiers.

Prefer existing readers over introducing a new reader.

Prefer existing validation functions over new validation frameworks.

⸻

7. NO-NEW-SUBSYSTEM RULE

The remediation MUST NOT introduce:

* new subsystem;
* new service;
* new database;
* new ledger;
* new lifecycle engine;
* new Plan engine;
* new decision engine;
* new provenance subsystem;
* new Agent;
* new capability;
* new workflow;
* new execution layer.

The desired architecture remains:

Existing CEO Decision
        ↓
Existing Operational Record
        ↓
Existing Plan / Plan Step References
        ↓
Existing Readers / Provenance

⸻

8. BACKWARD COMPATIBILITY

Existing records must remain readable.

Older records that do not contain the new explicit provenance information must NOT be rewritten merely to satisfy the new format.

The reader must distinguish:

legacy record

from:

new explicitly-provenanced record

If legacy ACCEPT/REWORK records can still be reconstructed from their existing structure, preserve that behavior.

Do not fabricate historical decision fields.

Do not infer historical REJECT values and write them retroactively.

⸻

9. CERTIFIED HISTORY PROTECTION

Certified historical evidence must remain byte-identical.

Do not modify:

* certified P11 evidence;
* certified P12 evidence;
* historical manifests;
* Founder Decision records;
* governance baseline;
* canonical artifacts.

If the existing CEO decision record is itself inside a protected/certified location, determine the sanctioned operational successor path before writing.

Never bypass an existing certified-write guard.

⸻

10. AUTHORITY BOUNDARY

This remediation does not change authority.

The CEO remains the actor authorized to make the existing operational decision.

Agents:

CANNOT
- ACCEPT their own result
- REWORK their own result
- REJECT their own result
- change decision authority
- create delegation authority

Founder authority remains unchanged.

No agent receives decision authority through this remediation.

⸻

11. REQUIRED IMPLEMENTATION BEHAVIOR

The CEO decision writer should be able to produce records conceptually equivalent to:

ACCEPT

decision: ACCEPT
resulting_plan: <existing plan/version reference or appropriate existing value>
rework_target: none

REWORK

decision: REWORK
resulting_plan: <revised plan/version reference>
rework_target: <new step reference>

REJECT

decision: REJECT
resulting_plan: <resulting plan/version reference where applicable>
rework_target: none

Do not assume these exact serialization names are required.

Use the repository’s existing naming conventions.

⸻

12. DECISION VALIDATION

The writer must reject malformed decision records.

At minimum:

ACCEPT

Must not require a rework target.

REWORK

Must have:

resulting/revised Plan reference
+
rework target

unless existing architecture proves an equivalent representation is already sufficient.

REJECT

Must not carry a rework target.

Do not allow:

REWORK
without target

to appear as a falsely complete provenance record.

Do not silently convert malformed records to another decision.

⸻

13. PLAN / STEP INTEGRITY

For REWORK:

Verify that:

resulting Plan

actually contains:

rework target Step

and that the referenced Step belongs to that resulting Plan/version.

Do not rely on step names.

Use canonical identity.

This directly addresses the S-5 finding that Plan Step identity was not preserved across revisions.

⸻

14. REJECT INTEGRITY

For REJECT:

The system must not interpret:

REJECT

as automatic execution failure.

It means:

CEO refused the result/path.

The resulting Plan behavior remains determined by existing Plan semantics.

If the refusal requires authority beyond the CEO’s envelope, the existing escalation mechanism must remain the route.

Do not introduce a new rejection escalation mechanism.

⸻

15. ACCEPT INTEGRITY

ACCEPT must continue to require the verification evidence already established by S-4.

Do not weaken:

Agent Result
→ Verification
→ CEO ACCEPT

by allowing an unsupported result to become ACCEPTED.

Premature acceptance must remain refused.

⸻

16. REWORK INTEGRITY

REWORK must continue to require a genuine verification finding or equivalent existing evidence that justifies rework.

Do not allow:

CEO decision = REWORK

to become merely a textual declaration with no revised Plan.

The resulting Plan and rework target must be structurally linked.

⸻

17. PROVENANCE REQUIREMENT

After implementation, a fresh process must be able to reconstruct:

ACCEPT

Agent
 ↓
Result
 ↓
Verification
 ↓
CEO Decision = ACCEPT
 ↓
Plan Outcome

REWORK

Agent
 ↓
Result
 ↓
Verification Finding
 ↓
CEO Decision = REWORK
 ↓
Revised Plan
 ↓
Rework Target Step

REJECT

Agent
 ↓
Result
 ↓
Verification
 ↓
CEO Decision = REJECT
 ↓
Resulting Plan / existing terminal path

No reason-text interpretation may be required for the classification itself.

⸻

18. REQUIRED NEGATIVE CONTROLS

Add or extend tests only where necessary.

At minimum:

N1

Agent cannot write CEO decision.

N2

Agent cannot self-ACCEPT.

N3

Agent cannot self-REJECT.

N4

ACCEPT without valid verification is refused.

N5

REWORK without resulting Plan is refused.

N6

REWORK without valid rework target is refused.

N7

Rework target belonging to another Plan is refused.

N8

REJECT cannot silently become REWORK.

N9

Historical records are not rewritten.

N10

Certified evidence cannot be mutated.

N11

Fresh-process reconstruction does not depend on reason text.

N12

Founder authority remains unchanged.

⸻

19. REQUIRED POSITIVE TESTS

Construct minimal representative cases for:

P1 — ACCEPT

Use an existing valid Agent → Result → Verification path.

Prove:

ACCEPT
→ persisted
→ readable
→ Plan outcome correct
→ fresh-process reconstruction correct

P2 — REWORK

Use a genuine verification failure.

Prove:

REWORK
→ revised Plan
→ exact new Step reference
→ Plan/Step relationship valid
→ fresh-process reconstruction correct

P3 — REJECT

Use a bounded operational refusal that does not require Founder authority.

Prove:

REJECT
→ persisted
→ no rework target
→ resulting path reconstructable
→ fresh-process reconstruction correct

Do not manufacture a business-domain scenario that requires a new capability.

Use existing Agency/engineering mechanisms.

⸻

20. LEGACY TEST

Select representative pre-MR-S5-1 records.

Verify:

old record
→ existing reader
→ same historical meaning

No retroactive migration is allowed unless the repository already has an authorized migration mechanism.

If the old record cannot provide the new explicit provenance field, report that fact rather than fabricating it.

⸻

21. FRESH-PROCESS TEST

Terminate the process/session that created the records.

Start a fresh process.

Reconstruct independently:

ACCEPT
REWORK
REJECT

using persisted records.

The result must not depend on:

* in-memory registry;
* Python object state;
* process-local maps;
* temporary variables;
* reason-text interpretation.

This test is mandatory.

⸻

22. MUTATION TESTS

Deliberately mutate or remove:

1. decision field;
2. resulting Plan reference;
3. rework target;
4. Plan/Step relationship;
5. verification evidence.

Confirm that the reader detects the appropriate inconsistency.

Do not commit mutated evidence.

Use temporary/read-only fixtures or test copies.

⸻

23. REGRESSION TESTING

Run:

1. MR-S5-1 tests;
2. S-4 tests;
3. S-3 tests;
4. S-2 tests;
5. S-1 tests;
6. agency integration tests;
7. relevant P11/P12 integrity tests;
8. citation/stale/reference audits;
9. certified-byte integrity checks.

Compare against the immediately preceding clean baseline.

Any pre-existing failures must remain explicitly identified as pre-existing.

Do not silently attribute unrelated failures to MR-S5-1.

⸻

24. INTEGRITY BASELINE

Before construction, capture:

Git commit
Certified evidence digest
Operational ledger state
Relevant Plan/Delegation records
Test baseline

After construction verify:

Certified digest unchanged
Certified files unchanged
Founder records unchanged
Governance unchanged
Authority unchanged
Agent registry unchanged
Capability catalog unchanged
Deployment state unchanged

⸻

25. SCOPE GUARD

MR-S5-1 is complete when the three provenance facts are explicit and reconstructable.

Do NOT expand the work into:

* Plan state redesign;
* Plan Step lifecycle redesign;
* execution-record redesign;
* CEO execution subsystem;
* REJECT lifecycle architecture;
* new escalation model;
* organization expansion;
* candidate Executive Agent activation;
* deployment;
* P10/P11/P12 redesign.

If such a need is discovered, stop and record it as a separate finding.

⸻

26. EXHAUSTION / STOP CONDITION

Stop construction when:

ACCEPT
    explicit + reconstructable
REWORK
    explicit + resulting Plan + rework target + reconstructable
REJECT
    explicit + reconstructable
Legacy records
    remain readable
Certified history
    unchanged
Authority
    unchanged
Fresh-process reconstruction
    PASS
Negative controls
    PASS
Regression
    PASS or pre-existing failures explicitly classified

Do not continue polishing semantics beyond this boundary.

⸻

27. REQUIRED RESULT PACKAGE

Return:

A — Baseline

Commit, hashes, state counts, test baseline.

B — Construction

Exactly what existing mechanism was minimally extended.

C — Decision Provenance

Show how:

ACCEPT
REWORK
REJECT

are now persisted.

D — Plan Provenance

Show resulting Plan references.

E — Rework Provenance

Show exact Plan Step references.

F — Legacy Compatibility

Show old records remain readable.

G — Positive Tests

P1–P3.

H — Negative Controls

N1–N12.

I — Fresh Process

Independent reconstruction result.

J — Mutation Tests

Evidence that ambiguity/integrity failures are detected.

K — Regression

S-1 through S-4 and relevant system suites.

L — Integrity

Certified bytes and authority/governance invariants.

M — Remaining Findings

Only findings actually discovered during construction.

⸻

28. REQUIRED CLOSURE CLASSIFICATION

At the end, classify:

MR-S5-1

as exactly one:

COMPLETE / VERIFIED

or:

BLOCKED

or:

INCOMPLETE

If COMPLETE / VERIFIED, explicitly state:

G-S4-1 → CLOSED
G-S4-2 → CLOSED
G-S4-3 → CLOSED / NO REMEDIATION REQUIRED

Do not reopen G-S4-3 unless construction proves an actual contradiction with the S-5 finding.

⸻

29. FINAL ARCHITECTURAL INVARIANT

The final architecture must remain:

Founder
   ↓
CEO
   ↓
Plan
   ↓
Delegation
   ↓
Agent
   ↓
Result
   ↓
Verification Evidence
   ↓
CEO Decision
   ├── ACCEPT
   ├── REWORK
   └── REJECT
          ↓
     Existing Plan / Escalation semantics

The remediation adds provenance, not a new decision architecture.

⸻

30. FINAL PRINCIPLE

Make the existing semantics explicit; do not create new semantics to solve a representation problem.

MR-S5-1 is successful only if the system becomes more deterministic without becoming architecturally larger.
````
