# `P6` Knowledge admission — human governance decision surface

> **THIS IS A DECISION SURFACE. IT IS NOT A DECISION.**
>
> Prepared under `ACT-CC-P12-014 §36.8`, which makes *"a governance decision
> reserved to Founder"* a hard stop and requires the decision surface be
> prepared rather than self-authorized. The decision instrument in `§4` is
> **deliberately blank**.
>
> `SURFACE ≠ DECISION · PREPARATION ≠ AUTHORIZATION · SILENCE ≠ APPROVAL`

---

## 1. Why this exists

`FD-P12-001` ratified `E12` with `§C = R1 — CONSUMPTION BY REAL SYSTEM WORK`.
`ACT-CC-P12-014` built the real work path and ran it: **seven of eight canonical
phases are now consumed by real system work.** One is not.

```text
P4 Runtime       CONSUMED BY REAL SYSTEM WORK
P5 Intelligence  CONSUMED BY REAL SYSTEM WORK
P6 Knowledge     NOT CONSUMED — no execution ever recorded   ← this surface
P7 Memory        CONSUMED BY REAL SYSTEM WORK
P8 Tools         CONSUMED BY REAL SYSTEM WORK
P9 Workflow      CONSUMED BY REAL SYSTEM WORK
P10 Department   CONSUMED BY REAL SYSTEM WORK
P11 Organization CONSUMED BY REAL SYSTEM WORK
```

**`P6` is not blocked by engineering.** The work that would consume Knowledge
exists, runs, and reaches the Knowledge subsystem through the Execution
Contract on a RUNNING Runtime. It reads nothing because there is nothing Active
to read, and admitting something is a governed act this office may not perform.

---

## 2. The boundary, read from the canonical bodies

| Step | Body |
|---|---|
| To consume Knowledge, work must read an **Active** `KnowledgeVersion` | `KnowledgeRetrieval.active(key)` |
| An Active version exists only through admission | `KnowledgeAdmission.admit(candidate, authorization)` |
| Admission admits **iff** Governance authorizes the promotion | *"Admission is handed a `GovernanceReview` … and admits IFF the provenance-verified result is `True`"* |
| Authorization reflects a **human** decision, never an automatic one | `GovernanceReview.promotion_authorized`: *"True iff a human `approve` **produced by this Governance** is on record for this candidate … Default is deny — absence of an authorising, provenance-verified human decision means no promotion (fail closed)"* |
| The decision requires an accountable human | `ReviewDecision(candidate, decision, authority, rationale)` with `HumanAuthority(reviewer_id)`: *"a human authority requires a non-empty reviewer identity"* |

**No resident Active Knowledge version exists.** Knowledge hosted by a Runtime
is assembled per-runtime (`create_memory_subsystem`'s Knowledge counterpart
builds its store fresh), and no durable resident Knowledge store carries an
admitted version.

**This office cannot supply `HumanAuthority`.** Constructing one would be
fabricating human consent — the failure every Act in this programme forbids,
and `§36.8`'s hard stop.

---

## 3. What is being asked, and what it would do

The work path (`aios_corpus_health_run.py`) judges the corpus against criteria
it holds **as Knowledge rather than as a constant in the worker** — which is the
point: a threshold hard-coded in the worker is the worker's opinion; a threshold
held as an admitted Knowledge version is the system's, and changing it is a
governed act.

**The proposed criteria content:**

```text
knowledge_item_key:             corpus-health.criteria
stale_governance_sources_max:   0
citation_errors_max:            0
live_stale_assertions_max:      0
```

**What admission would and would not do.** It would make the criteria readable
by the work, so `P6` becomes consumable and the verdict stops being withheld. It
would **not** make the verdict favourable — the work measures the real corpus
and reports `HEALTHY` or `DEGRADED` from whatever the audits return. It would
**not** satisfy `E12-06` by itself: `R1` requires consumption by real work, and
that consumption is measured, not granted.

```text
ADMISSION ≠ CONSUMPTION      CONSUMPTION ≠ E12-06 SATISFIED
```

**Current measured facts** the criteria would be applied to, from the live run:
`stale_governance_sources 0` · `citation_errors 0` · `live_stale_assertions 0`.
On these numbers the verdict would be `HEALTHY` — stated so the decision is made
with the consequence visible, not as an argument for making it.

---

## 4. Decision instrument — **deliberately blank**

```text
P6 KNOWLEDGE ADMISSION — corpus-health.criteria

ADMIT THIS KNOWLEDGE ITEM:
  [  ] APPROVE — admit the criteria as proposed
  [  ] APPROVE WITH MODIFICATIONS  (specify)
  [  ] REJECT — do not admit
  [  ] DEFER

MODIFICATIONS:      ______________________________
RATIONALE:          ______________________________   (required — a decision
                                                      without a reason is not
                                                      accountable)
REVIEWER IDENTITY:  ______________________________   (HumanAuthority.reviewer_id;
                                                      must be non-empty)
DATE:               ______________________________
SIGNATURE:          ______________________________

STATUS: PENDING HUMAN GOVERNANCE DECISION
```

**No box is ticked, no reviewer named, no date entered, no signature present.**
This office prepared the surface and stops here.

---

## 5. If admitted

The work path requires **no change**. It already reads
`execution.runtime.knowledge.retrieval.active("corpus-health.criteria")` on
every run and records the captured content into `knowledge_consumed` when a
version is there. What remains is delegated and ordinary: record the decision
through `GovernanceReview.record_decision`, admit through `KnowledgeAdmission`,
re-run the work, and re-measure `E12-06`.

## 6. If not admitted

`P6` remains `NOT CONSUMED`, `E12-06` remains `NOT SATISFIED`, and `§74 Part J`
remains unsatisfied on its `VERIFICATION` condition. That is a legitimate
terminal state, not a defect to engineer around — `ACT-CC-P12-014 §46`:
*"Failure is a valid engineering result. It must not be converted into PASS by
changing the acceptance interpretation."*
