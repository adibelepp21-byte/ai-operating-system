# `FD-P13-005` — Founder Disposition of P13 Blueprint Draft v0.3

**Document type:** Founder Decision Record
**Disposition:** **OPTION B** — ACCEPT WITH MODIFICATION, bounded to `F-1` + `F-2`
**Status:** FINAL — ISSUED · **Founder:** Moriarty · 23 September 2026
**Reviewed artifact:** `P13-BLUEPRINT-DRAFT-v0.3-NON-CANONICAL.md` · `sha256 6212a717…39e2`
**Predecessor:** `ACT-CC-P13-007` — COMPLETE / SPENT

---

## Provenance

The body below `§ RECORD` is the Founder's, persisted **verbatim**. The
surrounding material is Claude's and is separated for that reason.

## The operative consequence: no modification is authorized

```text
DISPOSITION        OPTION B — ACCEPT WITH MODIFICATION (F-1, F-2 only)
ACT-CC-P13-004     SPENT      ACT-CC-P13-005   SPENT
ACT-CC-P13-006     SPENT      ACT-CC-P13-007   COMPLETE / SPENT
ACT-CC-P13-008     REQUIRED — DOES NOT EXIST
```

`§8`: *"This Founder Decision itself does not constitute the execution Act for
modifying v0.3 … a new bounded execution instrument is required."*

**v0.3 was not modified and v0.4 does not exist.** `ACT-CC-P13-008` was verified
absent before anything else was done.

## Preservation verified — `§9`

```text
v0.1  75775cbd4cdccc0404243beb815e2d52c66b44201d02b98856f8a22d08d4d5f1   MATCH
v0.2  a4095a33610e099bcc0960f27b75a5104b6ab049f065b16bcddea011b89b9c57   MATCH
v0.3  6212a7171fa22cfad23e3625ea62d3191b5ed3cc7391e5d86d6c3a9990b139e2   MATCH
```

**None was appended to.** All three are now fixed by Founder-recorded hashes; an
append would break them. This record points at them.

## One observation for `ACT-CC-P13-008`, offered as fact

`§6` prescribes the corrected ledger counts:

```text
UPGRADES 1  ·  DOWNGRADES / PRECISION GAINS 6  ·  CORRECTIONS 1  ·  STRUCTURAL 7
                                                                   = 15
```

**v0.3's ledger carries 16 rows** (`L-01` … `L-16`, counted this turn). The
sixteenth is **`L-02`**, which belongs to a fifth category already present in
v0.3's summary block at line 693:

```text
PROVENANCE STRENGTHENED, CONCLUSION UNCHANGED:  1   (L-02)
```

**`§6` anticipates this**, and its own wording resolves it: *"or an equivalent
accounting representation that **accurately reconciles every ledger row**."*
Writing only the four prescribed numbers would leave the ledger at 15 of 16 and
would not reconcile — which is the defect `F-2` exists to remove. **Retaining
the fifth line satisfies `§6` as written.**

This is stated as an arithmetic fact for the correction Act to act on, **not as
a criticism of the decision and not as a modification of it.** The Founder's
prescribed four counts are each correct; they simply do not enumerate the fifth
category, and `§6` already permits the equivalent representation that does.

## A note on `§19`'s checkbox polarity

`§19` marks `[X]` against the disposition, the accepted artifact and the two
required corrections, and leaves `[ ]` against *Scope Expansion*,
*Canonicalization*, *P13 Construction*, *P13 Certification*, *GAP-0001 Closure*
and *Native Core Modification* — each of which is **labelled `NOT AUTHORIZED`**.

The polarity is inverted from earlier records, where `[X]` marked the withheld
items. **The effect is identical under either reading**: every one of those six
is not authorized, whether the box is read as marking the label or as
withholding it. Recorded because a reader comparing records might otherwise
pause over it; **nothing done here depends on which reading is correct.**

## Register effect

`GAP-0001` **OPEN · APEX**, unchanged (`§14`). Register **28**. Native Core
**11** (`§15`). 12 Founder-reserved and 2 Architect-reserved matters preserved,
0 decided (`§16`, `§17`). `P13 CONSTRUCTION = NOT AUTHORIZED` (`§13`).

**`ACCEPT WITH MODIFICATION ≠ CANONICALIZATION`** (`§12`). v0.3 is accepted as
the **non-canonical working basis** and nothing more (`§4`).

---

# § RECORD — issued by the Founder, verbatim

FD-P13-005

FOUNDER DISPOSITION OF P13 BLUEPRINT DRAFT v0.3

Document Type: Founder Decision Record
Decision Domain: P13 Preparation / Blueprint Disposition
Predecessor: ACT-CC-P13-007
Reviewed Artifact: P13-BLUEPRINT-DRAFT-v0.3-NON-CANONICAL.md
Artifact SHA256: 6212a7171fa22cfad23e3625ea62d3191b5ed3cc7391e5d86d6c3a9990b139e2
Status Before Decision: NON-CANONICAL
P13 Canonical Definition: NOT ESTABLISHED
GAP-0001: OPEN · APEX
P13 Construction Authorization: NOT GRANTED
Native Core: 11

