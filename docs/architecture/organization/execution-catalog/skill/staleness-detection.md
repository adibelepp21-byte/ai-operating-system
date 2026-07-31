# Staleness Detection

This document is a Skill instance, documented per the
[Skill Framework](../../skill-framework.md). It does not itself
grant or define any authority. Skill creation and lifecycle authority
are governed exclusively by Canonical Domain Model §5 and §6, per Skill
Framework §3.

## Metadata

- **Name:** Staleness Detection
- **Canonical Key:** `skill.staleness-detection` — assigned per EARC's
  Canonical Identifier Model and Canonical Key Format (EARC §9, EARC
  Amendment v1.1). Recorded in the existing Metadata structural section
  (Skill Framework §8); does not amend Skill Framework's Mandatory
  Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v2.0

## Purpose / Description

A discrete, bounded unit of executable ability (Domain Model §2) that
identifies passages within a specified governance document describing
a state — resolved, unresolved, pending — that no longer matches the
current, ratified state of the document or section it refers to.
Stated only in the abstract.

## Interface

Accepts a document reference and, optionally, a set of sections within
it already known to have changed. Produces a severity-ranked list of
passages whose described state may no longer match, ordered from most
to least likely to require review. Records this Skill's current
interface boundary (Skill Framework §9).

## Permitted Invocation Context

Invoked by an Agent Instance of the
[Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md).

## Version History

- **v2.0** — Changed the produced output from an unranked list of
  passages to a severity-ranked list. This is a behaviorally-material
  change, not merely interface-preserving evolution: a caller relying
  on v1.0's unranked output shape would need to adapt to the ranked
  structure. Documented at promotion time per Domain Model §6
  ("Skill/Tool version changes that alter behavior materially should
  be documented at promotion time, not just interface-checked"). Per
  Skill Framework §13 item 1, this framework takes no position on
  whether "promotion time" in this sense is the same concept as the
  governed Memory-to-Knowledge promotion process (Domain Model §7
  invariant 8); that ambiguity is unaffected by this change.
- **v1.0** — Initial creation. No prior version exists.
