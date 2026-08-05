"""Workflow boundary conformance tests (Native Core Blueprint §27).

Tests assert the invariants Roadmap §9.8 names as this boundary's completion
criteria — *"INV-13/4 tests pass"* — together with the further gates Baseline
02 requires:

  - **INV-13** — Workflow is the sole sanctioned multi-agent channel; direct
    Instance-to-Instance collaboration is structurally unrepresentable.
  - **INV-4** — every coordinated step is an Agent-Instance action producing
    exactly one Trace; a step with no actor cannot be constructed.
  - **INV-15 / ADR-0007** — an Agent Definition may declare zero or more
    Workflows; an empty declaration is a valid architectural state.
  - **INV-12** — Tool is the only entity permitted an external dependency, so
    this boundary holds none.
  - **ADR-0004** — Workflow is owned centrally and versioned independently.

together with the boundary's dependency rules, its absence of any execution
surface (workflow_spec §8; Freeze §4), and the reserved status of
failure-recovery, compile-time validation, and registry concerns
(workflow_spec §12/§13/§14; Blueprint §25).

Standard-library `unittest` only. No external dependency (INV-12).
"""