1. DECISION SUBJECT

This Founder Decision disposes of:

P13-BLUEPRINT-DRAFT-v0.3-NON-CANONICAL.md

following the completed execution of:

ACT-CC-P13-007 — P13 v0.3 Founder Review Preparation & Disposition Analysis Act.

The Founder Review Package reports:

ACT-CC-P13-007 = EXECUTION COMPLETE
EXHAUSTION = EXHAUSTED_WITH_CLASSIFIED_REMAINDER

No prior Founder disposition was made by Claude Code.

2. FOUNDER DECISION

SELECTED OPTION

OPTION B — ACCEPT WITH MODIFICATION

The Founder accepts v0.3 as the current non-canonical working basis for
continued P13 preparation, subject to bounded correction of the two defects
identified by ACT-CC-P13-007.

This decision does not canonicalize v0.3.

It does not establish the substantive canonical definition of P13.

It does not authorize P13 construction.

It does not authorize P13 certification.

3. BASIS OF DECISION

The Founder Decision is based on the evidence recorded by
ACT-CC-P13-007.

The following conditions were independently verified:

7/7 O5 mappings independently re-verified
14/14 architectural sections byte-identical v0.2 → v0.3
Native Core = 11
v0.1 preserved
v0.2 preserved
v0.3 preserved
No canonicalization occurred
No construction occurred
No Founder decision was made by Claude
No Architect decision was made by Claude
18/18 negative controls held

The review also established that the two identified defects are located in the
evidence apparatus of v0.3 rather than in its substantive architecture.

4. ACCEPTANCE BOUNDARY

Acceptance under this Decision means:

v0.3 is accepted as the current non-canonical working basis for the
next bounded correction operation.

Acceptance does NOT mean:

v0.3 = CANONICAL
v0.3 = P13 DEFINITION
v0.3 = AUTHORIZATION
v0.3 = CONSTRUCTION
v0.3 = CERTIFICATION

The artifact remains:

NON-CANONICAL

until a separate valid Founder canonicalization decision establishes otherwise.

5. REQUIRED MODIFICATION — F-1

Defect

F-1 identified that v0.3 §O5.4 states:

ESTABLISHED — the seventeen-item list is complete again

However, the number seventeen originates from the P13-004 preparation record
and no resident canonical source enumerating seventeen P13 scope items was
identified.

Therefore the word:

complete

is stronger than the evidence supports.

Required Correction

The correction shall:

1. preserve the seventeen-item preparation-record list;
2. preserve the individual classifications;
3. preserve the seven independently verified O5 mappings;
4. remove or qualify the unsupported ESTABLISHED completeness claim;
5. explicitly state that the seventeen-item enumeration is a
    PREP-RECORD;
6. explicitly distinguish completeness relative to the preparation record from
    completeness relative to a canonical P13 scope definition;
7. preserve GAP-0001 as OPEN/APEX;
8. avoid creating a canonical P13 scope through wording.

The correction shall be the minimum textual change necessary to restore
epistemic accuracy.

6. REQUIRED MODIFICATION — F-2

Defect

The v0.3 change ledger summary states:

UPGRADES: 0

while row L-13 explicitly identifies itself as:

the only upgrade in this lineage

The review established that the underlying row-level facts are correct but the
summary counter is stale.

Required Correction

The change ledger shall be corrected to reflect the actual row-level state:

UPGRADES: 1
DOWNGRADES / PRECISION GAINS: 6
CORRECTIONS: 1
STRUCTURAL: 7

or an equivalent accounting representation that accurately reconciles every
ledger row.

No substantive architectural change is authorized by this correction.

7. BOUNDARY OF MODIFICATION

The authorized correction scope is strictly:

F-1
F-2

The following are explicitly OUT OF SCOPE:

P13 identity redesign
P13 mission redesign
P13 architecture redesign
five candidate surface redesign
Agent lifecycle selection
autonomy boundary decision
P13 exit criteria decision
Native Core modification
Native Core #12
Optimization → Governance resolution
ADR-0029 resolution
P13 corpus reconstruction
GAP-0001 closure
canonicalization
P13 construction
P13 certification

No modification outside F-1 and F-2 is authorized by this Decision.

8. NEW EXECUTION AUTHORITY REQUIRED

This Founder Decision itself does not constitute the execution Act for modifying
v0.3.

Because:

ACT-CC-P13-004 = SPENT
ACT-CC-P13-005 = SPENT
ACT-CC-P13-006 = SPENT
ACT-CC-P13-007 = COMPLETE / SPENT

a new bounded execution instrument is required.

The authorized next instrument is:

ACT-CC-P13-008
P13 NON-CANONICAL BLUEPRINT v0.3
F-1 / F-2 CORRECTION ACT

Its sole purpose shall be to apply the two corrections identified above and
produce:

P13-BLUEPRINT-DRAFT-v0.4-NON-CANONICAL.md

The new Act shall preserve v0.3 immutably.

