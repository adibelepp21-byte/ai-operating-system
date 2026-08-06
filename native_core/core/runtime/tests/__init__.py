"""Runtime boundary conformance tests (Native Core Blueprint §27).

Baseline 04B — Runtime Conformance. A **verification** baseline: it verifies the
Runtime boundary's existing architectural structure and adds no behavior.

Tests assert the invariants runtime_spec and Roadmap §9.10 name for this
boundary:

  - **INV-3** — Runtime hosts Agent Instances. Hosting is expressed through the
    inverted `ExecutionConsumer` contract, so no `Runtime → Agent` dependency
    exists and no cycle can arise.
  - **INV-4** — every Agent-Instance action produces exactly one Trace. Runtime
    authors none of its own (OQ-2): it is audited *through* the action.
  - **INV-12** — Tool is the only entity permitted an external dependency, so
    this boundary holds none. Its cross-boundary imports are limited to
    Infrastructure facilities and the Knowledge **composition root**.
  - **INV-13** — coordination runs through Workflow only. Runtime exposes no
    channel by which one Agent Instance could reach another.

together with the structural contracts runtime_spec states: Runtime is a
**facility, not an actor** (§1); it **owns no Knowledge** (§8; Freeze §5); it
makes no governance decision (§10); and it fails closed on invalid lifecycle
transitions and out-of-state access (§11).

Verification is **structural wherever possible** — AST inspection, dataclass
inspection, `inspect.signature`, abstract-interface inspection, public-API
inspection — in preference to runtime simulation.

**Observation O-1 is record-only.** runtime_spec §12/§14 reserve the Runtime
lifecycle state model to the Architect, and the Phase 4.0 directive exercised
that reservation. These tests verify the state model **as implemented** — its
determinism, completeness, and fail-closed behaviour. They neither ratify nor
question the reservation.

**No source file in this boundary is modified by this baseline.** Any
requirement or defect discovered is reported as evidence, never repaired here.

Standard-library `unittest` only. No external dependency (INV-12).
"""
