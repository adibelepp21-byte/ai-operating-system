# `ACT-CC-P6-062` — T-12 Gate Resolution

**Act:** `ACT-CC-P6-062` · **Mutation:** this record only
**Result:** **T-12 RESOLVED — PHASE 6 SEPARATELY GATED** (§20 **STATE B**)
**Authority class:** **A** — an existing decision already resolves T-12
**Executor:** AIOS Co-Founder

> **NEW DECISION: NONE — EXISTING AUTHORITY SUFFICIENT.** The Founder delegated
> full authority to resolve T-12. It did not need to be exercised: T-12 was
> decided on **2026-08-22**. Issuing a decision over a closed question would have
> manufactured authority, not applied it.

> This record **supersedes the T-12 finding of
> `AIOS_P6_061_D1_SOURCE_REVIEW_AND_CORRECTION_v1.0.md`**. That record is **not
> edited**; the superseded finding remains visible there.

---

## 1. Result

[E] **`GDR-0028` — Founder Decision · T-12 Scoped Ratification of the Phase 3.289
Knowledge Admission Model.** Governance Decision Register, **2026-08-22**,
decided by **Founder / Architect (Moriarty)**. Its own header states:

> **Closes:** the `T-12` ratification question — **within the scope stated below
> and no further**

[E] **Supersession check (§6):** `GDR-0028` is the **final entry** in the
append-only Governance Decision Register (…0025 · 0026 · 0027 · **0028**).
Nothing supersedes it. The only later document mentioning T-12 anywhere in the
repository is **my own record from this session**, which named it as open.

## 2. My error — the same one, twice

[E] `ACT-CC-P6-061` identified T-12 as *"the single decision standing in front
of"* Phase 6, on the authority of `AIOS_F03_CLOSURE_AND_NEXT_GATE_v1.0.md`
(**2026-08-21**). **`GDR-0028` is dated 2026-08-22.** The closure record was
accurate when written and was superseded the next day.

[A] This is **the identical failure `ACT-CC-P6-061` was written to correct**, in
the Act that corrected it. There I found that `ACT-CC-P6-060` had relied on a
record superseded one day later — and then substituted a new claim, T-12, without
applying the freshness check to *that* claim.

[A] **Root cause, sharpened:** I applied the supersession check to the finding I
was *replacing* and not to the finding I was *substituting in*. The check belongs
to the conclusion, not to the correction.

[A] **Concrete methodological fix.** Both errors would have been caught by one
step neither Act took: **searching the Governance Decision Register**. It is the
tracked, canonical, append-only history of Founder decisions — the authoritative
answer to *"has X been decided?"* — and I searched program records and
architecture documents instead. For any question of the form *"is this decided?"*
the register is the **first** source, not a later one.

## 3. What `GDR-0028` ratified — [E], verbatim scope

Phase 3.289 §1–§15 become the canonical Knowledge Admission Model:

> the lifecycle {Candidate → Active → Superseded} with no intermediate state ·
> Memory as the sole candidate source, `occurrence_count` non-gating ·
> human-authorized promotion only · **exactly one gate** — the Governance
> subsystem's promotion authorization, affirmative `True` only · reject absolute ·
> conflict resolved by governed human review · governed replacement producing a
> new Active version with the prior **Superseded and retained** · **new version,
> never an in-place edit** · immutability of an admitted version · **fail closed**
> on any absence or non-authorization · Knowledge holds no authority of its own,
> and the direction is strictly Governance → Knowledge.

[E] **Ratification object pinned by integrity, not by title:**
`docs/architecture/history/phase3/AIOS_PHASE3_289_KNOWLEDGE_ADMISSION_MODEL_v1.0.md`
v1.0 as written, SHA-256 `1c7b5eaa6102f151…`, **159 lines**. The record states:
*"The hash and line count above are the ratified article. **Any later differing
text is not what was ratified.**"*

[E] **Authority basis:** Architecture Freeze §10 reserves the admission model to
the Architect; Phase 3.289 §20 defers to exactly this decision. The ratification
is the *"resolve it"* branch of Implementation Readiness Review §18 condition 1.

## 4. Why Phase 6 remains gated — [E] from the same instrument

`GDR-0028`'s **Explicit Scope Exclusions**, verbatim:

