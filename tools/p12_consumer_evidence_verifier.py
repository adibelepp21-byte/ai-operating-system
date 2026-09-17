"""`ACT-CC-P12-008 §4.1.C` — independent verification of the consumer claim.

**This module imports nothing from `tools.p12_state_verification`,** and it does
not parse Python. `§4.1.C` forbids a verifier that *"simply reproduces the same
implementation logic in a different function and calls that independence"*, so
the method here is not a second AST walk — it is **dynamic observation**:

- the surface's projection entry points are wrapped with a recorder;
- the candidate module's own function is then actually called;
- every projection call is recorded together with **whether the surface's
  declared sources were the resident ones at the moment of the call**.

That last part is the whole distinction, established by running the code rather
than by reading it. `§16` asks for *"evidence that it actually consumes the
state"*; a module that substitutes `SOURCES` and then calls `project()` is
reading its own fixture, and at the moment of the call the substitution is
directly observable. The AST measurement infers this from a `with` block's
extent. This one watches it happen. Two mechanisms with nothing in common
except the answer they must agree on.

The claim under verification is **passed in** rather than imported, which is how
this module stays independent of the one it checks. `verify()` takes the
measured consumer and importer sets and reports whether observation agrees.

`§11`: observation proves consumption, not execution by real system work. What
is driven here is the candidate's own entry point, in-process — that establishes
that the read happens when the function runs, not that any resident workflow
runs it. The two are reported separately and are not the same finding.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

SURFACE = "tools.p12_operational_state"

AGREES = "AGREES"
DISAGREES = "DISAGREES"
UNOBSERVABLE = "UNOBSERVABLE"

#: The candidate modules and the function in each that the measurement claims
#: does the reading. Named explicitly so a reader can check the pairing against
#: the source, and so this module never has to search for one.
CANDIDATES: Tuple[Tuple[str, str], ...] = (
    ("tools.p12_self_model_contract",
     "projection_freshness_is_not_source_freshness"),
    ("tools.p12_negative_control_verification", "_operational_state_projection"),
    ("tools.p12_mutation_verification", "_alter_state_authority"),
)

#: The surface's projection API, named here independently of the measurement
#: module's own constant so that a change there cannot silently narrow this.
READS: Tuple[str, ...] = ("project", "conflicts", "declares", "summary")


@dataclass
class Observation:
    module: str
    entry: str
    #: Projection calls made while `SOURCES` was the resident tuple.
    resident_reads: Tuple[str, ...] = ()
    #: Projection calls made while `SOURCES` had been substituted.
    substituted_reads: Tuple[str, ...] = ()
    error: Optional[str] = None

    @property
    def consumes(self) -> bool:
        return bool(self.resident_reads)


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def observe(module_name: str, entry: str) -> Observation:
    """Run one candidate's entry point and watch what it does to the surface."""
    from unittest import mock

    surface = importlib.import_module(SURFACE)
    resident_sources = surface.SOURCES
    resident: list = []
    substituted: list = []

    def recorder(name: str, original: Callable) -> Callable:
        def wrapped(*args, **kwargs):
            # Identity, not equality: a substituted tuple that happens to
            # compare equal is still a substitution.
            bucket = resident if surface.SOURCES is resident_sources \
                else substituted
            bucket.append(name)
            return original(*args, **kwargs)
        return wrapped

    patches = [mock.patch.object(surface, name,
                                 recorder(name, getattr(surface, name)))
               for name in READS if hasattr(surface, name)]
    observation = Observation(module_name, entry)
    try:
        module = importlib.import_module(module_name)
        function = getattr(module, entry)
        for patch in patches:
            patch.start()
        try:
            function()
        finally:
            for patch in patches:
                patch.stop()
    except Exception as exc:
        for patch in patches:
            try:
                patch.stop()
            except RuntimeError:
                pass
        observation.error = f"{type(exc).__name__}: {exc}"
        return observation
    observation.resident_reads = tuple(sorted(set(resident)))
    observation.substituted_reads = tuple(sorted(set(substituted)))
    return observation


def observations() -> Tuple[Observation, ...]:
    return tuple(observe(module, entry) for module, entry in CANDIDATES)


def _path(module_name: str) -> str:
    #: `"/".join(...)` rather than `str.replace`: the resident "this module
    #: writes nothing" control reads call names by AST and cannot tell
    #: `str.replace` from `Path.replace`. Narrowing that control to let this
    #: through would weaken a real check to accommodate a cosmetic choice.
    return "/".join(module_name.split(".")) + ".py"


