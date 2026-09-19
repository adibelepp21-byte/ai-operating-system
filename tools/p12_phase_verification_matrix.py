"""P12-W6 — the `§46` P4–P11 Verification Matrix.

`AIOS_P12_ROADMAP_PRD_CONSTRUCTION_BLUEPRINT_v1.0 §46`, verbatim:

> **For every phase:**
> ```text
> PHASE CAPABILITY INPUT OUTPUT OWNER AUTHORITY STATE INTEGRATION
> EVIDENCE VERIFICATION REGRESSION
> ```
> *"P4–P11 certification may be used as prior evidence but does not substitute
> for P12 integration verification."*

**Eleven attributes for each of eight phases, and this artifact had never been
built.** `§46` was read repeatedly — it grounds `p12_cross_phase_verification`,
it is quoted in `P12-F15-DISCOVERY.md §1`, it appears in five return packages —
and every reading took the clause that suited the question in hand. The matrix
the section actually requires was deferred in `P12-009` on the ground that
*"`E12-06` has no measurable interpretation, so nothing requires the exercise
now"*. `FD-P12-001` ratified `E12` and selected `§C = R1`; that ground is gone,
and the deferral went with it. Found by `ACT-CC-P12-016`'s hidden-requirement
search, which is what that search is for.

**Every cell is measured or `UNKNOWN`, and an `UNKNOWN` carries its reason.**
The precedent is the resident `PHASE-PD-CAPABILITY-AND-DEPENDENCY-MAP.md`, whose
own headline is that *"most answers are `UNKNOWN`, and each `UNKNOWN` is a
measurement with a stated reason"*. `§46` asks what the matrix says, not what it
would be convenient for it to say, and a cell filled by inference would make the
whole table unreadable — `UNKNOWN ≠ FALSE`, and a guess is neither.

**Two taxonomies, not one.** The canonical phase list is **not** the eleven
Native Core boundaries: `P5`, `P8`, `P10` and `P11` have no 1:1 boundary, and
`p12_cross_phase_verification` settled that *"the actual graph governs"*. So a
phase's `CAPABILITY`, `INPUT` and `OUTPUT` are read from a boundary only where
one actually corresponds, and are `UNKNOWN` — with that reason — where none
does. Inventing a correspondence to fill four rows is the conflation the
Phase–PD map exists to refuse.

**This module owns no truth and assigns nothing.** `STATE` comes from the
cross-phase verifier, `INTEGRATION` from the integration graph, `REGRESSION`
from the regression anchors, `OWNER` from the Phase–PD map — each read, none
re-derived here, and none assigned. `§11`: nothing owns what it integrates.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

#: `§46`'s eleven attributes, in its order. The order is the section's, not a
#: presentation choice, so a reader comparing the two sees the same table.
ATTRIBUTES: Tuple[str, ...] = (
    "PHASE", "CAPABILITY", "INPUT", "OUTPUT", "OWNER", "AUTHORITY", "STATE",
    "INTEGRATION", "EVIDENCE", "VERIFICATION", "REGRESSION",
)

UNKNOWN = "UNKNOWN"

#: Where a phase corresponds 1:1 to a frozen Native Core boundary. The four
#: phases absent from this map are absent because no boundary corresponds —
#: `p12_cross_phase_verification` states it and the Phase–PD map refuses the
#: inference that would supply one.
PHASE_BOUNDARY: Dict[str, str] = {
    "P4": "runtime",
    "P6": "knowledge",
    "P7": "memory",
    "P9": "workflow",
}

#: Why a phase has no boundary, stated once so every affected cell can cite it.
NO_BOUNDARY = ("no Native Core boundary corresponds 1:1 to this phase; the "
               "phase list and the eleven frozen boundaries are two taxonomies")

#: The resident map that answers `§46`'s ownership question, and answers it
#: `UNKNOWN` for every phase.
PHASE_PD_MAP = Path(
    "docs/architecture/platform-organization/"
    "PHASE-PD-CAPABILITY-AND-DEPENDENCY-MAP.md")


@dataclass(frozen=True)
class PhaseRow:
    """One phase's row. Every field is a measurement or a stated `UNKNOWN`."""

    phase: str
    capability: str
    input: str
    output: str
    owner: str
    authority: str
    state: str
    integration: str
    evidence: str
    verification: str
    regression: str

    def as_row(self) -> Tuple[str, ...]:
        return (self.phase, self.capability, self.input, self.output,
                self.owner, self.authority, self.state, self.integration,
                self.evidence, self.verification, self.regression)

    @property
    def unknown_cells(self) -> Tuple[str, ...]:
        return tuple(name for name, value in zip(ATTRIBUTES, self.as_row())
                     if value.startswith(UNKNOWN))


