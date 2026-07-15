# AIOS — AI Operating System

AIOS is a long-lived, modular AI Operating System foundation — an engineering
foundation intended to support many AI-powered Departments, specialized
Agents, shared Skills, Workflows, Knowledge, and Memory systems over many
years. It is not a single application, and not a single agent.

## Status

This repository currently contains its foundational documentation layer
only. No implementation exists yet. Structure, technology choices, and code
are deliberately deferred until the conceptual and governance foundation is
complete.

## Architectural Vision

AIOS is organization-centric, not agent-centric: intelligence is organized
around a stable structure of Departments and Capabilities, which persist
independently of which Agents or underlying models currently implement
them. This is the mechanism that keeps AIOS vendor-agnostic and
model-agnostic as the AI landscape changes.

The system is modeled as:

- An **Organizational Spine** (Organization → Department → Capability) —
  slow-changing, single-owner, accountable structure.
- An **Execution Layer** (Agent Definition, Agent Instance, Skill, Workflow,
  Tool, Runtime) — fast-changing, many-to-many implementations of
  Capabilities.
- Two **Shared Substrates** (Knowledge, Memory) — cross-cutting,
  graph-structured resources any part of the Spine or Execution Layer can
  draw on.
- A **Trace** record — the immutable audit trail that makes every Agent
  action explainable after the fact.

See `docs/architecture/domain-model/canonical-domain-model-v1.md` for the
full, ratified semantic foundation this system is built on.

## Governance

AIOS is governed by the ratified Engineering Constitution v1.0 — see
`docs/constitution/engineering-constitution-v1.md`. Structural changes to
the domain model require an Architecture Decision Record (ADR) — see
`docs/architecture/adr/README.md`.

## Documentation

- `docs/constitution/` — the ratified Engineering Constitution v1.0
  (governance)
- `docs/architecture/domain-model/` — the Canonical Domain Model (semantic
  foundation)
- `docs/architecture/adr/` — Architecture Decision Records
- `docs/principles/` — engineering principles (planned)
- `docs/glossary/` — canonical terminology (planned)
