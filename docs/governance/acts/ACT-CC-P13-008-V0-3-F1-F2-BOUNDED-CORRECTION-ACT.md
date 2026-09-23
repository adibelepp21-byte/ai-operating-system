# `ACT-CC-P13-008` — P13 Non-Canonical Blueprint v0.3 · `F-1`/`F-2` Bounded Correction & Verification Act

**Document type:** Founder-Issued Bounded Execution Authority
**Issued by:** Founder — Moriarty · 23 September 2026 · `§28`
**Status:** FINAL — ISSUED · **OPERATIVE**
**Parent decision:** [`FD-P13-005`](FD-P13-005-FOUNDER-DISPOSITION-OF-BLUEPRINT-V0-3.md) — Option B
**Target:** v0.3 `sha256 6212a717…39e2` → `P13-BLUEPRINT-DRAFT-v0.4-NON-CANONICAL.md`
**Predecessor Acts:** `-004` · `-005` · `-006` · `-007` — all **SPENT**

```text
SCOPE   F-1 AND F-2 ONLY
NATIVE CORE 11 · GAP-0001 OPEN · APEX · CANONICALIZATION NOT AUTHORIZED
```

---

## Provenance

The body below `§ RECORD` is the Founder's, persisted **verbatim**. The
surrounding material is Claude's and is separated for that reason.

## `§10` confirms the arithmetic observation, independently derived

`P13-012 §4` reported that `FD-P13-005 §6`'s four counts sum to 15 against 16
ledger rows, with `L-02` in a fifth category. **`§10` of this Act prescribes
exactly that five-category reconciliation totalling 16**, and `§9.1` states
`L-02` *"MUST NOT be forced into one of the four other categories."*

The categorisation was re-derived this execution from each row's own direction
column, **not read off the Act's numbers**, and returns the same result:

```text
UPGRADE 1 (L-13) · DOWNGRADE/PRECISION 6 (L-01 L-03 L-04 L-11 L-14 L-16)
CORRECTION 1 (L-15) · STRUCTURAL 7 (L-05…L-10, L-12) · PROVENANCE 1 (L-02)
                                                                   = 16
```

Execution record:
[`P13-013`](../../architecture/p13-preparation/P13-013-ACT-CC-P13-008-EXECUTION-RECORD.md).

---

# § RECORD — issued by the Founder, verbatim

ACT-CC-P13-008

P13 NON-CANONICAL BLUEPRINT v0.3

F-1 / F-2 BOUNDED CORRECTION & VERIFICATION ACT

Document Type: Founder-Issued Bounded Execution Authority
Authority Class: P13 Preparation / Non-Canonical Blueprint Correction
Executor: Claude Code — Co-Founder / Delegated Execution Authority
Issuing Authority: Founder — Moriarty
Parent Founder Decision: FD-P13-005
Parent Review Act: ACT-CC-P13-007
Target Artifact: P13-BLUEPRINT-DRAFT-v0.3-NON-CANONICAL.md
Target SHA256: 6212a7171fa22cfad23e3625ea62d3191b5ed3cc7391e5d86d6c3a9990b139e2
Target Status: NON-CANONICAL
Output Artifact: P13-BLUEPRINT-DRAFT-v0.4-NON-CANONICAL.md
P13 Canonical Definition: NOT ESTABLISHED
GAP-0001: OPEN — APEX
P13 Construction Authorization: NOT GRANTED
Native Core: 11
Status: FINAL — ISSUED

1. PURPOSE

This Act authorizes Claude Code to perform the two bounded corrections accepted
by Founder Decision FD-P13-005 against:

P13-BLUEPRINT-DRAFT-v0.3-NON-CANONICAL.md

The only authorized substantive correction targets are:

F-1 — O5.4 completeness / epistemic classification defect
F-2 — Change-ledger accounting reconciliation defect

The purpose is to produce:

P13-BLUEPRINT-DRAFT-v0.4-NON-CANONICAL.md

and independently verify that the two defects have been corrected without
architectural, canonical, authority, or scope expansion.

2. GOVERNING DECISION

Founder Decision FD-P13-005 selected:

OPTION B — ACCEPT WITH MODIFICATION

The accepted modification scope is expressly limited to:

F-1
F-2

FD-P13-005 §8 requires this Act before any modification occurs.

Therefore:

FD-P13-005
    ↓
ACT-CC-P13-008
    ↓
v0.3 → v0.4

No execution authority is inferred from FD-P13-005 beyond this Act.

3. EXECUTION TAKEOVER

Claude Code is granted full bounded execution autonomy for all technical work
necessary to execute F-1 and F-2.

This includes:

