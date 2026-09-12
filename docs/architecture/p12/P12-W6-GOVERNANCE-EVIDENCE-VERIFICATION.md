# P12-W6 — Governance Evidence Verification

**Scope item:** `§19` **GOVERNANCE**, specified by Blueprint `§26`.
**Status:** [E] measured. **1 of 9 elements established · 6 partial · 2 absent**,
across 385 resident governance instruments.
**Instrument:** `tools/p12_governance_evidence_verification.py`
**Conformance:** `tools/tests/test_p12_governance_evidence_verification.py` (17 tests).

---

## 1. What `§26` asks

[A] `§26`: governance evidence must establish — decision body, authority,
effective date, scope, status, provenance, affected surfaces, current state,
verification. It closes: *"Register entries are records of decisions, not
substitutes for decision authority."*

## 2. What was measured, stated precisely

[C] **Machine-readable establishment.** An instrument may establish its
authority in a paragraph and carry no `Authority:` label; this module does not
count it.

[C] That is deliberate, and it is the point. `§26` exists so governance evidence
can be **used**, and every resident consumer of it — the governance index, the
register, the derived views, the citation audit, this suite — reads labels. An
element stated only in prose is established for a human reader and **absent for
every consumer**.

[C] This is not an overclaim to be softened. It is the result, provided the
module says which of the two it measured — and it does, in its docstring and in
every emitted line.

[C] Counts, never booleans. An element that one instrument in 385 states is not
established by the corpus, and a boolean would report it identically to one that
all 385 state. The `ESTABLISHED` threshold is declared as data
(`ESTABLISHED_FRACTION = 0.5`) so it can be argued with rather than buried in a
comparison.

## 3. Result

| `§26` element | Status | Instruments carrying a label |
|---|---|---|
| decision body | PARTIAL | 93 / 385 |
| authority | PARTIAL | 107 / 385 |
| effective date | PARTIAL | 33 / 385 |
| scope | PARTIAL | 23 / 385 |
| status | PARTIAL | 123 / 385 |
| provenance | **ESTABLISHED** | 385 / 385 — structural |
| **affected surfaces** | **ABSENT** | 0 / 385 |
| current state | PARTIAL | 48 / 385 |
| **verification** | **ABSENT** | 0 / 385 |

[E] `{'elements': 9, 'established': 1, 'partial': 6, 'absent': 2}`

[E] The single established element is **provenance**, and it is established
structurally rather than by any instrument choosing to state it: every indexed
instrument carries its source path and content hash by construction.

## 4. The finding

[D] **Eight of `§26`'s nine elements are not reliably readable from governance
evidence.** The best-covered label reaches 123 of 385 instruments — under a
third. Two elements, **affected surfaces** and **verification**, have no
resident label at all: no instrument in the corpus states which surfaces a
decision affects, or that the decision was independently verified.

[D] `§26` closes by warning that register entries are *records* of decisions and
not substitutes for decision authority. The measured corpus sits on the far side
of a different gap: for most instruments, the record does not carry enough
structure for a consumer to tell what the decision governs.

## 5. The result does not depend on my choice of population

[C] The denominator is arguable, so both were measured. The obvious objection —
that 385 is diluted by documents which are not decision instruments — predicts
that a narrower population would score better.

[E] **It scores worse.** Over the 33 instruments under `docs/governance/acts/`:
decision body 5/33, authority 11/33, effective date 7/33, scope 1/33, status
6/33, current state 2/33, affected surfaces 0/33, verification 0/33.

[D] Founder acts state these elements in prose, at length and unambiguously, and
label them less often than the corpus average. The objection is falsified in the
direction opposite to the one it predicts, and a conformance control holds that
comparison so it cannot silently invert.

## 6. Falsifiability

[C] One established element of nine is a strong claim, so each status is proven
able to move: a label in every instrument reports `ESTABLISHED`; a label in a
minority reports `PARTIAL`; a label in none reports `ABSENT`; an element gains
coverage the moment a label is declared for it; an empty label value
(`Status:` with nothing after it) is not counted; a label appearing below the
header window is not counted. The same promotion is driven at runtime by
`p12_negative_control_verification`.

## 7. What this does not establish

[C] `PARTIAL` does not mean a decision lacks authority. It means the authority
is not readable as data from that instrument. **Nothing here is a claim that any
decision was improperly made.**

[C] No instrument was edited. Adding the missing labels to 385 resident
documents would be a corpus-wide rewrite of governance evidence, and adding
`affected surfaces` or `verification` fields to the record model is **P12-W3
construction**, not W6 verification. `GOVERNANCE` is truthfully classified here;
it is not closed.

---

**Suite state at this record:** `native_core` 801 (1 expected failure) ·
`consumers` 276 · `tools` 949 · total **2026**.
