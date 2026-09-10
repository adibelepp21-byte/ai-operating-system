# E10 Verification and P10 Certification Package

> **PREPARED ≠ CERTIFIED.** `FD-P10-004 §24` requires this statement and means
> it literally. This document records verification performed under delegated
> authority. **It is not a certification, it does not certify P10, and it does
> not close P10 governance.** `§17` withholds all three from me:
> *"Claude Code is expressly prohibited from self-certifying P10 or declaring
> Founder/governance certification or closure."*
>
> **Measuring instrument:** [`FD-P10-004`](../../governance/acts/FD-P10-004-RATIFICATION-OF-MEASURABLE-PHASE-10-EXIT-CRITERIA.md),
> Status `DECIDED`. **Verified against its ratified text**, recovered verbatim,
> not against my superseded candidate wording.
> **Verification date:** 2026-09-10 (four discovery cycles) · **Verifier:** Claude Code / Co-Founder

---

## 1. Outcome

**`E10 = PASS` on all six criteria. `P10 COMPLETE` is recommended as a
determination. `P10 CERTIFICATION` and `GOVERNANCE CLOSURE` remain PENDING and
are the Founder's alone.**

This is `FD-P10-004 §29` **Outcome A**. The state it supports is exactly the one
`§23` permits and no more:

```
P10 COMPLETE                  <- determination, recommended here
P10 CERTIFICATION  = PENDING  <- Founder authority required
P10 GOVERNANCE CLOSURE = PENDING  <- Founder/governance authority required
```

**The loop ran three times, and every cycle after the first found something.**
`§18` forbids stopping because the first pass succeeded. Cycle two found a
defect in my own loader that cycle one had passed over (`§3.4`); cycle three
attacked the *pattern* rather than waiting for a symptom and found its mirror
(`§3.5`). **All three cycles are recorded, including the ones that made this
document wrong before they made it right.**

**The ratification did not make P10 pass.** `§32`: *"The purpose of E10
ratification is not to make P10 appear complete. The purpose is to make P10
completion objectively testable."* The fresh discovery `§14` mandates **found
three real verification gaps and closed all three** (`§4.4`, `§3.4`, `§3.5`);
had any been unclosable within delegated authority, this document would have
read `P10 NOT COMPLETE`.

---

## 2. What the mandatory fresh pass actually found

`§14` forbids the inference `previously: no gap + E10 ratified = no gap`. The
pass was run against the ratified wording, which is **broader** than the
candidate wording in three places. Each addition was treated as a new question,
not as a restatement of one already answered.

| Ratified addition | Was it already verified? | Result |
|---|---|---|
| `§5(5)` *"population survives negative/falsification testing"* | Partly | Existing negative controls found; the missing-Department claim re-attacked from sources — **§3.1** |
| `§6` Agent Instance must not be misclassified as an Agent Definition | **No** | Now structurally verified — **§3.2** |
| `§10(4)` *"verification mechanisms actually test the claimed invariants"* | **No** | **Two gaps found and closed** — **§4.4**, **§3.4** |

**Both gaps discovered were gaps in the verification itself**, which is the
class `§14` exists to catch. The second was found by the `§18` loop **after this
document had already recorded `E10-01 = PASS`** — see `§3.4`, which is left
standing as a correction rather than edited away.

---

## 3. Findings from fresh discovery

### 3.1 "No required Department is missing" — attacked, survived

`§19` requires negative completion claims be actively falsified. The corpus was
swept for every distinct `X Department` name rather than for the two already
known.

- **"Home Department" — 71 occurrences, the strongest candidate.** It is **not a
  Department**. It is an accountability *role* for Knowledge under the historical
  design (`DM §5/§8`), and it occurs **only** under `docs/architecture/history/`.
  The canonical Domain Model carries the superseded wording:
  *"Knowledge | Collectively owned by the Organization; each item has a home
  **Platform Division**."* Eliminated on content, not on substring — and it is a
  live instance of `§10(7)`, *historical state is not confused with current
  state*.
- **"Security Department" — 1 occurrence**, in my own prior verification record,
  recording the decision **not** to create one. Security ownership is reserved to
  the Founder by `FD-P10-003 §10` and tracked as `AR-002`. **Reserved, not
  missing.**
- **Only two Approved ADRs establish a Department**: `ADR-0003` (Platform),
  `ADR-0008` (Engineering). Both are resident. **No third exists to be missing.**
- **"future Departments' … once established"** in the Governance Artifact
  Integrity Capability is a **forward scope exclusion**, not a present
  obligation. It bounds that Capability; it requires no Department now.

