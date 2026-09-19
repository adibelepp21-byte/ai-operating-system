"""`ACT-CC-P12-007 §14` — independent verification of the reported phase state.

**This module imports nothing from `tools.p12_phase_authorization`.** `§14`
forbids the shape `writer → same writer helper → self-confirming verifier`, and
the resident precedent is `tools/p12_governance_join_reader.py`, which resolves
an escalation through the register and a delegation through the provenance
module rather than through the writer that produced the join. The same
discipline is applied here and is enforced structurally by
`tools/tests/test_p12_phase_authorization.py`, which reads this file's imports
by AST.

What independence buys: this module derives the Founder-stated state **from the
instrument itself, by its own parse**, and then compares that against what
`p12_self_model.authority()` reports. If the reader's section splitting, phase
matching or dimension matching is wrong, the two derivations disagree and the
check fails. A verifier that called the reader could not tell the difference
between *"the state is X"* and *"the reader says the state is X"*.

`§14` requires six things to be independently established, and there is one
check for each. The fourth is the one that matters most and the one
`AuthorityProvenance` deliberately does not do: that type's own docstring says
*"a resolved citation proves the pointer is real, not that the cited source
supports the claim made about it."* Resolution is necessary and insufficient.
`provenance supports the claim` reads the cited section of the cited file and
confirms the claimed state is actually written there — the difference between
`STATUS ≠ PROVENANCE` and `PROVENANCE ≠ AUTHORIZATION` in `§37`'s invariants.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

SATISFIED = "SATISFIED"
UNSATISFIED = "UNSATISFIED"
UNRESOLVED = "UNRESOLVED"

#: The verifier's own recognisers, deliberately written independently of the
#: reader's: this one extracts the block by locating its heading and the next
#: heading, rather than by splitting the whole instrument into sections.
_STATE_HEADING = re.compile(r"^\d+\.\s+FINAL STATE TRANSITION\s*$", re.M)
_ANY_HEADING = re.compile(r"^\d+\.\s+\S.*$", re.M)
_ISSUED_SECTION = re.compile(
    r"^\d+\.\s+FINAL FOUNDER DECISION\s*$(.*?)(?=^\d+\.\s+\S|\Z)",
    re.M | re.S)


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def _instruments(root: Path) -> Tuple[Path, ...]:
    """Issued instruments carrying a state-transition block, found this
    module's own way: a body that holds both markers, where issuance is read
    from inside the decision section so the resident stale `Status: PENDING`
    header in the preamble cannot answer for it."""
    directory = root / "docs" / "governance" / "acts"
    if not directory.is_dir():
        return ()
    found = []
    for path in sorted(directory.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if not _STATE_HEADING.search(text):
            continue
        section = _ISSUED_SECTION.search(text)
        if section and re.search(r"^Status:\s*ISSUED\s*$", section.group(1),
                                 re.M):
            found.append(path)
    return tuple(found)


def _block(text: str) -> Optional[str]:
    """The state-transition block: from its heading to the next heading."""
    heading = _STATE_HEADING.search(text)
    if heading is None:
        return None
    rest = text[heading.end():]
    following = _ANY_HEADING.search(rest)
    return rest[:following.start()] if following else rest


def stated_state(entity: str, root: Path = REPO_ROOT) -> Optional[dict]:
    """This module's own reading of one phase's stated dimensions.

    Returns `None` when no single issued instrument states anything for the
    entity — which is not the same as the entity being unauthorized.
    """
    instruments = _instruments(root)
    if len(instruments) != 1:
        return None
    block = _block(instruments[0].read_text(encoding="utf-8"))
    if block is None:
        return None
    dimensions, current = {}, None
    for raw in block.splitlines():
        line = raw.strip()
        if re.fullmatch(r"P\d+", line):
            current = line
            continue
        match = re.fullmatch(r"([A-Z][A-Z ]*[A-Z])\s*=\s*(TRUE|FALSE)", line)
        if match and current == entity:
            dimensions[match.group(1)] = match.group(2) == "TRUE"
    if current is None:
        return None
    return {"instrument": instruments[0].relative_to(root).as_posix(),
            "dimensions": dimensions} if dimensions or entity else None


def _reported(root: Path) -> dict:
    from tools import p12_self_model as model
    value = model.authority(root).value
    return value.get("phase_authorization") or {}


def verify(entity: str = "P13", root: Path = REPO_ROOT) -> Tuple[Check, ...]:
    """`§14`'s six, each established independently of the reader."""
    checks = []
    instruments = _instruments(root)
    reported = _reported(root)
    states = reported.get("states") or {}
    claim = states.get(entity) or {}
    independent = stated_state(entity, root)

    # 1 — the authoritative Founder source.
    if len(instruments) != 1:
        checks.append(Check("authoritative source", UNRESOLVED,
                            f"{len(instruments)} issued instruments carry a "
                            "state-transition block; exactly one must"))
    else:
        cited = claim.get("authority_record")
        expected = instruments[0].relative_to(root).as_posix()
        checks.append(Check(
            "authoritative source",
            SATISFIED if cited == expected else UNSATISFIED,
            f"independently found {expected}; the self-model cites {cited!r}"))

    # 2 — the current authorization state, derived here, not read from there.
    if independent is None:
        checks.append(Check("authorization state", UNRESOLVED,
                            f"no issued instrument states a state for {entity}"))
    else:
        mine = independent["dimensions"].get("AUTHORIZED")
        theirs = claim.get("authorized")
        checks.append(Check(
            "authorization state",
            SATISFIED if mine == theirs and mine is not None else UNSATISFIED,
            f"independently derived AUTHORIZED={mine}; the self-model "
            f"reports {theirs}"))

    # 3 — provenance resolves to a real file.
    record = claim.get("authority_record")
    resolves = bool(record) and (root / record).is_file()
    checks.append(Check(
        "provenance resolves", SATISFIED if resolves else UNSATISFIED,
        f"cited record {record!r} "
        f"{'resolves' if resolves else 'does not resolve'}"))

    # 4 — provenance *supports* the claim, which resolution does not establish.
    if not resolves or independent is None:
        checks.append(Check("provenance supports the claim", UNSATISFIED,
                            "cannot be established without a resolving record "
                            "and an independently derived state"))
    else:
        block = _block((root / record).read_text(encoding="utf-8"))
        dimensions = claim.get("dimensions") or {}
        written = block is not None and all(
            re.search(rf"^{re.escape(entity)}$.*?^{re.escape(name)}\s*=\s*"
                      rf"{'TRUE' if value else 'FALSE'}$",
                      block, re.M | re.S)
            for name, value in dimensions.items())
        checks.append(Check(
            "provenance supports the claim",
            SATISFIED if written and dimensions else UNSATISFIED,
            f"every reported dimension for {entity} "
            f"{'is' if written else 'is not'} written in the cited section"))

    # 5 — semantic correctness: nothing is reported that the source omits.
    if independent is None:
        checks.append(Check("no inferred dimension", UNRESOLVED,
                            "no independently derived state to compare"))
    else:
        reported_dimensions = set((claim.get("dimensions") or {}))
        invented = sorted(reported_dimensions - set(independent["dimensions"]))
        checks.append(Check(
            "no inferred dimension",
            SATISFIED if not invented else UNSATISFIED,
            "the self-model reports no dimension the Founder did not state"
            if not invented else f"invented: {invented}"))

    # 6 — resistance to a false-positive textual match.
    probe = ("A roadmap discussing P13 at length, in which P13 is named "
             "repeatedly and P13 authorization is described as future work.")
    fooled = _block(probe) is not None
    checks.append(Check(
        "false-positive resistance",
        SATISFIED if not fooled else UNSATISFIED,
        "prose naming the entity carries no state-transition block, so it "
        "yields no authorization state" if not fooled else
        "prose was accepted as a state source"))
    return tuple(checks)


def summary(entity: str = "P13", root: Path = REPO_ROOT) -> dict:
    checks = verify(entity, root)
    return {
        "entity": entity,
        "checks": len(checks),
        "satisfied": sum(1 for c in checks if c.status == SATISFIED),
        "unsatisfied": sum(1 for c in checks if c.status == UNSATISFIED),
        "unresolved": sum(1 for c in checks if c.status == UNRESOLVED),
        "not_satisfied": tuple(c.name for c in checks
                               if c.status != SATISFIED),
    }


def main(argv=None) -> int:
    import json
    print(json.dumps(summary(), indent=2, default=str))
    for check in verify():
        print(f"  {check.status:<12} {check.name}: {check.detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
