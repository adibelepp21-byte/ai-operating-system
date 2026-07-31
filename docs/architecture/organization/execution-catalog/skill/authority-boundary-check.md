# Authority Boundary Check

This document is a Skill instance, documented per the
[Skill Framework](../../skill-framework.md). It does not itself
grant or define any authority. Skill creation and lifecycle authority
are governed exclusively by Canonical Domain Model §5 and §6, per Skill
Framework §3.

## Metadata

- **Name:** Authority Boundary Check
- **Canonical Key:** `skill.authority-boundary-check` — assigned per
  EARC's Canonical Identifier Model and Canonical Key Format (EARC §9,
  EARC Amendment v1.1). Recorded in the existing Metadata structural
  section (Skill Framework §8); does not amend Skill Framework's
  Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v1.0

## Purpose / Description

A discrete, bounded unit of executable ability (Domain Model §2) that
checks whether a governance document's content stays within the
authority tier it claims for itself — for example, whether a
Principle-Document-tier document introduces content reserved to the
Canonical Domain Model or the Constitution. Stated only in the
abstract.

## Interface

Accepts a document reference. Returns a list of passages that appear
to exceed the document's own declared authority tier. Records this
Skill's current interface boundary (Skill Framework §9).

## Permitted Invocation Context

Invoked by an Agent Instance of the
[Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md).

## Version History

- **v1.0** — Initial creation. No prior version exists.
