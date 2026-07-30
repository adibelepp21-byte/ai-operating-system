"""
Shared cross-boundary primitives (Native Core Blueprint §16).

Holds only primitives that carry no subsystem responsibility — here, the
failure/result signaling convention used to express Fail-Closed behaviour
(PR-4) uniformly across boundaries.

Governance constraints on `shared` (Blueprint §16, enforced by construction):
  - holds NO external dependency (INV-12),
  - holds NO governance authority,
  - holds NO entity ownership,
  - is a dependency SINK: everything may import `shared`; `shared` imports
    nothing from `core`.
"""

from .result import Failure, Outcome, Success

__all__ = ["Outcome", "Success", "Failure"]
