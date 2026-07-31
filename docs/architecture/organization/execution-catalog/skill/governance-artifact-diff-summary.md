# Governance Artifact Diff Summary

This document is a Skill instance, documented per the
[Skill Framework](../../skill-framework.md). It does not itself
grant or define any authority. Skill creation and lifecycle authority
are governed exclusively by Canonical Domain Model §5 and §6, per Skill
Framework §3.

## Metadata

- **Name:** Governance Artifact Diff Summary
- **Canonical Key:** `skill.governance-artifact-diff-summary` —
  assigned per EARC's Canonical Identifier Model and Canonical Key
  Format (EARC §9, EARC Amendment v1.1). Recorded in the existing
  Metadata structural section (Skill Framework §8); does not amend
  Skill Framework's Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v1.0

## Purpose / Description

A discrete, bounded unit of executable ability (Domain Model §2) that
produces a plain-language summary of what changed in a governance
document between two recorded points in its history, for use in a
review or ratification record. Stated only in the abstract.

## Interface

Accepts a document reference and two points in its recorded history.
Returns a plain-language summary of the difference. Records this
Skill's current interface boundary (Skill Framework §9), invoking the
[Version Control Diff Interface](../tool/version-control-diff-interface.md).

## Permitted Invocation Context

Invoked by an Agent Instance of the
[Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md).

## Version History

- **v1.0** — Initial creation. No prior version exists.
