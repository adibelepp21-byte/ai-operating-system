"""Knowledge boundary conformance tests (Native Core Blueprint §27).

Baseline 04A — Knowledge Conformance. A **verification** baseline: it verifies
the Knowledge boundary's existing architectural structure and adds no behavior.

Tests assert the invariants knowledge_spec and the Roadmap §9.5 name for this
boundary:

  - **INV-7** — Knowledge is durable and versioned; a change produces a new
    version and prior versions are preserved, never overwritten or deleted.
  - **INV-8** — Knowledge is entered **only** through governed promotion. No
    public admission path exists that does not require a Governance
    authorization surface.
  - **INV-12** — Tool is the only entity permitted an external dependency, so
    this boundary holds none. Its cross-boundary imports are restricted to the
    three knowledge_spec §7 permits: Memory (candidate source), Governance
    (promotion authority), and an Infrastructure storage facility.
  - **OQ-2** — Knowledge storage is a facility, not an independent traced
    actor; it authors no Trace.
  - **PR-3 / PR-4** — Knowledge decides nothing (Governance decides) and fails
    closed on the absence of authorization.

Verification is **structural wherever possible** — AST inspection, dataclass
inspection, public-API inspection, signature inspection — in preference to
runtime simulation, per the Baseline 04A authorization.

**No source file in this boundary is modified by this baseline.** Any
requirement or defect discovered during verification is reported as evidence in
the Implementation Report, never repaired here.

Standard-library `unittest` only. No external dependency (INV-12).
"""
