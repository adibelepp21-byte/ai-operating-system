# Engineering

This Department was established by
[ADR-0008](../../adr/decisions/ADR-0008.md). This document records that
decision; it does not itself grant or define any authority. Department
and Capability creation and retirement authority is governed exclusively
by Engineering Constitution §3.4 and Canonical Domain Model §6.

## Name

Engineering

## Scope

The Engineering Department is accountable for AIOS's own construction and
self-directed reasoning: the abilities by which AIOS builds, changes,
verifies, and plans work on itself.

## Responsibilities

- Owning the Capabilities listed below, and being accountable for them.
  Ownership is accountability, not implementation: per Canonical Domain
  Model §2, a Capability is a contract independent of what implements it.
- Owning and being accountable for any Agent Definitions it creates, per
  Canonical Domain Model §2 and §5.
- Upholding AI Collaboration Principles (Constitution §14) for
  contributors, and eventually operational agents, working within this
  Department.

## Explicit Exclusions

- Holds no Constitutional Tier authority. Cannot amend the Engineering
  Constitution under any circumstance; that authority remains
  exclusively the Architect's, per Constitution §3.1 and §16.
- Holds no independent Canonical Domain Model approval authority. May
  propose Domain Model changes via ADR; approval remains Architect-gated
  per Constitution §3.2 and §5 regardless of which Department proposes.
- Holds no authority to create or retire Departments or Capabilities.
  That remains an architectural decision under Constitution §3.4 and
  Canonical Domain Model §6.
- Does not define new governance authority or hierarchy tiers. Any such
  change remains Constitutional Tier, per Constitution §3.1 and §4.
- Is not a generic container for intelligence work. Per ADR-0008, a
  Capability enters Engineering only when its accountability is AIOS's
  own construction or self-directed reasoning, and only by a further
  Architecture Decision Record. Being intelligence-related is not
  sufficient. A Capability whose accountability lies in a business,
  product, scientific, quantitative, linguistic, creative, or strategic
  domain does not enter Engineering merely because it involves reasoning
  or models; it requires its own Department decision.

## Relationship with Platform

Engineering is a peer of [Platform](../platform/README.md), not a
subordinate and not a successor. Platform remains accountable for AIOS's
governance and semantic substrate — the Constitution, the Canonical
Domain Model, and their subordinate procedural documents. Engineering is
accountable for building and reasoning about AIOS. Neither Department
absorbs, supervises, or overrides the other, and no ownership moves
between them.

## Owned Capabilities

- [Engineering Intelligence](capabilities/engineering-intelligence.md)
- [Cognitive Intelligence](capabilities/cognitive-intelligence.md)