**The claim survives.** It survived an attack that had a genuine chance of
breaking it — the leading candidate outnumbered both real Departments by 5:1.

### 3.2 Agent Instance is not misclassified as an Agent Definition

`§6`'s exclusion is now verified three ways, none of which is a restatement of
another:

1. **Structurally impossible in the frozen contract.** `AgentDefinition` carries
   `owning_department_key`; `AgentInstance` carries only `agent_instance` and the
   `AgentDefinition` it realizes — **it has no owner field at all**. A transient
   Instance cannot supply ownership because there is nowhere to put it.
2. **Records honour the distinction.** All five Workflows name their invoker as
   *"an Agent Instance of the [Governance Artifact Integrity Agent]"* — never the
   Definition acting directly.
3. **A verifier now enforces it.** `w4_continuity` raises
   `workflow-invokes-definition-directly` if a Workflow names its invoker without
   the words *Agent Instance*, with a negative control proving that branch fires.

This is why the population count is **3 Agent Definitions** and not some larger
number inflated by Instances: **no Agent Instance record exists on disk at all.**

### 3.3 The circular check remains declined, and stays disclosed

`OwnershipGraph.disputed_agent_definition_ownership` is still **NOT RUN**. It
compares a Definition against a named owning Department, and the only such
declaration these records carry **is** the nesting — so it would compare nesting
against itself and pass by construction. **A check that cannot fail is not
evidence.** The decline is printed in the tool's own output, not buried here.
`§6`'s concern is met by §3.2 instead, which can fail.

### 3.4 A defect in my own verification, found after I had recorded PASS

`§18` requires the loop to continue *"not stop simply because the first E10
verification pass is successful."* It did, and it caught a defect **in my own
loader** that this document's first version had already passed over.

**`read_departments` accepted a Department directory whose README cites no
establishing ADR** — recording an empty `establishing_adrs` tuple, counting it in
the population, and saying nothing. Demonstrated directly: a fabricated
`marketing/` directory with no ADR was read and accepted.

So `§5` condition 3 — *"no unauthorized Department has been introduced"* — was
evidenced **only by the observation that the resident population happens to be
clean**. `§10(4)` asks that mechanisms *"actually test the claimed invariants."*
**A check that cannot fail is not evidence**, and this one could not fail.

`unestablished()` now reports Departments **and** Capabilities citing no
establishing ADR, with negative controls in both directions and a positive
control proving the fixture can come back clean. The resident population reports
**0 and 0** — the same answer as before, but now for a reason that could have
been otherwise.

**This correction is recorded, not applied silently.** The first version of this
package stated condition 3's evidence as *"Population = 2; both ADR-established."*
That was a true observation resting on a mechanism that could not detect its own
falsification, and `E10-01` was **under-evidenced when first recorded as PASS**.
It is now properly evidenced. The verdict is unchanged; **the ground under it is
not**, and the difference is exactly what `§14` was written to expose.

### 3.5 A third cycle, and the mirror of the same defect

The loop ran a third time, attacking the pattern cycle two exposed — **checks
that cannot fail** — rather than waiting for a new symptom. Two findings:

**`_owner_disagreements` was sound but unproven.** The cross-check comparing a
Capability's stated `## Owner` against its nesting was asserted `== []` on the
resident corpus and never shown able to fire. Planting a contradicting owner and
a missing owner shows it reports both. **This was a missing control, not a
defect** — the distinction is kept rather than counted as a third gap, since the
mechanism worked all along.

**`NON_DEPARTMENT_DIRS` excluded `platform-runtime`, a directory that has never
existed anywhere in this repository** — speculatively added by me in `338f4ac`.
It changed no result, because excluding nothing excludes nothing. But it is the
**exact mirror of `G-I`**: rather than admitting an unauthorized Department, it
would have **silently suppressed a legitimate one** established under that name,
and `§5` condition 2 (*"no required Department is demonstrably missing"*) fails
in the one way a population count can never reveal — the entry simply never
appears. Removed, and a test now requires every exclusion to name a directory
that exists, so no future exclusion can quietly become a hole.

---

## 4. E10 results

### 4.1 `E10-01` — Department Identity & Population · **PASS**

