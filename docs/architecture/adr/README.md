# Architecture Decision Records (ADR)

## Purpose

This document defines how Architecture Decision Records (ADRs) operate
within AIOS: their required structure, their lifecycle, and the validation
and supersession discipline that governs them.

This document does not define why ADR authority exists. That authority —
who may propose, who may approve, what an ADR may and may not change, and
how delegation works — is defined exclusively in Engineering Constitution
§3 (Decision-Making Process). This document never restates that authority;
it only describes the mechanics that operate beneath it.

An ADR captures a significant, durable architectural decision: its
context, the alternatives considered, the decision made, and its
consequences. The goal is that the reasoning behind a structural choice in
AIOS survives long after the discussion that produced it.

## Authority

ADR authority — proposal rights, approval rights, delegation, and
non-delegable decisions — is governed exclusively by Engineering
Constitution §3. This document does not restate that content. See
Constitution §3.1–§3.4.

The relationship among AIOS's governance artifacts, including the ADR
Framework's place beneath the Constitution and the Canonical Domain Model,
is governed exclusively by Engineering Constitution §4 (Governance
Artifact Relationship).

## ADR Framework Ownership

Changes to this document are governed by content ownership, not by a
single uniform process:

- **Procedural mechanics** — lifecycle, structure, validation,
  identifiers, storage conventions, and supersession/deprecation
  mechanics — are owned by this document and may be updated through
  direct Architect-approved documentation changes.
- **Constitution authority content** — decision authority, tiers,
  delegation boundaries, and approval rights — remains exclusively
  governed by the Engineering Constitution and is never redefined by
  this document; it appears here only by reference.
- **Architectural decisions that use the ADR process** continue to
  follow the normal ADR mechanism defined elsewhere in this document,
  unaffected by how this document itself is maintained.

This preserves the distinction stated in Purpose, above: this document
defines how ADRs operate, not why ADR authority exists.

## When an ADR Is Required

What an ADR may change is defined in Constitution §3.4. This document
adds only the following procedural trigger, which the Constitution does
not itself state:

- An ADR is required to reverse or materially reinterpret a prior ADR
  (see Supersession and Deprecation, below).

An ADR is not required for implementation-tier work within already-approved
Capabilities, or for Knowledge additions made through the governed-review
promotion pipeline.

## ADR Lifecycle

An ADR moves through the following states:

- **Proposed** — drafted and submitted by any contributor. Not yet binding.
- **Under Review** — the approving authority is evaluating it. May return
  to Proposed for revision.
- **Approved** — accepted by the approving authority. Binding and active
  immediately.
- **Rejected** — declined. Terminal; retained permanently as record.
- **Superseded** — a later, separately approved ADR explicitly replaces
  this one's decision.
- **Deprecated** — the decision no longer applies because its context
  ceased to exist, without a replacement decision existing.

Archived is not a distinct state. Every terminal state (Rejected,
Superseded, Deprecated) is retained indefinitely as permanent record.

## ADR Structure

Every ADR contains:

- **Metadata** — including a unique identifier. Identifiers use
  zero-padded sequential numbering (ADR-0001, ADR-0002, …), assigned by
  the approving authority when an ADR enters Under Review. Filename and
  storage location follow the ADR Storage convention, below.
- **Context** — why this is being considered now.
- **Problem Statement** — the specific gap or need being addressed.
- **Decision** — what was decided, stated precisely enough to be checked
  against later.
- **Alternatives Considered** — what else was evaluated and why it wasn't
  chosen.
- **Consequences** — what changes as a result, including any Domain Model
  edit the decision requires.
- **Validation** — how the decision was checked before approval (see
  Validation Model, below).
- **Approval Record** — who approved the ADR and under what authority
  (direct Architect, or a named delegation scope), and when.
- **Status History** — a chronological record of every lifecycle
  transition.

## ADR Storage

Approved ADRs are stored under `docs/architecture/adr/decisions/`, one
file per ADR, named by its identifier alone: `ADR-0001.md`,
`ADR-0002.md`, and so on. No descriptive slug, metadata suffix, or
additional filename convention is used.

This defines repository organization only. It implies no tooling,
generation mechanism, or storage technology.

## Validation Model

Every Architectural Tier ADR requires:

- **Authority validation** — confirms the proposer and approver each have
  valid standing for this ADR under Constitution §3.
- **Boundary validation** — confirms the ADR does not reach into
  Constitutional Tier territory, does not introduce a technology,
  language, framework, or infrastructure decision, and does not exceed
  what Constitution §3.2 permits to be delegated.
- **Contradiction check** — confirms the ADR does not conflict with any
  prior Approved ADR that is not already Superseded or Deprecated.

An ADR affecting the Canonical Domain Model additionally requires:

- **Semantic integrity validation** — confirms the ADR is consistent with
  existing Domain Model content and does not itself reproduce entity,
  relationship, or invariant text.
- **Entity/relationship/invariant impact review** — the ADR explicitly
  enumerates which Domain Model entities, relationships, or invariants it
  affects.

## Supersession and Deprecation

The authority required to supersede or deprecate an ADR must be equal to
or higher than the authority that approved the original ADR.

- A delegate-approved ADR may be superseded or deprecated by that same
  scoped delegate, or by the Architect.
- An Architect-approved ADR may be superseded or deprecated by the
  Architect only.
- An ADR affecting the Canonical Domain Model may be superseded or
  deprecated by the Architect only, regardless of who approved it
  originally, consistent with Domain Model changes being non-delegable
  under Constitution §3.2.

## Delegation Documentation

A grant of architectural-tier approval authority to a delegate
(Constitution §3.2) requires durable governance documentation of its
scope, the delegate, and the date granted or revoked.

A delegation grant is not an ADR and does not require one. It is a direct
exercise of authority the Constitution already grants, not an
architectural-tier decision subject to the trigger rules above. A
delegation grant does not introduce a Canonical Domain Model entity.

## Status

ADR-0001 and ADR-0002 have been approved. Approved ADRs are stored under
`docs/architecture/adr/decisions/`, per the ADR Storage convention,
above.
