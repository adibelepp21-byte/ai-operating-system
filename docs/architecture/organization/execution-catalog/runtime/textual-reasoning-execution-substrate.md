# Textual Reasoning Execution Substrate

This document is a Runtime instance, documented per the
[Runtime Framework](../../runtime-framework.md). It does not itself
grant or define any authority. Runtime creation and lifecycle
authority are governed exclusively by Canonical Domain Model §5 and
§6, per Runtime Framework §3.

## Metadata

- **Name:** Textual Reasoning Execution Substrate
- **Canonical Key:** `runtime.textual-reasoning-execution-substrate` —
  assigned per EARC's Canonical Identifier Model and Canonical Key
  Format (EARC §9, EARC Amendment v1.1). Recorded in the existing
  Metadata structural section (Runtime Framework §8); does not amend
  Runtime Framework's Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), grouped
  with Skill and Tool, not by a Department.
- **Version:** v1.1

## Purpose / Description

An execution substrate (Domain Model §2) capable of reading repository
text content, performing textual reasoning over it, and producing
textual output — as of v1.1, either prose or structured output —
matching the abstract Runtime Requirement already declared in the
[Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md)'s
own Runtime Requirements field. Stated only in the abstract; names no
specific technology, vendor, or model (Domain Model §8, Constitution
§6.2 invariant 1).

## Hosted Relationship

- **Hosts Agent Instance:** may host an Agent Instance of the
  [Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md)
  (Domain Model §4, Runtime-hosts-Agent-Instance). This field records
  the existence of the relationship only; it does not describe Agent
  Instance's own behavior, lifecycle, or execution semantics.

## Compatibility Boundary Representation

As of v1.1, this Runtime's declared capability includes structured
output in addition to prose output. Whether this addition constitutes
a preserved compatibility boundary is not determined by this document;
per Runtime Framework §12, this framework does not define what
constitutes a compatibility boundary for a Runtime, using the same
treatment already applied by the Workflow Framework to its own,
textually identical lifecycle wording.

## Version History

- **v1.1** — Extended Purpose/Description to note this Runtime may
  also produce structured, not only prose, output. See Compatibility
  Boundary Representation, above, for why this framework takes no
  position on whether this addition preserves a compatibility
  boundary.
- **v1.0** — Initial creation. No prior version exists.
