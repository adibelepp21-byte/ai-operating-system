# `DEC-F03-053` — T-2 Skill Half · Architectural Determination Record

**Recorded under:** FOUNDER · `ACT-CC-F03-053 §8` · **Recording date:** 2026-08-21
**Determination:** **S-ALT-1 — Derived / No Direct Relationship**

> **THE `[O]` RESERVATION IS NOT DISCHARGED BY THIS RECORD.**
> `ACT-CC-F03-053 §9` [E]: *"Sampai architectural determination diratifikasi dan
> successor gate diterbitkan: `[O]` reservation **tidak boleh dianggap
> discharged**"* — and Domain Model, Architecture Freeze, Blueprint,
> `capability_spec`, `skill_spec`, source code and conformance tests may none of
> them be mutated. **Nothing was.** This record states a determination and
> changes no artifact.

---

## 1. Determination

```text
DEC-F03-053
[X] S-ALT-1 — Derived / No Direct Relationship
Founder: Moriarty · Date: 21-08-2026 · Confirmation: Moriarty.
```

`§12` integrity: exactly one alternative selected · attribution · date ·
confirmation. **VALID.** No default was taken and nothing was inferred.

**What was determined (`§6`):** that a direct `Capability ↔ Skill` relationship
takes **no** semantic form in the AIOS architecture — the two entities are
*"sufficiently represented through existing derived paths."*

**What was not determined (`§6`):** implementation, class or module structure,
API, storage, reference representation, conformance-test implementation, or any
canonical artifact mutation.

## 2. The basis, re-verified

The two derived paths S-ALT-1 rests on were re-exercised end-to-end against the
built code at `2402da7`:

```text
Path 1   Capability  ←implements—  Agent Definition  —specifies→  Skill    ✅ implemented
Path 2   Capability  ←realizes—    Workflow          —contains→   Skill    ✅ implemented
```

Both are ratified on both legs, and both now run in code — Path 1 through
`AgentDefinition.implemented_capabilities` + `.specified_skills`, Path 2 through
`WorkflowRealization` + `WorkflowComposition`.

## 3. `§10` check — no construction target remains from the direct edge

**[E] Confirmed.** No source module in `core/capability/` or `core/skill/`
references a pending direct edge; searched and empty. No module is blocked on
it. Under S-ALT-1 there is nothing to build, now or later, from a direct
`Capability ↔ Skill` relationship.

**The existing conformance guard needs no change and gets none.**
`test_skill_and_workflow_composition_is_not_modelled` asserts the Capability
surface names neither Skill nor Workflow. Under S-ALT-1 that assertion becomes
**permanently** correct rather than provisionally correct — its basis strengthens
from *"reserved, pending"* to *"determined: no direct edge exists."* Changing it
is neither necessary nor authorized.

## 4. Closure inventory — for the successor gate, not for now

**[E] Six live sites carry the Skill-half reservation.** A closure gate would
need to address each; **none was touched here.**

| # | Site | Current text |
|---|---|---|
| 1 | **Freeze §10** | `Capability↔**Skill**` in the Inferred-relationships entry |
| 2 | `capability_spec §12` | **[O]** *"Capability↔**Skill** composition is currently Inferred (reserved)"* |
| 3 | `capability_spec §14` | **[O]** *"Capability↔**Skill** relationship ratification — the Skill half only"* |
| 4 | `skill_spec §14` | **[O]** *"Skill↔Capability/Workflow composition ratification (Inferred)"* |
| 5 | **Domain Model §4** | inline note: *"**Capability ↔ Skill remains `[O]` reserved** — see Freeze §10"* |
| 6 | **`NCIR §9.6`** | **Reserved [O]:** *"Capability↔Skill/Workflow (Inferred)"* |

**[E] Historical records that must be preserved, never rewritten** — four files
under `docs/architecture/history/` (Phase-3 Authorization Review §90,
Implementation Readiness Review, Architecture Specification §59/§214,
Architecture Review R-A1/C-2) record the reservation as it stood. They are
history and remain accurate as history.

## 5. **[D] New finding — the bundling defect has a third instance**

`NCIR §9.6` still reads **Reserved [O]:** *"Capability↔Skill/**Workflow**
(Inferred)."* The **Workflow** half was ratified under `DEC-F03-045` and
canonicalized under `DEC-F03-046`, so that line is now **stale**.

This is the **third** document with the same defect and the same root cause —
an entry that bundles `Capability/Workflow` (or `Skill/Workflow`) as one item,
so discharging half a bundle leaves the other half mis-stated:

| Document | Stale claim |
|---|---|
| `workflow_spec §14` | lists **Workflow↔Skill** as `[O]` while `§7` says `[E]` *"composed within Workflows"* — recorded as **Track B** |
| `skill_spec §14` | same contradiction, mirrored — recorded in the `-052` package |
| **`NCIR §9.6`** | still bundles the **already-ratified Workflow half** with the Skill half — **new here** |

**Not touched, not resolved.** `§9` forbids mutating any of them, and `§11`
grants no specification authority. All three share one root cause, so **one
decision could close all three** rather than three.

## 6. State

| Check | Result |
|---|---|
| Domain Model · Freeze · Blueprint | **hash-identical** |
| `capability_spec` · `skill_spec` · `workflow_spec` | **hash-identical** |
| Constitution · Finding Register | **hash-identical** |
| Source and conformance tests | **0 files changed** |
| `Capability ↔ Skill` reservation | **`[O]` — NOT discharged** |
| `native_core` · `tools` · `bounded_exception` | **584** · **20** · **29 OK**, unchanged |
| Entity count · core boundaries | **12** · **11** |
| Construction authority | **NONE** (`§11`) |

## 7. Successor (`§10`)

S-ALT-1 was selected, so `§10`'s branch applies: *"successor Act harus mencatat
closure T-2 Skill half dan memastikan tidak ada construction target yang
tersisa."* The second half of that is **already verified** (§3). The first half —
recording closure and discharging the six live `[O]` sites — requires its own
gate, prepared as `ACT_CC_F03_054_T2_SKILL_CLOSURE_GATE.md`, **awaiting Founder
issuance**.

**Current state (`§11`):** `ARCHITECTURAL DETERMINATION MADE → RATIFICATION AND
CLOSURE PENDING → CONSTRUCTION NOT AUTHORIZED`.
