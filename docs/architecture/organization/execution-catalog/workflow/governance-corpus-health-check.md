# Governance Corpus Health Check

This document is a Workflow instance, documented per the
[Workflow Framework](../../workflow-framework.md). It does not
itself grant or define any authority. Workflow creation and lifecycle
authority are governed exclusively by Canonical Domain Model §5 and
§6, per Workflow Framework §3.

## Metadata

- **Name:** Governance Corpus Health Check
- **Canonical Key:** `workflow.governance-corpus-health-check` —
  assigned per EARC's Canonical Identifier Model and Canonical Key
  Format (EARC §9, EARC Amendment v1.1). Recorded in the existing
  Metadata structural section (Workflow Framework §8); does not amend
  Workflow Framework's Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v1.0

## Purpose / Description

An explicit, inspectable composition (Domain Model §2) that produces a
periodic consolidated view of the governance corpus's open items and
recent change history, for Architect review. Stated only in the
abstract.

## Composed Elements

- **Contains Skill:**
  [Open Item Tracking Review](../skill/open-item-tracking-review.md),
  [Governance Artifact Diff Summary](../skill/governance-artifact-diff-summary.md)
  (Domain Model §4, Workflow-contains-Skill).
- **Invokes Agent Instance:** invoked by an Agent Instance of the
  [Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md)
  (Domain Model §4, Workflow-invokes-Agent-Instance).

## Compatibility Boundary Representation

Records, for this Workflow, the current representation of the boundary
Domain Model §6 refers to when it requires "compatibility boundaries
preserved where applicable" across a version change. No prior version
exists; no boundary has yet been exercised.

## Version History

- **v1.0** — Initial creation. No prior version exists.
