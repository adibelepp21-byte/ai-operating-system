# Knowledge Architecture Discovery — Entity Proposal v1.0

**Status:** Design discussion only. No entity is created or implemented by this document.
**Version:** v1.0
**Authority:** Subordinate to the ratified Canonical Domain Model, which already defines Knowledge as an entity (§2) with ownership (§5) and lifecycle (§6) rules. This document proposes a possible field-level shape consistent with those rules and with real evidence already gathered in this repository — it does not introduce a new entity, and every field below is explicitly marked by how firmly it is grounded.
**Approved by:** Architect, Phase 7 — Knowledge Architecture Discovery.

---

## Marking Legend

- **Evidence-backed** — a real, already-built, tested mechanism in this repository demonstrates this field works.
- **Architecture-required** — the ratified Constitution or Domain Model mandates this field exist, even though no code implements it yet.
- **Future decision** — plausible and likely necessary, but no evidence or ratified text currently specifies its shape.
- **Unknown** — not enough evidence exists to say whether this is even needed.

---

## Proposed Fields

| Field | Marking | Rationale |
|---|---|---|
| `content` | **Evidence-backed** | `promotion.CandidatePackage.content` already carries exactly this — real, reviewed text, proven end-to-end through 6 real Human Review decisions. |
| `provenance` (source Trace/Memory chain) | **Evidence-backed** | `promotion.Provenance` (memory_id, trace_ids, agent_definition_name) is real, tested, and has been cross-referenced back to source Trace records in every phase this arc. |
| `evidence_summary` (confidence, occurrence, source type) | **Evidence-backed** | `promotion.EvidenceSummary` is real and already distinguishes tool/heuristic/model_generated sources with recovered confidence and occurrence data. |
| `review_history` (which Human Review decision(s) admitted this) | **Evidence-backed** | The real Human Review contract already produces exactly this data (`decision`, `reviewer_identity`, `rationale`, `decision_timestamp`) — Memory Governance's `review_state()` already derives it by cross-reference. |
| `owning_department` | **Architecture-required, currently unresolvable** | Domain Model §5 requires it; the Department Mapping Evidence Pass found no real Department data anywhere in this system. This field is required by the ratified model but has zero evidence-backed resolution mechanism today. |
| `version` | **Architecture-required** | Domain Model §6 requires Knowledge be "versioned." No implementation exists; no evidence yet of what a version identifier should look like for this system (semantic version, monotonic integer, and Trace-linked timestamp are all plausible, none evidenced). |
| `status` (e.g. active / deprecated / superseded) | **Architecture-required** | Domain Model §6 requires revision/supersession/non-casual-deletion. The *concept* is required; the concrete state set is not yet evidenced — see the Lifecycle Discovery document for alternatives. |
| `superseded_by` / `supersedes` (reference to another Knowledge entity) | **Future decision** | Plausible given the ratified "revised/superseded via review" language, but no real mechanism in this repository has ever exercised a supersession relationship — not evidenced, only inferred from governance text. |
| `admission_decision_reference` (link to the Trace record(s) that admitted it) | **Evidence-backed pattern, unbuilt field** | The pattern already exists for Human Review (`candidate_snapshot` embeds the reviewed content permanently in Trace) — the same pattern would plausibly extend to Knowledge admission, but no Knowledge-specific decision type exists yet. |
| `conflict_status` / `conflicting_with` | **Unknown** | `memory_governance.detect_conflicts()` proves *detection* is possible at the Memory layer, but zero organic conflicts have ever occurred in real data (4 independent scans, this arc), and no resolution contract exists. Whether Knowledge itself needs a conflict field, or whether conflicts are resolved entirely before admission, is unknown. |
| `retrieval_metadata` (e.g. what a retrieval system would index this by) | **Unknown** | The dormant `execution/knowledge/retrieval.py` prototype indexes real Documents by word, not by any Knowledge-entity-specific metadata. Whether a future Knowledge entity needs its own retrieval metadata, separate from full-text indexing of wherever it's stored, is unaddressed by any evidence gathered so far. |

## Ownership

Per Domain Model §5: collectively owned by the Organization, with a home Department. **Architecture-required, currently unresolvable** — same finding as the Concept Analysis document. No proposal here can responsibly assign a concrete ownership mechanism without Department resolution existing first.

## Lifecycle

See `KNOWLEDGE_LIFECYCLE_DISCOVERY_v1.0.md` for the full exploration. Summary here: Domain Model §6 mandates "versioned; revised/superseded via review; not casually deleted" as requirements, not a state machine — the concrete states remain a **Future decision**.

## Relationships

- **Knowledge ← admitted-from ← Memory/Promotion candidate**: **Evidence-backed as a pattern** (the exact provenance-chain technique already used for Human Review), unbuilt as a Knowledge-specific relationship.
- **Knowledge ← reviewed-by ← Human Review decision**: **Evidence-backed as a pattern**, same caveat.
- **Knowledge → consumed-by → Agent Instance (Trace)**: **Architecture-required** (Domain Model's Agent-Instance-consumes-Knowledge relationship, §4) but **zero real evidence** — `knowledge_consumed` is empty on all 540 real Trace records; this relationship has never been exercised even once.
- **Knowledge ↔ Knowledge (supersession/conflict)**: **Future decision / Unknown**, per above.

## Versioning Requirements

**Architecture-required** in principle (Domain Model §6), **Unknown** in mechanism. No real precedent exists anywhere in this codebase for versioning a governed, durable record — Trace is append-only (no versioning needed, every record stands alone); Human Review decisions are likewise append-only events, not versioned revisions of a single entity. Knowledge would be the first entity in this system requiring true multi-version-of-one-thing semantics.

## Admission Requirements

See `KNOWLEDGE_ADMISSION_BOUNDARY_v1.0.md` for full analysis. Summary: **Evidence-backed** that governed human review of a candidate works (6 real decisions, all types); **Unknown** whether admission to Knowledge specifically requires anything beyond what candidate review already captures, or a distinct, additional decision step.

## Deprecation Requirements

**Architecture-required** (Domain Model §6: "not casually deleted"), **Unknown** in mechanism. No code in this repository has ever deprecated anything. Whether deprecation should reuse the Human Review contract's `reject` semantics, or require a new decision type, is unaddressed by evidence.

## Conflict Requirements

**Unknown**, consistent with the Memory Governance Hardening findings this arc already produced: conflict *detection* is proven; conflict *resolution* has been explicitly out of scope for every phase so far, and zero organic conflicts have ever occurred to observe real resolution needs against.
