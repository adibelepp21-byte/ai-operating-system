# P13-016 — FDR-2 Decision Surface: P13 Definition, Boundary, Meaning & Exit Contract

| Field | Value |
|---|---|
| **Prepared under** | `FDR-1 §21` (*"PROCEED TO FDR-2"*), `§18` (independently authorized CEO work), V2 `A18` Founder Review Interface |
| **Prepared by** | Claude Code — AIOS Co-Founder + Delegated CEO |
| **Date** | 2026-09-24 |
| **Decision basis** | Blueprint v0.4 (`00efeeae…`, preserved, **non-canonical**, the review basis under `FDR-1 §6`) |
| **Status** | **PREPARATION ONLY.** Nothing here decides, canonicalizes or authorizes. Every recommendation is marked **[REC]** and binds no one |

```text
THIS DOCUMENT          evidence + options + recommendation, per FDR-1 §21 item
THE FOUNDER            decides each item (§12 decision form)
UNCHANGED              P13 canonical NOT ESTABLISHED · AUTHORIZATION NOT GRANTED ·
                       CONSTRUCTION NOT AUTHORIZED · NATIVE CORE = 11 · v0.1–v0.4 preserved
```

`FDR-1 §17` requires that items A–G *"are not to be inferred from v0.4"*.
Accordingly, each item below presents v0.4's proposal as **one option among
several**. Each option carries its evidence and its consequence, and none is
treated as the default.

---

## 1. New evidence since v0.4

**E-1 — the 100-question reconciliation** (`FDR-1 §12`).
`P13-015-FOUNDATIONAL-QUESTION-RECONCILIATION.json` classifies all 100
foundational questions against the live system. Every citation is re-verified
by `tools/foundational_question_reconciliation.py`, including *measured
absences*: a claim like "0 Evaluation symbols" is itself checked.

```text
ALREADY SOLVED     29   the substrate already answers these (P6–P12, governance)
PARTIAL            30   partly answered; the missing part is named per row
P13 CORE           21   no resident mechanism; a P13 capability would answer them
FOUNDER RESERVED   17   the Founder's to decide (identity, autonomy, completion)
P13 FRONTIER        2   Q39 unknown-weakness discovery · Q91 frontier selection
UNKNOWN             1   Q23 conflicting sources: no mechanism found, absence not asserted
```

**What E-1 establishes** [OBS → INF]:

* **59 of 100 are already solved or partial.** P13 is not a greenfield phase.
  Most of the self-knowledge, governance-of-evolution and Founder-support
  questions are answered by P6–P12 and the V2 governance model.
* **The 21 P13-CORE questions cluster onto v0.4's five candidate surfaces**,
  with no remainder:

| v0.4 candidate surface | P13-CORE questions it would answer |
|---|---|
| context assembly | Q17, Q61, Q62, Q63 |
| evaluation | Q33, Q38, Q40, Q46, Q53 |
| reasoning | Q28, Q57, Q59 |
| next action (propose-only) | Q19, Q41, Q69, Q70, Q71, Q72, Q73, Q89 |
| evolution | Q27 |

  This is evidence that v0.4's hypothesis **covers** the measured core. It is
  not evidence that the hypothesis is *the* definition. Other definitions could
  cover the same questions.
* **Autonomy is the pivot.** 6 of the 17 reserved questions (Q48, Q74, Q75,
  Q77, Q90, Q92) turn on the autonomy boundary. So does the permitted reach of
  core question Q69 (next action).

**E-2 — the ecosystem relationship map** (`tools/ecosystem_relationships.py`,
GOAL-V2-005). Of the Goal's seven chain relationships: 3 are bound in code, 2
by data, 1 only through Organization. **Memory ↔ Intelligence is not
connected**, by the recorded design of P5.

**E-3 — measured absences.** `native_core/` has 0 `Reasoning` and 0
`Evaluation` symbols. The Cognitive Intelligence Capability realizes 2 of its
3 declared sub-abilities; Reflection is unrealized.

