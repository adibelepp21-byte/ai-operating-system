# `GOAL-V2-004` — Certified-Evidence Write Closure · P10 · P11 · P12

**Issued by:** Founder — Moriarty · **Dated:** 24 September 2026 · **Status (as issued):** FINAL — FOUNDER ISSUED
**Received and persisted:** 2026-09-24, by Claude Code, AIOS Co-Founder + Delegated CEO
**Execution record:** `docs/governance/AIOS_GOAL_V2_004_CERTIFIED_EVIDENCE_WRITE_CLOSURE_RECORD_v1.0.md`

## Provenance

The Goal / Target arrived as one message with no attachment. The fenced block
below is that message exactly as issued, from its first line through
`END OF GOAL / TARGET 04`. Its UTF-8 sha256, taken over the fenced content, is
`1f04d491af5c67fb1489580cce00b0b333c46d8a7c9ab55ca2669e0ae1eb5862`.

This header was written by Claude and is not part of the Founder's text.

# § RECORD — issued by the Founder, verbatim

````text
FOUNDER GOAL / TARGET 04

CERTIFIED-EVIDENCE WRITE CLOSURE — P10 · P11 · P12

Document Type: Founder Goal / Target Instruction
Goal ID: GOAL-V2-004
Issuing Authority: Founder — Moriarty
Executor: Claude Code — AIOS Co-Founder + Delegated CEO
Authority Basis: Active Co-Founder V2 Authority Model
Referenced Control Surface: AIOS CEO Authority / Escalation Matrix
Predecessor: GOAL-V2-003 — Post-Goal-002 Re-Discovery & Next Authorized Construction Frontier
Frontier: FR-3-01
Status: FINAL — FOUNDER ISSUED
Date: 24 September 2026

⸻

1. FOUNDER GOAL

The Founder establishes the following Goal:

CLOSE THE CERTIFIED-EVIDENCE WRITE PATHS ACROSS P10, P11, AND P12 SO THAT NO RESIDENT EXECUTABLE ENTRY POINT CAN MODIFY CERTIFIED EVIDENCE WITHOUT BEING REFUSED BEFORE THE FIRST WRITE.

The purpose of this Goal is to establish a consistent, enforceable evidence
boundary across all currently certified phases.

⸻

2. FOUNDER TARGET

The Target is achieved when the CEO has established and verified that:

1. every relevant resident executable entry point has been identified;
2. every relevant write path into certified P10, P11, and P12 evidence has been
    mapped;
3. a resident entry point either:
    * writes only to an authorized uncertified/live location, or
    * is refused before its first write when its intended target is certified
        evidence;
4. no relevant entry point can leave a half-written certified state before
    refusal;
5. P10, P11, and P12 possess appropriate integrity detection corresponding to
    their certified evidence;
6. certified evidence can be independently checked against its authoritative
    certified state;
7. the protection mechanism does not depend solely on one specific write API
    such as write_text() or write_bytes();
8. repeatable execution demonstrates zero unauthorized certified writes;
9. mutation testing demonstrates that the relevant protections fail closed or
    otherwise detect the attempted violation;
10. the resulting state is persisted, verified, and re-discovered.

⸻

3. FRONTIER BASIS

This Goal originates from the fresh discovery performed under
GOAL-V2-003.

The discovered frontier was:

FR-3-01
Certified-Evidence Write Closure
P10 · P11 · P12

The discovery identified that 5 of 11 resident executable entry points
could still write into certified evidence.

The observed affected surfaces included:

P12 trace / governance / wiring / integrated-execution evidence
P11 resident instance evidence

The P11 case is particularly important because P11 did not previously have the
same manifest-based detection coverage as P12.

These findings are the basis for this Goal.

They must nevertheless be freshly re-verified during execution.

⸻

4. STARTING EVIDENCE IS NOT CURRENT TRUTH

The CEO shall independently verify the current state before implementation.