def observed_consumers() -> Tuple[str, ...]:
    """Modules observed reading the surface over its **resident** sources."""
    return tuple(sorted(_path(o.module) for o in observations() if o.consumes))


def verify(claimed_consumers: Tuple[str, ...],
           claimed_importers: Tuple[str, ...]) -> Tuple[Check, ...]:
    """`§4.1.C`'s four requirements, against a claim supplied by the caller."""
    found = observations()
    checks = []

    # 1 — the previously missed AST shape is now recognized. Every candidate
    #     binds the surface through `from tools import X as y`, which is the
    #     form the superseded implementation could not see; if the claim names
    #     none of them, the correction did not take.
    candidates = {_path(module) for module, _ in CANDIDATES}
    seen = candidates & set(claimed_importers)
    checks.append(Check(
        "the missed import shape is recognized",
        AGREES if seen == candidates else DISAGREES,
        f"{len(seen)} of {len(candidates)} modules importing the surface as "
        f"`from tools import … as …` appear in the measured importer set"))

    # 2 — nothing omitted, nothing invented, judged by observation.
    observed = {_path(o.module) for o in found if o.consumes}
    unobservable = [o for o in found if o.error]
    if unobservable:
        checks.append(Check(
            "consumers are neither omitted nor invented", UNOBSERVABLE,
            f"could not run: {[(o.module, o.error) for o in unobservable]}"))
    else:
        claimed = set(claimed_consumers)
        checks.append(Check(
            "consumers are neither omitted nor invented",
            AGREES if observed == claimed else DISAGREES,
            f"observed {sorted(observed)}; measured {sorted(claimed)}"
            + (f"; omitted {sorted(observed - claimed)}" if observed - claimed
               else "")
            + (f"; invented {sorted(claimed - observed)}" if claimed - observed
               else "")))

    # 3 — a substituted read is not a consumption. This is the check that
    #     would fail if the measurement counted importers.
    fixture_only = {_path(o.module) for o in found
                    if o.substituted_reads and not o.resident_reads}
    leaked = fixture_only & set(claimed_consumers)
    checks.append(Check(
        "a substituted read is not counted",
        AGREES if not leaked else DISAGREES,
        f"observed reading only over substituted sources: {sorted(fixture_only)}"
        + (f"; wrongly counted as consumers: {sorted(leaked)}" if leaked
           else "; none of them is counted as a consumer")))

    # 4 — the surface's own near-name must not be confused with it.
    checks.append(Check(
        "a prefix name is not the surface",
        AGREES if not any("operational_state_verifier" in c
                          for c in claimed_consumers) else DISAGREES,
        "`tools.p12_operational_state_verifier` is a different module whose "
        "name contains the surface's; it is not in the measured consumer set"))
    return tuple(checks)


def summary(claimed_consumers: Tuple[str, ...],
            claimed_importers: Tuple[str, ...]) -> dict:
    checks = verify(claimed_consumers, claimed_importers)
    return {
        "checks": len(checks),
        "agrees": sum(1 for c in checks if c.status == AGREES),
        "disagrees": sum(1 for c in checks if c.status == DISAGREES),
        "unobservable": sum(1 for c in checks if c.status == UNOBSERVABLE),
        "observed_consumers": sorted(_path(o.module)
                                     for o in observations() if o.consumes),
        "not_agreeing": tuple(c.name for c in checks if c.status != AGREES),
    }


def main(argv=None) -> int:
    """Prints what was **observed**, and nothing about any claim.

    An earlier version imported `p12_state_verification` here to fetch the
    claim and print a verdict. That was a convenience, and it broke the
    independence this module's docstring asserts — caught by this Act's own
    control rather than noticed. Comparing observation against the claim is the
    caller's job, which is why `verify()` takes the claim as an argument.
    """
    import json
    found = observations()
    print(json.dumps({
        "candidates": len(found),
        "observed_consumers": list(observed_consumers()),
        "unobservable": [o.module for o in found if o.error],
    }, indent=2, default=str))
    for observation in found:
        print(f"  {observation.module}.{observation.entry}: "
              f"resident={list(observation.resident_reads)} "
              f"substituted={list(observation.substituted_reads)}"
              + (f" error={observation.error}" if observation.error else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