9. VERSION PRESERVATION

The following artifacts remain immutable historical records:

v0.1
SHA256:
75775cbd4cdccc0404243beb815e2d52c66b44201d02b98856f8a22d08d4d5f1
v0.2
SHA256:
a4095a33610e099bcc0960f27b75a5104b6ab049f065b16bcddea011b89b9c57
v0.3
SHA256:
6212a7171fa22cfad23e3625ea62d3191b5ed3cc7391e5d86d6c3a9990b139e2

None may be overwritten.

10. v0.4 STATUS

If ACT-CC-P13-008 executes successfully:

v0.4 = NON-CANONICAL

v0.4 shall not automatically inherit any stronger status from this Decision.

In particular:

v0.4 ≠ CANONICAL P13
v0.4 ≠ P13 AUTHORIZATION
v0.4 ≠ P13 CONSTRUCTION AUTHORIZATION
v0.4 ≠ P13 CERTIFICATION

11. REQUIRED VERIFICATION AFTER MODIFICATION

ACT-CC-P13-008 shall independently verify:

F-1 corrected
F-2 corrected
v0.3 unchanged
v0.4 hash persisted
seven O5 mappings unchanged
Native Core = 11
architectural sections unchanged
GAP-0001 remains OPEN
no Founder-reserved matter decided
no Architect-reserved matter decided
no canonicalization occurred
no construction occurred

The resulting v0.4 must then undergo a fresh Founder review gate.

12. NO AUTOMATIC CANONICALIZATION

This Decision explicitly establishes:

ACCEPT WITH MODIFICATION
≠
CANONICALIZATION

After v0.4 exists, the next question remains whether the resulting artifact is
sufficiently defined and authorized for Founder canonicalization consideration.

Canonicalization requires a separate Founder decision.

13. NO AUTOMATIC P13 AUTHORIZATION

Nothing in this Decision authorizes:

P13 CONSTRUCTION
P13 IMPLEMENTATION
P13 ACTIVATION
P13 DEPLOYMENT
P13 CERTIFICATION

P13 remains:

NOT AUTHORIZED FOR CONSTRUCTION

14. GAP-0001

GAP-0001 — WHAT IS P13? remains:

OPEN
APEX

This Decision does not close it.

The correction of F-1 and F-2 does not constitute a substantive resolution of
P13 identity.

15. NATIVE CORE

The Native Core remains:

11

No Native Core modification is authorized.

No twelfth Native Core boundary may be created under the resulting correction
Act.

16. FOUNDER-RESERVED MATTERS

The following remain Founder-reserved unless separately decided:

canonical P13 definition
meaning of "Super Intelligence"
P13 continuation
canonicalization
P13 construction authorization
P13 certification
Native Core expansion
P13 exit criteria
autonomy boundary
Agent lifecycle
P13 corpus residency
FD-2 ratification

No item above is decided by this record except the disposition of v0.3 stated in
§2.

17. ARCHITECT-RESERVED MATTERS

The following remain Architect-reserved:

AD-P13-001
Optimization → Governance
AD-P13-002
ADR-0029 cross-PD interface

Neither is modified or decided here.

18. GOVERNANCE INVARIANTS

This Decision preserves:

DRAFT ≠ CANON
CANONICALIZATION ≠ CONSTRUCTION
CONSTRUCTION ≠ CERTIFICATION
READINESS ≠ AUTHORIZATION
EVIDENCE ≠ AUTHORITY
VERIFICATION ≠ CANONICALIZATION
EXHAUSTION ≠ FOUNDER DECISION

19. FOUNDER AUTHORIZATION

Decision:
[X] OPTION B — ACCEPT WITH MODIFICATION
Accepted Artifact:
P13-BLUEPRINT-DRAFT-v0.3-NON-CANONICAL.md
Acceptance Status:
ACCEPTED AS NON-CANONICAL WORKING BASIS
Required Corrections:
[X] F-1
[X] F-2
Scope Expansion:
[ ] NOT AUTHORIZED
Canonicalization:
[ ] NOT AUTHORIZED
P13 Construction:
[ ] NOT AUTHORIZED
P13 Certification:
[ ] NOT AUTHORIZED
GAP-0001 Closure:
[ ] NOT AUTHORIZED
Native Core Modification:
[ ] NOT AUTHORIZED
Next Execution Instrument:
ACT-CC-P13-008
Founder:
Moriarty
Signature:
Moriarty
Date:
23 September 2026
Status:
FINAL — ISSUED

20. OPERATIVE EFFECT

Upon persistence of this Founder Decision:

v0.3
    ↓
ACCEPTED WITH MODIFICATION
    ↓
F-1 + F-2 ONLY
    ↓
NEW BOUNDED ACT
    ↓
v0.4 NON-CANONICAL
    ↓
FRESH VERIFICATION
    ↓
FOUNDER REVIEW

No other P13 construction activity is authorized.

The purpose of this Decision is to preserve the valid work already completed,
correct the two demonstrated evidence defects, and prevent either defect from
being silently carried into the next P13 decision gate.
