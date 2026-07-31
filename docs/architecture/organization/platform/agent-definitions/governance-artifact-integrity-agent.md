# Governance Artifact Integrity Agent

This Agent Definition is created as ordinary Department-discretion,
Implementation Tier work under Canonical Domain Model §6, implementing
the [Governance Artifact Integrity](../capabilities/governance-artifact-integrity.md)
Capability that [ADR-0003](../../../adr/decisions/ADR-0003.md)
established. It is documented per the
[Agent Definition Framework](../../agent-definitions.md). This document
does not itself grant or define any authority, and its creation did not
require an ADR — creating an Agent Definition within an already-approved
Capability is not an architectural-tier decision.

## Metadata

- **Name:** Governance Artifact Integrity Agent
- **Version:** 1.1
- **Status:** Active

## Purpose / Description

This Agent Definition specifies a class of Agent that carries out the
Governance Artifact Integrity Capability's definition: reviewing AIOS's
governance artifacts for internal consistency and accuracy, identifying
where an artifact diverges from what it describes or duplicates another
artifact's authoritative content, and proposing corrections. It performs
review and proposal work only; it does not itself constitute governance
authority.

## Owning Department

[Platform](../README.md)

## Implemented Capability

[Governance Artifact Integrity](../capabilities/governance-artifact-integrity.md)

## Behavior and Permissions

An Agent Instance of this Agent Definition is authorized to:

- Read AIOS's governance and procedural documents and compare their
  content against one another for internal consistency, staleness, and
  unauthorized duplication of authoritative content.
- Propose corrections to non-authoritative, non-defining documentation
  wording (for example, status statements, citations, structural
  descriptions) within the scope of the Governance Artifact Integrity
  Capability.

This Agent Definition claims no approval authority, no governance
authority, no Architecture Decision Record authority, and no Constitution
interpretation authority. Any proposed correction requires approval under
Engineering Constitution §3 at the tier appropriate to what is being
changed, exactly as required of any other contributor; nothing in this
document alters that requirement. An Agent Instance of this Agent
Definition operates strictly within the Capability, permissions, Skills,
and Workflows declared here, per Constitution §14.2, and records an
escalation through its Trace rather than proceeding on inference wherever
a matter falls outside this authorized scope — including any matter
touching Constitutional Tier or Architectural Tier authority, Domain
Model semantics, or ADR approval.

## Permitted Skills

This Agent Definition specifies the following Skills, per the specifies
relationship (Domain Model §4) and per EARC's Reference Model and
canonical key format (EARC §9, as amended by EARC Amendment v1.1):

- [`skill.authority-boundary-check`](../../execution-catalog/skill/authority-boundary-check.md)
- [`skill.citation-discipline-verification`](../../execution-catalog/skill/citation-discipline-verification.md)
- [`skill.correction-proposal-drafting`](../../execution-catalog/skill/correction-proposal-drafting.md)
- [`skill.duplicate-content-detection`](../../execution-catalog/skill/duplicate-content-detection.md)
- [`skill.governance-artifact-diff-summary`](../../execution-catalog/skill/governance-artifact-diff-summary.md)
- [`skill.governance-cross-reference-scan`](../../execution-catalog/skill/governance-cross-reference-scan.md)
- [`skill.open-item-tracking-review`](../../execution-catalog/skill/open-item-tracking-review.md)
- [`skill.section-numbering-consistency-check`](../../execution-catalog/skill/section-numbering-consistency-check.md)
- [`skill.staleness-detection`](../../execution-catalog/skill/staleness-detection.md)
- [`skill.terminology-consistency-scan`](../../execution-catalog/skill/terminology-consistency-scan.md)

Each listed Skill's own Permitted Invocation Context field already names
an Agent Instance of this Agent Definition as its invoker; this list
completes that previously one-directional citation. Per Canonical Domain
Model §7 invariant 15, an empty Skill declaration remains a valid
architectural state and no minimum Skill cardinality is required — this
list is populated because these ten Skills already exist and already
declare this Agent Definition as their invoker, not because
non-emptiness is itself required. This question, previously tracked as
Agent Definition Framework Open Architectural Question 5, remains
resolved by [ADR-0007](../../../adr/decisions/ADR-0007.md).

## Permitted Workflows

This Agent Definition specifies the following Workflows, per the same
specifies relationship (Domain Model §4) applied to Permitted Skills,
above:

- [`workflow.governance-corpus-health-check`](../../execution-catalog/workflow/governance-corpus-health-check.md)
- [`workflow.governance-synchronization-review`](../../execution-catalog/workflow/governance-synchronization-review.md)
- [`workflow.post-amendment-consistency-sweep`](../../execution-catalog/workflow/post-amendment-consistency-sweep.md)
- [`workflow.pre-ratification-validation`](../../execution-catalog/workflow/pre-ratification-validation.md)
- [`workflow.terminology-audit`](../../execution-catalog/workflow/terminology-audit.md)

Each listed Workflow's own Invokes Agent Instance field already names an
Agent Instance of this Agent Definition; this list completes that
previously one-directional citation. Per Canonical Domain Model §7
invariant 15, an empty Workflow declaration remains a valid architectural
state and no minimum Workflow cardinality is required — this list is
populated because these five Workflows already exist and already declare
this Agent Definition as their invoker, not because non-emptiness is
itself required. This question, previously tracked as Agent Definition
Framework Open Architectural Question 5, remains resolved by
[ADR-0007](../../../adr/decisions/ADR-0007.md).

## Runtime Requirements

Stated only in the abstract, per Canonical Domain Model §8 and
Constitution §6.2 invariant 1: this Agent Definition requires an execution
substrate capable of reading and analyzing repository text content,
performing textual reasoning over that content, and producing proposed
textual edits. No specific technology, vendor, provider, API, or
infrastructure product is named or implied anywhere in this document.

## Version History

- **v1.1** — Populated Permitted Skills (ten entries) and Permitted
  Workflows (five entries) with the Skills and Workflows created under
  this Agent Definition's own Governance Artifact Integrity Capability
  scope during Governance Freeze Beta, each of which already names an
  Agent Instance of this Agent Definition as its invoker in its own
  Permitted Invocation Context or Invokes Agent Instance field. The
  governing Capability contract is unchanged from v1.0 — still the state
  defined by [ADR-0003](../../../adr/decisions/ADR-0003.md). Per
  Canonical Domain Model §7 invariant 15 and
  [ADR-0007](../../../adr/decisions/ADR-0007.md), this update does not
  establish a minimum Skill or Workflow cardinality; it records which of
  the already-declared, previously one-directional relationships are now
  reciprocated, consistent with Agent Definition Framework §8's
  treatment of Permitted Skills/Permitted Workflows as permitted to be
  empty, not required to be empty.
- **v1.0** — Initial creation. Established as Department-discretion,
  Implementation Tier work under Canonical Domain Model §6. The governing
  Capability contract version is referenced, per Agent Definition
  Framework §11's version representation convention, as the state defined
  by [ADR-0003](../../../adr/decisions/ADR-0003.md), the ADR that most
  recently defined the Governance Artifact Integrity Capability. No
  independent Capability version number is presumed or invented.
