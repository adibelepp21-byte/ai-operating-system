"""
Human Review Decision Recording — Execution-side boundary only.

This module is the Execution Event half of a Human Review Event, per the
Human Review Event Layer Assessment v1.0. It records an already-made
human judgment; it never makes one. The Governance Event — the human
deciding approve/reject/edit — happens entirely outside this module,
outside the Runtime, and is not represented anywhere in this file: there
is no candidate ranking, no candidate selection, no threshold, and no
comparison against confidence/occurrence_count/evidence quality anywhere
in this module's logic. `record_decision()` accepts a decision that has
already been made and does exactly one thing: writes it to Trace.

Architecture placement: reuses the same real, existing primitives
orchestrator.py itself uses to produce a Trace record for an Agent
Instance action — agent_definition.load(), runtime.bind_runtime(),
agent_instance.spawn(), trace.new_record(), trace.TraceWriter — with no
Workflow or Skill dispatch loop, because recording a review decision is
not a Skill invocation against a Workflow: it is a distinct, minimal
kind of action this system has not had before, and forcing it through
the Skill/Workflow abstraction would require inventing governance
documents this phase is explicitly not authorized to create. The
spawn -> action -> terminate record shape mirrors orchestrator.run()'s
own real pattern exactly (3 Trace records per invocation), rather than
inventing a leaner, novel shape.

Validation happens strictly before any Agent Instance is spawned. If
validation fails, no Trace record is written at all -- there is no
legitimate action to record, no different in kind from a malformed
function call. This is distinct from orchestrator.py's
skill_not_permitted path, where a real Agent Instance already exists and
its denied attempt is itself the action being recorded; here, a missing
reviewer identity or an invalid decision value means no real decision
was ever made, so nothing is recorded as having happened.

Candidate integrity: the reviewed execution.promotion.CandidatePackage
is stored as a full, self-contained snapshot (via dataclasses.asdict)
inside the Trace record's outputs, never as a bare id -- because
execution.promotion.select_candidates() is stateless and recomputable,
a live-only reference could resolve to different facts later. What the
reviewer actually saw is captured permanently at record time.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Optional

from . import agent_definition, agent_instance as agent_instance_mod, runtime as runtime_mod, trace
from .promotion import CandidatePackage

VALID_DECISIONS = frozenset({"approve", "reject", "edit"})


class ValidationError(ValueError):
    """Raised when a HumanReviewDecisionInput fails validation. Carries
    the full list of errors, not just the first one -- fail closed with
    a complete explanation, not a partial one."""

    def __init__(self, errors):
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class HumanReviewDecisionInput:
    """The already-made human judgment, as received by the Execution
    Event. Every field here is data about a decision that has already
    happened outside the Runtime -- this dataclass has no method, no
    default-computing logic, and no way to derive a decision from its
    own fields."""

    candidate_snapshot: Optional[CandidatePackage]
    decision: Optional[str]
    reviewer_identity: Optional[str]
    rationale: Optional[str]
    timestamp: Optional[float]
    edited_content: Optional[str] = None
    department_override: Optional[str] = None
    department_override_reason: Optional[str] = None
    reviewer_confidence: Optional[float] = None
    additional_notes: Optional[str] = None


def validate_decision_input(decision_input: HumanReviewDecisionInput) -> list:
    """Pure function: input in, list of error strings out (empty = valid).
    Never raises, never guesses a missing value, never infers a default
    for anything the caller left out. Checks presence/shape of required
    fields only -- never reads candidate_snapshot.evidence.confidence,
    .occurrence_count, or .review_flags for any comparison, because
    those are evidence-quality signals this module has no authority to
    act on."""
    errors = []

    snapshot = decision_input.candidate_snapshot
    if snapshot is None:
        errors.append("candidate_snapshot is required and was not provided")
    elif not isinstance(snapshot, CandidatePackage):
        errors.append("candidate_snapshot must be a CandidatePackage instance")
    else:
        if not snapshot.content:
            errors.append("candidate_snapshot.content is required and was empty")
        if snapshot.provenance is None:
            errors.append("candidate_snapshot.provenance is required")
        if snapshot.evidence is None:
            errors.append("candidate_snapshot.evidence is required")
        if snapshot.review_flags is None:
            errors.append("candidate_snapshot.review_flags is required (may be an empty tuple, not absent)")

    if decision_input.decision not in VALID_DECISIONS:
        errors.append(f"decision must be one of {sorted(VALID_DECISIONS)}, got {decision_input.decision!r}")

    if not decision_input.reviewer_identity:
        errors.append("reviewer_identity is required and was not provided")

    if not decision_input.rationale:
        errors.append("rationale is required and was not provided")

    if decision_input.timestamp is None:
        errors.append("timestamp is required and was not provided")

    if decision_input.decision == "edit" and not decision_input.edited_content:
        errors.append("edited_content is required when decision == 'edit'")
    if decision_input.decision != "edit" and decision_input.edited_content:
        errors.append("edited_content must not be provided when decision != 'edit' (ambiguous otherwise)")

    has_override = bool(decision_input.department_override)
    has_override_reason = bool(decision_input.department_override_reason)
    if has_override != has_override_reason:
        errors.append("department_override and department_override_reason must both be provided together, or neither")

    return errors


def _snapshot_to_dict(snapshot: CandidatePackage) -> dict:
    return asdict(snapshot)


def record_decision(decision_input: HumanReviewDecisionInput, *, runtime_selector=None) -> dict:
    """Records an already-made Human Review decision as exactly one
    Agent Instance action's worth of Trace records (spawn, the decision
    itself, terminate -- the same 3-record shape orchestrator.run() uses
    for any run), with no Workflow and no Skill, since none applies
    here. Raises ValidationError, writing nothing to Trace, if the input
    fails validation -- fail closed, no partial or guessed recording.

    Returns a small dict identifying what was written: the decision
    Trace record's own trace_id and the Trace file it was written to.
    This module never returns anything resembling "approved" or
    "rejected" as a computed verdict -- it echoes back only where the
    already-made decision was durably recorded.
    """
    errors = validate_decision_input(decision_input)
    if errors:
        raise ValidationError(errors)

    agent_def = agent_definition.load()
    rt = runtime_mod.bind_runtime(agent_def.name, selector=runtime_selector)
    instance = agent_instance_mod.spawn(agent_def, rt)
    trace_writer = trace.TraceWriter()

    trace_writer.write(trace.new_record(instance, rt, outputs={"event": "spawned"}))
    instance.activate()

    outputs = {
        "event": "human_review_decision_recorded",
        "decision": decision_input.decision,
        "reviewer_identity": decision_input.reviewer_identity,
        "rationale": decision_input.rationale,
        "decision_timestamp": decision_input.timestamp,
        "edited_content": decision_input.edited_content,
        "department_override": decision_input.department_override,
        "department_override_reason": decision_input.department_override_reason,
        "reviewer_confidence": decision_input.reviewer_confidence,
        "additional_notes": decision_input.additional_notes,
        "candidate_snapshot": _snapshot_to_dict(decision_input.candidate_snapshot),
    }
    decision_record = trace.new_record(instance, rt, outputs=outputs, status="success")
    trace_writer.write(decision_record)

    instance.terminate()
    trace_writer.write(trace.new_record(instance, rt, outputs={"event": "terminated"}))

    return {"trace_id": decision_record.trace_id, "trace_file": str(trace_writer.path)}
