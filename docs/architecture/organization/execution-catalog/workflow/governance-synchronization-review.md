# Governance Synchronization Review

This document is a Workflow instance, documented per the
[Workflow Framework](../../workflow-framework.md). It does not
itself grant or define any authority. Workflow creation and lifecycle
authority are governed exclusively by Canonical Domain Model §5 and
§6, per Workflow Framework §3.

## Metadata

- **Name:** Governance Synchronization Review
- **Canonical Key:** `workflow.governance-synchronization-review` —
  assigned per EARC's Canonical Identifier Model and Canonical Key
  Format (EARC §9, EARC Amendment v1.1). Recorded in the existing
  Metadata structural section (Workflow Framework §8); does not amend
  Workflow Framework's Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v1.1

## Purpose / Description

An explicit, inspectable composition (Domain Model §2) that reviews a
governance document following a ratified amendment to a document it
cites, to determine whether its own references to that document remain
accurate. Stated only in the abstract.

## Composed Elements

- **Contains Skill:**
  [Governance Cross-Reference Scan](../skill/governance-cross-reference-scan.md),
  [Staleness Detection](../skill/staleness-detection.md),
  [Correction Proposal Drafting](../skill/correction-proposal-drafting.md),
  [Authority Boundary Check](../skill/authority-boundary-check.md)
  (Domain Model §4, Workflow-contains-Skill).
- **Invokes Agent Instance:** invoked by an Agent Instance of the
  [Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md)
  (Domain Model §4, Workflow-invokes-Agent-Instance). This field
  records the existence of the relationship only; it does not describe
  Agent Instance's own behavior.

## Compatibility Boundary Representation

As of v1.1, this Workflow's composition includes one additional Skill
([Authority Boundary Check](../skill/authority-boundary-check.md))
beyond its v1.0 composition, so proposed corrections are checked
against authority-tier boundaries before being finalized. Whether this
addition constitutes a preserved compatibility boundary is not
determined by this document; per Workflow Framework §12, this
framework does not define what constitutes a compatibility boundary
for a Workflow or when the qualifier "where applicable" does or does
not apply, and does not resolve that ambiguity here. This field
records only what has been documented, consistent with its own
self-limited definition (Workflow Framework §9).

## Version History

- **v1.1** — Added
  [Authority Boundary Check](../skill/authority-boundary-check.md) to
  Composed Elements. See Compatibility Boundary Representation, above,
  for why this framework takes no position on whether this addition
  preserves a compatibility boundary.
- **v1.0** — Initial creation. No prior version exists.
