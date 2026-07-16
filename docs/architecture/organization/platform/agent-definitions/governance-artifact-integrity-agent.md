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
- **Version:** 1.0
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

None declared. No Skill entity, Skill Framework, or Skill storage
convention exists yet in AIOS. Per Agent Definition Framework §10, Skill
reference validation is aspirational until such a framework exists, and
its absence is not treated as a defect. This field is therefore left
unpopulated rather than naming placeholder Skills that would have no
governed definition behind them. Per Canonical Domain Model §7 invariant
15, an empty Skill declaration is a valid architectural state and no
minimum Skill cardinality is required; this question, previously tracked
as Agent Definition Framework Open Architectural Question 5, is resolved
by [ADR-0007](../../../adr/decisions/ADR-0007.md).

## Permitted Workflows

None declared, for the same reason as Permitted Skills, above: no
Workflow entity, Workflow Framework, or Workflow storage convention
exists yet. Per Canonical Domain Model §7 invariant 15, an empty
Workflow declaration is likewise a valid architectural state and no
minimum Workflow cardinality is required; this question, previously
tracked as Agent Definition Framework Open Architectural Question 5, is
resolved by [ADR-0007](../../../adr/decisions/ADR-0007.md).

## Runtime Requirements

Stated only in the abstract, per Canonical Domain Model §8 and
Constitution §6.2 invariant 1: this Agent Definition requires an execution
substrate capable of reading and analyzing repository text content,
performing textual reasoning over that content, and producing proposed
textual edits. No specific technology, vendor, provider, API, or
infrastructure product is named or implied anywhere in this document.

## Version History

- **v1.0** — Initial creation. Established as Department-discretion,
  Implementation Tier work under Canonical Domain Model §6. The governing
  Capability contract version is referenced, per Agent Definition
  Framework §11's version representation convention, as the state defined
  by [ADR-0003](../../../adr/decisions/ADR-0003.md), the ADR that most
  recently defined the Governance Artifact Integrity Capability. No
  independent Capability version number is presumed or invented.
