# P13-018 — P13 Construction Authority Gate (prepared for the Founder)

| Field | Value |
|---|---|
| **Prepared under** | `FDR-2 §8` (*"PREPARE CONSTRUCTION AUTHORIZATION GATE"*), `§9` (required contents), `D10` |
| **Date** | 2026-09-24 |
| **Canonical basis** | `docs/architecture/p13/AIOS_P13_CANONICAL_BLUEPRINT_v1.0.md` |
| **Status** | **PREPARED, NOT DECIDED.** P13 construction is **not authorized** until the Founder records a decision on §2 |
| **Decided** | 2026-09-24 — **APPROVED WITH BOUNDED INITIAL AUTHORITY**: `D-1` APPROVE · `D-2b` · `D-3` YES. Decision: `docs/governance/acts/P13-018-FOUNDER-CONSTRUCTION-AUTHORITY-GATE-DECISION.md` (Decision Register `§22`). The status row above is this surface as prepared |

## 1. FDR-2 §9's twenty required contents

| # | Required content | Where | State |
|---|---|---|---|
| 1 | canonical P13 definition | Blueprint §1 (`D01`, verbatim) | ✔ canonical |
| 2 | canonical mission | Blueprint §1 (`D03`) | ✔ canonical |
| 3 | architecture | Blueprint §3.1–§3.3 | ✔ prepared |
| 4 | component boundaries | Blueprint §3.2 (eight components, one per C-01 link, each with owns / consumes / emits) | ✔ prepared |
| 5 | Native Core placement | Blueprint §3.1: tools layer, **NATIVE CORE = 11**, no `native_core/` change | ✔ per `D09` |
| 6 | integration map | Blueprint §4. Each relationship carries the requirement that proves it; Memory → P13 is the one new relationship | ✔ prepared · **one conditional (§2 D-3)** |
| 7 | authority model | Blueprint §5.1: envelopes are the only source of *may execute* | ✔ prepared |
| 8 | autonomy contract | Blueprint §2 C-02, §5 | ✔ prepared · **initial envelope open (§2 D-2)** |
| 9 | execution boundaries | Blueprint §3.2 (bounded cycle), §5.2, §10 | ✔ prepared |
| 10 | refusal behaviour | Blueprint §5.2–§5.3 (typed, durable, recorded) | ✔ prepared |
| 11 | escalation behaviour | Blueprint §5.3 (existing escalation register; human response only) | ✔ prepared |
| 12 | evidence model | Blueprint §6 (P12 `§29`'s twelve elements, mapped field by field) | ✔ prepared |
| 13 | trace model | Blueprint §6 (P13-owned live Trace store, append-only) | ✔ prepared |
| 14 | verification contract | Blueprint §7 (live acceptance and negative controls per criterion, plus non-regression) | ✔ prepared |
| 15 | E13-01 … E13-07 | Blueprint §2 C-05, §7, §9 | ✔ canonical + measurable |
| 16 | residual frontier contract | Blueprint §2 C-06; `P13-017` (`0017`, `0018` as frontier); `P13-015` (Q39, Q91 frontier; Q23 unknown) | ✔ prepared |
| 17 | construction scope | Blueprint §10 IN | ✔ prepared |
| 18 | prohibited construction scope | Blueprint §10 OUT | ✔ prepared |
| 19 | certification requirements | Blueprint §11 | ✔ prepared (the certification decision itself is separate) |
| 20 | rollback / recovery conditions | Blueprint §11 | ✔ prepared |

**Pre-construction gates (`D09`):** PRE-01 registered (Register `§21`) ·
PRE-02 in Blueprint §1–§2 · PRE-03 in §5 · PRE-04 in §7 · PRE-05 in §4 ·
PRE-06 in §3 and §10. **All six are met on paper.** No P13 code exists.

## 2. What the Founder decides at this gate

**D-1 — Construction authorization.** Whether to authorize construction of
exactly Blueprint §10 IN, with §10 OUT prohibited. Verification follows §7,
and certification is a later, separate decision.

**D-2 — Initial P13 action envelope** (Blueprint §5.1). Without one, a built
P13 can only escalate, and **E13-05 cannot be verified live**, because live
verification of *"execute authorized action"* needs an authorized action.

| Option | Envelope | Consequence |
|---|---|---|
| **D-2a** | none | P13 is advisory in practice. E13-05 is only fixture-verifiable, so the exit contract cannot be met as written |
| **D-2b** | **`P13-ENV-01`, evidence-only**: run the resident read-only verifiers (self-model, integrity, relationship map, reconciliation checker); write P13 records to `docs/operations/p13/`; raise escalations. **Nothing else** | E13-05 is verifiable live, with no action that changes code, governance, delegations, knowledge or certified evidence |
| **D-2c** | D-2b + execution within existing **W4 delegation grants** (`FD-P11-001`), by grant scope | P13 can perform organizational work already delegated. Larger surface; W4 scopes govern it |

**[REC] D-2b, issued by the Founder in the construction authorization
itself.** The CEO could issue it under `A10`, but the CEO would then be both
building P13 and granting its first authority. Having the Founder issue it
removes any question of authority self-expansion (`R06`).

**D-3 — Knowledge criterion** (Blueprint §4, the conditional row). Whether
E13-02 includes `FD-P12-002`'s admitted corpus-health criteria. If yes,
Knowledge → P13 (read-only) becomes a required relationship. If no, E13-02 uses
only criteria from resident instruments: certified-evidence integrity and the
E13 contract itself.
**[REC] yes.** It is the one ratified, machine-readable evaluation criterion
AIOS already holds, and reading it admits nothing.

## 3. What stays reserved regardless

`AD-P13-001` (not needed) · `AD-P13-002` (not touched) · `GAP-0009` (not
needed) · `GAP-0006` (not needed) · `FD-2` (not relied on) · any Native Core
change · certification.

## 4. Decision form (for the Founder; Claude does not fill it)

```text
D-1  Construction of Blueprint §10 IN          [ ] AUTHORIZE   [ ] AMEND: ____   [ ] WITHHOLD
D-2  Initial action envelope                   [ ] D-2a  [ ] D-2b  [ ] D-2c  [ ] other: ____
D-3  FD-P12-002 criteria in E13-02             [ ] YES   [ ] NO
     Blueprint §3–§11 architecture             [ ] ACCEPT  [ ] AMEND: ____
```
