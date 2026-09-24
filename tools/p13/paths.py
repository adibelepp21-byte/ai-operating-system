"""Where P13 reads and where it may write (Blueprint `§3.1`, `§6`).

P13 writes its evidence only beneath `live` (`docs/operations/p13/`), the root
`P13-ENV-01` designates. Its one state-changing capability (`FDR-3`,
`P13-ENV-02`) reaches the S-OPS object beneath `s_ops`, and only through that
surface's own `transition`. Everything else here is read.

Tests keep the real tree for reading and point `live_override` at a temporary
directory. That moves the S-OPS root into the same temporary directory, so no
test writes the live root and no test can reach the real S-OPS object.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
LIVE_ROOT = "docs/operations/p13"
S_OPS_ROOT = "docs/operations/s-ops"


@dataclass(frozen=True)
class Paths:
    repo: Path
    #: Tests read the real tree and write a temporary live root.
    live_override: Optional[Path] = None

    @property
    def live(self) -> Path:
        return self.live_override or self.repo / LIVE_ROOT

    @property
    def s_ops(self) -> Path:
        """The S-OPS surface's root. Under a test's live override, it is inside
        that temporary directory, never the real one."""
        if self.live_override is not None:
            return self.live_override / "s-ops"
        return self.repo / S_OPS_ROOT

    @property
    def cycles(self) -> Path:
        return self.live / "cycles"

    @property
    def trace(self) -> Path:
        return self.live / "trace"

    @property
    def escalations(self) -> Path:
        return self.live / "escalations"

    @property
    def trace_stores(self) -> Path:
        return self.repo / "docs/architecture/p12/trace-stores"

    @property
    def knowledge_store(self) -> Path:
        return self.repo / "docs/architecture/p12/aios-runtime-store/native_core_storage"

    @property
    def envelopes(self) -> Path:
        return self.repo / "docs/governance/p13-envelopes"

    @property
    def delegation_register(self) -> Path:
        return self.repo / "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md"

    @property
    def decision_register(self) -> Path:
        return self.repo / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"

    @property
    def matrix(self) -> Path:
        return (self.repo / "docs/architecture/p13-preparation/"
                "P13-015-FOUNDATIONAL-QUESTION-RECONCILIATION.json")


LIVE = Paths(REPO_ROOT)
