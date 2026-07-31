# Knowledge Architecture Discovery — Concept Analysis v1.0

**Status:** Design discussion only. No implementation authorized by this document.
**Version:** v1.0
**Authority:** Subordinate to the ratified Engineering Constitution and Canonical Domain Model. This document does not define or redefine the Knowledge entity — it analyzes what the ratified definition means in practice, using real repository evidence, and identifies what remains undecided.
**Approved by:** Architect, Phase 7 — Knowledge Architecture Discovery.

---

## 1. What Is Knowledge?

The Canonical Domain Model defines Knowledge as: *"Curated, canonical, reviewed, versioned understanding. Durable; not casually deleted."* (§2, Entity Definitions). Ownership: *"Collectively owned by the Organization; each item has a home Department"* (§5). Lifecycle: *"Versioned; revised/superseded via review; not casually deleted — audit trail matters"* (§6). Invariant 8: *"Memory is promoted to Knowledge only through governed review — never automatically."*

Read together, four properties are non-negotiable, per the ratified model, not this document's invention:

1. Knowledge is the *result* of a governed review process, never a direct capture of raw observation.
2. Knowledge is durable — its removal is a governed act (deprecation/supersession), never a silent deletion.
3. Knowledge is versioned, with an audit trail across revisions.
4. Knowledge has an owning Department, even though the Organization holds it collectively.

## 2. What Is Not Knowledge

- **A raw observation.** An Agent Instance encountering something is Memory or Trace evidence, not Knowledge, until it passes governed review (invariant 8).
- **A retrieval result.** Finding a passage of text that answers a query is not the same as that passage being curated, reviewed understanding — it is, at most, a pointer to where understanding might already live in an existing governance document.
- **A cached fact.** Something remembered because it was observed once, or many times, is Memory — provisional by definition, with a retention window, not Knowledge's durability.
- **A human's individual judgment about one candidate.** A single `approve`/`reject`/`edit` decision (the real Human Review contract, `review_decision.py`) is a governance *event*, not itself a Knowledge entity — it is evidence that could, in a not-yet-built admission step, justify creating or updating one.

## 3. Trace vs. Memory vs. Evidence vs. Document vs. Retrieval Result vs. Knowledge Entity

| Concept | What it is, per real repository evidence | Persistence | Mutability | Governed? |
|---|---|---|---|---|
| **Trace** | The immutable, append-only record of one real Agent Instance action (`trace.py`). 540 real records exist. | Permanent, on-disk `.jsonl` | Never mutated | Not itself governed content — it is the record *of* governance and non-governance actions alike |
| **Evidence** | A single finding inside a Trace record's `outputs.evidence` list — e.g. `{"source": "tool", "kind": "cross_reference_check", "resolved": false, "detail": "..."}`. Real, structured, but scoped to one Trace record. | Persists only as part of its parent Trace record | Immutable (part of an immutable record) | No — raw output of a Skill/Tool, not reviewed |
| **Memory** | A derived, deduplicated view over many Evidence entries sharing `(observation_kind, content)`, computed fresh on every call (`memory/extractor.py`). 370 real records exist, with no stable identity across recomputation. | None by default | Not applicable — recomputed, never stored as a governed record | No — explicitly provisional |
| **Document** | A real, on-disk governance artifact under `docs/` (e.g. an ADR, a Skill/Tool/Workflow/Runtime definition, the Constitution itself). | Permanent, version-controlled | Mutated only through the ratified Decision-Making Process | Yes — but as *governance text*, not as the Knowledge entity the Domain Model defines |
| **Retrieval result** | The output of the dormant `execution/knowledge/retrieval.py` prototype — a `RetrievalHit`/`EvidenceReference` pointing at a line in a real Document. Real, tested, but never consumed by any Trace (`knowledge_consumed` is empty on all 540 real records). | None — computed on demand | Not applicable | No — explicitly self-disclaimed as creating "no Knowledge entity, storage convention, or promotion pipeline" |
| **Knowledge entity** | Does not exist in this repository today. Would be the *output* of a governed review step applied to a Memory or Promotion candidate, per invariant 8. | Would need to be durable, per the ratified definition — no mechanism exists yet | Would be versioned, revised via review — no mechanism exists yet | Yes, by definition — the only one of these six concepts that is inherently governed |

## 4. Ownership and Authority

Per the ratified Domain Model (§5), Knowledge is collectively owned by the Organization with each item having a home Department. This repository's real, current state cannot resolve that ownership: the **Department Mapping Evidence Pass** (a prior phase) established that no Department field exists anywhere in Trace or the Execution Layer, and `promotion.py`'s `department_status` is honestly `"unavailable"` on every real candidate, never guessed. A Knowledge entity's Department ownership therefore has no evidence-backed resolution mechanism today — this is a real, open gap, not a design choice available to close in this phase.

Authority to *admit* something into Knowledge is not addressed by any ratified document beyond invariant 8's "governed review, never automatically." What "governed review" concretely requires for Knowledge specifically — as distinct from the Human Review contract already built for Memory-candidate review — is exactly what Tasks 2 through 4 of this discovery phase exist to explore, not to decide.