* baseline verification;
* source inspection;
* exact target-location identification;
* modification;
* artifact generation;
* hash calculation;
* change accounting;
* tests;
* citation audit;
* negative controls;
* comparison against v0.3;
* re-verification;
* persistence;
* fresh re-discovery;
* exhaustion determination.

No Micro-Act is required for ordinary technical work within this scope.

Claude Code must not request Micro-Acts for routine correction, testing,
verification, or persistence.

4. BASELINE VERIFICATION

Before modifying anything, Claude Code MUST independently verify:

Target:
P13-BLUEPRINT-DRAFT-v0.3-NON-CANONICAL.md
SHA256:
6212a7171fa22cfad23e3625ea62d3191b5ed3cc7391e5d86d6c3a9990b139e2

The baseline must also verify:

v0.1 preserved
v0.2 preserved
v0.3 present
v0.3 hash matches
repository state understood
ACT-CC-P13-008 is the active execution authority

If the v0.3 hash does not match:

STOP — BASELINE INTEGRITY FAILURE.

No reconstruction is permitted.

5. HISTORICAL IMMUTABILITY

The following artifacts MUST remain unchanged:

v0.1
SHA256:
75775cbd4cdccc0404243beb815e2d52c66b44201d02b98856f8a22d08d4d5f1
v0.2
SHA256:
a4095a33610e099bcc0960f27b75a5104b6ab049f065b16bcddea011b89b9c57
v0.3
SHA256:
6212a7171fa22cfad23e3625ea62d3191b5ed3cc7391e5d86d6c3a9990b139e2

v0.3 is a historical review artifact after this Act executes.

It MUST NOT be overwritten.

The output must be a new artifact:

P13-BLUEPRINT-DRAFT-v0.4-NON-CANONICAL.md

6. F-1 — O5.4 COMPLETENESS CLAIM

6.1 Finding

ACT-CC-P13-007 identified:

F-1 — MATERIAL

The v0.3 O5.4 section places the statement:

ESTABLISHED — the seventeen-item list is complete again

inside an ESTABLISHED block.

The review established that:

* the number seventeen originates in the P13-004 preparation record;
* the preparation record was derived from the non-resident corpus;
* no resident canonical P13 source was identified that enumerates seventeen
    P13 scope items.

Therefore:

17-item preparation-record enumeration
≠
canonical P13 scope enumeration

7. F-1 REQUIRED CORRECTION

Claude Code shall make the minimum textual correction necessary to prevent
the v0.3 wording from asserting canonical completeness.

The corrected v0.4 must clearly distinguish:

PREPARATION-RECORD ENUMERATION

from:

CANONICAL P13 SCOPE

The seventeen-item list may remain.

The underlying item classifications may remain.

The seven independently verified O5 mappings may remain.

But v0.4 MUST NOT state or imply that:

seventeen is the canonically established complete P13 scope.

The corrected wording must preserve the epistemic state actually supported by
the evidence.

8. F-1 PRESERVATION REQUIREMENTS

The correction MUST NOT:

* remove the seventeen preparation-record items merely to avoid the defect;
* redefine the P13 scope;
* establish a new canonical scope;
* close GAP-0001;
* infer missing canonical scope;
* replace UNKNOWN with FACT;
* replace preparation evidence with canonical evidence;
* alter the seven verified O5 mappings.

The goal is:

CORRECT CLASSIFICATION

not:

ARCHITECTURAL RESOLUTION

9. F-2 — CHANGE LEDGER ACCOUNTING

9.1 Finding

ACT-CC-P13-007 identified:

F-2 — MINOR

The v0.3 change ledger contains:

L-01 … L-16

Therefore:

TOTAL LEDGER ROWS = 16

The v0.3 summary separately contains:

UPGRADES
DOWNGRADES / PRECISION GAINS
CORRECTIONS
STRUCTURAL
PROVENANCE STRENGTHENED, CONCLUSION UNCHANGED

L-02 belongs to:

PROVENANCE STRENGTHENED, CONCLUSION UNCHANGED

It MUST NOT be forced into one of the four other categories.

10. F-2 REQUIRED RECONCILIATION

The corrected ledger MUST reconcile all sixteen rows.

The minimum factual reconciliation is:

UPGRADES                              1
DOWNGRADES / PRECISION GAINS          6
CORRECTIONS                           1
STRUCTURAL                            7
PROVENANCE STRENGTHENED,
CONCLUSION UNCHANGED                  1
-----------------------------------------
TOTAL                                 16

The exact labels may be retained if they are already present in v0.3.

Equivalent wording is permitted only if:

ALL 16 ROWS
=
ACCOUNTED FOR

The correction MUST NOT eliminate L-02.

The correction MUST NOT reclassify L-02 merely to make the arithmetic fit.

11. F-2 ACCOUNTING INVARIANT

The following invariant must hold after correction:

