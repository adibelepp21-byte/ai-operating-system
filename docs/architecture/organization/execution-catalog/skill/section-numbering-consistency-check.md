# Section Numbering Consistency Check

This document is a Skill instance, documented per the
[Skill Framework](../../skill-framework.md). It does not itself
grant or define any authority. Skill creation and lifecycle authority
are governed exclusively by Canonical Domain Model §5 and §6, per Skill
Framework §3.

## Metadata

- **Name:** Section Numbering Consistency Check
- **Canonical Key:** `skill.section-numbering-consistency-check` —
  assigned per EARC's Canonical Identifier Model and Canonical Key
  Format (EARC §9, EARC Amendment v1.1). Recorded in the existing
  Metadata structural section (Skill Framework §8); does not amend
  Skill Framework's Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v1.0

## Purpose / Description

A discrete, bounded unit of executable ability (Domain Model §2) that
checks whether a governance document's own internal cross-references
to its own numbered sections still match that document's current
section numbering. Stated only in the abstract.

## Interface

Accepts a document reference. Returns a list of internal
cross-references whose target section number no longer matches.
Records this Skill's current interface boundary (Skill Framework §9),
invoking the
[Document Structure Parser Interface](../tool/document-structure-parser-interface.md).

## Permitted Invocation Context

Invoked by an Agent Instance of the
[Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md).

## Version History

- **v1.0** — Initial creation. No prior version exists.
