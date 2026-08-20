# Construction Frontier — Phase 5, Increment T-9

**Prepared under:** FOUNDER · `ACT-CC-F03-038 §6`, `§7`, `§19` · **Date:** 2026-08-21
**Predecessor:** `ACT-CC-F03-037` (T-1 ownership reconciliation — COMPLETE)
**Interpretation:** `DEC-PHASE5-SEMANTICS = OPTION B` — CANONICAL

> **Not canonical architecture.** This artifact records a frontier assessment
> and an engineering result. It ratifies nothing.

---

## D-01. Construction Frontier Report

### D-01.1 State re-verified from resident evidence (`§2`)

`§2`'s table was not taken as a substitute for evidence. Re-verified: four
protected artifacts hash-identical; working tree clean at `fb01f72`; core region
recounted at **eleven** directories; suites green; `P7-F-2` still the sole
registered exception, `"repair not authorized"` under `GDR-0014`.

### D-01.2 Completed targets

| Target | Act | State |
|---|---|---|
| Capability subsystem (INV-1/9/10/11/14) | -031/-034 | COMPLETE |
| Department realization + `DepartmentRef` binding | -036 | COMPLETE |
| T-1 — Capability ownership reconciliation | -037 | COMPLETE |

### D-01.3 Frontier computation

Each subsystem's own **Completion** criterion in `NCIR §9.1`–`§9.11` was checked
against the suite. All eleven pass. The frontier is therefore **not** a missing
subsystem — it is unrealized surface inside ratified boundaries.

Reading `Freeze §4` verbatim produced the finding:

