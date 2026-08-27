# `ACT-CC-P6-065` — Graphify Architecture Verification

**Act:** `ACT-CC-P6-065` · **Mutation:** this record only · **Construction: NONE**
**Result:** **Graphify is NOT part of canonical AIOS Knowledge architecture**
**Executor:** AIOS Co-Founder

> **CONSTRUCTION: NONE · ARCHITECTURE MODIFICATION: NONE · GRAPHIFY DEPENDENCY
> ADDED: NO · GRAPHIFY SOURCE IMPORTED: NO · T-12 MODIFIED: NO · T12-D-004
> MODIFIED: NO · PROTECTED STATE: UNTOUCHED**

---

## 1. Executive result (§29.1)

```
GRAPHIFY STATUS:              D — NON-CANONICAL EXTERNAL TOOL
                              (§19: NO — TOOLING ONLY)
AIOS KNOWLEDGE IMPLEMENTATION: C — native, independent of Graphify
                              (and NOT a graph model — see §6)
PHASE 6 IMPACT:               NO IMPACT
CONSTRUCTION:                 NONE
```

## 2. Governance freshness — register first (§4, §5)

[E] **Governance Decision Register searched first: `graphify` returns ZERO hits.**
Absent from every governance record, including `GDR-0028`, the current final
entry. No instrument authorizes, requires, or references it.

[A] Freshness applied to the **conclusion**, not merely to a replaced source: I
searched for any later instrument that could make Graphify canonical and found
none. No source conflict exists.

## 3. The one canonical mention — and it disclaims dependency [E]

Repo-wide, `graphify` appears in **two** files. Content-anchored per §14:

[E] **`docs/architecture/history/AIOS_DECISION_REVIEW_METHOD_VALIDATION_PLAN_v1.0.md`
§3 "Corpus-Independence Requirements"**, verbatim:

> The validation process must be usable on **any** repository. Therefore it must
> **not depend on**:
> - **Graphify** — **no dependency on any specific tooling, parser, or graph
>   representation.** The methodology operates on *observed repository content*,
>   however observed; **the observation mechanism is out of scope and must not be
>   assumed.**
> - **AIOS** — no dependency on AIOS canon, entities, invariants, or documents.

[A] **The sole canonical mention of Graphify in the entire corpus is an explicit
statement of non-dependency**, listing it beside AIOS itself as something the
methodology must work without. Canon treats it as an **external observation
mechanism**, out of scope by design. The second hit is unrelated prose in a DSPy
validation record.

## 4. Dependency finding (§14, §15, §29.6)

```
Graphify runtime dependency:        NONE
Graphify build dependency:          NONE
Graphify test dependency:           NONE
Graphify dependency-manifest entry: NONE — the repository has no manifest at all
Graphify documentation reference:   1 (a non-dependency statement, §3)
```

[E] **AST-level import scan** across `native_core/`, `tools/`, `consumers/`:
**0 imports.** Not a textual scan — `ast.Import` / `ast.ImportFrom` nodes, as §14
requires. [E] No `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile` or
lockfile exists anywhere in AIOS: the core is stdlib-only by construction
(INV-12), so there is no manifest for Graphify to be absent from.

**Classification: NO DEPENDENCY.**

## 5. Five-source inventory (§2, §29.3) — they are **not one project** [E]

| # | Identity | Package | License | Language | Finding |
|---|---|---|---|---|---|
| 1 | `Graphify-Labs/graphify` v8 | PyPI `graphifyy` | LICENSE = **MIT**; `license = {file}` | Python (256) | — |
| 2 | `rhanka/graphify` main | npm **`@sentropic/graphify`** | MIT | **TypeScript (635)** | different project entirely |
| 3 | `safishamsi/graphify` v2 | PyPI `graphifyy` | declares MIT — **no LICENSE file shipped** | Python (60) | *"A Claude Code skill"* |
| 4 | `safishamsi/graphify` v4 | PyPI `graphifyy` | MIT | Python (134) | — |
| 5 | `Graphify-Labs/graphify` v8 | PyPI `graphifyy` | **`license = "Apache-2.0"`** | Python (337) | — |

[E] **Three distinct GitHub owners.** *"Graphify"* is not one project, so there is
no single artifact that could hold canonical status even in principle.

[E] **Two findings worth flagging, both verified rather than inferred:**
1. **License divergence.** src1 and src5 both present as `Graphify-Labs/graphify`
   v8 with the same README, yet src1 resolves to **MIT** and src5 declares
   **Apache-2.0**. Same claimed identity, different licence.
2. **src3 declares MIT in `pyproject.toml` but ships no `LICENSE` file**, while
   publishing to PyPI.