Do not assume that:

5 / 11

remains the current number.

Do not assume that the previously identified scripts remain unchanged.

Do not assume that no additional write paths exist.

The actual current state must be rediscovered.

⸻

5. SCOPE

The primary scope is:

P10 certified evidence
P11 certified evidence
P12 certified evidence
Resident executable entry points
Write-path enforcement
Evidence integrity detection
Mutation / negative-control verification

The Goal may include supporting changes outside these directories when they are
necessary to achieve the Target.

Cross-phase repair is permitted where required by the Target and within the
active V2 authority envelope.

⸻

6. CERTIFIED-EVIDENCE MODEL

The CEO shall preserve the distinction:

CERTIFIED EVIDENCE
≠
LIVE OBSERVATION
≠
GENERATED PROOF
≠
TEMPORARY TEST OUTPUT
≠
HISTORICAL RECORD
≠
CURRENT RUNTIME STATE

A live or regenerated observation must not silently become a mutation of
certified evidence.

Where new evidence is required, the CEO shall determine an appropriate
uncertified/live location.

⸻

7. WRITE-PATH DISCOVERY

The CEO shall discover all relevant ways in which resident executable
entry points can write into:

docs/architecture/p10
docs/architecture/p11
docs/architecture/p12

or their equivalent certified evidence surfaces.

Discovery must not be limited to:

write_text()
write_bytes()

The CEO shall account for relevant mechanisms including, where applicable:

* open();
* file replacement;
* rename;
* copy;
* append;
* serialization;
* generated files;
* subprocesses;
* shell commands;
* helper functions;
* indirect writers;
* repository scripts;
* test fixtures;
* publishing functions;
* runtime stores;
* other write APIs.

The exact discovery mechanism is left to the CEO.

⸻

8. FIRST-WRITE REQUIREMENT

The critical invariant is:

TARGET IS CERTIFIED
        ↓
WRITE ATTEMPT DETECTED
        ↓
REFUSE
        ↓
NO CERTIFIED STATE MODIFIED

The following state is insufficient:

WRITE
   ↓
PARTIAL MODIFICATION
   ↓
REFUSE

The CEO must eliminate or correctly govern such half-written states.

⸻

9. P10 · P11 · P12 CONSISTENCY

The CEO shall determine and implement an appropriate common integrity model
for P10, P11, and P12.

The exact implementation does not need to be identical if the evidence
structures legitimately differ.

However, each certified phase must have:

CERTIFIED STATE
+
IDENTIFIABLE EVIDENCE BOUNDARY
+
INTEGRITY VERIFICATION
+
WRITE PROTECTION
+
PROVENANCE

The CEO shall not assume that because P12 has a manifest, P10 and P11 are
automatically protected.

⸻

10. P10 AND P11 CONTENT MANIFESTS

The previous discovery established that P10 and P11 do not have content
manifests equivalent to P12.

The CEO shall determine whether content manifests are the appropriate
mechanism for P10 and P11.

If they are:

* construct them from authoritative certified state;
* preserve provenance;
* avoid reconstructing unsupported historical state;
* verify their contents;
* add appropriate negative controls;
* integrate them into the evidence integrity model.

If another mechanism is demonstrably more appropriate, the CEO may use it
within delegated authority and document the rationale.

⸻

11. CERTIFIED STATE SOURCE

For each certified phase, the CEO shall identify:

WHAT IS CERTIFIED?
WHO / WHAT CERTIFIED IT?
WHEN WAS IT CERTIFIED?
WHAT EXACT STATE WAS CERTIFIED?
WHERE IS THAT STATE REPRESENTED?
HOW IS THAT STATE VERIFIED?

The CEO must preserve:

CERTIFICATION AUTHORITY
≠
IMPLEMENTATION ASSUMPTION

No implementation change may manufacture a new certification decision.

⸻

12. ENTRY-POINT SAFETY

