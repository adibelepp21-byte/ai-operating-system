# `ACT-CC-P6-064-R1` — External Repository Research for Phase 6

**Act:** `ACT-CC-P6-064-R1` · **Mutation:** this record only
**Result:** **LIMITED REFERENCES FOUND** · **Strategy: REFERENCE-ONLY**
**Executor:** AIOS Co-Founder

> **REPOSITORY ADOPTED: NO · DEPENDENCY ADDED: NO · SOURCE CODE IMPORTED: NO ·
> LICENSE TRANSPLANTED: NO · PHASE 6 CONSTRUCTION: NO · T12-D-004 CONSTRUCTED: NO**

---

## 1. Executive result

**LIMITED REFERENCES FOUND.** Strong external work exists for **versioning,
immutability, provenance and validation** — and **none** implements T-12's
admission semantics. The gap is not a maturity gap in the ecosystem; it is a
category difference, and §7 below states why.

[A] **Reference value is real but cannot be consumed yet.** The two areas where an
external reference would help most — **admission implementation** and **storage**
— are exactly the two `GDR-0028` closes: *"no admission implementation"* and
**T12-D-004 DEFERRED**. This research is therefore input to the Phase 6
*authorization* decision, not to construction.

## 2. Method and its limits (§27.2, §9)

Discovery by public web search across §4 categories A–G; verification by public
documentation and one direct repository-page fetch (TerminusDB, for license).

[E] **Limit, stated plainly:** this session's GitHub access is scoped to
`adibelepp21-byte/ai-operating-system`. I did **not** clone, enumerate, or
inspect the source trees, test suites or dependency manifests of any external
repository, and I did not route around that scope. §8 asks for source inspection;
I could not perform it. **Every architectural claim below is therefore
`DOCUMENTED`, not `IMPLEMENTED`/`TESTED`** — the distinction §9 requires. Star
counts and README claims were not used as evidence of suitability.

## 3. Candidate inventory (§27.3)

| Repository | URL | License | Activity | Primary purpose | Evidence |
|---|---|---|---|---|---|
| **TerminusDB** | `github.com/terminusdb/terminusdb` | **Apache 2.0** *(verified on repo page)* | v12 released May 2026; 5,798 commits | Immutable RDF document-graph with git-like commits, branch, diff, merge, time-travel | DOCUMENTED |
| **Dolt** | `github.com/dolthub/dolt` | **Apache 2.0** | active; Go | Versioned SQL database — "Git for Data"; commits, branches, merges over tables | DOCUMENTED |
| **lakeFS** | `github.com/treeverse/lakeFS` | **Apache 2.0** | updated 2026-05-30 | Git-like branch/commit/merge/revert over S3-class object storage | DOCUMENTED |
| **OpenLineage** | `github.com/OpenLineage/OpenLineage` | Apache 2.0 *(stated; not repo-verified)* | LF AI & Data | Open **standard** for lineage metadata — run/job/dataset model | DOCUMENTED |
| **Marquez** | `github.com/MarquezProject/marquez` | Apache 2.0 *(stated; not repo-verified)* | LF AI & Data **graduated** | Reference implementation of OpenLineage; dataset/job provenance | DOCUMENTED |
| **Great Expectations** | `github.com/great-expectations/great_expectations` | Apache 2.0 (OSS core; GX Cloud commercial) | active | Validation suites and **Checkpoints** run before downstream consumption | DOCUMENTED |
| **Open Policy Agent** | `github.com/open-policy-agent/opa` | Apache 2.0 *(stated; not repo-verified)* | **CNCF graduated** | General policy engine; admission control (Gatekeeper) | DOCUMENTED |

[A] Excluded per §6: general knowledge-base products, RAG demos, and CRUD stores
whose relevance was only the word *"knowledge"*.

## 4. Top candidates ranked (§27.4)

| Rank | Repository | Primary fit | T-12 fit | Versioning | Provenance | Admission | Storage | Recommendation |
|---|---|---|---|---|---|---|---|---|
| 1 | **TerminusDB** | immutable versioned knowledge graph | **PARTIAL** | STRONG | PARTIAL (commit authorship) | **NONE** | own layer store | **A — high-value architectural reference** |
| 2 | **Dolt** | versioned structured data | PARTIAL | STRONG | PARTIAL | **NONE** | own | **B — pattern reference** |
| 3 | **Marquez / OpenLineage** | provenance model | PARTIAL | WEAK | **STRONG** | NONE | n/a | **B — pattern reference** |
| 4 | **Great Expectations** | pre-admission validation | PARTIAL | NONE | WEAK | **PARTIAL** (automated only) | n/a | **B — pattern reference** |
| 5 | **lakeFS** | versioned object storage | WEAK | STRONG | WEAK | NONE | **STRONG** | **D — research only** *(see §6)* |
| 6 | **Open Policy Agent** | policy gate | **WEAK** | NONE | NONE | PARTIAL (**machine** decision) | n/a | **D — research only** |

[A] No candidate is classified **C — implementation candidate**. §21 requires
demonstrated compatibility with AIOS architecture and T-12; none demonstrates it,
and none was inspected at source level.

## 5. T-12 compatibility (§27.5)

