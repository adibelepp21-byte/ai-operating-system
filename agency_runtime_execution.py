"""FR-2 (`FD-FR2-001`) — the wiring of the Runtime-hosted Agency path.

**Why this file is at the repository root.** The path needs two things that
live in mutually isolated regions: the authority side in `tools/`
(`tools/w4_runtime_execution.py`: the grant, the per-step re-check, the
Runtime, the manifest, the escalation wiring) and the Agent side in
`consumers/` (`consumers/delegated_step.py`: the participant that runs the
delegated work inside one `TracedAction`). Neither region may import the other,
so the binding lives outside both, as `w4_first_execution.py` does for W4.

It binds and decides nothing. Everything it exposes is the `tools/` function of
the same name with the resident participant supplied.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from consumers.delegated_step import DelegatedStep  # noqa: E402
from tools import w4_runtime_execution as _hosted  # noqa: E402

PARTICIPANT = DelegatedStep


def hosted_executor(delegation, registry, runtime, writer, **options):
    """`RuntimeHostedExecutor` with the resident participant."""
    return _hosted.RuntimeHostedExecutor(delegation, registry, runtime, writer,
                                         participant=PARTICIPANT, **options)


def run_hosted_plan(delegation, registry, runtime, writer, plan, perform, **options):
    """`run_hosted_plan` (the hosted run path) with the resident participant."""
    return _hosted.run_hosted_plan(delegation, registry, runtime, writer, plan, perform,
                                   participant=PARTICIPANT, **options)
