# Open Item Tracking Review

This document is a Skill instance, documented per the
[Skill Framework](../../skill-framework.md). It does not itself
grant or define any authority. Skill creation and lifecycle authority
are governed exclusively by Canonical Domain Model §5 and §6, per Skill
Framework §3.

## Metadata

- **Name:** Open Item Tracking Review
- **Canonical Key:** `skill.open-item-tracking-review` — assigned per
  EARC's Canonical Identifier Model and Canonical Key Format (EARC §9,
  EARC Amendment v1.1). Recorded in the existing Metadata structural
  section (Skill Framework §8); does not amend Skill Framework's
  Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v1.0

## Purpose / Description

A discrete, bounded unit of executable ability (Domain Model §2) that
collects the explicitly recorded open items across a specified set of
governance documents and reports which remain open, which have since
been closed elsewhere without the originating document being updated,
and which are duplicated across more than one document's own tracking
section. Stated only in the abstract.

## Interface

Accepts a set of document references. Returns a consolidated list of
open items with their current status per document. Records this
Skill's current interface boundary (Skill Framework §9).

## Permitted Invocation Context

Invoked by an Agent Instance of the
[Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md).

## Version History

- **v1.0** — Initial creation. No prior version exists.
