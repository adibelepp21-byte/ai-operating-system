# Cross-Department Artifact Conformance Review

This document is a Workflow instance, documented per the
[Workflow Framework](../../workflow-framework.md). It does not
itself grant or define any authority. Workflow creation and lifecycle
authority are governed exclusively by Canonical Domain Model §5 and
§6, per Workflow Framework §3.

**This is the first resident Workflow whose composed Skills are invoked by
Agent Instances of Agent Definitions owned by two different Departments.**
It is written under `DP-02 §11` item 10. The two Skills it composes both
existed before it: `skill.artifact-conformance-verification` documents the
Testing sub-ability ADR-0008 established, and
`skill.citation-discipline-verification` has been declared by the
Governance Artifact Integrity Agent since that Definition was written.

## Metadata

- **Name:** Cross-Department Artifact Conformance Review
- **Canonical Key:** `workflow.cross-department-artifact-conformance-review`
  — assigned per EARC's Canonical Identifier Model and Canonical Key Format
  (EARC §9, EARC Amendment v1.1). Recorded in the existing Metadata
  structural section (Workflow Framework §8); does not amend Workflow
  Framework's Mandatory Document Fields.
- **Owning designation:** Owned centrally (Domain Model §5), not by a
  Department.
- **Version:** v1.0

## Purpose / Description

An explicit, inspectable composition (Domain Model §2) in which an
engineered artifact is first checked against its stated conformance
criteria, and the record that results is then checked for citation
discipline. Stated only in the abstract.

**The second step depends on the first.** Citation discipline is checked
against the record the conformance step produces, so it has nothing to
examine until that record exists. The dependency is a real ordering
constraint, not a declared one: the two steps could not be exchanged.

**Neither step decides anything.** Conformance verification reports per
criterion; the citation check reports pointers that fail to resolve. A
finding from either is evidence, and evidence is not an approval.

## Composed Elements

- **Contains Skill:**
  [Artifact Conformance Verification](../skill/artifact-conformance-verification.md),
  [Citation Discipline Verification](../skill/citation-discipline-verification.md)
  (Domain Model §4, Workflow-contains-Skill).
- **Invokes Agent Instance:** invoked by an Agent Instance of the
  [Engineering Intelligence Agent](../../engineering/agent-definitions/engineering-intelligence-agent.md)
  for the conformance step, and by an Agent Instance of the
  [Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md)
  for the citation-discipline step (Domain Model §4,
  Workflow-invokes-Agent-Instance).

  The two Agent Definitions are owned by different Departments —
  [Engineering](../../engineering/README.md) and
  [Platform](../../platform/README.md) — which is what makes the
  coordination this Workflow expresses a **cross-Department** one. Per
  Domain Model §5 an Agent Instance is *"accountable to the Platform
  Division that owns its Agent Definition"*, so the Department of each
  participant is resolved through its Definition rather than asserted here.

## Compatibility Boundary Representation

Records, for this Workflow, the current representation of the boundary
Domain Model §6 refers to when it requires "compatibility boundaries
preserved where applicable" across a version change. No prior version
exists; no boundary has yet been exercised.

## Version History

- **v1.0** — Initial creation. No prior version exists. Composes two
  Skills that both predate it; creates no Capability, no Skill and no
  Agent Definition.
