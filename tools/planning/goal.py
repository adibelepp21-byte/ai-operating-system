"""Goal and the authority citation every planning artifact carries.

`DP-04 §8.1`: Goal *"is a legitimate P11 organizational concept"*, *"shall not be
created as a new Native Core subsystem/entity"*, and *"does not create authority
by itself."* Its purpose is *"to represent organizational intent that can be
decomposed and translated into plans and executable organizational work."*
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .exceptions import InvalidGoal

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@dataclass(frozen=True)
class AuthorityProvenance:
    """A **citation** to the instrument under which work was authorized.

    This is the single most important type in the package, and what it is *not*
    matters more than what it is: **it is not authority.** It is a pointer to
    where authority is recorded, exactly as a footnote is not the source it
    cites. `ACT-CC-P11-005 §36`: ``IDENTIFIER ≠ DECISION BODY``.

    ``record`` must resolve to a real file, for the same reason a delegation must
    cite an instrument that exists (`tools/delegation_catalog.py`): a plan whose
    authority points at nothing has authorized itself, and `DP-04 §8.2` says
    *"A Plan cannot authorize itself."*

    **There is no ``is_authorized()`` here, and adding one would be the defect.**
    Resolution proves the citation is real. It does not prove the cited
    instrument grants what the citing artifact claims — that reading is a human
    act. The corpus citation auditor makes the same disclaimer in the same words:
    *a resolved citation proves the pointer is real, not that the cited source
    supports the claim made about it.*
    """

    instrument: str
    record: str

    def __post_init__(self):
        if not isinstance(self.instrument, str) or not self.instrument.strip():
            raise InvalidGoal("an authority citation requires an instrument name")
        if not isinstance(self.record, str) or not self.record.strip():
            raise InvalidGoal("an authority citation requires a record path")
        if not (REPO_ROOT / self.record).is_file():
            raise InvalidGoal(
                f"authority record does not resolve: {self.record} — "
                "a citation to nothing is self-authorization")

    def cited(self) -> str:
        """What this artifact *claims* as its authority. Not a permission check."""
        return f"{self.instrument} ({self.record})"


@dataclass(frozen=True)
class Goal:
    """Organizational intent, decomposable into plans.

    Frozen, and carries no state. A Goal that could change would be a plan; a
    Goal that could be marked *achieved* would be reporting execution outcome,
    which belongs to Trace and Workflow rather than here.

    **Deliberately absent:** any method returning permission, and any priority,
    weight or importance field. `DP-04 §8.1` — a Goal cannot *"expand Founder
    authority"*, *"expand constitutional authority"*, *"self-authorize"*,
    *"override governance"*, *"override architecture"*, or *"create
    permissions."*
    """

    key: str
    statement: str
    authority: AuthorityProvenance

    def __post_init__(self):
        if not isinstance(self.key, str) or not self.key.strip():
            raise InvalidGoal("a goal requires a key")
        if not isinstance(self.statement, str) or not self.statement.strip():
            raise InvalidGoal("a goal requires a statement of intent")
        if not isinstance(self.authority, AuthorityProvenance):
            raise InvalidGoal("a goal requires an authority citation")
