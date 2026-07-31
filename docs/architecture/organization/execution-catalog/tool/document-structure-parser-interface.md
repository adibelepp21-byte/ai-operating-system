# Document Structure Parser Interface

This document is a Tool instance, documented per the
[Tool Framework](../../tool-framework.md). It does not itself grant
or define any authority. Tool creation and lifecycle authority are
governed exclusively by Canonical Domain Model §5 and §6, per Tool
Framework §3.

## Metadata

- **Name:** Document Structure Parser Interface
- **Canonical Key:** `tool.document-structure-parser-interface` —
  assigned per EARC's Canonical Identifier Model and Canonical Key
  Format (EARC §9, EARC Amendment v1.1). Recorded in the existing
  Metadata structural section (Tool Framework §8); does not amend Tool
  Framework's Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), grouped
  with Skill and Runtime, not by a Department.
- **Version:** v1.0

## Purpose / Description

An integration point (Domain Model §2) that reads a specified
governance document and returns its recognized structural elements
(section headings and their order), without interpreting their
content. Stated only in the abstract.

## Interface

Accepts a document reference. Returns an ordered list of that
document's recognized structural elements. Records this Tool's current
interface boundary (Tool Framework §9).

## Version History

- **v1.0** — Initial creation. No prior version exists.
