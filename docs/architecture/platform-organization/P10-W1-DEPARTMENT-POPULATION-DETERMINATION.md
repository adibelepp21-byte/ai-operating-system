# P10-W1 — Department Population Determination

> **Authority:** `ACT-CC-P10-002` (Construction / Completion / Authority Resolution Gate)
> executing the Blueprint's own `P10-W1`, which asks *"department apa yang
> canonical; **platform function apa yang bukan department**; … capability apa
> yang department-owned."*
>
> **`ACT §14`:** every candidate below was tested by trying to prove it
> **unnecessary**. **`ACT §23`:** nothing is created for symmetry.

---

## 1. Result

```text
EXISTING DEPARTMENTS      2   Platform (ADR-0003) · Engineering (ADR-0008)
NEW DEPARTMENTS REQUIRED  0
FINAL REQUIRED POPULATION 2
```

**Zero is a conclusion from evidence, not an absence of effort.** The tests that
produced it are below, and each one had a way to come out differently.

## 2. The orphan test — `ACT §13.7`, `§19`

A new Department is required only if a **responsibility is orphaned**. Measured:

| Measure | Result | Source |
|---|---:|---|
| Capabilities with no owning Department | **0** | `organization_catalog` over the resident records |
| Agent Definitions with no owning Department | **0** | same |
| Capability record `## Owner` disagreeing with its Department nesting | **0** | two-sided cross-check |
| Execution-catalog artifacts unreferenced | 4 | `validate_execution_catalog` |

**The four are not orphaned Department responsibilities.** `Freeze §4` places
Runtime, Tool, Skill and Workflow as **owned centrally**, not by any Department.
Already classified `NOT-A-GAP` at `C4-N1`; re-tested here rather than inherited.

**One candidate orphan was investigated and disproved.**
`knowledge-consuming-agent` appears in `consumers/knowledge_agent.py:186` and is
owned by neither Department. **It is an `agent_instance` argument to
`TracedAction`, not an Agent Definition** — and `Freeze §4` makes Agent Instance
*"not owned — transient"*. `INV-2` does not reach it. **A name that looks like a
definition is not a definition.**

## 3. What is NOT a Department — the half of `P10-W1` that is easy to skip

### 3.1 `PD-01` … `PD-10` — platform functions, not Departments

**Rejected, on four independent grounds:**

| Ground | Source |
|---|---|
| The Blueprint says so directly | *"Claude tidak boleh menganggap PD-01–PD-10 otomatis menjadi departments"* |
| The Act says so | `ACT-CC-P10-002 §15`: *"Never perform PD-01 → Department …"* |
| The Founder Decision says so | `FD-P10-003 §5`: `CANONICAL DEPARTMENT = EXPLICITLY ESTABLISHED ORGANIZATIONAL UNIT` and **not** `PD = DEPARTMENT` |
| The authorization Act says so | `ACT-CC-P10-AUTHORIZATION §5`: PDs are the **source/definition** track; P10 is **operationalization** |

**`ADR-0029` remains open on the *semantics*** — whether Department and Platform
Division are one entity type — **and that question is not this one.** Even under
the reading most favourable to identity, no source establishes the *ten* as the
Department population, which is what `§15` bars.

### 3.2 Security Owner · Quality Authority · Governance Authority — roles, not Departments

**The strongest candidates for a new Department, and the evidence disproves
them.** `G-03`, corrected under `FAE-P10-FRONTIER-01`:

> *"A **Security Owner / Security Authority** role, defined in the **frozen**
> `PD-02` corpus … **What is absent: the binding.** No resident source states
> that `PD-08` **is** the Security Owner."*
> — and *"**Extends to `PD-09` Quality** — same pattern."*

**These are Platform-Division-layer authority roles whose *binding to a CPID* is
unmade.** They are not unowned Department responsibilities. Creating a Security
Department would **manufacture a second home for a responsibility that already
has a layer** — and would do it while the binding question is Founder-reserved.

**Disposition: NOT REQUIRED as Departments** · the binding remains a separate,
Founder-reserved item (`ACT §18`, `FD-P10-003 §10`).

### 3.3 The six Master Program names

`Volume VII §3` names Executive Office · Engineering · Finance · Research ·
Marketing · Content. **`Volume VII` is non-resident** (`ESC-C7-01`); the six are
known only through `G-09`'s citation. **`FD-P10-003 §4.1(3)` requires an
authoritative source that *explicitly establishes Department identity*, read as
a body.** A citation of a non-resident list is not that.

