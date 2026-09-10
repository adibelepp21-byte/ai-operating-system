# ARCHITECT DECISION INSTRUMENT — DP-03

## P11 Organizational Architectural Surface & Interfaces

| Field | Value |
|---|---|
| **Decision ID** | `DP-03` |
| **Phase** | P11 — Autonomous Organization |
| **Authority Tier** | **Architect-Reserved** |
| **Status** | **`DECISION-PENDING`** |
| **Authoritative input** | **`DP-04` — ISSUED 2026-09-10** |
| **Prepared under** | `ACT-CC-P11-003` |

> # `DECISION-PENDING` — Architect sections untouched
>
> **`§16`, `§17`, `§18`, `§19` are exactly as supplied. Claude filled none of
> them**, including `§16.5` where the recommendation is obvious — the Act forbids
> pre-filling *"even if its recommendation is obvious."*
>
> **`CLAUDE PREPARES · ARCHITECT DECIDES · FOUNDER AUTHORIZES.`**

---

## 6. Actual-source verification (`§6`)

### 6.2 `DP-04` read as an actual body, not an identifier

Read from the persisted issued instrument, `sha256 cfe6c573…`:

| Extracted | Value |
|---|---|
| Selected option | `§14` **OPTION C — organizational-layer representation outside the frozen Native Core** |
| `Goal` | `§8.1` P11 organizational concept; *"does not create authority by itself"* |
| `Plan` | `§8.2` *"shall exist in the organizational layer **outside the frozen Native Core**"* |
| `Delegation` | `§8.3` *"first-class P11 organizational relation/record outside the frozen Native Core"* |
| `OrganizationalState` | `§8.4` bounded projection; system-wide integration reserved to **P12** |
| No-New-Entity | `§9` *"does NOT create … Native Core subsystem #12"* |
| P12 boundary | `§10` P12 owns *Unified Operational State* |
| Effective authority | `§26` **`ARCHITECT DECISION ≠ FOUNDER AUTHORIZATION`** |

**No conflict discovered. `DP-04` remains unchanged and is not reopened.**

### 6.3 Native Core — a twelfth is not required