```
T12-D-003 — Validity-Condition Catalogue:      DEFERRED
T12-D-004 — Storage Facility:                  DEFERRED
T12-D-006 — Cross-Process Signal Trust:        PROCESS-SCOPED / ROUTED
No general Phase-6 construction
No governed read-path construction
No storage construction
No validity-condition semantics
No Identity / Authentication mutation
```

```
Construction Authority:  NONE
Mutation Authority:      BOUNDED — RATIFICATION RECORD ONLY
```

[A] **The decision that closed T-12 also, in the same breath, withheld Phase 6.**
This is not an inference from silence — *"No general Phase-6 construction"* and
*"Construction Authority: NONE"* are the instrument's own words.

[A] **A sharper consequence worth stating.** Phase 6's construction target is
`NCIR §9.5` — *"versioned, **admission-gated Knowledge store**"*. `GDR-0028`
ratifies the **admission** half and **defers the store**: `T12-D-004 — Storage
Facility: DEFERRED`, *"No storage construction."* So the Phase 6 target is
bisected by the very decision that resolved its gate. Whoever authorizes Phase 6
will be authorizing across a deferral, and should do so knowingly.

## 5. Authority determination (§11) — Class **A**

| Class | Applies? |
|---|---|
| **A — existing decision already resolves T-12** | **YES** |
| B/C — delegated determination or new decision | No — the question is closed |
| D — Founder-only | Moot |
| E — source conflict | No. `GDR-0028` supersedes the F03 closure by date and by register authority |

[A] The delegation in §2 of the Act was real and sufficient. **It was not
needed.** Deciding a settled question would have created a second, competing
instrument over the same matter — the collision pattern already recorded twice in
this program (`ACT-CC-P6-055`, `DEC-P6-040`).

## 6. T-12 gate matrix (§15)

| Criterion | Source | Evidence | Status |
|---|---|---|---|
| Canonical admission semantics | `GDR-0028` §3 | Phase 3.289 §1–§15 ratified | **SATISFIED** |
| Single admission gate | `GDR-0028` §3 | Governance promotion authorization, affirmative `True` only | **SATISFIED** |
| Versioning semantics | `GDR-0028` §3 | new version, never in-place; prior Superseded and retained | **SATISFIED** |
| Rejection semantics | `GDR-0028` §3 | reject absolute; fail closed on absence/non-authorization | **SATISFIED** |
| Authority direction | `GDR-0028` §3 | strictly Governance → Knowledge; Knowledge holds none | **SATISFIED** |
| Ratification recorded | Register, `GDR-0028` | final entry, append-only | **SATISFIED** |
| Validity-condition catalogue | `GDR-0028` exclusions | **T12-D-003 DEFERRED** | **OUT OF SCOPE** |
| Storage facility | `GDR-0028` exclusions | **T12-D-004 DEFERRED** | **OUT OF SCOPE** |
| Phase 6 construction authority | `GDR-0028` | **NONE** | **NOT GRANTED** |

## 7. Status

```
T-12                     RESOLVED — GDR-0028, 2026-08-22, scoped
Master Roadmap Phase 6   NOT BEGUN · not eligible to construct · construction authority NONE
P7                       NOT AUTHORIZED — unchanged
Phase 5                  complete — unchanged
P6-AES-01                separate track — unchanged (§4 distinction preserved)
```

[A] Phase 6 is **NOT BEGUN**. It is not made eligible by T-12's resolution,
because the same instrument withholds construction authority explicitly.

## 8. Protected state (§10, §21.11)

[E] **PROTECTED STATE: UNTOUCHED.** All 13 remain unstaged and unmodified. Five
are T-12 material.

[A] Worth recording: **none was needed.** T-12 resolved entirely from
`docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md`, a tracked canonical
source. The Act's §10 asked whether resolution required touching them; the answer
is **no**, and it was answered by finding the decision rather than by reasoning
about the bar.

## 9. Verification

```
Created                  this record only     Modified files   0
Protected packages       13 — untouched       native_core      676 OK (expected failures = 1)
consumers 22 OK · tools 89 OK                 C1–C4 · E-01 · Phase 5 · 26 edges — untouched
```

**Construction performed: NONE.** No decision issued. No protected package
touched. No canonical artifact amended.

**DEVIATIONS: NONE.**
