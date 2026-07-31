# Cross-Reference Link Validator Interface

This document is a Tool instance, documented per the
[Tool Framework](../../tool-framework.md). It does not itself grant
or define any authority. Tool creation and lifecycle authority are
governed exclusively by Canonical Domain Model §5 and §6, per Tool
Framework §3.

## Metadata

- **Name:** Cross-Reference Link Validator Interface
- **Canonical Key:** `tool.cross-reference-link-validator-interface` —
  assigned per EARC's Canonical Identifier Model and Canonical Key
  Format (EARC §9, EARC Amendment v1.1). Recorded in the existing
  Metadata structural section (Tool Framework §8); does not amend Tool
  Framework's Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), grouped
  with Skill and Runtime, not by a Department.
- **Version:** v1.0

## Purpose / Description

An integration point (Domain Model §2) that checks whether a given
cross-reference (a citation from one governance document to a section
of another) still resolves to a section that exists and matches the
cited description. Stated only in the abstract.

## Interface

Accepts a citing document, a cited document, and a cited section
reference. Returns whether the reference still resolves. Records this
Tool's current interface boundary (Tool Framework §9).

## Version History

- **v1.0** — Initial creation. No prior version exists.