| `§5` pass condition | Evidence |
|---|---|
| 1. traceable to legitimate authority | Engineering ← `ADR-0008` (**Approved**); Platform ← `ADR-0003` (**Approved**). Read from each record's own *"established by"* sentence, not from any ADR merely mentioned nearby — a defect corrected earlier and regression-tested. |
| 2. no required Department missing | **§3.1**, attacked and survived |
| 3. no unauthorized Department introduced | `unestablished()` reports **0 departments, 0 capabilities** citing no establishing ADR — **a mechanism that can fail**, with negative controls both ways. **This replaces the bare observation first recorded here; see `§3.4`.** `execution-catalog/` is excluded as catalog material, and the exclusion is explicit, not incidental |
| 4. identity consistent with canonical architecture | Organization root `aios` **derived from the Domain Model's own Organization row**, failing closed when absent |
| 5. survives negative/falsification testing | `AMentionIsNotAnEstablishment`, `ItNeverConvertsAPlatformDivisionIntoADepartment`, `TheRootIsDerivedFromTheDomainModel` (2 fail-closed controls), plus §3.1 |

### 4.2 `E10-02` — Ownership Integrity · **PASS**

| `§6` pass condition | Evidence |
|---|---|
| valid ownership of owned Capabilities | 3 Capabilities, `INV-1` unowned **0** |
| no unauthorized ownership | record/nesting disagreements **0** |
| no conflicting Department ownership | **0** disputes |
| declarations agree with the runtime graph | Two-sided cross-check: each Capability's own `## Owner` section against the directory it is nested under — **two independent statements**, so disagreement is detectable |
| ownership invariants pass | `INV-1` **0** unowned · `INV-2` **0** unowned |
| does not cross reserved authority boundaries | **Checked, not assumed.** `governance-artifact-integrity` is *artifact* integrity — internal consistency of documents — and states *"it does not itself grant or define any authority."* It is **not** the Governance Authority reserved by `FD-P10-003 §10` / `AR-004`. No Capability touches Security or Quality authority |
| negative controls demonstrate failure | 4 planted-defect controls on the chain, each verified to fire **alone** |
| Agent Instance not misclassified | **§3.2** |

### 4.3 `E10-03` — Work Entry & Capability Selection · **PASS**

`resolve_work_entry()` resolves all three Capabilities to an accountable
Department and implementing Agent Definition.

**`§7` says "invalid **or** unknown", and only *unknown* had been tested.** The
fourth discovery cycle probed the invalid shapes: empty string, whitespace,
`None`, non-string types, `../../etc/passwd`, and the near-misses a helpful
normalizer would accept — `COGNITIVE-INTELLIGENCE`, a trailing space, an
underscore separator. **Every one fails closed**; only the exact key resolves.
The strictness is itself the guarantee, and is now asserted so that a later
change trimming or lowercasing the key — turning fail-closed into best-effort
matching — fails a test rather than passing quietly.

**No Work entity was created.** `§7` permits the criterion to be satisfied
functionally and forbids introducing an entity to satisfy it; `Freeze §4` says
*"No new entity."* `WorkEntry` is a **resolution result**, recomputed on every
call — nothing stored, owned, versioned, traced, or given a lifecycle — and
`test_it_is_not_a_work_entity` asserts the absence of every one of those
properties so that a later change adding one fails a test.

### 4.4 `E10-04` — Department → Execution Continuity · **PASS (gap found and closed)**

**This is where the fresh pass earned its keep.** Two verifiers already covered
this ground and **both reported clean**: `w4_chain` walked Department → Capability
→ Agent Definition; the Agent Integration Validator walked Agent Definition →
Workflow/Skill bidirectionally, 0 findings.

**Nothing joined them.** The composed path a Department actually originates was
evidenced by two passing halves lying adjacent — which is not a verified chain.
`§10(4)` asks that mechanisms *"actually test the claimed invariants"*, and no
mechanism tested the join.

`w4_continuity` now walks the whole path and checks four independently falsifiable
claims: the declared Workflow has a record; it cites back to the Agent Definition
that declared it; it names an **Agent Instance** as invoker; and every Skill it
contains is one its invoker was permitted.

```
platform -> governance-artifact-integrity -> governance-artifact-integrity-agent
    -> governance-corpus-health-check        -> 2 skill(s)
    -> governance-synchronization-review     -> 4 skill(s)
    -> post-amendment-consistency-sweep      -> 2 skill(s)
    -> pre-ratification-validation           -> 2 skill(s)
    -> terminology-audit                     -> 2 skill(s)
5 chains · 12 skill links · 0 defects
```

**Two Engineering Agent Definitions declare no Workflow, and that is not a
defect.** `DM §7` invariant 15 and `ADR-0007` make an empty declaration a valid
architectural state with no minimum cardinality. They are reported as
**terminal**, and a test asserts the terminal count **so that a later change
which manufactures a Workflow to lengthen those chains fails rather than
passes** — `§27` forbids that construction and none was performed.

