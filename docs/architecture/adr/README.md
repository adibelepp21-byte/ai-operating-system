# Architecture Decision Records (ADR)

This directory holds the Architecture Decision Records for AIOS. This file
establishes the ADR framework only — no decisions have been recorded yet.

## Purpose

An ADR captures a significant, durable architectural decision: the context
that prompted it, the alternatives considered, the decision made, and its
consequences. The goal is that the reasoning behind a structural choice in
AIOS survives long after the discussion that produced it — this repository
is meant to be read and extended over many years, by people and agents who
were not present for the original conversation.

## When an ADR Is Required

An ADR is required whenever a proposed change would:

- Add, remove, or redefine a canonical entity in the Domain Model
- Change a relationship, ownership rule, lifecycle rule, or invariant
  stated in the Domain Model
- Promote a concept out of the Architectural Backlog into the canonical
  model
- Establish a new cross-Department architectural convention
- Reverse or materially reinterpret a prior ADR

An ADR is **not** required for implementation-level decisions that stay
within the bounds of the existing Domain Model and prior ADRs — those are
left to engineer or agent discretion.

## Relationship to the Engineering Constitution

The Engineering Constitution (planned — see `docs/constitution/`) will be
the highest-authority governance document of AIOS, and will formalize the
Decision-Making Process that governs how ADRs are proposed, reviewed, and
approved. Until the Constitution is drafted and ratified, ADRs are governed
directly by System Architect approval. Once the Constitution exists, this
document will be updated to defer to it rather than duplicate it.

## Decision Authority Levels

- **Constitutional-level** — changes to the Engineering Constitution
  itself. Always requires System Architect approval.
- **Architectural-level** — changes to the Canonical Domain Model or other
  durable architectural conventions. Requires an ADR and System Architect
  approval.
- **Implementation-level** — decisions made within the bounds of the
  existing Domain Model and approved ADRs. Engineer or agent discretion; no
  ADR required.

## Status

No ADRs have been created yet.
