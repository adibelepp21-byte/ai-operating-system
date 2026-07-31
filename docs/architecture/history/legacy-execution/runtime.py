"""
Runtime binding.

Reads the three real Runtime instances already documented under
docs/architecture/organization/execution-catalog/runtime/ and selects
one to host a materializing Agent Instance — realizing the ratified
Runtime-hosts-Agent-Instance relationship (Domain Model §4) for an
actual execution, not just a static document citation.

Upgraded per the Execution Foundation Stabilization Phase with an
explicit selection parameter (`selector`), replacing the prior
undocumented first-match behavior: a caller (a script, or in principle
the Architect) may now name which Runtime canonical key to bind, and
binding fails loudly if that Runtime doesn't exist or doesn't declare it
may host the requested Agent Definition. Omitting `selector` keeps the
previous deterministic default (first match by filename sort order),
now stated explicitly rather than left incidental.

This is a parameter, not a scheduler: no allocation, no scoring, no
resource accounting, no Runtime Allocation Framework. Real Runtimes are
described only in the abstract by governance (Constitution §6.2
invariant 1); RuntimeDescriptor is a thin pointer back to that document,
standing in for whatever substrate a real deployment would eventually
bind to.
"""

from dataclasses import dataclass
from pathlib import Path

from .governance_reader import CATALOG_ROOT, canonical_key, read

RUNTIME_DIR = CATALOG_ROOT / "runtime"


@dataclass(frozen=True)
class RuntimeDescriptor:
    canonical_key: str
    path: Path


def available_runtimes():
    runtimes = []
    for f in sorted(RUNTIME_DIR.glob("*.md")):
        text = read(f)
        key = canonical_key(text)
        if key and "Hosts Agent Instance" in text:
            runtimes.append(RuntimeDescriptor(canonical_key=key, path=f))
    return runtimes


def bind_runtime(agent_definition_name, selector=None):
    candidates = available_runtimes()

    if selector is not None:
        for rt in candidates:
            if rt.canonical_key == selector:
                if agent_definition_name not in read(rt.path):
                    raise RuntimeError(
                        f"{selector} does not declare it may host an Agent Instance of {agent_definition_name!r}"
                    )
                return rt
        raise RuntimeError(f"no declared Runtime with canonical key {selector!r}")

    for rt in candidates:
        if agent_definition_name in read(rt.path):
            return rt
    raise RuntimeError(f"no declared Runtime hosts an Agent Instance of {agent_definition_name!r}")