For every relevant executable entry point, the CEO shall determine one of:

SAFE
    → only writes to authorized uncertified/live locations
GUARDED
    → may target certified locations but is refused before writing
NON-WRITING
    → has no relevant certified-evidence write capability
RETIRED / HISTORICAL
    → not part of the live executable surface
UNKNOWN
    → requires further discovery

UNKNOWN must not be treated as safe.

⸻

13. HALF-WRITE ELIMINATION

The CEO shall specifically test for the class of failure discovered in
FR-3-01:

ENTRY POINT
    ↓
WRITE CERTIFIED FILE
    ↓
GUARD
    ↓
REFUSAL

The desired behavior is:

ENTRY POINT
    ↓
TARGET RESOLUTION
    ↓
CERTIFIED?
    ↓
YES
    ↓
REFUSE
    ↓
NO WRITE

If a different architecture achieves the same invariant, that is acceptable.

⸻

14. INTEGRITY DETECTION

Protection must not depend solely on prevention.

The CEO shall ensure that certified-state integrity can also be independently
checked.

Detection should identify, as applicable:

MODIFIED
MISSING
ADDED
UNEXPECTED
UNREADABLE

The exact vocabulary may follow the existing evidence framework.

The important requirement is that unauthorized change cannot silently appear as
a clean certified state.

⸻

15. NEGATIVE CONTROLS / MUTATION TESTING

The CEO shall demonstrate that the protection mechanisms actually detect or
prevent violations.

At minimum, the verification strategy should exercise mutations equivalent
to:

REMOVE / BYPASS WRITE GUARD
CHANGE CERTIFIED FILE
ADD FILE TO CERTIFIED ROOT
DELETE CERTIFIED FILE
ALTER CERTIFICATION REFERENCE
TARGET LIVE WRITER AT CERTIFIED ROOT

The exact mutation set may be expanded when discovery reveals additional
failure modes.

A mutation test that can corrupt certified evidence during its own execution
must itself be designed to prevent persistent damage to the authoritative
tree.

⸻

16. TEST ISOLATION

Mutation and negative-control testing must not require destructive modification
of the actual authoritative certified tree.

Where necessary, use:

* isolated worktrees;
* temporary copies;
* controlled fixtures;
* disposable stores;
* equivalent test environments.

The CEO shall preserve the actual certified evidence throughout execution.

⸻

17. LIVE / CERTIFIED SEPARATION

The CEO shall preserve the architecture established in GOAL-V2-002:

CERTIFIED EVIDENCE
        ↓
READ-ONLY / PROTECTED
LIVE OBSERVATIONS
        ↓
MUTABLE / SEPARATE

The CEO shall not solve write protection by simply freezing a directory that
still contains legitimate live operational state.

If a certified directory contains operational stores that genuinely require
mutation, the CEO shall determine the correct separation within delegated
architecture authority.

⸻

18. HISTORICAL RECORDS

Historical evidence must not be silently rewritten.

Previously recorded post-certification modifications must remain traceable in
history.

The CEO shall distinguish:

HISTORICAL MODIFICATION
≠
CURRENT CERTIFIED STATE

Restoring current certified bytes does not require rewriting Git history.

⸻

19. NO CERTIFICATION CHANGE

This Goal does not authorize:

* recertification;
* decertification;
* changing Founder certification decisions;
* changing the meaning of P10/P11/P12 certification;
* changing phase identity;
* changing phase completion state;
* changing Founder Reserved Authority.

The objective is protection and integrity enforcement of the already
certified state.

⸻

20. NO SCOPE EXPANSION

This Goal does not authorize:

P13 construction
Native Core expansion
new phase authorization
roadmap rewrite
governance model change
authority expansion
Founder authority modification
final AIOS acceptance

If the work exposes a necessary issue outside this envelope, classify and
escalate it.

Do not silently absorb it into this Goal.

⸻

