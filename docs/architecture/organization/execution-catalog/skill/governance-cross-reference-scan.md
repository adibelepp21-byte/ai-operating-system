# Governance Cross-Reference Scan

This document is a Skill instance, documented per the
[Skill Framework](../../skill-framework.md). It does not itself
grant or define any authority. Skill creation and lifecycle authority
are governed exclusively by Canonical Domain Model §5 and §6, per Skill
Framework §3.

## Metadata

- **Name:** Governance Cross-Reference Scan
- **Canonical Key:** `skill.governance-cross-reference-scan` — assigned
  per the Execution Artifact Repository Convention's Canonical
  Identifier Model and Canonical Key Format (EARC §9, as amended by
  EARC Amendment v1.1). This key is a documentation-level reference
  identity only; it does not define, redefine, or substitute for this
  Skill's entity identity, which remains governed exclusively by the
  Canonical Domain Model (§6). No dedicated Canonical Key field
  currently exists in Skill Framework §9; this key is recorded here, in
  the existing Metadata structural section (Skill Framework §8), as a
  fact EARC's own already-ratified content already requires be
  assignable and citable — this recording does not itself amend, or
  presuppose an amendment to, Skill Framework's Mandatory Document
  Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v1.1

## Purpose / Description

A discrete, bounded unit of executable ability (Domain Model §2) that
reviews a specified set of AIOS governance or procedural documents and
identifies where their content is internally inconsistent — where one
document's cross-reference to another no longer matches that other
document's current, ratified content; where a status statement no
longer reflects what a cited section actually establishes; or where
content is duplicated rather than cited. Stated only in the abstract;
names no specific technology, vendor, or model (Domain Model §8,
Constitution §6.2 invariant 1).

## Interface

Accepts a reference to one or more governance or procedural documents
as its scope, and optionally a set of specific sections within that
scope to which the search should be narrowed. Produces a structured
account of any cross-reference inconsistency found within that scope,
without proposing or applying a correction itself. This field records the current, documented
representation of this Skill's interface boundary (Skill Framework
§9); it does not define what "interface" means for a Skill as a class,
and does not interpret Skill Framework's own citation of Domain Model
§6 beyond recording this Skill's current interface content.

## Permitted Invocation Context

Invoked by an Agent Instance of the
[Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md)
Agent Definition, within that Agent Definition's own declared Behavior
and Permissions. This Skill does not itself declare, expand, or
restrict that Agent Definition's authority; any such declaration
belongs exclusively to the Agent Definition document itself, per Agent
Definition Framework §8.

## Version History

- **v1.1** — Added an optional section-scope parameter to the
  Interface, narrowing the search to specific sections within a
  document rather than the whole document. This is interface-preserving:
  an invocation that does not supply the new parameter behaves
  identically to v1.0. Recorded per Domain Model §6 ("a Skill may
  evolve as long as the interface is preserved").
- **v1.0** — Initial creation. No prior version exists.
