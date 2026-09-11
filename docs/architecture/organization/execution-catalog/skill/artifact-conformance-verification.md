# Artifact Conformance Verification

This document is a Skill instance, documented per the
[Skill Framework](../../skill-framework.md). It does not itself
grant or define any authority. Skill creation and lifecycle authority
are governed exclusively by Canonical Domain Model §5 and §6, per Skill
Framework §3.

**This record documents an ability that already existed.** It is written
under `DP-02 §11` item 10 and the `E11-04` directive's evidence-anchored
non-manufacture test, and the order of proof was the directive's, not
convenience:

| | Established | Date |
|---|---|---|
| The Capability, including **Testing** among its seven sub-abilities | [ADR-0008](../../../adr/decisions/ADR-0008.md) | 2026-07-30 |
| The record that **Coding and Testing** are the realized subset | [Engineering Intelligence](../../engineering/capabilities/engineering-intelligence.md) | 2026-08-28 |
| The resident implementation — `REALIZED_SUB_ABILITIES = ("Coding", "Testing")`, with `verify()` | `consumers/engineering_intelligence_agent.py` | 2026-09-02 |
| The ability **exercised, and evidenced**: 13 of 13 conformance criteria against `tools/w4_delegation.py` | `docs/architecture/p11/w4-operations/first-execution.evidence.json` | 2026-09-11 |
| **This Skill record** | — | after all of the above |

The ability, its Capability, its implementation and one recorded exercise
of it all predate this document. Deleting `E11-04` would leave every one
of them unchanged.

## Metadata

- **Name:** Artifact Conformance Verification
- **Canonical Key:** `skill.artifact-conformance-verification` — assigned
  per EARC's Canonical Identifier Model and Canonical Key Format (EARC §9,
  EARC Amendment v1.1). Recorded in the existing Metadata structural
  section (Skill Framework §8); does not amend Skill Framework's
  Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v1.0

## Purpose / Description

A discrete, bounded unit of executable ability (Domain Model §2) that
checks an engineered artifact against a stated set of conformance
criteria and reports, per criterion, whether the artifact satisfies it.
Stated only in the abstract.

This is the **Testing** sub-ability of the
[Engineering Intelligence](../../engineering/capabilities/engineering-intelligence.md)
Capability, worded as that Capability's own Agent Definition words it:
*"Verify engineered artifacts against their stated conformance criteria,
within the Testing sub-ability of the same Capability."*

**It reports; it does not decide.** A criterion that is unsatisfied is
recorded as unsatisfied. Nothing in this Skill authorizes a change, waives
a criterion, or treats its own finding as an approval.

## Interface

Accepts an artifact reference and a set of stated conformance criteria.
Returns one result per criterion, each recording whether that criterion is
satisfied. Records this Skill's current interface boundary (Skill
Framework §9).

## Permitted Invocation Context

Invoked by an Agent Instance of the
[Engineering Intelligence Agent](../../engineering/agent-definitions/engineering-intelligence-agent.md).

## Version History

- **v1.0** — Initial creation. No prior version exists. Documents an
  ability established by ADR-0008 and realized in a resident consumer
  before this record was written; creation of this record neither extends
  the Engineering Intelligence Capability's scope nor realizes any of its
  five unrealized sub-abilities.
