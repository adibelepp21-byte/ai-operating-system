# Engineering Intelligence Agent

This Agent Definition is created as ordinary Department-discretion,
Implementation Tier work under Canonical Domain Model §6, implementing
the [Engineering Intelligence](../capabilities/engineering-intelligence.md)
Capability that [ADR-0008](../../../adr/decisions/ADR-0008.md)
established. It is documented per the
[Agent Definition Framework](../../agent-definitions.md). This document
does not itself grant or define any authority, and its creation did not
require an ADR — creating an Agent Definition within an already-approved
Capability is not an architectural-tier decision.

## Metadata

- **Name:** Engineering Intelligence Agent
- **Version:** 1.1
- **Status:** Active

## Purpose / Description

This Agent Definition specifies a class of Agent that carries out the
Engineering Intelligence Capability's definition: constructing, changing,
verifying, and safeguarding AIOS's own engineered artifacts. Consistent
with that Capability's recorded Phase 5 realization boundary, an Agent
Instance of this Agent Definition operates within the Coding and Testing
sub-abilities only; the remaining five sub-abilities named in the
Capability — Architecture, Security, Review, Refactoring, and
Documentation — are within the Capability's long-term contract but are
not realized in Phase 5, and this Agent Definition does not act on them.

## Owning Department

[Engineering](../README.md)

## Implemented Capability

[Engineering Intelligence](../capabilities/engineering-intelligence.md)

## Behavior and Permissions

An Agent Instance of this Agent Definition is authorized to:

- Construct and change engineered artifacts within AIOS, within the
  Coding sub-ability of the Engineering Intelligence Capability.
- Verify engineered artifacts against their stated conformance criteria,
  within the Testing sub-ability of the same Capability.

This Agent Definition claims no approval authority, no governance
authority, no Architecture Decision Record authority, and no Constitution
interpretation authority. It carries no authority to create or retire
Departments or Capabilities, and none to amend the Canonical Domain
Model. Any change requiring approval under Engineering Constitution §3
requires that approval at the tier appropriate to what is being changed,
exactly as required of any other contributor; nothing in this document
alters that requirement. An Agent Instance of this Agent Definition
operates strictly within the Capability, permissions, Skills, and
Workflows declared here, per Constitution §14.2, and records an
escalation through its Trace rather than proceeding on inference wherever
a matter falls outside this authorized scope — including any matter
touching Constitutional Tier or Architectural Tier authority, Domain
Model semantics, or ADR approval.

## Permitted Skills

This Agent Definition specifies the following Skill, per the specifies
relationship (Domain Model §4) and per EARC's Reference Model and
canonical key format (EARC §9, as amended by EARC Amendment v1.1):

- [`skill.artifact-conformance-verification`](../../execution-catalog/skill/artifact-conformance-verification.md)

That Skill's own Permitted Invocation Context field already names an Agent
Instance of this Agent Definition as its invoker; this list completes that
previously one-directional citation — the same pattern the
[Governance Artifact Integrity Agent](../../platform/agent-definitions/governance-artifact-integrity-agent.md)
records for its ten.

Per Canonical Domain Model §7 invariant 15 and
[ADR-0007](../../../adr/decisions/ADR-0007.md), an empty Skill
declaration remains a valid architectural state and no minimum cardinality
is required. **This list is populated because the ability it names already
existed**, not because non-emptiness is required: ADR-0008 established the
Testing sub-ability on 2026-07-30, the Capability record named Coding and
Testing as the realized subset on 2026-08-28, `consumers/engineering_intelligence_agent.py`
implemented them on 2026-09-02, and an Agent Instance of this Definition
exercised the ability on 2026-09-11 — 13 of 13 conformance criteria
against `tools/w4_delegation.py`, recorded in
`docs/architecture/p11/w4-operations/first-execution.evidence.json`.

**Until v1.1 this section read "None declared", and that was accurate when
written.** No Skill record existed to name. The prior text also said *"No
Skill exists within the Engineering Department's scope"*, which conflated
two things Domain Model §5 keeps apart: Skills are **owned centrally**, not
by a Department, and what an Agent Definition declares is which centrally
owned Skill it is permitted to use. The correction is recorded here rather
than made silently.

## Permitted Workflows

This Agent Definition specifies the following Workflow, per the same
specifies relationship (Domain Model §4) applied to Permitted Skills,
above:

- [`workflow.cross-department-artifact-conformance-review`](../../execution-catalog/workflow/cross-department-artifact-conformance-review.md)

That Workflow's own Invokes Agent Instance field names an Agent Instance
of this Agent Definition among its participants; this list completes that
citation.

Per Canonical Domain Model §7 invariant 15 and
[ADR-0007](../../../adr/decisions/ADR-0007.md), an empty Workflow
declaration remains a valid architectural state and no minimum cardinality
is required. As with Permitted Skills above, the prior *"No Workflow
exists within the Engineering Department's scope"* conflated central
ownership with departmental scope; Workflows are **owned centrally**
(Domain Model §5).

## Runtime Requirements

Stated only in the abstract, per Canonical Domain Model §8 and
Constitution §6.2 invariant 1: this Agent Definition requires an execution
substrate capable of reading repository source content, producing and
changing source artifacts, and executing conformance verification over
them. No specific technology, vendor, provider, API, or infrastructure
product is named or implied anywhere in this document.

## Version History

- **v1.1** — Permitted Skills and Permitted Workflows populated.
  Behaviourally material for recording purposes (Domain Model §6): this
  Definition's instances may now appear as a `WorkflowStep` performer,
  which an empty Skill declaration made structurally impossible. **No
  capability is added.** The ability named was established by ADR-0008,
  realized in a resident consumer, and exercised and evidenced before this
  version; what changes is that the organizational record now names it.
  Written under `DP-02 §11` item 10 and its evidence-anchored
  non-manufacture test — the work exists on record before the declaration
  does. The governing Capability contract version is unchanged.
- **v1.0** — Initial creation. Established as Department-discretion,
  Implementation Tier work under Canonical Domain Model §6, closing the
  transient zero-implementer condition that
  [ADR-0008](../../../adr/decisions/ADR-0008.md) recorded for this
  Capability under Canonical Domain Model §7 invariant 14. The governing
  Capability contract version is referenced, per Agent Definition
  Framework §11's version representation convention, as the state defined
  by [ADR-0008](../../../adr/decisions/ADR-0008.md), the ADR that most
  recently defined the Engineering Intelligence Capability. No independent
  Capability version number is presumed or invented.