---

## 2. Item 1 — P13 canonical definition (`FDR-1 §17 A`)

| Option | Statement | Evidence for | Consequence |
|---|---|---|---|
| **1-A** | The v0.4 hypothesis (`FDR-1 §7`): *the system-level capacity for AIOS to reason about, evaluate, and govern its own state and next action across the existing AIOS substrate* | covers all 21 P13-CORE questions (E-1); builds on the 59 solved or partial; consistent with the Goal's `§4` exclusions | bounded; the five surfaces become specifiable |
| **1-B** | F1's broad hypothesis set: 17 capabilities including capability acquisition, governed self-improvement execution and research | F1 `§3` | reopens the 6 autonomy-bound reserved questions; larger and harder to bound; most rows collide with item 6 |
| **1-C** | Narrow: evaluation and reasoning only. No next-action, no evolution | the two measured absences (E-3) | leaves 9 CORE questions (next action, evolution) unanswered, deferred to a later phase |
| **1-D** | Path C: P13 does not proceed | — | `FDR-1 §5` found no evidence for it; it remains a Founder option |

**[REC] 1-A**, carrying the exclusions of item 2. It is the only option
grounded on both halves of the measurement: what exists (E-1's 59) and what
is absent (E-1's 21, E-3). It also neither duplicates P12 nor requires
autonomy beyond item 6-A.

## 3. Item 2 — meaning of "Super Intelligence" (`§17 B`)

| Option | Statement | Consequence |
|---|---|---|
| **2-A** | A **name**. It denotes P13 as defined in item 1 and makes **no capability claim** beyond what the exit contract verifies | nothing to over-claim; a claim can be made only through the exit contract |
| **2-B** | A **substantive property**: a defined level or class of intelligence | requires criteria no resident source supplies; high risk of an unverifiable claim |
| **2-C** | Leave open | P13 cannot be canonicalized while its title has no settled meaning |

**[REC] 2-A**, with `FDR-1 §10`'s eight exclusions stated in the definition
itself: not AGI, not consciousness, not unrestricted autonomy, not
self-modifying intelligence, not omniscience, not guaranteed superiority, not
human replacement, not unlimited capability.

## 4. Item 3 — mission / intended outcome (`§17 C`)

| Option | Statement |
|---|---|
| **3-A** | v0.4 `O2`. AIOS can answer, from evidence and under governance, three questions it cannot today: *What state am I actually in? · Is that state good? · What should I do next?* Each answer is traceable, refusable, and subject to human authority |
| **3-B** | F1 `§3`'s outcome list, as a mission |
| **3-C** | Founder-authored mission |

**[REC] 3-A.** Question 1 is P12's (already answered, E-1 Q8–Q13); questions
2 and 3 are exactly E-3's two absences. The mission is then measurable, and
it maps onto item 8's criteria.

## 5. Item 4 — scope (`§17 D`)

**[REC], if 1-A:**

```text
IN     the P13-CORE questions (21), through the five surfaces
IN     the P13-owned remainder of PARTIAL rows: Q14 weaknesses, Q15 self-model
       drift, Q26 known unknowns, Q36/Q37 system-level health
OUT    Native Core #12 (frozen) · autonomous runtime / daemon / scheduler / queue ·
       self-modification of code or governance · a system-integration layer (P12,
       certified) · any change to certified P1–P12 evidence ·
       Optimization → Governance (Architect-reserved, AD-P13-001)
OPEN   the frontier rows Q39, Q91 → residual frontier register (F1 §31)
       Q23 conflicting sources → UNKNOWN, needs evidence before classification
```

## 6. Item 5 — the P12 → P13 boundary (`§17 D`, `§21.5`), including contradiction C-1

| Owner | Holds |
|---|---|
| **P12** (certified) | self-model · operational state · observation · system integration (`D-2`) · verification architecture · evidence model |
| **P13** (proposed) | judgement *over* that state: evaluation, reasoning, next-action proposals. P13 **reads** P12 and never rewrites it |

**C-1** — v0.4 `O3` says *"nothing new integrated at system level"*, while
the Goal frames P13 as ecosystem integration:

| Option | Statement |
|---|---|
| **5-A** | No new integration: P13 consumes P12 as-is |
| **5-B** | **Necessity-driven:** a relationship enters P13 scope only where a ratified surface demonstrably requires it, and it is then built as a P13 consumer, never as a change to P12's integration |
| **5-C** | Full ecosystem connectivity as a P13 goal in itself |

**[REC] 5-B.** It is what `FDR-1 §14` already requires (*"a proposed
conceptual graph [does not] automatically become an implementation
requirement"*), and it resolves C-1 without reopening P12.

## 7. Item 6 — autonomy boundary (`§17 E`)

| Option | Permitted | Prohibited |
|---|---|---|
| **6-A** | evaluate, reason and **propose**, when invoked by a human or by the CEO under a Goal; every proposal is typed, durable, refusable | executing any proposal; self-activation; scheduling; background operation; acting on silence |
| **6-B** | 6-A, plus executing a proposal **inside an existing Founder delegation** (the W4 pattern), with escalation on anything out of scope | anything outside an explicit delegation |
| **6-C** | continuous self-directed operation | — (would engage R01/R04-level questions) |

**[REC] 6-A for P13**, with 6-B left to a later, separate Founder decision.
Evidence: today AIOS has no daemon, no scheduler and no self-activation. The
W4 executor already refuses and escalates out-of-scope steps (E-1 Q76). 6-A
adds judgement without adding any authority, and every 6-A prohibition can
be held by a negative control.

## 8. Item 7 — required ecosystem relationships (`§21.7`)

Measured state (E-2) against **[REC] 1-A + 5-B**:

| Relationship | Now | Required by 1-A? | Why |
|---|---|---|---|
| Knowledge ↔ Memory | CODE | consumed | context assembly reads both |
| Memory ↔ Intelligence | **NOT CONNECTED** | **yes, as read access** | context assembly and evaluation need memory. Built as a P13 consumer; P5 unchanged |
| Intelligence ↔ Capability | DATA | consumed | capability gaps (Q27) read declarations |
| Capability ↔ Workflow | MEDIATED | **no** | no CORE question needs a direct edge. Workflow ↔ Skill stays Architect / Native Core |
| Workflow ↔ Organization | CODE | consumed | — |
| Organization ↔ Governance | CODE + DATA | consumed | proposals reach humans through escalation / review |
| Governance ↔ Founder Decision | DATA | consumed | proposals cite authority; decisions stay human |
| *(adjacent)* Evaluation → Governance | absent | **depends** | a route through `OptimizationProposal` needs `AD-P13-001` (Architect). A route through the escalation register does not |

## 9. Item 8 — exit contract (`§17 F`): candidate `E13` criteria

The format follows `FD-P10-004`, where the Founder ratified measurable exit
criteria. **These are candidates for ratification, not criteria.**

| ID | Candidate criterion | Measured by |
|---|---|---|
| **E13-01** | Each ratified surface is resident, importable, and **exercised live on real system state** with Trace evidence. Fixtures do not count | P12 `§46` live-verification discipline |
| **E13-02** | Every ratified P13-CORE question moves to **ALREADY SOLVED**, with pointers the reconciliation checker verifies | `tools/foundational_question_reconciliation.py` |
| **E13-03** | Every evaluation, conclusion and proposal carries P12 `§29`'s twelve preservation elements | provenance verification |
| **E13-04** | Every next-action output is a proposal: typed, durable and refusable. **No proposal executes** without `HumanAuthority` (6-A) | negative controls: recommendation → decision, execution attempt, silence |
| **E13-05** | Absent evidence yields `UNKNOWN`, never a conclusion | negative control with evidence removed |
| **E13-06** | Non-regression: certified P1–P12 evidence intact, Native Core = 11, full suites green, write probe 0 certified writes | GOAL-V2-004 instruments |
| **E13-07** | Exhaustion: fresh discovery finds no authorized + actionable + sufficiently sourced in-scope P13 work | `§55` / F3 `§21.3` / F6 `§18` |

The acceptance ladder stays distinct (`FDR-1 §19`): `E13 met ≠ certified ≠
Founder acceptance ≠ AIOS complete`.

## 10. Item 9 — completion semantics (`§21.9`, Q96)

| Option | Statement |
|---|---|
| **9-A** | **Bounded:** P13 completes when the ratified E13 contract is met. Everything beyond it goes to a residual frontier register (F1 `§31`) |
| **9-B** | **Evolutionary:** P13 has no end point |

**[REC] 9-A.** 9-B makes *"P13 complete"* unfalsifiable, which the evidence
discipline of every phase since P4 forbids.

## 11. Item 10 — construction authorization prerequisites (`§17 G`)

**[REC]** P13 construction may be considered only when **all** of these hold:

1. items 1–9 are decided in `FDR-2`;
2. a **canonicalization act** exists. Its form is the Founder's choice, for
   example `FDR-2` itself as the canonical definition, with v0.4 as
   architecture basis, or a v0.5 drafted under `FDR-2`;
3. a **placement decision**: tools layer vs Native Core. **[REC] tools layer**,
   with `NATIVE CORE = 11` unchanged. This touches `FD-2`, since it is
   architecture;
4. `AD-P13-001` is disposed of, **only if** the evaluation → governance route
   needs `OptimizationProposal` (item 7, last row);
5. the E13 criteria are ratified;
6. an explicit **P13 construction authorization** instrument exists (`§58`
   link 4), naming its envelope.

**Not prerequisites** [INF]: Agent-lifecycle canon (`GAP-0009`), unless a
ratified surface needs agent identity; corpus residency (`GAP-0006`),
because under 1-A no construction rests on a corpus-only statement.

---

## 12. Decision form (for the Founder; Claude does not fill it)

```text
1  Definition             [ ] 1-A   [ ] 1-B   [ ] 1-C   [ ] 1-D   [ ] other: ____
2  "Super Intelligence"   [ ] 2-A   [ ] 2-B   [ ] 2-C
3  Mission                [ ] 3-A   [ ] 3-B   [ ] 3-C
4  Scope                  [ ] as §5 [ ] modified: ____
5  P12→P13 / C-1          [ ] 5-A   [ ] 5-B   [ ] 5-C
6  Autonomy boundary      [ ] 6-A   [ ] 6-B   [ ] 6-C
7  Required relationships [ ] as §8 [ ] modified: ____
8  Exit contract          [ ] ratify E13-01…07   [ ] modify   [ ] reject
9  Completion semantics   [ ] 9-A   [ ] 9-B
10 Construction prereqs   [ ] as §11 [ ] modified: ____
   Placement              [ ] tools layer   [ ] other (Architect path)
   Canonicalization form  ____
```

## 13. Open matters FDR-2 may take or leave

`GAP-0009` agent canon · `GAP-0006` corpus residency · `FD-2` Founder ≡
Architect · `AD-P13-001` · `AD-P13-002` · the four OPEN escalations
(GOAL-V2-005 FDR-5).

## 14. Verification of this package

* The E-1 matrix holds: 100/100 questions, every evidence pointer verified
  (`test_foundational_question_reconciliation`, 6 tests).
* E-2 holds: the relationship map is stable, with 0 stale reasons.
* v0.1–v0.4 hashes are unchanged. `NATIVE CORE = 11`. Nothing under
  `docs/architecture/p13/` exists or was created. No P13 construction.
