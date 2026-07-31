# Terminology Consistency Scan

This document is a Skill instance, documented per the
[Skill Framework](../../skill-framework.md). It does not itself
grant or define any authority. Skill creation and lifecycle authority
are governed exclusively by Canonical Domain Model §5 and §6, per Skill
Framework §3.

## Metadata

- **Name:** Terminology Consistency Scan
- **Canonical Key:** `skill.terminology-consistency-scan` — assigned
  per EARC's Canonical Identifier Model and Canonical Key Format (EARC
  §9, EARC Amendment v1.1). Recorded in the existing Metadata
  structural section (Skill Framework §8); does not amend Skill
  Framework's Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v1.0

## Purpose / Description

A discrete, bounded unit of executable ability (Domain Model §2) that
identifies places where a governance document uses a term already
defined precisely elsewhere in the corpus (for example, a Canonical
Domain Model term) in a way that appears inconsistent with that
definition. Stated only in the abstract.

## Interface

Accepts a document reference and a reference term set to check
against. Returns passages using a checked term inconsistently. Records
this Skill's current interface boundary (Skill Framework §9), invoking
the
[Text Similarity Comparison Interface](../tool/text-similarity-comparison-interface.md).

## Permitted Invocation Context

Invoked by an Agent Instance of the
[Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md).

## Version History

- **v1.0** — Initial creation. No prior version exists.
