"""
Review authority (governance_spec §2/§5/§10/§11; Constitution §3, §6.2 invariant 2).

Governance holds authority over decisions and the Memory→Knowledge promotion
(Freeze §8; INV-8). The single frozen rule this module enforces is the
Human-Authority boundary: a governed decision requires an explicit **human**
authority. Automation may request, recommend, and detect; it may never decide
or supply the authority for a decision (Constitution §6.2 invariant 2; PR-3).

`HumanAuthority` is a human attestation: constructing one asserts that a real
human holds the authority for a decision. The system never synthesises one on
automation's behalf and never proceeds on urgency, tooling signals, or
inferred permission — required approval must exist, explicitly, before any
governed action (§6.2 invariant 2). Authority *tiers* and *delegation scopes*
(Constitution §3.1–§3.4) are governed extension points, [O] reserved
(governance_spec §12/§13); this module fixes only the human-vs-automation
boundary that the frozen architecture makes absolute.

Fail closed (PR-4): an authority without a real reviewer identity is invalid,
and an invalid authority can authorise nothing.
"""

from __future__ import annotations

from dataclasses import dataclass


class InvalidAuthority(ValueError):
    """Raised when an authority cannot stand for a governed decision. Fail closed."""


@dataclass(frozen=True)
class HumanAuthority:
    """A human reviewer's authority to make a governed decision.

    `reviewer_id` identifies the human accountable for the decision. It must be
    a non-empty string — an anonymous or absent identity cannot hold authority
    (fail closed). Tiers/delegation are [O] reserved."""

    reviewer_id: str

    def __post_init__(self):
        if not isinstance(self.reviewer_id, str) or not self.reviewer_id.strip():
            raise InvalidAuthority("a human authority requires a non-empty reviewer identity")