**Disposition: SOURCE-BLOCKED**, not rejected. If `Volume VII` is supplied, four
of the six become candidates immediately — **Engineering already exists**, and
**Executive Office is the one name shared with the PD roster**, which is `G-09`'s
overlap.

## 4. `ACT §22` — the reuse test, run before any creation

| Responsibility surface | Absorbable by an existing Department? |
|---|---|
| Governance artifact integrity | **Yes — Platform**, already owns it (`ADR-0003`) |
| Construction, change, verification, planning of AIOS itself | **Yes — Engineering**, already owns both Capabilities (`ADR-0008`) |
| Runtime · Tool · Skill · Workflow instances | **N/A — owned centrally** (`Freeze §4`), not Department-owned by design |
| Security / Quality / Governance authority | **N/A — Platform-Division-layer roles** (`§3.2`) |

**No responsibility was found that an existing Department cannot legitimately
absorb and that architecture supports as a new boundary.** `ACT §22`'s
three-part conjunction fails at its first clause, so no creation follows.

## 5. Authority Resolution Queue (`ACT §25`), classified per `ACT §6`

**`ACT §24` bars writing `AUTHORITY-BLOCKED` before this table exists.**

| ID | Required item | Missing authority | `§6` class | Sources inspected | Delegated path tested? | Decision package | Status |
|---|---|---|---|---|---|---|---|
| **AR-001** | Department/Platform-Division entity **semantics** | Architect determination | **E — ARCHITECT** | `ADR-0010`, `ADR-0011`, `FD-6`/`GDR-0020`, `E-64`, Domain Model terminology note, `Freeze §4` | **Yes** — `DEL-T4.4-CF-001 §3.2` exclusion 9 withholds Domain Model semantics; `Constitution §3.2` non-delegable | **`ADR-0029` — Proposed, decision-ready, 3 options, recommendation stated** | **PREPARED · NOT AUTHORIZED** |
| **AR-002** | `Security Owner` → CPID binding | Founder identity assertion | **D — FOUNDER** | `G-03`, `PD-02 A5 §12`, `AUTHORITY-FRONTIER-MATRIX` row `G-03` | **Yes** — matrix records decide=Founder, execute=Co-Founder; `FAE-P10-FRONTIER-01 §7` bars the binding | `G-03` records both options: bind, **or** record that the Owner is deliberately not `PD-08` | **READY FOR FOUNDER** |
| **AR-003** | `Quality Authority` → CPID binding | Founder identity assertion | **D — FOUNDER** | `G-03` *Extends to*, `A5:331` | Yes — same path as `AR-002` | Same shape as `AR-002` | **READY FOR FOUNDER** |
| **AR-004** | `Governance Authority` binding | Founder identity assertion | **D — FOUNDER** | `FD-P10-003 §10`, `ACT §18` | Yes — expressly withheld by `FD-P10-003 §10` unless stated otherwise, and it is not | Not prepared — `§10` withholds it explicitly rather than leaving it open | **FOUNDER-RESERVED** |
| **AR-005** | Department population beyond the two | The `Volume VII` body | **F — INDISPENSABLE EXTERNAL SOURCE** | `G-09`, `E-64`, `E-65`, `ESC-C7-01`, full resident search | **Yes** — four-surface recovery exhausted at `SG-01`; the six names exist only as citation | **Not preparable** — a decision cannot establish a population whose source is absent | **SOURCE-BLOCKED** |

**No queue item is class `G` (constitutionally prohibited) or `H` (unknown).**
**Every one has an identified holder and a stated next step**, which is what
`ACT §30`'s authority-exhaustion trace requires before any blockage is called
genuine.

## 6. What this determination does not do

It does not create a Department, rename a Platform Division, bind an owner role,
resolve `ADR-0029`, or treat the absence of a required Department as proof that
the population is final for all time. **`FD-P10-003 §6` requires source lineage
for every Department included *or excluded*** — `§3` is that lineage for the
exclusions, and `§2` is the evidence for the inclusions.

**If `Volume VII` is supplied, `AR-005` reopens this determination immediately.**
That is recorded so a later executor does not read `NEW DEPARTMENTS REQUIRED: 0`
as permanent.