COUNT(L-01 … L-16)
=
SUM(ALL EXPLICIT LEDGER CATEGORY COUNTS)
=
16

Any additional ledger category must be explicitly named.

No row may remain implicitly unaccounted.

No row may be double-counted.

No row may be omitted.

12. MINIMUM-CHANGE RULE

Claude Code shall perform the smallest modification set necessary to correct:

F-1
F-2

The following v0.3 content shall remain unchanged unless a literal textual
adjustment is mechanically required by F-1 or F-2:

O1
O2
O3
O4
O5 mappings other than the defective completeness statement
O6
O7
O8
O9
O10
§N
§S
§R
§D
§Q

No architectural redesign is permitted.

13. NO ARCHITECTURAL CHANGE

This Act does not authorize:

* P13 architecture redesign;
* P13 identity redesign;
* mission redesign;
* five-surface redesign;
* Agent lifecycle selection;
* autonomy definition;
* exit-criteria definition;
* Agent architecture decision;
* Optimization → Governance resolution;
* ADR-0029 resolution;
* P13 system-integration redesign.

Any discovered issue outside F-1/F-2 must be:

FIND
→ CLASSIFY
→ RECORD
→ DO NOT MODIFY

14. NO CANONICALIZATION

This Act does NOT authorize:

P13 canonicalization

Therefore:

v0.4 = NON-CANONICAL

regardless of how successful the correction and verification are.

Successful execution does not establish canonical P13 definition.

15. NO P13 CONSTRUCTION

This Act does not authorize:

* implementation;
* runtime construction;
* deployment;
* activation;
* operationalization;
* P13 certification;
* P13 completion.

P13 remains:

NOT AUTHORIZED FOR CONSTRUCTION

16. GAP-0001

GAP-0001 — WHAT IS P13? remains:

OPEN — APEX

F-1 correction must not close it.

F-2 correction must not close it.

The existence of a corrected preparation artifact does not resolve the
substantive canonical P13 definition.

17. NATIVE CORE

Native Core remains:

11

No Native Core change is authorized.

No Native Core #12 may be created.

18. FULL VERIFICATION REQUIREMENTS

After correction, Claude Code MUST verify:

V-01 v0.3 baseline hash remains unchanged.
V-02 v0.1 remains unchanged.
V-03 v0.2 remains unchanged.
V-04 v0.4 exists.
V-05 v0.4 is explicitly non-canonical.
V-06 F-1 wording is corrected.
V-07 F-2 ledger accounting reconciles all 16 rows.
V-08 L-02 remains represented in its fifth category.
V-09 Seven O5 mappings remain independently supported.
V-10 Native Core remains 11.
V-11 GAP-0001 remains OPEN/APEX.
V-12 No P13 construction occurred.
V-13 No canonicalization occurred.
V-14 No Founder decision was manufactured.
V-15 No Architect decision was manufactured.
V-16 No previous Act was reused as authority.

19. FALSIFICATION

Claude Code must attempt to falsify its own correction.

At minimum:

F-TEST-01 Attempt to show that v0.4 still implies: 17 = canonical complete P13 scope
F-TEST-02 Attempt to produce an arithmetic mismatch in the 16-row ledger.
F-TEST-03 Attempt to identify an unaccounted ledger row.
F-TEST-04 Attempt to identify a double-counted ledger row.
F-TEST-05 Attempt to show that L-02 was silently absorbed into another category.
F-TEST-06 Attempt to identify architectural changes outside F-1/F-2.
F-TEST-07 Attempt to show that v0.4 accidentally acquired canonical status.

If falsification succeeds, the defect must be recorded rather than hidden.

20. NEGATIVE CONTROLS

Claude Code shall verify:

NC-01  v0.1 unchanged
NC-02  v0.2 unchanged
NC-03  v0.3 unchanged
NC-04  v0.3 hash preserved
NC-05  v0.4 is the only intended new Blueprint artifact
NC-06  no previous Act reused
NC-07  no self-authorization
NC-08  no canonicalization
NC-09  no P13 construction
NC-10  no Native Core modification
NC-11  no Native Core #12
NC-12  GAP-0001 remains open
NC-13  no Founder decision manufactured
NC-14  no Architect decision manufactured
NC-15  no proposal converted into canonical fact
NC-16  no preparation record converted into canonical scope
NC-17  L-02 not eliminated
NC-18  all 16 ledger rows accounted
NC-19  no ledger row double-counted
NC-20  F-1 and F-2 only substantive corrections

21. PERSISTENCE

Claude Code shall persist:

1. v0.4;
2. execution record;
3. correction ledger;
4. verification results;
5. falsification results;
6. negative-control results;
7. final hash;
8. final Git commit;
9. final exhaustion state.

v0.3 must remain available as immutable historical evidence.

22. RE-DISCOVERY