def _boundary_surface(boundary: str, root: Path) -> Optional[Tuple[int, Tuple[str, ...]]]:
    """A boundary's public surface count and its declared upward dependencies.

    Read by `ast` from the package's own `__init__` and modules — the boundary
    declares both, and reading them is not the same as deciding them.
    """
    package = root / "native_core" / "core" / boundary
    init = package / "__init__.py"
    if not init.is_file():
        return None
    try:
        tree = ast.parse(init.read_text(encoding="utf-8"))
    except (OSError, SyntaxError):
        return None
    exported: Tuple[str, ...] = ()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "__all__"
                for t in node.targets):
            try:
                exported = tuple(ast.literal_eval(node.value))
            except ValueError:
                exported = ()
    dependencies = set()
    for path in sorted(package.glob("*.py")):
        try:
            module = ast.parse(path.read_text(encoding="utf-8"))
        except (OSError, SyntaxError):
            continue
        for node in ast.walk(module):
            # `from ..memory import X` — level 2 leaves this package.
            if (isinstance(node, ast.ImportFrom) and node.level
                    and node.level >= 2 and node.module):
                dependencies.add(node.module.split(".")[0])
    return len(exported), tuple(sorted(dependencies))


def _owner(phase: str, root: Path) -> str:
    """`§46`'s `OWNER`, from the resident Phase–PD map.

    The map's central finding is that **zero resident sources assign a Phase to
    a PD as its provider**, and `ACT-CC-P6-071 §12` explicitly rejected deriving
    one from domain ownership. So this is `UNKNOWN` for every phase, and that is
    the measurement — `F-17` is the open Founder matter it names.
    """
    if not (root / PHASE_PD_MAP).is_file():
        return f"{UNKNOWN} — the Phase–PD map does not resolve"
    return (f"{UNKNOWN} — no resident source assigns a provider PD to a phase "
            f"({PHASE_PD_MAP.name}; F-17 Founder-reserved)")


def _authority(phase: str, root: Path) -> str:
    """The instrument that authorizes the phase, where one is resident.

    Read through `p12_phase_authorization`, which recognises a Founder
    instrument by its body. It states a state for `P12` and `P13` only; for the
    rest this is `UNKNOWN`, which is a fact about the corpus and not about the
    phases.
    """
    try:
        from tools import p12_phase_authorization as phases
        stated = {s.entity: s for s in phases.phase_states(root)}
    except Exception as exc:  # the corpus cannot be read; say so
        return f"{UNKNOWN} — phase authorization unresolved: {exc}"
    state = stated.get(phase)
    if state is None:
        return (f"{UNKNOWN} — no issued Founder instrument states an "
                f"authorization for {phase}")
    record = state.authority.record
    return f"{phase} stated in {record}"


