# AIOS Phase 1–6 Governance Residual Closure & Final Baseline Assessment

**Prepared under:** FOUNDER · `ACT-CC-P1-6-077`
**Execution Office:** Claude Code / Co-Founder Office · **Date:** 2026-08-28
**Baseline:** `ACT-CC-P1-6-076`, independently re-verified per `§3`/`§5`
**Method:** register-first discovery · canonical source as authority · empirical
tests as evidence · Founder Decisions as governance authority

> **This artifact ratifies nothing, certifies nothing, and issues no Decision.**
> It records verification, remediation performed under `§19`, and one
> consolidated escalation package. No Decision ID is assigned anywhere in it.

---

## 1. Executive result

### OUTCOME **B** — CERTIFICATION-READY / DECISION PENDING

Technical evidence across Phase 1–6 is complete and green. **One** governance
action stands between the current state and a legitimately governance-closed
baseline: **Phase 5 has never been certified**, and that transition is reserved
to the Founder / Program Owner by Master Program Volume V §3.

`§24` conditions **3** (*"every required certification has been validly issued
and registered"*) and **5** (*"no Founder/Architect decision remains outstanding
that is required for the baseline declaration"*) are therefore **not satisfied**,
and the final declaration in `§30` is **withheld**. Declaring a baseline
governance-closed while one of its six phases has never been certified would be
promoting status by inference, which `§20` forbids in terms.

**Outcome A is not available. It is one Founder decision away.**

This Act also found and fixed a regression that `ACT-CC-P1-6-076` introduced and
shipped — see `§7`. It is disclosed there rather than folded into a summary line.

---

## 2. Corrections to `ACT-CC-P1-6-076`

`§5` requires that a P076 conclusion not be carried forward merely because P076
states it. Two are corrected here.

### 2.1 `R-14` was materially misframed — `GDR-0001` already dispositions it

P076 recorded that *"the canonical Master Program is not in the tracked
repository"* and recommended a Founder admission decision, implying an
unresolved corpus gap. **`GDR-0001` — Founder Decision G1′, Constitutional Tier,
Ratified, 2026-07-30 — already settles the Master Program's standing**, verbatim:

> *"The Master Program continues as the strategic planning and governance program
> above execution, but **no longer functions as an independent constitutional
> source for repository architecture**."*
>
> *"The repository Constitutional corpus becomes the constitutional and semantic
> authority for repository governance."*

The Master Program's absence from the tracked corpus is therefore **not a
defect and not an accident** — it reflects a ratified Founder decision about the
authority relationship between the Master Program and the repository. It remains
the source of *phase definitions* as strategic program material; repository
*architecture* authority sits with the ratified Constitution / Domain Model pair.

`R-14` is reclassified **C — FORMALLY DISPOSITIONED / NON-BLOCKING**. Admission
remains available to the Founder as an option, but it is **not required for
Phase 1–6 closure**, and P076's framing of it as an open gap was wrong.

### 2.2 P076's own `tools` evidence was stale at the moment it was recorded

P076 reported `tools` **146 OK**. That measurement was taken *before* its closure
record was committed, and the record's own content changed the result once
tracked. Detail in `§7`.

---

## 3. Phase 1–6 closure matrix

| Phase | Criteria | Technical evidence | Governance status | Residual | Blocking? | Final |
|---|---|---|---|---|---|---|
| **P1** | Vol II §4.1 — one canonical definition per core entity | verified — Freeze §4/§5, twelve entities, coverage-complete | complete per Vol II §4.1; no Register entry (predates `GDR-0001`) | `R-01` closed, `R-09` remediated | **NO** | **COMPLETE / NON-BLOCKING RESIDUAL** |
| **P2** | Vol II §4.1 — Runtime runs a basic Execution Contract | verified — RUNNING-gated execution re-demonstrated live this Act | certified within Gate 4's surface (`GDR-0002`) | `R-02` | **NO** | **COMPLETE / NON-BLOCKING RESIDUAL** |
| **P3** | Vol II §4.1 — all Execution Contract components stable | **5 of 8** built; Planner · Scheduler · Orchestrator absent | exit precondition **formally invalidated** by `GDR-0002` precond. 10 | `R-03` | **NO** | **FORMALLY DISPOSITIONED / NON-BLOCKING** |
| **P4** | Vol II §4.3 — Agent runnable end-to-end | 19 modules; verified | **CERTIFIED** — `GDR-0002`, Frozen → Certified, 2026-07-30 | none | **NO** | **COMPLETE / CERTIFIED** |
| **P5** | `E5-1 … E5-5` (`GDR-0005`) | **all five PASS** — §5 | criteria ratified; implementation authorized (`GDR-0006`); **certification absent** | `R-07` | **NO** for P7 | **CERTIFICATION READY / FOUNDER DECISION REQUIRED** |
| **P6** | `E6-01 … E6-03` (`FD-P6-001`) | PASS — 12 runtime tests re-run green | **CERTIFIED** — `FD-P6-002`, registered | `R-11`, `R-12` | **NO** | **COMPLETE / CERTIFIED** |

The matrix distinguishes, as `§23` requires: **technical completion** (P5 has it),
**certification** (P4, P6 have it; P5 does not), **governance closure** (pending
on P5), **non-blocking residual** (P1, P2, P3), **unresolved decision** (`R-07`,
`R-03`, `R-13`), and **active blocker** (**none**).

---

## 4. Residual inventory — final dispositions

Dispositions per `§7`: **A** closed · **B** remediated under existing authority ·
**C** formally dispositioned / non-blocking · **D** Founder decision required ·
**E** Architect decision required · **F** active blocker.

| Residual | Phase | Source | Current status | Authority required | Blocking? | Action |
|---|---|---|---|---|---|---|
| **R-01** | P1 | Vol II §4.1; Freeze §5 | Exit satisfied; no discrete certification record — Phase 1 predates the Register | none | **NO** | **C** — dispositioned. Retrospective certification is available to the Founder but is not required. |
| **R-02** | P2 | Vol II §4.1; `GDR-0002` | Same; Phase 2's surface certified inside Gate 4 | none | **NO** | **C** |
| **R-03** | P3 | `GDR-0002` precond. 10; Construction Frontier `T-6/T-7/T-8` | Planner · Scheduler · Orchestrator **NOT RATIFIED, NOT AUTHORIZED**. Re-verified this Act: no authorizing record exists anywhere in the corpus; the only two matches both *confirm* non-ratification | **Founder / Architect** | **NO** | **D** — escalated (§8, item 2). **Not constructed.** `§19` condition 2 fails: the outcome is not authorized — authority is withheld, not merely absent. |
| **R-05** | P5 | `GDR-0005 §3.5.3` | `E5-2` implemented and green on the real execution path | none | **NO** | **A** — closed by P076 remediation, re-verified this Act. |
| **R-06** | P5 | `GDR-0005 §3.5.3` | `E5-3` implemented and green | none | **NO** | **A** — closed, re-verified. |
| **R-07** | P5 | Vol V §3 second gate; `GDR-0006` | **Phase 5 has never been certified.** Register searched directly: no Phase 5 certification decision exists, and `GDR-0006` withholds it in terms — *"This authorization does not certify Phase 5."* | **Founder / Program Owner** | **NO** for P7; **YES** for the baseline declaration | **D** — escalated (§8, item 1). Evidence package complete. |
| **R-08** | P5 | ADR-0008; Agent Definitions | Stale Capability `Status` sections corrected | none | **NO** | **A** — closed by P076. |
| **R-09** | P1 | ADR-0003; Agent Definition | Stale Platform Capability `Status` corrected | none | **NO** | **A** — closed by P076. |
| **R-10** | P5 | `GDR-0005` (2026-07-30) vs. `AIOS_F03_CLOSURE_AND_NEXT_GATE §5.2` (2026-08-20) | The document calls Phase 5's exit *"not a mechanically checkable exit"* three weeks after five measurable criteria were ratified. Historical record; **not rewritten** | none | **NO** | **C** — discrepancy recorded, history preserved (`§24`/`§34` of P076). |
| **R-11** | P6 | `DEC-P6-042` → `ADR-0028` | Five ADRs carrying *"BLOCKED — FOUNDER DECISION REQUIRED"* are **superseded**; E-01 is resident in `consumers/` and green | none | **NO** | **C** — superseded; historical records left intact. |
| **R-12** | P6 | `GDR-0028`; `FD-P6-002` | `T12-D-003` and `T12-D-004` **DEFERRED**. Re-verified: no record resolves either; newest authoritative statement is `FD-P6-002` | **Founder** | **NO** | **C** — deferred and out of scope by `§15`. Untouched. |
| **R-13** | P5 | `capability_spec §12`/`§14`; `GDR-0025`-region `OB-01` | `T-2` composition **[O]** reserved · `T-3` versioned-contract format **[O]** reserved · `T-4` blocked on `OB-01`, which *"Requires a Founder appointment act"* | **Architect** (`T-2`,`T-3`) / **Founder** (`OB-01`,`T-4`) | **NO** | **D/E** — escalated (§8, items 3–4). No Phase exit criterion depends on any of them. |
| **R-14** | all | `GDR-0001` (Constitutional Tier, Ratified) | **Reclassified — see §2.1.** The Master Program's standing is already dispositioned; its absence is not a gap | none required | **NO** | **C** — dispositioned. P076's framing corrected. |
| **R-15** *(new)* | — | this Act, `§27` cond. 11 | **Regression introduced and shipped by P076** in `c4551ef`; two `tools` tests failed | none | **was YES** | **B** — remediated under `§19`. See `§7`. |

**Counts:** A 4 · B 1 · C 7 · D 2 · E 1 (with `R-13` spanning D and E) · **F 0.**

**No active blocker (F) exists.**

---

## 5. Phase 5 — `E5-1 … E5-5` evidence

Re-verified this Act for freshness, not carried forward from P076.

| Criterion | Requirement | Evidence | Result |
|---|---|---|---|
| **E5-1** | ≥ 1 capability per in-scope category; **minimum verified = 2** | both categories exercised in one Execution on one RUNNING Runtime | **PASS** |
| **E5-2** | ≥ 2 ordered sub-steps, **on real execution rather than plan** | `Agent → Execution → Runtime (RUNNING) → participation`; 3 ordered sub-steps produced during participation | **PASS** |
| **E5-3** | **exactly 2** of 7 — Coding and Testing | both realized and verified; the other five asserted absent | **PASS** |
| **E5-4** | Engineering Phase Checklist — Validation · Dependency Audit · Regression · Integrity Report, on real execution; capabilities lacking a checklist = **0** | all four completed (P076 §7); regression re-run this Act | **PASS** |
| **E5-5** | six deferred categories retain status; cancelled/removed/reordered = **0** | all six still recorded; **0** governance records modified | **PASS** |

**Regression, re-measured this Act:**

| Suite | P076 reported | This Act |
|---|---|---|
| `native_core` | 676 OK (1 expected `P7-F-2`) | **676 OK (1 expected)** |
| `consumers` | 128 OK | **128 OK** |
| `tools` | 146 OK | **146 OK** — after the `§7` remediation; **2 failures** before it |

**Per `§12`, this is evidence and stops there.** `GDR-0006` withheld
certification expressly and Vol V §3 reserves the Frozen → Certified transition
to the Founder *"berdasarkan bukti implementasi."* No Phase 5 certification is
issued, implied, or inferred by this record.

---

## 6. Phase 6 — verification only

| Item | State |
|---|---|
| `FD-P6-001` | registered, heading count 1, line 4014 |
| `FD-P6-002` | registered, heading count 1, line 4169 |
| Dependency | preserved — line 4177 records `FD-P6-001` as predecessor |
| Order | `FD-P6-001` precedes `FD-P6-002` |
| `E6-01/02/03` | PASS — 12 runtime tests re-run green this Act |
| Knowledge Promotion | **REQUIRED — SATISFIED** |
| Knowledge Graph · RAG · Semantic Search | **SUPPORTING — NOT AN EXIT GATE** |
| T-12 | **UNCHANGED** — article 159 lines, `sha256 1c7b5eaa6102f151…`, 0 modifications |
| `T12-D-004` | **DEFERRED** |
| Register | unmodified — `5502533d4179e09b…`, 30 entries |

Phase 6 was not reopened.

---

## 7. `R-15` — a regression this office introduced, disclosed in full

**What happened.** `ACT-CC-P1-6-076` shipped commit `c4551ef` with `tools`
reported as 146 OK. It was not 146 OK once committed. Two tests in
`tools/tests/test_governance_index.py::KnownRetrievalFailures` failed:

```
AssertionError: '2026-08-21' != '2026-08-28'   : the newest mention leads
AssertionError: 'docs/program/AIOS_CONSTRUCTION_FRONTIER_v1.0.md'
             != 'docs/program/AIOS_P1_6_076_PHASE_1_6_FINAL_CLOSURE_AND_RESIDUAL_AUDIT_v1.0.md'
```

**Why the P076 measurement missed it.** The governance index enumerates
`tracked_markdown()` via `git ls-files`. P076's closure record cites
`DEC-PHASE5-SEMANTICS` and is dated 2026-08-28, so once **committed** it became
the newest tracked mention of that identifier and displaced the two constants
those tests pinned. Every `tools` run in P076 happened while the record was still
**untracked** — and therefore invisible to the index. The suite was green for a
reason that ceased to hold at the moment of commit. **The regression was real,
was mine, and was pushed.**

**Diagnosis before repair.** The index was queried directly. Its behaviour is
**correct**: the titled tier leads by directness, the mention tier is ordered
newest-first, and the P076 record genuinely *is* the newest mention. No
implementation defect exists. What broke were two literal constants that were a
snapshot of the corpus at the time they were written.

**What was changed, and why this is not a test weakened to pass.** The standing
rule is that a conformance test is never modified merely to make an
implementation pass. Nothing about the implementation was made to pass here — it
already behaved correctly. The two constants were replaced with assertions of
the property the class exists to protect, in a form that survives corpus growth:

- chronological surfacing — **kept unchanged**;
- the decided reading remains present in the surfaced mention tier — **added**;
- everything the decided reading outranks is **verifiably older** — **added**;
- everything ahead of it is **verifiably newer**, never undated or older —
  **added**.

The result is **strictly stronger** than the constants it replaces, and the
change is recorded in the class docstring rather than left to be rediscovered.

**Non-vacuity proved, not assumed.** A structural probe confirms the new loops do
real work: the mention tier holds 9 records, the decided reading sits at position
1, with **1** record checked ahead of it and **7** behind — 8 live comparisons.
An assertion that never executes is not evidence.

**Standing lesson recorded.** A suite run before committing a document that the
suite's own corpus scanner reads by `git ls-files` is not a measurement of the
committed state. Any future Act whose deliverable is a tracked governance
document must re-run `tools` **after** staging or committing it.

---

## 8. Consolidated Founder / Architect decision package

Per `§25`: one package, no Decision IDs, no approval status. The item numbers
below are **references within this package only** — they are not Decision
identifiers and must not be treated as such.

### Item 1 — Phase 5 certification (Frozen → Certified) · **FOUNDER**

| Field | Content |
|---|---|
| **Exact issue** | Phase 5's ratified exit criteria `E5-1 … E5-5` are all satisfied with current evidence, and Phase 5 has never been certified. No certification decision exists in the Register. |
| **Canonical source** | Master Program Volume V §3 — *"Volume/Boundary/Phase berpindah Frozen → Certified \| … \| **Pemilik Program (Moriarty), berdasarkan bukti implementasi**"*; `GDR-0006` — *"This authorization does not certify Phase 5."* |
| **Evidence** | §5 of this record; `ACT-CC-P1-6-076` §5–§7; regression `native_core` 676 OK (1 expected), `consumers` 128 OK, `tools` 146 OK |
| **Authority owner** | Founder / Program Owner. Engineering Constitution §3.1 — *"the Architect, exclusively"*; §16 — no delegation |
| **Options** | **(a)** Certify Phase 5 Frozen → Certified and declare completion against `E5-1 … E5-5`. **(b)** Withhold certification pending further evidence, naming what evidence is wanted. **(c)** Revise scope or criteria first — a `GDR-0005` amendment, constitutionally reserved |
| **Consequences** | **(a)** `§24` conditions 3 and 5 become satisfiable; the baseline can be declared governance-closed. **(b)** Baseline remains Outcome B; nothing regresses; Phase 7 dependency is unaffected either way. **(c)** Re-opens a ratified criteria set; the heaviest option, and nothing in the evidence calls for it |
| **Recommendation** | **(a)**, on the evidence — offered as a recommendation only, with no status assigned |
| **Blocks Phase 1–6 closure?** | **YES** — this is the single action standing in front of Outcome A |
| **Blocks Phase 7?** | **NO** — Vol II §5 makes Phase 7 depend on Phase 4, which is Certified |
| **Proposed governance wording** | *"Phase 5 — Intelligence Ecosystem is certified Frozen → Certified against the ratified exit criteria E5-1 through E5-5, on the implementation evidence recorded by `ACT-CC-P1-6-076` and re-verified by `ACT-CC-P1-6-077`. The six deferred Intelligence categories retain their recorded status; no category is cancelled, removed, or reordered. No new Phase 5 requirement is introduced. Phase 7 is not authorized by this decision."* |

### Item 2 — Phase 3 remainder: Planner · Scheduler · Execution Orchestrator · **FOUNDER / ARCHITECT**

| Field | Content |
|---|---|
| **Exact issue** | Three of Phase 3's eight exit components are unbuilt and **explicitly unauthorized** for construction. Absence of implementation is not authorization to implement. |
| **Canonical source** | `GDR-0002` precond. 10 (*"Not applicable — invalidated during validation"*); Construction Frontier `T-6/T-7/T-8` **NOT RATIFIED / NOT AUTHORIZED**; `DEC-PHASE5-SEMANTICS` — *"does not ratify Planner, Scheduler or Execution Orchestrator"*; `NCIR §9.10` **[O]** reservation |
| **Evidence** | Re-verified this Act: **no authorizing record exists anywhere in the tracked corpus**. Planner has 0 occurrences of architectural surface; Scheduler and Orchestrator are `[O]`-reserved |
| **Authority owner** | Architect for ratification of architectural surface; Founder for construction authorization |
| **Options** | **(a)** Leave as-is — deferred, forward-dependent, non-blocking. **(b)** Ratify architectural surface, then authorize construction. **(c)** Formally retire the three from Phase 3's exit definition |
| **Consequences** | **(a)** Status quo; Phase 3 stays dispositioned non-blocking; nothing downstream is affected. **(b)** Opens genuine new construction requiring its own specification. **(c)** Amends a canonical exit criterion — constitutionally reserved and the heaviest option |
| **Recommendation** | **(a)** — the forward dependency on Phase 5 that made this circular is precisely why `GDR-0002` invalidated the precondition; nothing has changed that |
| **Blocks Phase 1–6 closure?** | **NO** — formally dispositioned |
| **Blocks Phase 7?** | **NO** |
| **Proposed governance wording** | *"Phase 3's remaining components — Planner, Scheduler, Execution Orchestrator — remain unratified and unauthorized for construction. Their absence does not block Phase 1–6 baseline closure, and does not block Phase 7."* |

### Item 3 — `T-2` and `T-3` · **ARCHITECT**

| Field | Content |
|---|---|
| **Exact issue** | `T-2` Capability↔Skill/Workflow composition is *"Inferred (reserved)"*; `T-3` versioned-contract representation has *"no format defined here"* |
| **Canonical source** | `capability_spec §12`, `§14` — both marked **[O]** |
| **Authority owner** | Architect, exclusively |
| **Options** | **(a)** Leave reserved. **(b)** Ratify the composition relationship and/or a contract-representation format |
| **Consequences** | **(a)** No effect on Phase 1–6. **(b)** Unblocks work that no current Phase criterion requires |
| **Recommendation** | **(a)** — no Phase 1–6 exit criterion depends on either |
| **Blocks Phase 1–6 closure?** | **NO** |
| **Blocks Phase 7?** | **NO** |

### Item 4 — `OB-01` and `T-4` · **FOUNDER**

| Field | Content |
|---|---|
| **Exact issue** | *"Through which **actor** is PD-02's operative authority exercised?"* — no resident instrument names the occupant. `T-4` Capability Catalog category instantiation is blocked on it, because assigning a category to an owning Department is an INV-1 ownership decision |
| **Canonical source** | Register line 3466 — *"Requires a Founder appointment act, structurally analogous to `APT-CD1.1-AA-001`"* |
| **Authority owner** | Founder / Program Owner |
| **Options** | **(a)** Leave open. **(b)** Issue the appointment act, which also unblocks `T-4` |
| **Consequences** | **(a)** No effect on Phase 1–6; `T-4` stays conditionally eligible. **(b)** Opens Catalog category instantiation |
| **Recommendation** | Founder's call; no Phase 1–6 criterion depends on it. `E5-1` was satisfied without `T-4` because `ADR-0008` already assigned both Intelligence Capabilities to the Engineering Department by architectural decision |
| **Blocks Phase 1–6 closure?** | **NO** |
| **Blocks Phase 7?** | **NO** |

### Item 5 — Master Program repository admission · **FOUNDER, optional**

| Field | Content |
|---|---|
| **Exact issue** | The Master Program is Founder-supplied material outside the tracked corpus. **`GDR-0001` already dispositions its authority** (§2.1); admission is a residency question, not an authority gap |
| **Canonical source** | `GDR-0001` — Constitutional Tier, Ratified |
| **Authority owner** | Founder |
| **Options** | **(a)** Leave as-is. **(b)** Admit it to the corpus as strategic-program material, explicitly *not* as a constitutional source — the distinction `GDR-0001` draws |
| **Consequences** | **(a)** Phase definitions continue to rest on Founder-supplied material, as `GDR-0001` contemplates. **(b)** Improves resident traceability; must not disturb the `GDR-0001` authority relationship |
| **Recommendation** | **(b)** as a convenience, with `GDR-0001`'s limitation stated in the admitted document. **Not required for closure** |
| **Blocks Phase 1–6 closure?** | **NO** |
| **Blocks Phase 7?** | **NO** |

### Item 6 — `T12-D-003` / `T12-D-004` · **FOUNDER, not for now**

Both remain **DEFERRED** and were verified only. `§15` bars their resolution
under this Act, and nothing in Phase 1–6 depends on either. Listed for
completeness; **no decision is sought**.

---

## 9. Phase 7 — the three questions kept separate

`§30` requires baseline closure, Phase 7 readiness, and Phase 7 authorization to
be distinguished. They are not the same question and they do not have the same
answer.

| Question | Answer | Basis |
|---|---|---|
| **Is the Phase 1–6 baseline governance-closed?** | **NOT YET** | Phase 5 certification outstanding — `§24` conditions 3 and 5 unmet |
| **Is Phase 7's canonical dependency satisfied?** | **YES** | Vol II §5 — *"7 Memory Ecosystem ← Phase 4"*; Phase 4 is **CERTIFIED** (`GDR-0002`). Per `§21` of P076's Act, read as stated: Phase 7 depends on neither Phase 5 nor Phase 6 |
| **Is Phase 7 authorized?** | **NO** | `§22` forbids it here. Phase 7 additionally requires its own `E7` criteria ratified as measurable (Vol VIII §3, step 2) — those do not exist, and `GAP-02` records that Phases 7–13 metrics remain at principle level |

**No active Phase 1–6 blocker prevents Phase 7 readiness.** The outstanding
Phase 5 certification blocks the *baseline declaration*, not Phase 7's
dependency. Both statements are true simultaneously and neither is allowed to
absorb the other.

**The final `§30` declaration is withheld** because `§24` is not satisfied. It
becomes available on Item 1 alone.

---

## 10. Integrity

| Item | Value |
|---|---|
| HEAD before this Act | `c4551ef` |
| Governance Register hash | `5502533d4179e09b…` — **unmodified**, before and after |
| Register entries | 30 — unchanged |
| T-12 article | 159 lines, `1c7b5eaa6102f151…` — **unmodified** |
| `T12-D-003` / `T12-D-004` | **DEFERRED** — unchanged |
| Protected packages | **13** — none read, staged, committed, or referenced |
| `native_core/` | **0 files changed** |
| Files modified this Act | 1 — `tools/tests/test_governance_index.py` (`R-15`) |
| Files created this Act | 1 — this record |
| Phase 7 construction | **none** |
| Decisions issued | **none** |
| Decision IDs assigned | **none** |

---

## 11. Disclosed defects in this Act's own verification

1. **A `tools` regression shipped in `c4551ef`** — mine, from P076, diagnosed
   and remediated in `§7`. The measurement that missed it was structurally
   incapable of catching it.
2. **A predecessor-field grep used `-A1`** where the value is inline, printing
   nothing. Re-run correctly: the `FD-P6-001 → FD-P6-002` dependency is intact
   at line 4177. Had the empty output been read as absence, it would have been a
   false finding against a correctly registered Decision.
3. **A protected-package count returned 14** in the prior Act because the
   pattern `docs/program/AIOS_[A-Z]` swept in that Act's own new record.
   Corrected by enumerating the set explicitly; the true count is **13**.
4. **A throwaway probe imported a nonexistent `build_index`** and raised. It was
   a scratch call, contributed to no finding, and the real probe that replaced
   it is the one reported in `§7`.

Two false positives were eliminated by content-anchoring rather than assumption:
the only two corpus matches for Planner *authorization* both **confirm**
non-ratification (*"are unratified"*, *"does not ratify"*); and the `grep` for
records resolving `T12-D-003/004` returned files that **cite** the deferrals
rather than resolve them.