[A] Neither is a defect in AIOS; both are reasons any future adoption question
would need licence review before, not after.

## 6. Graph semantics — the determinative finding (§7, §17, §29.8)

[E] **AIOS Knowledge is not a graph model.** From `models.py` and `retrieval.py`:

- identity is **`(knowledge_item_key, version_sequence)`** — a key-and-sequence pair
- `CanonicalStatus` — *"exactly two designations — no third"*
- retrieval surface is **`active(key)` · `version(identity)` · `history(key)`**
- **no node, edge, relation, ontology or traversal concept anywhere**

**§17 classification: NON-GRAPH KNOWLEDGE MODEL.**

[A] This settles §7's five questions cleanly:

| | Question | Answer |
|---|---|---|
| A | Does AIOS use graph-based Knowledge semantics? | **No** — it is a versioned item store |
| B | Does AIOS use the Graphify software? | **No** — 0 imports |
| C | Does canonical architecture require Graphify? | **No** — canon disclaims it (§3) |
| D | Does implementation depend on Graphify? | **No** |
| E | Could the semantics be satisfied without Graphify? | **They already are** — 50 tests green |

[A] **§18's option set assumes a graph.** The nearest correct answer is **C —
native implementation independent of Graphify**, with the qualifier that it is
not a *Knowledge Graph* implementation. AIOS and Graphify are not competing
implementations of one thing; they are **different categories of artifact** — a
governed versioned item store versus a corpus-to-graph extraction tool.

## 7. T-12 compatibility (§12, §29.9)

| T-12 rule | AIOS current implementation | Graphify (all five) | Result |
|---|---|---|---|
| Candidate → Active → Superseded | **YES** — evidenced | NO | AIOS only |
| Memory sole candidate source | **YES** | NO | AIOS only |
| Human-authorized promotion | **YES** | **NO — 0 files across all five** | AIOS only |
| Exactly one affirmative gate | **YES** | **NO — 0 files** | AIOS only |
| Reject absolute | **YES** | NO | AIOS only |
| New version, never in-place | **YES** | PARTIAL (src2: 20 files touching immutability) | AIOS only |
| Prior retained and superseded | **YES** | PARTIAL | AIOS only |
| Admitted version immutable | **YES** | PARTIAL | AIOS only |
| Fail closed | **YES** | UNKNOWN | AIOS only |
| Governance → Knowledge | **YES** | NO | AIOS only |

[E] **A governance admission gate is absent from all five archives** — searched
for `human approval`, `promotion_authorized`, `admission gate`, `governance
gate`, `human-authorized`: **zero files in every source.** This independently
reproduces `ACT-CC-P6-064-R1`'s finding by direct source inspection rather than
by documentation.

## 8. Architecture relationship (§20)

```
AIOS T-12  →  native_core/core/knowledge/  →  versioned, admission-gated item store
                                              (NOT a graph)

Graphify   →  external corpus-to-graph extraction tooling
           →  canon names it once, to disclaim dependency on it
```

## 9. Phase 6 impact (§21, §29.10)

**NO IMPACT.**

[A] Phase 6's target is a *"versioned, admission-gated Knowledge store"* — **not**
a knowledge graph. `ACT-CC-P6-064` established that target is already built and
green; re-verified here: **knowledge 50 OK · native_core 676 OK**. Graphify is
not required to satisfy it, and its absence is **not a Phase 6 defect** (§22).

## 10. T12-D-004 (§24, §29.11)

```
T12-D-004:           UNCHANGED — DEFERRED
STORAGE CONSTRUCTION: NOT AUTHORIZED UNDER THIS ACT
GRAPHIFY STORAGE:     REFERENCE ONLY
```

[A] Several archives persist graphs. **Persistence capability is not storage
authorization** — the same guard applied to lakeFS in `ACT-CC-P6-064-R1`.

## 11. Governance recommendation (§29.13)

```
FOUNDER DECISION REQUIRED: NO
```

[A] Nothing here needs a decision. Graphify is not canonical, not depended upon,
not required, and its absence blocks nothing. [R] If it is ever wanted, it would
enter as **tooling** — the role canon already assigns it — and would need its own
authorization, licence review (§5), and a choice among three unrelated projects.

## 12. Repository integrity (§29.14)

```
Created: this record only     Modified: 0      Deleted: 0
Protected packages modified: NONE (13 untouched)
Graphify dependency added: NO · source imported: NO
T-12 modified: NO · T12-D-004 modified: NO
knowledge 50 OK · native_core 676 OK (expected failures = 1)
```

[E] The five archives were extracted to the session scratchpad **outside the
repository** and were neither added to the tree nor referenced by it.

**DEVIATIONS: NONE.**