After verification, Claude Code MUST perform fresh re-discovery.

The purpose is to determine whether the correction introduced:

* new epistemic ambiguity;
* new arithmetic inconsistency;
* accidental architectural modification;
* status drift;
* authority drift;
* new material defect.

Rediscovery remains bounded to F-1/F-2 and their direct consequences.

It does not authorize general P13 redesign.

23. EXHAUSTION

The Act is exhausted when no additional authorized work remains that can
materially improve the correctness of F-1/F-2 correction and verification.

Valid terminal states:

EXHAUSTED
EXHAUSTED_WITH_CLASSIFIED_REMAINDER
BLOCKED_AUTHORITY
BLOCKED_DEPENDENCY

Claude Code shall not claim clean exhaustion if a material F-1/F-2 defect
remains undisclosed.

24. STOP CONDITIONS

Claude Code must stop and classify if:

1. v0.3 baseline does not match;
2. F-1 cannot be corrected without redefining P13;
3. F-2 cannot be reconciled without changing historical ledger facts;
4. an additional architectural defect is discovered;
5. canonicalization becomes necessary;
6. P13 construction becomes necessary;
7. Founder authority becomes necessary;
8. Architect authority becomes necessary;
9. correction would require changing v0.1/v0.2/v0.3;
10. evidence requires prohibited reconstruction.

Correct response:

STOP
→ CLASSIFY
→ PERSIST
→ HANDOFF

25. FINAL OUTPUT

Claude Code shall produce a final execution report containing:

1. Baseline verification
2. v0.3 hash
3. v0.4 hash
4. F-1 correction
5. F-2 correction
6. Full 16-row ledger reconciliation
7. L-02 explicit category
8. Diff summary
9. Architectural-preservation verification
10. O5 re-verification
11. Falsification results
12. Negative-control results
13. v0.1/v0.2/v0.3 preservation
14. Native Core measurement
15. GAP-0001 status
16. Authority-boundary verification
17. Re-discovery result
18. Exhaustion result
19. Git commit
20. Exact next gate

26. TERMINAL STATE

Successful completion means:

ACT-CC-P13-008 = COMPLETE
v0.3 = PRESERVED
v0.4 = NON-CANONICAL
F-1 = CORRECTED
F-2 = CORRECTED

It does NOT mean:

P13 = CANONICAL
P13 = AUTHORIZED
P13 = CONSTRUCTED
P13 = CERTIFIED
GAP-0001 = CLOSED

27. FINAL AUTHORITY BOUNDARY

The operative authority is:

FD-P13-005 → ACT-CC-P13-008 → F-1 / F-2 CORRECTION ONLY → v0.4 →
VERIFICATION → FOUNDER REVIEW

Claude Code is authorized to execute the entire technical correction and
verification loop without Micro-Acts.

Claude Code is NOT authorized to:

canonicalize P13
authorize P13 construction
close GAP-0001
modify Native Core
make Founder decisions
make Architect-reserved decisions

The governing principle remains:

FULL EXECUTION AUTONOMY WITHIN BOUNDED SCOPE; NO AUTHORITY CROSSING.

28. FOUNDER ISSUANCE

Founder: Moriarty
Decision: ISSUE ACT-CC-P13-008
Authority Granted: FULL BOUNDED EXECUTION AUTHORITY
Scope: F-1 / F-2 CORRECTION AND VERIFICATION
Target: P13-BLUEPRINT-DRAFT-v0.3-NON-CANONICAL.md
Target SHA256: 6212a7171fa22cfad23e3625ea62d3191b5ed3cc7391e5d86d6c3a9990b139e2
Output: P13-BLUEPRINT-DRAFT-v0.4-NON-CANONICAL.md
Modification Boundary: F-1 / F-2 ONLY
Canonicalization: NOT AUTHORIZED
P13 Construction: NOT AUTHORIZED
P13 Certification: NOT AUTHORIZED
Native Core Modification: NOT AUTHORIZED
GAP-0001 Closure: NOT AUTHORIZED
Founder Decision: RESERVED TO FOUNDER
Architect Decisions: RESERVED TO ARCHITECT
Micro-Act Requirement: NOT REQUIRED FOR ROUTINE WORK WITHIN SCOPE
Founder: Moriarty
Signature: Moriarty
Date: 23 September 2026
Status: FINAL — ISSUED

29. OPERATIVE EFFECT

Upon persistence of this Act, Claude Code may immediately begin execution.

No additional Founder confirmation is required for ordinary work within the
explicit F-1/F-2 boundary.

The expected transition is:

v0.3 → F-1 / F-2 bounded correction → v0.4 → independent verification →
falsification → re-discovery → exhaustion → Founder Review

No step in this sequence constitutes P13 canonicalization or P13 construction.