Native Core Blueprint `§4`, verbatim: *"The core region contains exactly the
eleven frozen subsystem boundaries — no more (no new entity/subsystem may be
introduced)."* **Verified by listing:** `agent · capability · governance ·
infrastructure · knowledge · memory · optimization · runtime · skill · trace ·
workflow` — **eleven.**

**`DP-03` requires no twelfth**, and `DP-04 §9` already closed the question.

### 6.4 Existing implementation — the decisive negative

**No `Plan`, `Goal`, or `Delegation` class exists anywhere** in `native_core/`,
`consumers/` or `tools/`. Searched by class definition, not by filename.

**This matters for the options:** `Option C`'s *"maximum reuse"* cannot mean
reusing a planning or delegation implementation, **because none exists.** It can
only mean reusing the **organizational record + loader pattern** that P10 built.

### 6.5 PD-01 — reference pattern, verified

| Boundary | Source, verbatim |
|---|---|
| Coordination constraints | `volume-1/pd-01-executive-office/D3.md:140` — the *Coordination Constraints* list states D3 must not `create governance authority`, and at `:141` must not `create unauthorized delegation`; it also bars overriding Platform ownership, bypassing compliance, and redefining architecture |
| `Governance ≠ Execution` | `A1.md:94`, `A10.md:201` |
| Performance boundary | `DIVISION-OPERATION-AND-PERFORMANCE-MODEL.md:100-106`, quoting `E-56`: *"performance assessment does not create strategy, governance, architecture, ownership, or execution authority"* · **`Measurement ≠ authority`** — *"A division's Performance Architecture confers nothing on it"* |
| The five distinctions | `AIOS_GAP_CLOSURE_P10_P13_CONSTRUCTION_ROADMAP_v1.0.md:370` carries all five in one block, including `Delegation ≠ Transfer of Ultimate Accountability` and `Governance ≠ Execution` |

**`§6.5`'s constraint honoured: the pattern is reused conceptually; no PD-01 domain
content is copied into P11.**

---

## 7. Reconciliation matrix (`§7`)

| P11 capability | Canonical definition | Current surface | Authority | Boundary | Evidence | Residual |
|---|---|---|---|---|---|---|
| **W1** Coordination | resident Blueprint: *cross-department coordination; work routing; dependency; handoff; escalation* | **`workflow`** | existing | **`INV-13`** — Workflow is *"the SOLE sanctioned multi-agent channel"* | `workflow/__init__.py`; `Freeze §4` | **confirmation only** |
| **W2** Planning | *goal decomposition; planning; prioritization; sequencing; dependency-aware execution* | **none exists** | P11/Architect | **outside Native Core** (`DP-04 §8.2`) | `§6.4`; `DP-04` | **ARCHITECT** |
| **W3** Delegation | *organizational delegation; authority boundary; accountability; delegation tracking; delegation verification* | **none exists** | governed | **outside Native Core** (`DP-04 §8.3`) | `§6.4`; `DP-04` | **ARCHITECT** |
| **W6** Performance | *running · completed · failed · blocked · escalation · improvement opportunities* | **`optimization`** — `ObservationPublication` | **detect-only** | no authority creation | `optimization/contract.py`; `E-56` | **confirmation** |
| **Native Core #12** | prohibited | none | Architect freeze | no new subsystem | `DP-04 §9`; Blueprint `§4` | **CLOSED** |

**No cell filled from assumption.**

---

## 8. W2 — Planning: the fourteen questions (`§8`)

| # | Question | Evidence-backed answer |
|---|---|---|
| 1 | Where does a `Goal` live? | Organizational layer, outside the core — `DP-04 §8.1` |
| 2 | Where does a `Plan` live? | Same — `DP-04 §8.2` |
| 3–5 | Who owns / may create / may modify a Plan? | **UNRESOLVED — Architect.** `DP-04` fixes the *layer*, not the ownership rule |
| 6 | What converts Plan → Work? | **`INV-13` constrains the answer**: execution reaches Agent Instances only through `Workflow`. A Plan cannot become executing work by any other path |
| 7 | Dependency information | `Capability` declares *"explicit versioned dependencies (INV-9)"*; cross-Department dependency requires governance (`INV-10`) |
| 8 | Interaction with Workflow | Plan → Workflow, **one direction**. Workflow does not read plans |
| 9 | With Capability/Ownership | **query only** — `OwnershipGraph` answers *which Department owns this Capability*; P10 already implements it |
| 10 | With Governance | **reference only.** Governance *"holds authority over decisions"* and decides *"nothing automatically"* (`PR-3`) |
| 11 | With Runtime | **none directly.** Runtime binds Definition→Instance; planning has no runtime edge |
| 12 | **Can Planning grant authority?** | **NO** — `DP-04 §8.1`/`§18`: *"Plan → Automatic authority"* is a prohibited transformation |
| 13 | **Can Planning self-authorize execution?** | **NO** — same |
| 14 | **Can Planning redefine constitutional or Founder authority?** | **NO** — `Constitution §6.2` inv. 2; `DP-04 §26` |

**`PLANNING ≠ AUTHORITY · PLAN ≠ AUTHORIZATION · GOAL ≠ AUTHORITY` — preserved.**

---

## 9. W3 — Delegation: the fifteen questions (`§9`)

`DP-04 §8.3` already fixes the **record shape**, and it answers several directly:

```text
AUTHORITY SOURCE → AUTHORIZED SCOPE → DELEGATED ACTOR/UNIT
                 → BOUNDARY → ACCOUNTABILITY → VERIFICATION