**No `Planner`, `Scheduler`, or `Execution Orchestrator` was created.** The
three runtime substrates remain unreferenced by any Agent Definition, reported
`informational`: Agent Definitions state Runtime Requirements **in the abstract**
per `DM §8` and `Constitution §6.2` invariant 1, which forbid naming a specific
technology. **The non-reference is required by the architecture, not a gap in
it** — a naive reading would have called it an execution-layer break.

### 4.5 `E10-05` — Organizational Boundary Integrity · **PASS**

`PD ≠ Department` is preserved **mechanically, not by intention**: the loader
never reads the Platform-Division tree, and `test_the_platform_organization_tree_is_not_consulted`
fails if it starts. No PD appears in the population. No parallel organizational
model exists — the ownership graph is the frozen `OwnershipGraph`, imported, not
reimplemented. Reserved authority is intact: `AR-001`…`AR-005` remain open and
**none was closed by this verification**. The `Department` / `Platform Division`
semantic conflict remains routed to `ADR-0029`, **Proposed, not Approved** —
Architect-reserved and deliberately undecided here.

### 4.6 `E10-06` — Evidence & Verification · **PASS**

| `§10` condition | Evidence |
|---|---|
| 1. evidence for every required dimension | §5 mapping, 9/9 |
| 2. traceable | Every claim cites a resident instrument or a runnable command |
| 3. current | **All evidence re-run today**, not carried forward — `§13` |
| 4. mechanisms actually test the invariants | **The one gap found — §4.4** |
| 5. negative controls exist | 5 defect kinds on the continuity verifier plus 2 on the establishment check, each with a control, each with a positive control proving its fixture can come back clean |
| 6. detector integrity verified | Each control confirmed to fire **alone**; a control passing because a *different* check tripped would prove nothing about its branch |
| 7. historical ≠ current | **§3.1** (Home Department); stale-state audit **0** live stale assertions across 449 documents, 54 historical uses correctly preserved |
| 8. filename/index ≠ canonical | Citation audit **84 documents, 0 errors**; the audit prints that a resolved citation proves the pointer real, **not** that the source supports the claim |
| 9. evidence persisted | This file, the verifier, its tests, and `FD-P10-004` itself |

---

## 5. Evidence matrix — the nine Blueprint dimensions

`§11` fixes the mapping and warns it *"MUST NOT be interpreted as deleting any of
the nine."* They are therefore listed individually, each with its own evidence.

| Dimension | Criterion | Evidence |
|---|---|---|
| identity | `E10-01` | 2 Departments, ADR-established; root derived from the Domain Model |
| authority | `E10-01`/`E10-05` | `ADR-0003`, `ADR-0008` Approved; reserved matters untouched |
| ownership | `E10-02` | `INV-1`/`INV-2` clean; two-sided cross-check |
| capability | `E10-02`/`E10-03` | 3 Capabilities owned; all resolve |
| execution | `E10-04` | Work entry → accountable Department → Agent Definition |
| workflow | `E10-04` | 5 joined chains into Workflow, reciprocity verified |
| coordination | `E10-04`/`E10-05` | Workflow-contains-Skill ⊆ invoker's permitted Skills |
| verification | `E10-06` | 1 360 tests; 5 negative controls; 3 auditors |
| lifecycle | `E10-04`/`E10-06` | `INV-14` zero-implementer check; Status sections current |

---

## 6. P1–P9 regression (`§26`)

Run fresh after every change in this pass:

| Suite | Result |
|---|---|
| `native_core` | **801 OK** (1 expected failure, `GDR-0014`, pre-existing and expected) |
| `consumers` | **276 OK** |
| `tools` | **294 OK** (272 before; +22 this pass) |
| Execution-catalog validators | **0 error, 0 warning**, 4 informational |
| Citation audit | 84 documents, **0 errors** |
| Stale-state audit | 449 documents, **0 stale assertions** |

**No regression.** No previously certified phase was reopened — `§26` permits
reopening only on actual regression, and none occurred. Phase 9 governance
remains **CLOSED** per `FD-P9-002`; nothing here reaches into it.

---

## 7. Gap classification (`§15`)

