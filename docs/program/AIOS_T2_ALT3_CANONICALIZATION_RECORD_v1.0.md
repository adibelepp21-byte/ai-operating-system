# T-2 / ALT-3 Canonicalization Record — C-1 · C-2 · C-3

**Executed under:** FOUNDER · `ACT-CC-F03-046` `DEC-F03-046 = OPTION A` · Moriarty · 21-08-2026
**Decision canonicalized:** `DEC-F03-045 = OPTION C — ALT-3` · *Workflow realizes Capability*
**Result:** **STATE A — CANONICALIZATION COMPLETE** · **no construction follows** (`§6`, `§18`)

---

## 1. Provenance (`§15`)

```text
Founder → DEC-F03-045 → OPTION C → ALT-3 (Workflow realizes Capability)
       → ACT-CC-F03-046 → Founder authorization → C-1 / C-2 / C-3 → Canonical Architecture
```

**[E] The implementation is not the source of this decision.** No implementation
exists for this relationship, and none was written. The architectural decision
preceded canonicalization, and canonicalization preceded — and did not become —
construction.

## 2. Pre-execution verification (`§7`)

| # | Check | Result |
|---|---|---|
| 1 | `DEC-F03-045 = OPTION C` | verified from the recorded decision |
| 2 | ALT-3 is the selected interpretation | verified |
| 3 | C-1, C-2, C-3 are exactly the targets | verified against `§3` |
| 4 | Skill half remains `[O]` | verified before and after |
| 5 | No additional relationship implied | verified — one edge added, content-anchored |
| 6 | Protected boundaries unchanged | Constitution and Finding Register hash-identical |
| 7 | Native Core boundaries remain **eleven** | verified |
| 8 | No construction authority inferred | none taken; zero source files touched |

## 3. Results

### C-1 — Canonical Domain Model §4 ✅

Added, adjacent to the existing Workflow relationships:

> - Workflow **realizes** Capability *(T-2 ALT-3; `DEC-F03-045`, canonicalized
>   under `DEC-F03-046` C-1. The converse does not hold: a Capability declares no
>   Workflow. **Capability ↔ Skill remains `[O]` reserved** — see Freeze §10.)*

`9ac46a8c…` → `fd6605da…`

### C-2 — Architecture Freeze ✅ (two edits, both within C-2)

**C-2a — §6 frozen *Observed* relationship table**, which is what makes the
relationship canonical rather than merely recorded:

> | Workflow realizes Capability | Workflow→Capability | Capability→Workflow (Blueprint §7 [E] admits only its Department and other Capabilities) | unchanged — Workflow central, Capability Dept-owned (INV-1) | governed |

Every column is grounded, none invented: *allowed direction* is ALT-3 itself;
*forbidden direction* restates Blueprint §7's **[E]** Capability
allowed-dependency list, which admits only its Department and other
Capabilities; *ownership* is **unchanged** and merely cites INV-1 and Freeze §4's
*"owned centrally"*; *lifecycle* is `governed`, which Freeze §4 already states
for both entities. **No ownership, lifecycle or authority semantics were
modified** (`§5`).

**C-2b — §10 partial discharge**, preserving the prior state rather than erasing
it (`§12`): the entry now reads `Capability↔**Skill**` and records verbatim that
it *"read `Capability↔Skill/Workflow` until `DEC-F03-046` C-2"*, that only the
Workflow half moved, and that **`Capability↔Skill/Workflow` is therefore *not*
fully ratified.**

`461740f7…` → `2bd97203…`

### C-3 — Native Core Blueprint §10, Workflow Package ✅

*Allowed dependencies* extended to *"realizes capability — **by reference
only**, carrying the Capability's key the way `AgentDefinitionRef` already
carries an Agent Definition's, so the package takes **no import of
`core/capability/`** and holds no Capability state."*

This satisfies `§3` C-3's prohibition on introducing Capability implementation
state or Capability imports into Workflow, and uses the minimum representation,
following the convention already resident in that package.

`f6653978…` → `74b89ba1…`

## 4. Files changed (`§14.5`) — exactly three

```
docs/architecture/domain-model/canonical-domain-model-v1.md
docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md
docs/architecture/AIOS_NATIVE_CORE_BLUEPRINT_v1.0.md
```

