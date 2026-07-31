# AIOS Execution Layer — Evolution Protocol v1.0

**Status:** Frozen Baseline
**Version:** v1.0
**Authority:** Subordinate to the ratified Engineering Constitution's Decision-Making Process (§3) and Amendment Process (§16). This protocol does not grant any authority the Constitution does not already grant — it codifies, as a repeatable process, the discipline this Execution Layer's entire development history has already followed.
**Approved by:** Architect, Phase 6 — Architecture Baseline Formalization.
**Applies to:** Any change to a frozen module, contract, or invariant recorded in `AIOS_ARCHITECTURE_CONSTITUTION_v1.0.md`, `AIOS_DOMAIN_MODEL_v1.0.md`, or `AIOS_BOUNDARY_MAP_v1.0.md`.

---

## 1. Change Proposal

Every proposed change to the frozen baseline must be stated by the Architect as an explicit directive naming its exact scope — which module, which behavior, which boundary. A proposal that does not name an exact scope is not authorization to change anything, per the standing rule this arc has followed without exception: automated feedback (e.g. a stop-hook) may request or recommend a change; it may never itself constitute authorization.

## 2. Impact Assessment

Before any code is written, the affected surface must be identified by direct inspection — not assumption:

- Which modules import, or are imported by, the module under change (dependency graph).
- Whether the change touches an owned data structure, a mutation path, or a persistence path (per the Boundary Map).
- Whether any real, on-disk data (the Trace corpus, `docs/` governance artifacts) would be affected.

This mirrors the discipline already applied in the Architecture Evidence Freeze and Foundation Test Coverage Hardening phases: read the real code and real data before proposing or making any change.

## 3. Invariant Review

Every invariant listed in `AIOS_ARCHITECTURE_CONSTITUTION_v1.0.md` §4 must be checked against the proposed change. If the change would touch an invariant:

- The specific invariant must be named.
- The proposal must state explicitly whether the invariant is preserved, weakened, or replaced — never left ambiguous.
- Any weakening or replacement of an invariant requires Architect authorization at the same tier the invariant itself was established (Constitutional Tier concerns route through the ratified Constitution's own §3.1; this layer's own invariants require explicit Architect sign-off, as every phase in this arc's history has required).

## 4. Contract Review

Every public dataclass/function contract listed in the Boundary Map must be checked for compatibility:

- A change that adds an optional field with a safe default is a compatible evolution (precedent: Tier 2's `fingerprint`/`from_cache`/`verification_status` additions to `ToolExecution`, all additive and defaulted).
- A change that removes a field, changes a field's meaning, or narrows what a function accepts is a breaking change and requires the same authorization rigor as an invariant change.
- No contract listed in this baseline may be silently reinterpreted — if real data reveals a contract's original assumption was wrong (precedent: the fingerprint generational-absence finding during Evidence Chain Auditability Hardening), the fix must be reported as a correction with its evidence, not applied silently.

## 5. Migration Planning

For any change affecting how existing real data (the Trace corpus) is read or interpreted:

- `trace_schema.py`'s precedent is the model: old records are never rewritten; new code is written to tolerate every real generation already on disk, verified against the actual corpus, not just synthetic fixtures (`test_trace_schema.py::RealCorpusNormalizationTest`).
- A migration that would require rewriting or deleting any existing Trace record is forbidden outright — Trace's append-only invariant has no exception.

## 6. Implementation Authorization

No implementation proceeds without an explicit, scoped Architect authorization distinct from a change proposal's initial framing. This arc's history shows this distinction matters concretely: multiple phases separated "prepare/present" steps from "execute" steps, requiring a second, explicit confirmation before any write occurred (the Human Review pilot and every subsequent real decision followed this exact two-step pattern). The same discipline applies to code changes: investigation and design may proceed on a general directive; an actual code write requires the Architect to have seen and confirmed the specific change.

## 7. Regression Requirement

After any change:

- The full `execution/tests` and `tools/tests` suites must be run and their result reported in full (pass/fail/skip counts), never summarized as "passing" without the real numbers.
- Any new behavior must be covered by a new or updated test exercising real data or a real, disclosed controlled scenario — mocking is permitted only where no real scenario can be constructed (precedent: the two Orchestrator authorization-boundary tests, which explicitly disclose their controlled substitution because no real negative case exists in current data).
- The real Trace corpus's record count and content must be confirmed unchanged unless the change explicitly authorizes a new write, in which case the exact expected delta must be stated and verified.
- `docs/` must be confirmed unchanged unless the change is itself a documentation change explicitly authorized under this protocol.

## 8. Versioning Rule

- A compatible evolution (additive field, new module with no changed dependency direction) does not require a new baseline version — it is recorded in a future revision of the Status Registry as a delta against v1.0.
- A breaking change to any invariant, contract, or boundary recorded in this baseline requires a new major version of the affected document (e.g. `AIOS_BOUNDARY_MAP_v2.0.md`), produced through this same six-step protocol, with the prior version retained, never overwritten — consistent with Trace's own append-only philosophy applied to governance documents themselves.
- Every new baseline version must state, explicitly, which invariants, contracts, or boundaries changed from the prior version and why, with the same evidence rigor this document itself was produced under.