21. F-4

F-4 — index and catalogue synchronization — is not automatically part of this
Goal.

If the CEO discovers that F-4 is directly necessary to establish or verify
certified-evidence protection, it may be included as a dependency or bounded
supporting repair.

Otherwise it remains separately classified.

The unresolved question concerning authority to edit
GOVERNANCE_INDEX.md must not be silently converted into authorization.

⸻

22. RE-DISCOVERY REQUIREMENT

After material construction:

VERIFY
    ↓
PERSIST
    ↓
RE-DISCOVER
    ↓
VERIFY AGAIN

The CEO must determine whether:

* new write paths appeared;
* new certified surfaces were discovered;
* a protection mechanism bypass exists;
* new live/certified conflicts appeared;
* existing consumers broke;
* new dependencies emerged;
* the integrity model remains coherent.

⸻

23. COMPLETION CRITERIA

The Target may be declared achieved only when the evidence supports all of
the following:

T4-01

All relevant resident executable entry points have been discovered or
classified.

T4-02

All relevant write paths into P10, P11, and P12 certified evidence have been
identified to the level required for reliable protection.

T4-03

Every relevant entry point either writes only to authorized uncertified/live
locations or is refused before its first certified-evidence write.

T4-04

No tested entry point can produce a half-written certified state before
refusal.

T4-05

P10 has an appropriate certified-state integrity mechanism.

T4-06

P11 has an appropriate certified-state integrity mechanism.

T4-07

P12’s existing integrity mechanism remains valid after the changes.

T4-08

Integrity detection identifies relevant modification, addition, deletion,
or equivalent certified-state drift.

T4-09

Mutation / negative-control testing demonstrates that protection is effective.

T4-10

The authoritative certified evidence remains intact after normal verification
and full relevant test execution.

T4-11

The live/certified storage separation remains operationally valid.

T4-12

Historical records remain preserved.

T4-13

Relevant full-suite/regression verification passes.

T4-14

Post-construction re-discovery is complete.

T4-15

Evidence supporting the Target completion claim is persisted.

⸻

24. REQUIRED VERIFICATION

The CEO shall perform sufficient verification to establish at least:

P10
CERTIFIED
    ↓
PROTECTED
    ↓
DETECTABLE
    ↓
VERIFIED
P11
CERTIFIED
    ↓
PROTECTED
    ↓
DETECTABLE
    ↓
VERIFIED
P12
CERTIFIED
    ↓
PROTECTED
    ↓
DETECTABLE
    ↓
VERIFIED

And at the system level:

ALL RELEVANT ENTRY POINTS
        ↓
NO UNAUTHORIZED CERTIFIED WRITE
        ↓
NO HALF-WRITE
        ↓
NO SILENT DRIFT

⸻

25. REQUIRED RESULT REPORT

Upon completion or blocking, the CEO shall return:

1. Target status
2. Current certified state of P10
3. Current certified state of P11
4. Current certified state of P12
5. Entry points discovered
6. Write paths discovered
7. Write paths repaired
8. Write paths intentionally refused
9. Certified evidence protection model
10. P10 integrity mechanism
11. P11 integrity mechanism
12. P12 integrity mechanism
13. Mutation / negative-control results
14. Regression results
15. Evidence integrity results
16. Live/certified separation result
17. Historical modifications preserved
18. Dependencies discovered
19. Remaining work
20. Blocked work
21. New findings
22. Authority analysis
23. Evidence persisted
24. Re-discovery result
25. Founder decisions required
26. Whether Target is achieved
27. Whether authorized construction remains
28. Whether V2 exhaustion applies

⸻

26. EXHAUSTION SEMANTICS

The CEO shall not declare exhaustion merely because:

* the five known writers are fixed;
* P10/P11 manifests exist;
* tests pass once;
* P12 remains intact;
* no currently visible defect remains.

Exhaustion requires the V2 exhaustion conditions to be satisfied after:

