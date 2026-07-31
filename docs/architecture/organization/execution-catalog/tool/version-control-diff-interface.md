# Version Control Diff Interface

This document is a Tool instance, documented per the
[Tool Framework](../../tool-framework.md). It does not itself grant
or define any authority. Tool creation and lifecycle authority are
governed exclusively by Canonical Domain Model §5 and §6, per Tool
Framework §3.

## Metadata

- **Name:** Version Control Diff Interface
- **Canonical Key:** `tool.version-control-diff-interface` — assigned
  per EARC's Canonical Identifier Model and Canonical Key Format (EARC
  §9, EARC Amendment v1.1). Recorded in the existing Metadata
  structural section (Tool Framework §8); does not amend Tool
  Framework's Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), grouped
  with Skill and Runtime, not by a Department.
- **Version:** v1.0

## Purpose / Description

An integration point (Domain Model §2) providing access to the
recorded change history of a specified repository artifact, returning
what changed between two recorded states. Stated only in the abstract;
names no specific technology, vendor, or model.

## Interface

Accepts a repository artifact reference and two points in its recorded
history. Returns a description of what changed between them. Records
this Tool's current interface boundary (Tool Framework §9).

## Version History

- **v1.0** — Initial creation. No prior version exists.