> **Department** — *"owns Capabilities **and Agent Definitions**"* · *"Ownership:
> owned by Organization; owns Capabilities/**Agent Definitions**"*

> **INV-2** — *"Every Agent Definition is owned by **exactly one Department**
> and implements at least one Capability."*

**[E]** Department's ratified ownership responsibility has **two** halves. The
`-036` realization built `owned_capabilities` and **not** the Agent Definition
half. That is ratified architecture left unrealized — a construction target, not
an architecture gap.

### D-01.4 Eligible / blocked / deferred

| # | Candidate | Architecture | Spec | Dependency | Authority | Eligibility |
|---|---|---|---|---|---|---|
| **T-9** | **Department ownership of Agent Definitions (INV-2 clause 1)** | **RATIFIED** — Freeze §4 (twice) + INV-2 | **SUFFICIENT** — `department_spec §1`, `§2` already name it | **SATISFIED** — Department realization COMPLETE; `agent_definition_key` ratified | **PRESENT** — `§11` *"governed ownership context"*; `§12` | **ELIGIBLE — SELECTED** |
| ~~T-10~~ | Agent Definition declaring its own owning Department (second side of the edge) | RATIFIED | — | satisfied | **AUTHORIZED** — `ACT-CC-F03-039` `DEC-AGENT-DEPT-OWNERSHIP = OPTION A` | **COMPLETE** — see correction below |
| ~~T-11~~ | INV-2 **clause 2** — Definition implements ≥1 Capability | RATIFIED | sufficient | satisfied | **AUTHORIZED** — `ACT-CC-F03-040` `DEC-AGENT-FACTORY-INV2-CLAUSE2 = OPTION A` | **COMPLETE** |
| T-2 | Capability↔Skill/Workflow composition | RATIFIED | **RESERVED** `capability_spec §12`/`§14` **[O]** | satisfied | ABSENT | NOT ELIGIBLE |
| T-3 | Versioned-contract representation | RATIFIED | **RESERVED** `capability_spec §14` **[O]** | satisfied | ABSENT | NOT ELIGIBLE |
| T-4 | Capability Catalog category instantiation | RATIFIED | sufficient | satisfied | **ABSENT** — assigning an owner is a governance data decision; `OB-01` unresolved | CONDITIONALLY ELIGIBLE |
| T-12 | Knowledge admission model | RATIFIED | **RESERVED** — `NCIR §9.5` *"Blocked by: Knowledge admission model"* **[O]** | satisfied | ABSENT | NOT ELIGIBLE |
| T-5…T-8 | Intelligence entity · Planner · Scheduler · Execution Orchestrator | **NOT RATIFIED** | none | — | **EXCLUDED** (`§10`, `§11`) | **NOT AUTHORIZED** |

### D-01.5 Selection under `§7`

The precedence hierarchy yields a determinate result, so no ambiguity was
packaged. **(1)** Founder authorization — Phase 5 Capability-centric *"and its
governed ownership context"* (`§11`) covers Department directly. **(2)** Canonical
architecture — Freeze §4 states the unrealized half twice and INV-2 fixes it.
**(3)** Canonical specification — `department_spec §1`/`§2` already name it as a
Department responsibility. Nothing lower in the hierarchy was needed. **T-9 is
the only candidate whose four conditions all pass.**

---

## D-02. Construction Implementation

- `Department.owned_agent_definitions` — a tuple of ratified `agent_definition_key`
  values, defaulting to empty. Held as **keys**, never as embedded Definition
  state, which is what keeps `department_spec §8`'s prohibition on depending on
  Agent intact. Both ownership sets validate through one shared routine.
- `OwnershipGraph` — INV-2 clause 1 enforced at construction: two Departments
  claiming one Definition raises `ConflictingAgentDefinitionOwnership` (PR-4),
  exactly as INV-1 does for Capabilities. Added `owner_of_agent_definition()`,
  `agent_definitions_of()`, and `unowned_agent_definitions()` — the last
  **flags and never raises** (PR-3), taking keys from the caller so that no
  `capability → agent` dependency is created.
- `exceptions.py` — `ConflictingAgentDefinitionOwnership`.
- `__init__.py` — 23 exports (was 22).
- `tests/test_ownership_conformance.py` — `TestInv2AgentDefinitionOwnership`,
  11 tests, including an assertion that no Agent import is introduced and an
  explicit test that clause 2 is **not** enforced.
- `department_spec` — §3, §5, §6, §10, §11 aligned with what §1 and §2 already
  stated; §13 records the target RESOLVED and names precisely what remains
  reserved.

### What was deliberately not built (`§13` discipline)

**[E]** INV-2 clause 2 and the Definition's own view of its owner both require
validating or constructing Agent Definitions. `agent_spec §12`/`§13` **[O]**
place that in the **Agent Factory**, *"reserved to the Architect"*. Ownership is
therefore **single-sided**, and the two-sided reconciliation applied to
Capabilities under `-037` **cannot** be performed for Agent Definitions until
that reservation is lifted. This is recorded, not worked around.

---

## D-03. Verification Report

| Check | Result |
|---|---|
| Targeted behaviour (8 probes, run independently of the tests) | PASS |
| `native_core` suite | **548 OK** (1 expected failure) |
| `tools` suite | **20 OK** |
| `bounded_exception` suite | **29 OK** |
| INV-1 unaffected by the change | PASS — re-probed |
| INV-2 clause 1 enforced; clause 2 not assumed | PASS |
| PR-3 (flag, never raise) for unowned Definitions | PASS |
| PR-4 (fail closed) on dual and duplicate claims | PASS |
| No Agent import in `ownership.py` (`department_spec §8`) | PASS — asserted in test |
| Core region boundary count | **11** — recounted directly |
| Constitution · Freeze · Domain Model · Finding Register | hash-identical |
| Governance registers mutated | **0** |
| `P7-F-2` governed exception | untouched, still expected-failure |
| Planner / Scheduler / Orchestrator constructed | **0 definitions** |

**Expected failure retained.** `P7-F-2` is admitted by `GDR-0014` and its
register entry reads *"repair not authorized"*. Left untouched per `§16`.

## D-04. Research Record

**No external research was used.** The target, its authority and its boundaries
came entirely from resident canonical sources — Freeze §4, INV-2, `NCIR §9`,
`agent_spec`, `department_spec`. Nothing was OBSERVED, ADAPTED or ADOPTED, so
this deliverable has no entries.

## D-05. Escalation Package

**Not produced — no genuine architecture or governance gap was encountered.**
T-10/T-11 are `[O]`-reserved and were left alone rather than solved through
implementation (`§9`). Their reservation is recorded above and in
`department_spec §13`; lifting it is an Architect decision, not an engineering
one, and this Act does not request it.

## D-06. Next construction frontier

**[A]** Within the Capability boundary and its ownership context, **no
non-reserved engineering gap remains.** Every remaining candidate is either
`[O]`-reserved to the Architect (T-2, T-3, T-10, T-11, T-12), blocked on a
Founder-reserved authority question (T-4), or unratified and excluded (T-5–T-8).

**[D]** The next increment therefore requires a decision the Founder or Architect
owns, not further engineering. The two smallest such decisions, in dependency
order, are: **(i)** whether the Agent Factory reservation (`agent_spec §12`/`§13`)
is lifted far enough to let an Agent Definition name its owning Department,
which would complete the INV-2 edge; and **(ii)** who may assign a Capability
category to an owning Department (T-4), which is entangled with `OB-01`.


---

## Correction — `ACT-CC-F03-039`

**[E] The T-10 row above, and the *"What was deliberately not built"* note in
D-02, were wrong** where they described the Agent Definition side of the INV-2
edge as `[O]`-reserved under `agent_spec §12`/`§13`. This was an error in this
report, disclosed and corrected rather than quietly amended.

Agent Definition ownership by Department is **`[E]` ratified in three canonical
sources and reserved in none**: `agent_spec §3 Owned Data`, Freeze §4's Agent
Definition entry, and Domain Model §5's Ownership Rules table. The
`agent_spec §12`/`§13` reservation covers Agent **construction** discipline, not
ownership. What genuinely remains reserved is **INV-2 clause 2** — that a
Definition *implements at least one Capability* — which does require checking a
Definition against Capabilities, and that characterization stands.

T-10 was built under `ACT-CC-F03-039`. **T-11 remains reserved.** The rows for
T-2, T-3, T-4, T-12 and T-5–T-8 are unaffected by this correction.


---

## Update — `ACT-CC-F03-040`

**T-11 is complete.** INV-2 clause 2 — *"…and implements at least one
Capability"* — was realized under `DEC-AGENT-FACTORY-INV2-CLAUSE2 = OPTION A`:
`AgentDefinition.implemented_capabilities` enforces *at least one* per
Definition, and `CapabilityGraph.implementer_counts` /
`implementers_of` / `unknown_implemented_capabilities` supply the corpus view,
closing the INV-14 orphan loop from what Definitions actually declare.

**Reservation exercised:** the *"validated against Capabilities"* surface only.
Governed **creation, registration and lifecycle** of Agent Definitions remain
`[O]` reserved to the Architect and unbuilt.

**Remaining frontier:** **T-2**, **T-3**, **T-12** `[O]`-reserved; **T-4**
blocked on Founder-reserved authority entangled with `OB-01`; **T-5**–**T-8**
unratified and excluded. No non-reserved engineering gap remains in the
Capability boundary, its ownership context, or the INV-2 edge.