DISCOVERY
→
CLASSIFICATION
→
AUTHORIZED WORK
→
VERIFICATION
→
EVIDENCE
→
RE-DISCOVERY

If another actionable authorized construction item remains within this Goal,
the CEO shall continue.

⸻

27. FOUNDER-READY COMPLETION BOUNDARY

If T4-01 through T4-15 are satisfied, the CEO may report:

GOAL-V2-004 TARGET ACHIEVED — CERTIFIED-EVIDENCE WRITE CLOSURE ESTABLISHED FOR P10, P11, AND P12.

This claim means only that the evidence-protection Target was achieved.

It does not mean:

P10 COMPLETE AGAIN
P11 COMPLETE AGAIN
P12 COMPLETE AGAIN
AIOS COMPLETE
SYSTEM INTEGRITY COMPLETE
ARCHITECTURE FINAL
FOUNDER ACCEPTANCE

Those remain separate claims.

⸻

28. ESCALATION

The CEO shall escalate if execution reveals:

* a Founder Reserved Authority matter;
* a required certification change;
* a governance-model change;
* an authority expansion;
* an unresolved canonical conflict outside delegated scope;
* a fundamental architectural decision outside bounded Architecture Authority.

The CEO shall otherwise continue autonomously within the active V2 envelope.

⸻

29. FINAL FOUNDER DIRECTIVE

Close the certified-evidence write paths across P10, P11, and P12.

Begin with fresh discovery rather than assuming the previously identified
five writers are exhaustive.

Ensure every relevant executable entry point either writes only to an
authorized uncertified/live location or is refused before its first write
into certified evidence.

Eliminate half-written certified states.

Establish appropriate integrity detection for P10 and P11 while preserving
the existing P12 protection model.

Preserve the separation between certified evidence and live observations.

Use mutation and negative-control verification to demonstrate that the
protection cannot silently fail.

Preserve historical records and certified state.

Do not change certification decisions or create new authority through
implementation.

Verify the resulting system, persist evidence, re-discover, and continue
until the Target is achieved, blocked by a genuine authority/dependency
boundary, or narrow V2 exhaustion is legitimately established.

⸻

30. FOUNDER ISSUANCE

Founder:
Moriarty
Goal ID:
GOAL-V2-004
Frontier:
FR-3-01
Goal:
CERTIFIED-EVIDENCE WRITE CLOSURE
P10 · P11 · P12
Executor:
Claude Code — AIOS Co-Founder + Delegated CEO
Authority:
ACTIVE CO-FOUNDER V2 AUTHORITY ENVELOPE
Construction:
AUTHORIZED WITHIN THIS TARGET AND DELEGATED BOUNDARIES
P13:
NOT PART OF THIS TARGET
F-4:
NOT AUTOMATICALLY INCLUDED
Founder Reserved Authority:
PRESERVED
Certification Decisions:
UNCHANGED
Micro-Act Requirement:
NOT REQUIRED FOR ORDINARY AUTHORIZED EXECUTION
Status:
FINAL — FOUNDER ISSUED
Founder:
Moriarty
Signature:
Moriarty
Date:
24 September 2026

31. OPERATIVE INSTRUCTION

GOAL-V2-004
      ↓
FRESH WRITE-PATH DISCOVERY
      ↓
P10 / P11 / P12 CERTIFIED-STATE MAPPING
      ↓
ENTRY-POINT CLASSIFICATION
      ↓
FIRST-WRITE SAFETY
      ↓
INTEGRITY DETECTION
      ↓
MUTATION / NEGATIVE CONTROL
      ↓
REGRESSION
      ↓
EVIDENCE PERSISTENCE
      ↓
RE-DISCOVERY
      ↓
TARGET COMPLETION / BLOCK / EXHAUSTION
      ↓
FOUNDER REVIEW

END OF GOAL / TARGET 04
````