| # | Gap | Class | State |
|---|---|---|---|
| G-A | Chain join between `w4_chain` and the Agent Integration Validator unverified | `E10-IN-BOUNDARY / ACTIONABLE` | **RESOLVED** — §4.4 |
| G-I | Department/Capability with no establishing ADR silently accepted | `E10-IN-BOUNDARY / ACTIONABLE` | **RESOLVED** — §3.4. Found by the `§18` loop **after** `E10-01` was first recorded PASS |
| G-J | `NON_DEPARTMENT_DIRS` excluded a directory that never existed, which would silently suppress a Department later given that name | `E10-IN-BOUNDARY / ACTIONABLE` | **RESOLVED** — §3.5 |
| G-B | `disputed_agent_definition_ownership` circular, cannot run | `E10-IN-BOUNDARY / ACTIONABLE` | **RESOLVED by substitution** — §3.2 provides a check that *can* fail; the decline stays disclosed |
| G-C | `Department` vs `Platform Division` semantics (`AR-001`) | `E10-IN-BOUNDARY / ARCHITECT-RESERVED` | **OPEN** — `ADR-0029` Proposed. Does **not** block: both Departments are ADR-established under either reading |
| G-D | Security Owner, Quality Authority bindings (`AR-002`/`AR-003`) | `E10-IN-BOUNDARY / FOUNDER-RESERVED` | **OPEN** — `FD-P10-003 §10`. Both options drafted at `G-03`; no Capability requires them today |
| G-E | Governance Authority binding (`AR-004`) | `E10-IN-BOUNDARY / FOUNDER-RESERVED` | **OPEN** — expressly withheld by `FD-P10-003 §10` |
| G-F | `Volume VII` not present in the repository (`AR-005`) | `E10-IN-BOUNDARY / SOURCE-BLOCKED` | **OPEN** — the only item **no decision can close**; it requires the artifact itself |
| G-G | Knowledge's *home Platform Division* unassigned | `E10-OUT-OF-BOUNDARY` | PD track. `ACT-CC-P10-AUTHORIZATION §5`: `PD ≠ P10` |
| G-H | 3 runtime substrates + 1 tool unreferenced | `NOT-REQUIRED` | Required by `DM §8` / `Constitution §6.2` inv. 1 — §4.4 |

**`§15`: "No gap may affect the completion verdict without a trace to E10 or a
higher authoritative requirement."** `G-C`…`G-F` are **reserved matters, not
completion-critical**: each is traced to the instrument reserving it, none is
mine to close, and none blocks any of the six criteria. `§16`'s resolution
sequence was run on each and terminates at reserved authority — **not at
"AUTHORITY MISSING"**, which `§16` forbids as a stopping point.

---

## 8. Authority status

**Exercised:** `§17` verification, evidence construction, gap identification,
delegated technical resolution, certification-material preparation. All within
`FD-P10-004` and `FD-P10-003`.

**Not exercised, and not available to me:** self-certification of P10, Founder
certification, governance closure, `ADR-0029` approval, Security/Quality/
Governance Authority binding, amendment of any frozen or constitutional
artifact, and the 13 protected packages — untouched, unstaged, uninspected.

---

## 9. The exact decision required from the Founder (`§24`)

> **Does the Founder certify Phase 10 — Department Ecosystem — as COMPLETE, on
> the evidence that `E10-01` … `E10-06` are verified PASS against `FD-P10-004`?**

Three answers are available, and **the second and third are real**:

1. **CERTIFY** — P10 becomes certified; governance closure may then be prepared.
2. **CERTIFY WITH CONDITIONS** — naming which reserved matters (`G-C`…`G-F`)
   must close first. **`G-F` cannot be closed by decision**; it needs `Volume VII`
   supplied.
3. **DECLINE** — naming what the six criteria fail to measure. `§11` preserves
   the nine dimensions as *"the authoritative conceptual boundary"*, so a
   dimension I mapped but the Founder reads as under-evidenced is a legitimate
   ground to decline, and `E10 = PASS` does not foreclose it.

**Nothing in this package should be read as pressure toward the first.** `§2`
fixes `RATIFICATION ≠ COMPLETION ≠ CERTIFICATION ≠ GOVERNANCE CLOSURE`, and
`§28` fixes `TEST PASSES ≠ FOUNDER CERTIFIED`.

---

## 10. How to reproduce every claim here

```
python3 tools/organization_catalog.py
python3 tools/validate_execution_catalog.py
python3 tools/corpus_citation_audit.py
python3 tools/stale_state_audit.py
python3 -m unittest discover -s native_core -t . -q
python3 -m unittest discover -s consumers  -t . -q
python3 -m unittest discover -s tools -t tools -q
```

**No claim in this document rests on my report of it.** Each is reproducible by
the Founder or by anyone else from the commands above, which is the only form of
evidence `§28` treats as distinguishable from assertion.