Nothing else. No source file, no test, no specification, no governance register.

## 5. Verification (`§10`)

| | Check | Result |
|---|---|---|
| **V-01** | `DEC-F03-045` remains OPTION C — ALT-3 | unchanged |
| **V-02** | Domain Model contains the authorized relationship | **PASS** — parsed, not grepped: 26 asserted relationships, the one added is exactly `('Workflow','realizes','Capability')` |
| **V-03** | Freeze reflects the Workflow half as frozen, Skill half `[O]` | **PASS** — §6 row added; §10 retains the Skill reservation |
| **V-04** | Blueprint synchronized | **PASS** |
| **V-05** | No Skill ratification | **PASS** — **zero** asserted Capability↔Skill edges; `skill_spec` untouched |
| **V-06** | Entity count | **12**, unchanged |
| **V-07** | Native Core boundary count | **11**, unchanged |
| **V-08** | No unauthorized construction | **0** source/test files changed |
| **V-09** | Protected state outside C-1…C-3 | Constitution `b73723f8…`, Finding Register `1eeb99a6…` — hash-identical |
| **V-10** | Regression | `native_core` **566 OK** (1 expected failure) · `tools` **20 OK** · `bounded_exception` **29 OK** |

## 6. Conformance-test discipline (`§11`) — **no test modified**

`test_capability_composition_is_not_modelled`
(`native_core/core/workflow/tests/test_workflow_conformance.py:535`) cites
**`workflow_spec §7/§14 [O]`** as its authority.

**[E] C-1…C-3 do not touch `workflow_spec`.** `§3` scopes this Act to the Domain
Model, the Freeze and the Blueprint. The authority the guard cites is therefore
**unchanged**, so under `§11` the test may **not** be updated. It was left
untouched and still passes. The eleven-boundary guard was likewise untouched.

### 6.1 The specification lag is deliberate, not drift

`workflow_spec §7` still reads *"realizes Capabilities **(Inferred, reserved)**"*
while the Freeze and Domain Model now carry the relationship as canonical.

**[E] This is the governance sequence working as designed**, not `§13` S-05.
`ACT-CC-F03-045 §10` orders *Canonicalization → **Specification
Synchronization** → Construction Authorization*, as separate stages. This Act
executed canonicalization only. **The three canonical artifacts agree with each
other**; the engineering specification trails by one stage and requires its own
authorization to synchronize. Recorded so the lag is not later mistaken for
inconsistency — or used as a pretext to edit the spec without authority.

## 7. Own-work disclosure

**[E] I mis-stated the size of the Domain Model relationship list.** The
`ACT-CC-F03-044` decision package and the `-045` commit message both describe it
as *"the ratified **24**-entry list."* Measured directly against `HEAD` before
this change, §4 held **25** top-level relationship bullets. The claim was wrong
by one in two committed artifacts.

**Not retroactively edited.** `§12` permits governance mutation only where
required to record this canonicalization, and states that *"no governance record
may be rewritten merely for consistency."* Correcting a past record is not
required by C-1…C-3, so the error is disclosed here and the prior documents are
left as written. The miscount had no bearing on any conclusion: the finding was
that the list contains **no** Capability↔Skill/Workflow edge, which held at 25
and holds now.

**A second self-check caught in flight:** my first V-05 probe grepped for
`capability.*skill` and reported one hit — its own new parenthetical, which says
*"Capability ↔ Skill remains `[O]` reserved."* A substring match on prose, not a
relationship. Replaced with a parser that extracts asserted `subject **verb**
object` triples; that check reports **zero** Capability↔Skill edges.

## 8. Terminal state (`§18`)

**STOP.** No construction follows. Not authorized and not begun: Workflow
construction · Capability construction · the Skill half of T-2 · INV-15 · T-12 ·
OB-01 · PD-02 activation. `DEC-AE04`, `DEC-REVOCATION`, `DEC-ADOPTION`, `RG-2`,
`RG-3` untouched.

**Next stage, requiring its own authorization:** specification synchronization of
`workflow_spec §7`/`§14` and the Workflow half of `capability_spec §12`/`§14` —
after which, and only then, the conformance guard in `§6` above comes into scope
and construction may be considered.
