# Phase–PD Capability & Dependency Map

> **Required by:** `ACT-CC-AIOS-FULL-SYSTEM-RESOLUTION-AND-AUTONOMOUS-CONTINUATION-GATE-v1.0 §20`;
> candidate v2.0 `§22`. **Built 2026-09-09**, having been a named required
> artifact in the `P10–P13 Blueprint` and the `Gap Closure Roadmap` and never
> built.
>
> **The headline result of this map is negative, and it is the point.**

---

## 0. The six questions `§20` requires the map to answer

```text
Which PD provides the capability?
Which Phase consumes it?
Which organizational unit owns it?
Which runtime executes it?
Which workflow invokes it?
Which evidence verifies it?
```

**Answered below for every Phase. Most answers are `UNKNOWN`, and each
`UNKNOWN` is a measurement with a stated reason.**

## 1. The distinction this map exists to hold

```text
PD ≠ Phase      Phase ≠ PD      PD ≠ Department (see §4)
```

`ACT §3`: *"PD-01–PD-10 SHALL NOT be treated as Phase 10, Phase 14, or a
replacement for Phase 1–13."* `README.md:9` records the same:
**"PD-01–PD-10 are not Phase 14."**

## 2. THE CENTRAL FINDING — no resident source establishes a Phase→PD provider relation

**Searched:** the whole `platform-organization` corpus, all ten division
records, the `P10–P13 Blueprint`, and the `Gap Closure Roadmap`.

**Result: zero resident sources assign a Phase to a PD as its provider.**

**And the inference was already tested and rejected on the record.**
`ACT-CC-P6-071 §12`, recorded at `divisions/PD-04-knowledge-and-intelligence.md`
`§1.4`, tested the proposition —

> *"PD-03 says PD-04 owns Knowledge & Intelligence, therefore PD-04 defines
> Phase 6"*

— and **rejected** it: **PD-04 holds *Knowledge Authority, not phase
authority*.** The division record states why the rejection is kept:

> *"the same inference — **domain ownership read as programme authority** — is
> exactly the conflation this corpus is built to avoid."*

**This map therefore does not draw the correspondence its own name suggests**,
because the one time it was attempted, the attempt was refused by an Act.

## 3. The one evidenced join — `Freeze §5` layer 4

The tracks **do** meet, and the meeting point is structural rather than
nominal. `Freeze §5`, quoted verbatim:

| Layer | Purpose | Inputs | Dependencies |
|---|---|---|---|
| **4 Capability** | owned ability + composition | **Department ownership** | **Organization/Department** |

**The frozen layer model takes organizational-unit ownership as an *input* to
the Capability layer.** `Freeze §4`: Capability is *"a Department-owned unit of
ability"* whose ownership is *"exactly one Department (`INV-1`)."*

```text
PLATFORM ORGANIZATION  →  owns Capability  →  Freeze §5 layer 4  →  running system
```

**This is the whole of the evidenced Phase↔PD integration**, and it is an
*ownership* join, not a provider join.

## 4. Per-Phase map

`Provider PD` is left `UNKNOWN` throughout for the reason in `§2`.

| Phase | Name | Provider PD | Owner unit | Runtime | Workflow | Evidence of state |
|---|---|---|---|---|---|---|
| P1 | Core Architecture | `UNKNOWN` | `UNKNOWN` (`G-09`) | `native_core/` | — | Freeze, Blueprint |
| P2 | Runtime Foundation | `UNKNOWN` | `UNKNOWN` | `native_core/core/runtime/` | — | Blueprint §20/§21 |
| P3 | Execution Contracts | `UNKNOWN` | `UNKNOWN` | `runtime/contract.py`, `runtime/execution/contract.py` | — | `AIOS_PHASE_RECONCILIATION_v1.0.md:32` |
| P4 | AI Runtime | `UNKNOWN` | `UNKNOWN` | implemented | — | **`PHASE 4.6 CLOSED`** 2026-07-30; `S-9` supersedes the 0% |
| P5 | Intelligence Ecosystem | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | — | **`FD-P5-001`**; `S-13` supersedes the 0% |
| P6 | Knowledge Ecosystem | `UNKNOWN` — inference **rejected** (`§2`) | `UNKNOWN` | `native_core/core/knowledge/` | — | **`FD-P6-002`**; `S-14`; `GDR-0028` |
| P7 | Memory Ecosystem | `UNKNOWN` | `UNKNOWN` | `native_core/core/memory/` | — | **`FD-P7-003`**; `S-15` |
| P8 | Tool Ecosystem | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | — | **`FD-P8-002`**; `S-16` |
| **P9** | **Workflow Ecosystem** | `UNKNOWN` | `UNKNOWN` | `UNKNOWN` | **the Phase itself** | **`FD-P9-002`** 2026-09-03; `S-17` supersedes the 0%. **Maturity NOT ESTABLISHED** |
| **P10** | **Department Ecosystem** | n/a — construction target | **undetermined (`G-09`)** | — | — | **BLOCKED** — `Volume VII §1.2` requires P9 *matang* |
| P11 | Autonomous Organization | n/a | `UNKNOWN` | — | — | gated behind P10 |
| P12 | AI Operating System | n/a | `UNKNOWN` | — | — | gated `P4–P11` |
| P13 | Super Intelligence Ecosystem | n/a | `UNKNOWN` | — | — | gated `P12`; discovery-driven |

## 5. What this map changes

**It converts a suspicion into a measurement.** The Phase↔PD correspondence is
not merely undocumented — **it is unevidenced, and the one attempt to derive it
was rejected by an Act.** Any future construction that assumes a Phase is
"owned" by a PD is now contradicting a recorded rejection rather than filling a
blank.

**It also isolates what would unblock it.** Two things, both reserved:

1. **`ADR-0029`** — the organizational-unit population. Until it is decided, the
   `Owner unit` column cannot be filled for any row.
2. **The non-resident Volume 1 / Volume 2 corpora** (`ESC-C7-01`) — where
   provider declarations would live if they exist.

**Neither is delegable, and neither was manufactured.**

## 6. What this map does not do

It does not assign a PD to any Phase; does not treat domain ownership as
programme authority; does not treat a certification as maturity
(**`PHASE CERTIFIED ≠ PHASE MATURE`**, candidate v2.0 `§38`); and does not
alter the P10 verdict, which remains **BLOCKED** on `Volume VII §1.2`.