```

| # | Question | Answer |
|---|---|---|
| 1 | Where represented? | Organizational relation/record outside the core — `DP-04 §8.3` |
| 2 | Who issues? | **UNRESOLVED — Architect** |
| 3 | What authority may it contain? | **Only authority the delegator already holds** |
| 4 | What may it **not** contain? | Authority the delegator lacks; constitutional or Founder authority; ultimate accountability |
| 5 | Scope | `AUTHORIZED SCOPE` field |
| 6 | Accountability | `ACCOUNTABILITY` field — **and it stays with the delegator** |
| 7 | Tracking | The record itself; provenance via **Trace**, immutable under `INV-4`/`INV-5` |
| 8 | Verification | `VERIFICATION` field; reconstructable from Trace |
| 9 | Interface to Workflow | **routing only** — bounded authority conveyed; `INV-13` still the sole channel |
| 10 | To Capability/Ownership | **scope validation** — is this actor within the owning Department? |
| 11 | To Runtime | **enforce bounds; never expand them** |
| 12 | To Governance | **reference, never creation.** This is the critical separation |
| 13 | Ultimate accountability preserved? | **YES** — `Delegation ≠ Transfer of Ultimate Accountability` is resident, `AIOS_GAP_CLOSURE_P10_P13_CONSTRUCTION_ROADMAP_v1.0.md:370` |
| 14 | **Can Delegation create authority?** | **NO** — `DP-04 §18` |
| 15 | **Can Delegation authorize itself?** | **NO** |

**Why `governance` cannot host this, restated from source:** `governance`
*"imports nothing from Knowledge, Capability, Skill, Workflow, Agent, Runtime, or
Optimization."* Delegation must reference **Capability/Ownership** and route to
**Workflow**. **Hosting it in governance would break that isolation** — which is
what keeps authority un-automatable (`Constitution §6.2` inv. 2).

**`DP-04 §15` resolves this without breaking either**: the relation lives outside
the core and *references* governance rather than becoming it.

---

## 10. W6 — Performance confirmation (`§10`)

> ### CONFIRM, DO NOT CONSTRUCT

The existing mechanism **already enforces every negative control `§10` requires**,
and it does so in its own contract rather than by convention:

| `§10` requires Performance MUST NOT | Existing enforcement |
|---|---|
| authorize | `optimization/__init__.py`: *"Optimization never submits, sends, notifies, requests, approves, promotes, **authorizes**, or **decides**"* |
| govern | *"It depends on Governance in no way"* — the dependency is **inverted** so *"automation cannot acquire a decision path"* |
| determine strategy | `E-56`: *"performance assessment does not create **strategy**, governance, architecture, ownership, or execution authority"* |
| execute | `Freeze §5` layer 10 — outputs are *"proposals only"* |
| promote itself into decision authority | `INV-8` forbids self-promotion; `PR-3` detect-don't-decide |

**And what Performance MAY do is already implemented:** `ObservationPublication`
(`optimization/contract.py:59`) with `PassiveObservationPublication`
(`composition.py:97`) — *"observes Trace and Memory and publishes what it
observed."*

**`Measurement ≠ authority`** — *"A division's Performance Architecture confers
nothing on it."*

**One constraint the Architect should make explicit:** optimization reserves
*"signal catalogue · evaluation scoring · **prioritization model** · optimization
algorithm · recommendation engine · ranking model · decision heuristics"* to the
Architect, unimplemented. **`W6` stays inside the confirmed home only while it
remains detect-only. The moment it ranks or scores, it re-enters reserved
ground** — and `P11-W2` needs *prioritization*, which is on that list.

---

## 11. W1 — Coordination confirmation (`§11`)

> ### CONFIRM — and it is not merely available, it is forced

`INV-13` makes `Workflow` *"the SOLE sanctioned multi-agent channel"*, and
`Freeze §4` forbids Agent Instances *"direct collaboration outside
Workflow/Knowledge/scoped Memory (INV-13)."*

**Cross-department coordination routed anywhere else violates an invariant.**
`§11`'s condition for proposing an alternative — *"unless authoritative evidence
proves the existing placement invalid"* — is **not met**; the evidence proves the
opposite.

**Boundary preserved**, corroborated by PD-01 `D3.md`, whose *Coordination
Constraints* bar D3 from `create governance authority` and from
`create unauthorized delegation`.
**`COORDINATION ≠ OWNERSHIP · ≠ GOVERNANCE · ≠ AUTHORITY CREATION`.**

---

## 12. Interface matrix (`§12`) — one amendment, evidence-driven

The supplied matrix is adopted with **one change**, which `§12` permits where
*"actual source evidence requires a different relationship"*:

| Organizational surface | Core surface | Direction | Authority effect |
|---|---|---|---|
| Planning | Workflow | Planning → Work | **none** |
| Planning | Capability/Ownership | query | **none** |
| Planning | Trace | observe | **none** |
| Planning | **Memory** | ~~read/write where authorized~~ → **read; write only as a promotion *candidate*** | **none** |
| Delegation | Workflow | routing | bounded only |
| Delegation | Capability/Ownership | scope validation | **none** |
| Delegation | Governance | reference | **no creation** |
| Delegation | Runtime | enforce bounds | **no expansion** |
| Performance | Trace | observe | **none** |
| Performance | Memory | publish evidence | **none** |
| Coordination | Workflow | route/handoff | **none** |

**Why the amendment.** `Freeze §4` scopes Memory to *"the producing Agent
Instance/Department"*, and `INV-8` admits Memory→Knowledge **only via governed
promotion**, forbidding self-promotion. An unqualified *"read/write where
authorized"* could read as a write path that bypasses `INV-8`. **Narrowed to
match the invariant rather than left ambiguous.**

---

## 13. Options (`§13`) — evaluated, not selected

| Criterion (`§14`) | **A** Shared surface | **B** Distinct surfaces | **C** Existing + records | **D** New component |
|---|---|---|---|---|
| Semantic correctness | good | **best separation** | good | **best isolation** |
| `DP-04` compliance | **yes** | **yes** | **yes** | **yes** |
| No-New-Entity / Freeze | **yes** | **yes** | **yes** | **yes** |
| P11 scope / P12 boundary | ok | ok | **ok** | risk of pre-empting P12 |
| Authority safety | needs explicit bounds | **clearest** | **record fields carry bounds** | clear |
| `Governance ≠ Execution` | preserved | preserved | **preserved** | preserved |
| Delegation ≠ accountability transfer | field-dependent | field-dependent | **field-dependent** | field-dependent |
| **Existing reuse** | partial | low | **highest — P10 pattern exists** | **none** |
| Interface clarity | medium — overload risk | **high** | high | high |
| **Reversibility** | medium | medium | **highest** | **lowest** |
| Verification complexity | medium | higher — two surfaces | **lowest — P10 suites extend** | highest |
| Future P12 integration | ok | ok | **ok** | **UNKNOWN** |

**`§6.4` constrains this table:** no planning or delegation implementation exists,
so `A`, `B` and `D` all mean **build something new**, differing only in shape.
**Only `C` reuses something that already works.**

---

## 15. CO-FOUNDER RECOMMENDATION

> # CO-FOUNDER RECOMMENDATION — **NOT ARCHITECT DECISION**

**`Option C` — existing organizational/capability surface plus explicit bounded
records — for both `W2` and `W3`. Confirm `W6` to `optimization` under an explicit
detect-only constraint. Confirm `W1` to `workflow`.**

**Why, from evidence rather than preference.**

**P10 already built this exact pattern and it is verified.** Records live under
`docs/architecture/organization/`; `tools/organization_catalog.py` reads them and
constructs the **frozen** `OwnershipGraph`, creating no entity and adding no
boundary. It carries 294 tool tests, negative controls that each fire in
isolation, and a fail-closed work-entry resolver. **`DP-04 §8.3` gives Delegation
a *record* shape — and a record surface outside the core is precisely what P10
already operates.**

**Why not the others.** `A` risks the semantic overload `§13` names, and Planning
and Delegation must stay distinguishable — `DP-04` treats them differently. `B`
doubles the surface for a benefit `C` obtains through separate record types. `D`
is the least reversible and, with **no existing implementation to displace**,
would be new architecture chosen over a proven pattern.

**Evidence vs inference, marked.** *Evidence:* the P10 pattern exists, is
verified, and adds no boundary; `DP-04` specifies a record shape; no planning or
delegation implementation exists. *Inference:* that record semantics will
adequately carry **plan lifecycle** — see `§20` Test 1, where this **does not
fully survive falsification**.

**Why this does not violate `DP-04`.** It creates no Native Core subsystem
(`§9`), keeps Delegation a governed relation/record outside the core (`§8.3`),
keeps Goal and Plan organizational concepts (`§8.1`/`§8.2`), and leaves
`OrganizationalState` a bounded projection with system-wide integration reserved
to P12 (`§8.4`).

**How authority boundaries are preserved.** Records **declare** bounds; they never
create them. Execution reaches agents only through `Workflow` (`INV-13`).
Governance is **referenced, never entered**. Accountability stays with the
delegator. Performance stays detect-only.

**Remaining uncertainty, stated plainly:** plan lifecycle, and who may create or
modify a Plan (`§8` questions 3–5). `DP-04` fixed the layer, not the ownership
rule. **Both are Architect matters and I do not resolve them.**

---

## 16. ARCHITECT CHOICE — RESERVED

**CLAUDE CODE HAS NOT COMPLETED THIS SECTION.**

**16.1 W2 Planning** — Architect Choice: `[ ARCHITECT TO SELECT ]` · Selected Option: `[ ARCHITECT TO ENTER ]` · Rationale: `[ ARCHITECT TO ENTER ]`

**16.2 W3 Delegation** — Architect Choice: `[ ARCHITECT TO SELECT ]` · Selected Option: `[ ARCHITECT TO ENTER ]` · Rationale: `[ ARCHITECT TO ENTER ]`

**16.3 W6 Performance** — Architect Choice: `[ ARCHITECT TO CONFIRM ]` · Decision: `[ ARCHITECT TO ENTER ]` · Rationale: `[ ARCHITECT TO ENTER ]`

**16.4 W1 Coordination** — Architect Choice: `[ ARCHITECT TO CONFIRM ]` · Decision: `[ ARCHITECT TO ENTER ]` · Rationale: `[ ARCHITECT TO ENTER ]`

**16.5 Native Core #12** — Architect Choice: `NO NEW NATIVE CORE SUBSYSTEM` · Status: `[ ARCHITECT TO CONFIRM ]` · Rationale: `[ ARCHITECT TO ENTER ]`

> **`§16.5` left unconfirmed deliberately.** The Act says Claude *"MUST NOT
> pre-fill this section, even if its recommendation is obvious."* It is obvious —
> `DP-04 §9` already closed it — **and the confirmation is still the Architect's.**

## 17. ARCHITECT RATIONALE — RESERVED

`[ ARCHITECT TO ENTER ]` — Claude must not write the Architect's rationale.

## 18. EFFECTIVE DATE — RESERVED

`[ ARCHITECT TO ENTER ]`

## 19. ARCHITECT SIGNATURE — RESERVED

Architect: `[ ARCHITECT TO ENTER ]` · Signature: `[ ARCHITECT TO ENTER ]`

---

## 20. Prove-me-wrong (`§20`) — seven tests, one survives against me

| Test | Outcome |
|---|---|
| **1 — Existing surface insufficiency** | **PARTIALLY SURVIVES — reported against my own recommendation.** A Delegation *record* maps cleanly onto the P10 pattern; a **Plan does not obviously**. Plans are **mutable over time** — resequenced, re-prioritized, adapted (`P11-W4` ends in `ADAPT`) — while P10's records are **static declarations read by a loader**. `DP-04 §8.2` names *"adaptation"* among Plan's semantics. **Whether a static-record surface can carry a mutating plan lifecycle without distortion is not established, and `Option C` is weaker here than `§15` alone would suggest** |
| **2 — Governance collision** | **FAILS to break it.** Records *reference* authority; Governance *decides*. `governance` imports nothing from the boundaries Delegation must touch, so a delegation record cannot become Governance without breaking an isolation that is externally enforced |
| **3 — Authority creation** | **FAILS.** `DP-04 §18` prohibits `Plan → automatic authority` and `Delegation → Governance authority`. Records declare bounds the delegator already holds |
| **4 — Accountability collapse** | **FAILS**, given the `ACCOUNTABILITY` field is mandatory. `Delegation ≠ Transfer of Ultimate Accountability` is resident and cited |
| **5 — Native Core pressure** | **FAILS.** No canonical source requires a twelfth; `DP-04 §9` closed it; the core lists eleven |
| **6 — P12 collision** | **FAILS while state stays organization-scoped.** `DP-04 §8.4` reserves system-wide integration to P12. **A real risk if planning state is later aggregated across the system** — flagged, not dismissed |
| **7 — Runtime bypass** | **FAILS.** `INV-13` makes Workflow the sole multi-agent channel; a record surface cannot open a parallel execution path without violating it |

**Six tests failed to break the recommendation. One did not, and it is recorded
rather than argued away** — `§20` requires updating the recommendation if
falsification succeeds. **It partially succeeded**, so `§15` now carries the plan
lifecycle question explicitly as unresolved, and `Option C` is recommended **with
that qualification** rather than unconditionally.

---

## 20.1 The guard caught me reformatting quotations

**`§25 K` verification failed on first run** — **two citation ERRORs, both in this
document**, both `TEXT MISMATCH`.

**The auditor was right and the failure was mine.** I had quoted PD-01 `D3.md`
and the Gap Closure Roadmap while **reformatting them** — collapsing a bullet
list onto one line, inserting `·` separators, adding bold the source does not
have. **Quote marks around edited text is precisely the discipline this guard
exists to catch**, and the text-verification path caught it at the cited line.

**Fixed by quoting exact substrings and describing the rest**, not by loosening
the check. The substance was never wrong — `create governance authority` and
`create unauthorized delegation` are both there, as is
`Delegation ≠ Transfer of Ultimate Accountability`. **The presentation was**, and
a quotation that has been tidied is no longer a quotation.

---

## 21. Negative-control assertions (`§21`)

```text
NC-01  DP-04 remains ISSUED and unchanged                    TRUE
NC-02  Native Core remains exactly eleven                    TRUE — verified by listing
NC-03  No Native Core #12 created                            TRUE
NC-04  Planning does not create authority                    TRUE
NC-05  Planning does not self-authorize                      TRUE
NC-06  Delegation does not create authority                  TRUE
NC-07  Delegation does not transfer ultimate accountability   TRUE
NC-08  Delegation does not become Governance                 TRUE
NC-09  Performance does not create authority                 TRUE — E-56, Measurement ≠ authority
NC-10  Performance does not execute                          TRUE — "proposals only"
NC-11  Coordination does not become ownership                TRUE — PD-01 D3
NC-12  P12 Unified Operational State not constructed         TRUE
NC-13  DP-03 does not authorize P11 construction             TRUE
NC-14  DP-03 does not ratify E11                             TRUE
NC-15  DP-03 does not grant Founder authority                TRUE
NC-16  Claude did not fill Architect Choice                  TRUE — §16 untouched, incl. §16.5
NC-17  Recommendation never represented as decision          TRUE
NC-18  Decision never represented as authorization           TRUE
```

## 22. Issuance conditions (`§22`)

> **`DP-03` becomes `ISSUED` only when `§16`, `§17`, `§18` and `§19` are
> completed by the Architect.** A recommendation, an implementation, a commit, a
> verification, an identifier, a filename, an index entry or a commit message is
> **insufficient** — `IDENTIFIER ≠ ACTUAL DECISION BODY`.

## Status

> # `STATUS = DECISION-PENDING`