def rows(root: Path = REPO_ROOT) -> Tuple[PhaseRow, ...]:
    """`§46`'s matrix, one row per canonical phase, measured at call time."""
    from tools import p12_cross_phase_verification as cross
    from tools import p12_e12_acceptance as acceptance
    from tools import p12_integration_graph as graph
    from tools import p12_regression_verification as regression

    exercised = {r.phase: r for r in cross.verify(root)}
    try:
        accepted = {p.phase: p for p in acceptance.phases(root)}
    except Exception:
        # No ratified boundary: the acceptance column is simply absent, and
        # saying so beats substituting a reading nobody ratified.
        accepted = {}
    edges = graph.graph()
    try:
        anchors = {a.regression_class: a for a in regression.verify()}
    except Exception:
        anchors = {}

    built = []
    for phase, name in cross.CANONICAL_PHASES:
        boundary = PHASE_BOUNDARY.get(phase)
        surface = _boundary_surface(boundary, root) if boundary else None
        if surface is None:
            capability = f"{UNKNOWN} — {NO_BOUNDARY}"
            inputs = f"{UNKNOWN} — {NO_BOUNDARY}"
            outputs = f"{UNKNOWN} — {NO_BOUNDARY}"
        else:
            exported, dependencies = surface
            capability = f"Native Core boundary {boundary!r} ({name})"
            inputs = (", ".join(dependencies) if dependencies
                      else "none — the boundary declares no upward dependency")
            outputs = f"{exported} public surface(s) exported by the boundary"

        result = exercised.get(phase)
        verdict = accepted.get(phase)
        state = (f"{result.status}"
                 + (f" · {verdict.verdict}" if verdict else "")) if result \
            else f"{UNKNOWN} — the cross-phase verifier returned no result"

        touching = tuple(e.integration_class for e in edges
                         if phase in (e.dependency, "")
                         or name.lower() in e.integration_class.lower()
                         or name.lower() in (e.source.lower(), e.target.lower()))
        integration = (", ".join(touching) if touching
                       else f"{UNKNOWN} — no declared integration class names "
                            "this phase")

        evidence = result.locator if result and result.locator else (
            f"{UNKNOWN} — no evidence locator")
        verification = (result.evidence if result
                        else f"{UNKNOWN} — no verification was performed")

        # `§46`'s `REGRESSION` column: which resident regression anchor covers
        # the evidence this row rests on, and whether it currently holds.
        anchor = _regression_for(phase, anchors)

        built.append(PhaseRow(
            phase=f"{phase} {name}",
            capability=capability,
            input=inputs,
            output=outputs,
            owner=_owner(phase, root),
            authority=_authority(phase, root),
            state=state,
            integration=integration,
            evidence=evidence,
            verification=verification,
            regression=anchor))
    return tuple(built)


#: Which regression class stands behind each phase's evidence. Named rather than
#: inferred: the anchors are a fixed resident set and guessing which one covers
#: a phase would be the inference `§46` is being read to avoid.
_REGRESSION_CLASS: Dict[str, str] = {
    "P4": "runtime", "P5": "functional", "P6": "evidence", "P7": "evidence",
    "P8": "functional", "P9": "workflow", "P10": "authority",
    "P11": "governance",
}


def _regression_for(phase: str, anchors: Dict) -> str:
    name = _REGRESSION_CLASS.get(phase)
    if name is None:
        return f"{UNKNOWN} — no regression class is declared for this phase"
    anchor = anchors.get(name)
    if anchor is None:
        return f"{UNKNOWN} — regression class {name!r} reported no result"
    return f"{name}: {anchor.status} ({anchor.anchor})"


def summary(root: Path = REPO_ROOT) -> dict:
    """What the matrix establishes, and what it leaves `UNKNOWN`."""
    built = rows(root)
    cells = len(built) * (len(ATTRIBUTES) - 1)  # PHASE names itself
    unknown = {r.phase: r.unknown_cells for r in built if r.unknown_cells}
    return {
        "phases": len(built),
        "attributes": len(ATTRIBUTES),
        "cells": cells,
        "unknown_cells": sum(len(v) for v in unknown.values()),
        "measured_cells": cells - sum(len(v) for v in unknown.values()),
        "unknown_by_phase": {k: list(v) for k, v in unknown.items()},
        "complete": not unknown,
    }


def main(argv=None) -> int:
    for row in rows():
        print(f"--- {row.phase}")
        for attribute, value in zip(ATTRIBUTES[1:], row.as_row()[1:]):
            print(f"    {attribute:<13} {value}")
    print()
    print("summary:", summary())
    print()
    print("Certification is prior evidence, not a substitute for P12")
    print("integration verification. An UNKNOWN is a measurement.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
