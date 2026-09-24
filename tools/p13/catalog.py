"""The `ActionCatalog`: every action type P13 can name, and what each one is.

An action type **not** in this catalog is REFUSED by the gate. A **reserved**
type is here only so the gate can recognize it and ESCALATE it: it has no
executor, and no envelope can make it executable (Blueprint `§5.2`). These are
the reserved types: code change, governance or certified-evidence change,
delegation issuance, knowledge admission, Native Core change, Constitution
change. `P13-018 §3` adds three: self-expanding the envelope, granting
authority, and external or business action.

Every executable type but two runs an **existing resident verifier,
read-only**. That is all `P13-ENV-01` permits: items 1 and 6. The cycle's own
records are written by the evidence store, on items 3 and 4.

The two others are state-changing: `s_ops.open` and `s_ops.close`, on one
object, `docs/operations/s-ops/S-OPS-01.json`. `FDR-3` granted them through
`P13-ENV-02` for the E13-05 proof, and `FDR-4` `FD-B` retired that envelope once
the proof completed. They remain in the catalog, with no envelope permitting
them, so the gate escalates any proposal of either. P13 never wrote the object
itself. It called the S-OPS surface's own `transition`.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Callable, Dict, Optional, Tuple

from tools.p13.paths import Paths

Produced = Dict[str, Any]


#: What an action does to state (the post-construction instruction, `§8.1`).
#: The classes exist so the gate can tell them apart and hold each to its own
#: requirements. A class being named here authorizes nothing: only a recorded
#: envelope does.
READ_ONLY, RECORD, STATE_CHANGING, EXTERNAL = (
    "read-only", "record", "state-changing", "external")
EFFECTS = (READ_ONLY, RECORD, STATE_CHANGING, EXTERNAL)

Footprint = Dict[str, str]


@dataclass(frozen=True)
class ActionType:
    """One action P13 can name.

    A state-changing type is executable only when it also declares how to
    **observe** its boundary (before and after) and how to **verify** the
    result. With either missing, the gate refuses it: *"No verification path:
    NO EXECUTION"* (`§8.5`). Each precondition returns the reason it fails, or
    None when it holds. One that fails refuses the action (`§8.3`).
    """

    name: str
    reserved: bool
    produces: Tuple[str, ...] = ()
    executor: str = ""
    run: Optional[Callable[..., Produced]] = None
    effect: str = READ_ONLY
    observe: Optional[Callable[[Paths, str], Footprint]] = None
    verify: Optional[Callable[[Paths, str, Footprint, Footprint], Tuple[bool, str]]] = None
    preconditions: Tuple[Callable[[Paths, str], Optional[str]], ...] = ()

    def __post_init__(self):
        if self.effect not in EFFECTS:
            raise ValueError(f"{self.name}: {self.effect!r} is not an effect class")

    @property
    def verifiable(self) -> bool:
        if self.effect == READ_ONLY:
            return True      # verified by re-evaluating what it produced
        return self.observe is not None and self.verify is not None


def _exists(relative: str, what: str):
    def precondition(paths: Paths, target: str) -> Optional[str]:
        return None if (paths.repo / relative).exists() else f"{what} is absent"
    return precondition


def _integrity(paths: Paths) -> Produced:
    from tools import certified_evidence_integrity as integrity
    report = integrity.verify(paths.repo)
    return {"integrity.holds": report.holds,
            "integrity.phases": {p: r.holds for p, r in report.phases.items()}}


def _reconciliation(paths: Paths) -> Produced:
    from tools import foundational_question_reconciliation as reconciliation
    result = reconciliation.verify(paths.matrix, paths.repo)
    return {"verification.foundational_question_reconciliation": {
        "holds": result["holds"], "counts": result["counts"],
        "faults": len(result["faults"])}}


def _ecosystem(paths: Paths) -> Produced:
    from tools import ecosystem_relationships as ecosystem
    report = ecosystem.report(paths.repo)
    return {"verification.ecosystem_relationships": {
        f"{r['left']}↔{r['right']}": r["status"] for r in report["relationships"]}}


def _own_evidence(paths: Paths) -> Produced:
    from tools.p13.evidence import EvidenceStore
    return {"verification.p13_evidence": EvidenceStore(paths).verify()}


# ---------------------------------------------------------------------------
# S-OPS (FDR-3; P13-ENV-02): the only state-changing types P13 can execute
# ---------------------------------------------------------------------------
#
# Two transitions of one object, `docs/operations/s-ops/S-OPS-01.json`, owned
# by the S-OPS operational proof surface (`docs/operations/s-ops/
# S-OPS-DEFINITION.md`). P13 never writes the object itself. It calls the
# surface's own `transition`, which compares and sets on the recorded state and
# enforces the window again.

#: Everything an S-OPS execution could touch and must not, besides its target:
#: the authority records. The whole S-OPS root is observed as well.
S_OPS_AUTHORITY = (
    "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md",
    "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md",
    "docs/governance/acts/FDR-3-S-OPS-DEDICATED-BOUNDED-OPERATIONAL-PROOF-SURFACE-FOR-E13-05.md",
)
S_OPS_ACTOR = "P13 (tools.p13, BoundedExecution)"


def _digest_file(path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return "absent"


def _s_ops_boundary(paths: Paths, target: str) -> Footprint:
    """The whole S-OPS root, the envelopes and the authority records, hashed."""
    from tools.s_ops import surface
    footprint: Footprint = {}
    if paths.s_ops.is_dir():
        for path in sorted(paths.s_ops.rglob("*")):
            if path.is_file():
                relative = path.relative_to(paths.s_ops).as_posix()
                footprint[f"{surface.ROOT}/{relative}"] = _digest_file(path)
    if paths.envelopes.is_dir():
        for path in sorted(paths.envelopes.glob("*.json")):
            footprint[f"docs/governance/p13-envelopes/{path.name}"] = _digest_file(path)
    physical = {S_OPS_AUTHORITY[0]: paths.delegation_register,
                S_OPS_AUTHORITY[1]: paths.decision_register,
                S_OPS_AUTHORITY[2]: paths.repo / S_OPS_AUTHORITY[2]}
    for relative, path in physical.items():
        footprint[relative] = _digest_file(path)
    return footprint


def _s_ops_read(paths: Paths):
    from tools.s_ops import surface
    return surface.read(paths.s_ops)


def _is_the_s_ops_object(paths: Paths, target: str) -> Optional[str]:
    from tools.s_ops import surface
    if target != surface.OBJECT:
        return f"{target!r} is not the S-OPS object {surface.OBJECT}"
    try:
        found = _s_ops_read(paths)
    except (OSError, ValueError) as error:
        return f"the S-OPS object is not the surface's own ({error})"
    return None if found is not None else "the S-OPS object is not provisioned"


def _s_ops_state_is(required: str):
    def precondition(paths: Paths, target: str) -> Optional[str]:
        try:
            state = (_s_ops_read(paths) or {}).get("state")
        except (OSError, ValueError) as error:
            return f"the S-OPS object cannot be read ({error})"
        return None if state == required else f"S-OPS-01 is {state}, not {required}"
    return precondition


def _s_ops_phase_in(allowed: Tuple[str, ...]):
    def precondition(paths: Paths, target: str) -> Optional[str]:
        from tools.s_ops import surface
        try:
            found = _s_ops_read(paths)
            now = surface.phase(found["window"], surface.utcnow()) if found else None
        except (OSError, ValueError, KeyError) as error:
            return f"the S-OPS window cannot be read ({error})"
        return (None if now in allowed else
                f"S-OPS-01's window phase is now {now}, not {'/'.join(allowed)}")
    return precondition


def _s_ops_run(name: str):
    def run(paths: Paths, target: str) -> Produced:
        from tools.s_ops import surface
        if target != surface.OBJECT:
            raise ValueError(f"{target!r} is not the S-OPS object")
        done = surface.transition(paths.s_ops, name, actor=S_OPS_ACTOR,
                                  basis="P13-ENV-02 (FDR-3 §4), after the AuthorityGate's EXECUTE")
        return {"s_ops.transition": done}
    return run


def _s_ops_verify(name: str, to_state: str):
    def verify(paths: Paths, target: str, before: Footprint,
               after: Footprint) -> Tuple[bool, str]:
        try:
            found = _s_ops_read(paths)
        except (OSError, ValueError) as error:
            return False, f"S-OPS-01 cannot be read back ({error})"
        if found is None:
            return False, "S-OPS-01 is gone"
        last = found["history"][-1]
        holds = (found["state"] == to_state and last.get("event") == name
                 and last.get("to") == to_state and before.get(target) != after.get(target))
        return holds, (f"S-OPS-01 reads back {found['state']}; its last history entry "
                       f"is {last.get('event')} {last.get('from')} → {last.get('to')}")
    return verify


def _s_ops_type(name: str) -> ActionType:
    from tools.s_ops import surface
    source, target, phases = surface.TRANSITIONS[name]
    return ActionType(
        f"s_ops.{name}", False, (), "tools.s_ops.surface.transition",
        _s_ops_run(name), effect=STATE_CHANGING, observe=_s_ops_boundary,
        verify=_s_ops_verify(name, target),
        preconditions=(_is_the_s_ops_object, _s_ops_state_is(source),
                       _s_ops_phase_in(phases)))


RESERVED = (
    "change.code", "change.governance", "change.certified_evidence",
    "issue.delegation", "admit.knowledge", "change.native_core",
    "change.constitution", "expand.envelope", "grant.authority",
    "external.action",
    # A remedy that did not bring about its expected consequence goes to a
    # human for review. It is never retried blindly, and never executable.
    "review.consequence",
)

CATALOG: Dict[str, ActionType] = {
    **{name: ActionType(name, reserved=True,
                        effect=EXTERNAL if name == "external.action" else STATE_CHANGING)
       for name in RESERVED},
    "verify.certified_evidence_integrity": ActionType(
        "verify.certified_evidence_integrity", False,
        ("integrity.holds", "integrity.phases"),
        "tools.certified_evidence_integrity.verify", _integrity),
    "verify.foundational_question_reconciliation": ActionType(
        "verify.foundational_question_reconciliation", False,
        ("verification.foundational_question_reconciliation",),
        "tools.foundational_question_reconciliation.verify", _reconciliation,
        preconditions=(_exists("docs/architecture/p13-preparation/"
                               "P13-015-FOUNDATIONAL-QUESTION-RECONCILIATION.json",
                               "the P13-015 matrix"),)),
    "verify.ecosystem_relationships": ActionType(
        "verify.ecosystem_relationships", False,
        ("verification.ecosystem_relationships",),
        "tools.ecosystem_relationships.report", _ecosystem,
        preconditions=(_exists(".git", "the git tree the import graph is read from"),)),
    "verify.p13_evidence": ActionType(
        "verify.p13_evidence", False, ("verification.p13_evidence",),
        "tools.p13.evidence.EvidenceStore.verify", _own_evidence),
    # Item 5. The gate records escalations itself; this entry is what an
    # envelope must permit for them to stand on it rather than on G-02 alone.
    "escalate": ActionType("escalate", False, (), "tools.escalation_register",
                           effect=RECORD),
    # FDR-3 / P13-ENV-02: the S-OPS proof surface's two transitions.
    "s_ops.open": _s_ops_type("open"),
    "s_ops.close": _s_ops_type("close"),
}


def producer(key: str, catalog: Dict[str, ActionType] = CATALOG) -> Optional[str]:
    """The executable action type whose run yields `key`, if one exists."""
    return next((a.name for a in catalog.values()
                 if not a.reserved and a.run and key in a.produces), None)
