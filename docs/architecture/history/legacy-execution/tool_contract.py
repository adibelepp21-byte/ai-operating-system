"""
Tool Request/Response contract — Tier 1 Universal Tool Contract.

`tool.ToolRequest` already exists and is unchanged (source of the
Executor's input). `ToolResponse` is new: the normalized output shape
every migrated adapter returns instead of a Tool-specific dict. Not
introduced as a replacement for `Evidence` (skill.py) — per the
Architect's explicit "Do NOT redesign Evidence" — `ToolResponse` sits
strictly between a Tool Adapter and the legacy dict shape Evidence is
still built from; Evidence's own shape and meaning are untouched.

`payload` absorbs whatever is Tool-specific: cross-reference match
detail, a similarity score, a parsed structural-element list. `status`
mirrors the `resolved` boolean every existing Tool already returns,
named generically since not every future Tool's output need be
boolean-shaped.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ToolResponse:
    status: bool
    payload: dict = field(default_factory=dict)
    confidence_hint: Optional[float] = None
    failure_reason: Optional[str] = None

    def to_legacy_evidence_dict(self):
        """Produces the exact dict shape existing adapters have always
        returned (`{"resolved": ..., "evidence": ..., "failure_reason":
        ...}`), so nothing downstream of a migrated adapter needs to
        change during the transition. This is the backward-compatibility
        seam the Architect's directive requires."""
        return {
            "resolved": self.status,
            "evidence": self.payload or None,
            "failure_reason": self.failure_reason,
        }