| T-12 constraint | TerminusDB | Dolt | Marquez | Great Expectations | OPA |
|---|---|---|---|---|---|
| Candidate → Active → Superseded, no intermediate | NONE | NONE | NONE | NONE | NONE |
| **Memory as sole candidate source** | NONE | NONE | NONE | NONE | NONE |
| **Human-authorized promotion** | **NONE** *(verified: no governance approval workflow)* | NONE | NONE | NONE | NONE — machine policy |
| **Exactly one affirmative gate** | NONE | NONE | NONE | PARTIAL | PARTIAL |
| Reject absolute | NONE | NONE | NONE | PARTIAL | PARTIAL |
| New version, never in-place | **STRONG** | **STRONG** | NONE | NONE | NONE |
| Prior version Superseded **and retained** | **STRONG** | **STRONG** | NONE | NONE | NONE |
| Admitted version immutable | **STRONG** | STRONG | NONE | NONE | NONE |
| Fail closed | UNKNOWN | UNKNOWN | UNKNOWN | PARTIAL | PARTIAL |
| **Governance → Knowledge direction** | NONE | NONE | NONE | NONE | NONE |

[E] TerminusDB's *"human approval / governance gate"* was **checked, not
assumed**: the repository page describes schema constraints for data quality and
**no approval workflow**. That is the single most important negative finding here.

## 6. T12-D-004 guard (§12, §27.6)

```
T12-D-004 STATUS:          DEFERRED / NOT AUTHORIZED
EXTERNAL STORAGE RESEARCH: REFERENCE ONLY
STORAGE CONSTRUCTION:      NOT PERFORMED
```

[A] **lakeFS is deliberately ranked 5th despite being the strongest storage
architecture found.** Ranking it higher would invite reading storage capability
as storage authorization. `GDR-0028` defers T12-D-004 with *"no selection,
provisioning, migration, or persistence architecture"* — an excellent external
storage design changes none of that. Classified **STORAGE DESIGN REFERENCE**.

## 7. Gaps — what no external repository solves (§23)

[A] External projects supply **mechanisms**. T-12 specifies **governance
semantics**. They are different kinds of thing, and the mismatch is structural:

| T-12 requires | Why external systems do not provide it |
|---|---|
| Human-authorized promotion as the **sole** gate | Versioned stores are built for *machine* throughput; a mandatory human gate is the property they are designed to avoid |
| **Memory** as sole candidate source | An AIOS-specific subsystem relation; no external analogue exists |
| **Governance → Knowledge**, one direction only | External stores accept writes from any authorized client |
| Absolute reject, fail closed on **absence** | Data tools generally fail *open* or quarantine and continue |
| Knowledge holds **no authority of its own** | An organizational-governance constraint, not a storage feature |

[A] **The conclusion worth stating.** The versioning half of Phase 6 is
well-served by prior art; the **admission** half is where AIOS is doing something
the ecosystem does not do. That is not a weakness in the design — it is the part
that carries the governance model, and it is precisely the part `GDR-0028`
ratified and left unimplemented.

## 8. Best references (§27.7)

```
BEST ARCHITECTURAL REFERENCE:          TerminusDB — immutable append-only layers,
                                       commit graph, time-travel over a knowledge graph
BEST VERSIONING / PROVENANCE REFERENCE: TerminusDB (versioning) · Marquez/OpenLineage (lineage model)
BEST ADMISSION / GOVERNANCE REFERENCE:  NONE ADEQUATE — Great Expectations for
                                       pre-admission validation shape only; no
                                       human-authorization semantics anywhere
BEST STORAGE REFERENCE:                 lakeFS — design reference only; T12-D-004 remains DEFERRED
```

## 9. Recommended strategy (§24, §27.8)

**REFERENCE-ONLY.**

[A] Grounds: no candidate was source-verified; none carries T-12's admission
semantics; the areas needing help most are unauthorized or deferred; and AIOS's
core (`native_core`) is deliberately stdlib-only with a Tool boundary as its sole
external-integration point (INV-12). Adopting any of these as a dependency would
collide with that boundary before it collided with anything else.

[R] If Phase 6 is authorized, the useful consumption is **conceptual**:
TerminusDB's append-only-layer model for immutable supersession, and
OpenLineage's run/job/dataset shape for provenance vocabulary — as *design
input*, implemented natively against T-12.

## 10. Governance boundary (§25, §27.10)

**Establishes:** what prior art exists, its licences as publicly stated, and —
evidentially — that **no external system implements T-12 admission**.
**Does not establish:** any architectural decision, dependency decision, or
construction authorization. **`RESEARCH FINDING ≠ ARCHITECTURAL DECISION ≠
DEPENDENCY DECISION ≠ CONSTRUCTION AUTHORIZATION.`**

[D] Whether any of this is considered in `ACT-CC-P6-064` is the Founder's call.
[R] It is relevant to exactly one clause of that authorization: whether Phase 6
builds admission natively (the evidence says it must) and how T12-D-004 is
treated.

## 11. Repository state (§20, §27.11)

```
AIOS TREE:              CLEAN — 0 modified
EXTERNAL REPOSITORIES:  NOT ADDED
PROTECTED STATE:        UNTOUCHED — 13
native_core · consumers · tools · C1–C4 · T-12 · T12-D-004 · Phase 5 · Roadmap · P7 — unchanged
Created:                this record only
```

**DEVIATIONS: NONE.**
