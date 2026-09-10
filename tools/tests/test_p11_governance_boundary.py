"""`P11-W7` — executable controls for the Human Governance Boundary.

`DP-01 §3 W7` authorizes construction that **preserves** the constitutional
human governance boundary, and names eight things P11 must not do. This module
is that package: **not a capability, a constraint.**

**Why this ranked ahead of the remaining capability packages.** `W1`, `W2`, `W4`
and `W5` all build organizational capability. `W7` builds the boundary that
constrains it. Building capability first and the boundary afterwards is the
ordering the Engineering Constitution `§6.2` invariant 2 exists to prevent —
*"No governance action proceeds solely because of urgency, automation, tooling
signals, inferred permission, or external pressure."* A control written after
the thing it constrains is written against a system that already works without
it.

**It also closes a gap I have flagged repeatedly and never closed.** The eight
candidate `E11` criteria measure *capability* — planning, delegation, execution,
coordination, observation, verification, escalation, accountability. **None of
them tests that the organization cannot self-authorize, that memory cannot
become authority, or that failure cannot present as completion.** `E10-06`
carried exactly that shape for P10. These tests are the P11 counterpart, offered
as evidence toward `E11` — **not as ratification of it**, which `DP-01 §20`
reserves to `DP-02` and the Founder.

**The prohibition list is read from `DP-01` itself**, not transcribed here. If
the Founder amends `W7`, ``TheProhibitionListMatchesTheInstrument`` fails until
this module is updated to match. A control that hard-codes the rule it enforces
stops being a control the moment the rule changes.

**Coverage is stated per prohibition, including where it is partial.** Four of
the eight are enforced against real structure; four are enforced against a
*representative* mechanism and are explicitly marked as such below. Claiming
eight-of-eight coverage would be the exact failure mode — *"failure presenting
as completion"* — that `W7` exists to make impossible.
"""

import ast
import re
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.governance import HumanAuthority, InvalidAuthority  # noqa: E402
from tools.delegation_catalog import read_delegations, verify  # noqa: E402
from tools.planning import (  # noqa: E402
    AuthorityProvenance,
    EscalationRequired,
    Goal,
    Plan,
    PlanStep,
    PlanningSurface,
)
from tools.tests.test_delegation_catalog import (  # noqa: E402
    _build_organization,
    _record,
)

DP01 = REPO_ROOT / "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md"
CORE = REPO_ROOT / "native_core/core"

#: The eleven frozen subsystem boundaries. Native Core Blueprint `§4`:
#: *"exactly the eleven frozen subsystem boundaries — no more"*.
FROZEN_BOUNDARIES = frozenset({
    "agent", "capability", "governance", "infrastructure", "knowledge",
    "memory", "optimization", "runtime", "skill", "trace", "workflow",
})

#: Each `W7` prohibition mapped to how it is controlled here, and **how far**.
#:
#: ``STRUCTURAL`` — enforced against the real structure of the system, so a
#: violation cannot be introduced without failing this suite.
#: ``REPRESENTATIVE`` — enforced against one mechanism that would have to break
#: first. **It does not prove the prohibition holds everywhere**, and saying so
#: is the point: an overstated control is worse than an absent one, because it
#: is counted.
COVERAGE = {
    "self-authorize": "STRUCTURAL",
    "self-expand authority": "STRUCTURAL",
    "modify Founder Reserved Authority": "REPRESENTATIVE",
    "modify constitutional boundaries": "STRUCTURAL",
    "convert operational success into authorization": "REPRESENTATIVE",
    "convert memory into authority": "STRUCTURAL",
    "convert performance evidence into authority": "REPRESENTATIVE",
    "convert delegation into authority creation": "REPRESENTATIVE",
}


def _w7_prohibitions():
    """The eight items `DP-01 §3 W7` lists, read from the instrument."""
    text = DP01.read_text(encoding="utf-8")
    block = re.search(r"^W7 — Human Governance Boundary\s*$(.*?)^§4 —",
                      text, re.M | re.S)
    if block is None:
        raise AssertionError("W7 block not found in DP-01 — the instrument moved")
    return [item.rstrip(".;").strip()
            for item in re.findall(r"^\*\s+(.+?)\s*$", block.group(1), re.M)]


def _imported_modules(path: Path):
    """Top-level module names a source file imports, via AST — not text search.

    A regex over import lines counts a module named inside a docstring or a
    comment. `INV-12`-style isolation claims are exactly where a false positive
    would be believed, so this parses.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                names.add(node.module.split(".")[-1] if node.level
                          else node.module.split(".")[0])
            elif node.level:
                names.update(alias.name.split(".")[0] for alias in node.names)
    return names


def _boundary_imports(boundary: str):
    """Every module name imported anywhere inside one frozen boundary."""
    names = set()
    for path in sorted((CORE / boundary).glob("*.py")):
        names |= _imported_modules(path)
    return names


class TheProhibitionListMatchesTheInstrument(unittest.TestCase):
    """The rule is read from `DP-01`, so it cannot drift from the rule.

    If this fails, `W7` was amended and these controls no longer describe what
    the Founder authorized. **That is a stop condition, not a test to update
    into agreement** — the correct response is to read the amended instrument
    and decide what it now requires.
    """

    def test_exactly_the_eight_prohibitions_are_covered(self):
        self.assertEqual(sorted(_w7_prohibitions()), sorted(COVERAGE))

    def test_coverage_is_declared_for_every_prohibition(self):
        for item in _w7_prohibitions():
            with self.subTest(prohibition=item):
                self.assertIn(COVERAGE[item], ("STRUCTURAL", "REPRESENTATIVE"))

    def test_partial_coverage_is_not_hidden(self):
        """Half of these are representative, and the suite says so out loud.

        Asserted rather than left implicit so that a later change cannot quietly
        relabel a representative control as structural to make the summary read
        better.
        """
        representative = {k for k, v in COVERAGE.items() if v == "REPRESENTATIVE"}
        self.assertEqual(len(representative), 4, sorted(representative))


class P11MustNotSelfAuthorize(unittest.TestCase):
    """`DP-01 §3 W7` — *"self-authorize"*. Coverage: STRUCTURAL.

    A delegation whose only authority is the record itself is the concrete form
    this prohibition takes in the organizational layer. `DP-01 §3 W3`: delegation
    *"does not authorize itself."*
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.org = Path(self._tmp.name) / "organization"
        self.org.mkdir()
        _build_organization(self.org)
        self.delegations = self.org / "delegations"
        self.delegations.mkdir()
        (Path(self._tmp.name) / "instrument.md").write_text("# x\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def _kinds(self, text):
        (self.delegations / "d.md").write_text(text, encoding="utf-8")
        return {k for k, _, _ in verify(read_delegations(self.delegations),
                                        self.org, self.delegations)}

    def test_a_delegation_citing_no_external_instrument_is_rejected(self):
        self.assertIn("authorizing-instrument-unresolvable",
                      self._kinds(_record(**{
                          "Authorizing Instrument": "Authorized under its own terms."})))

    def test_a_delegation_citing_an_instrument_that_does_not_exist_is_rejected(self):
        self.assertIn("authorizing-instrument-unresolvable",
                      self._kinds(_record(**{
                          "Authorizing Instrument": "[X](./nowhere.md)"})))

    def test_no_resident_delegation_exists_to_have_authorized_anything(self):
        self.assertEqual(read_delegations(), [])


class P11MustNotSelfExpandAuthority(unittest.TestCase):
    """`DP-01 §3 W7` — *"self-expand authority"*. Coverage: STRUCTURAL.

    Delegating a Capability the delegator does not own is authority appearing
    where none was held. Checked against the ownership graph frozen in P10.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.org = Path(self._tmp.name) / "organization"
        self.org.mkdir()
        _build_organization(self.org)
        self.delegations = self.org / "delegations"
        self.delegations.mkdir()
        (Path(self._tmp.name) / "instrument.md").write_text("# x\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_delegating_beyond_what_is_owned_is_rejected(self):
        (self.delegations / "d.md").write_text(
            _record(**{"Authorized Scope": "governance-artifact-integrity"}),
            encoding="utf-8")
        kinds = {k for k, _, _ in verify(read_delegations(self.delegations),
                                         self.org, self.delegations)}
        self.assertIn("scope-not-owned", kinds)


class AuthorityMustRemainHuman(unittest.TestCase):
    """`DP-01 §3 W7` — *"modify Founder Reserved Authority"*. Coverage: REPRESENTATIVE.

    **What is controlled:** the frozen human-vs-automation boundary in
    `native_core/core/governance/authority.py` — a governed decision requires an
    explicit human identity, and an absent one fails closed (`PR-4`).

    **What is NOT controlled:** the content of Founder Reserved sections in
    governance instruments. Nothing here prevents text being written into a
    reserved section of a document; that is held by review, not by code, and
    saying so is more useful than a test that implies otherwise.
    """

    def test_an_authority_without_a_human_identity_is_invalid(self):
        for bad in ("", "   ", None, 0):
            with self.subTest(reviewer_id=bad):
                with self.assertRaises(InvalidAuthority):
                    HumanAuthority(bad)

    def test_a_real_human_identity_is_accepted(self):
        """The mirror — without it the test above could pass on a constructor
        that rejects everything."""
        self.assertEqual(HumanAuthority("a-human").reviewer_id, "a-human")


class ConstitutionalBoundariesMustNotChange(unittest.TestCase):
    """`DP-01 §3 W7` — *"modify constitutional boundaries"*. Coverage: STRUCTURAL.

    `DP-01 §4`: **`NO NEW NATIVE CORE SUBSYSTEM OR ENTITY #12 IS AUTHORIZED`**.
    The same section states that *"The existing Native Core remains at:"* —
    **`11 frozen subsystem boundaries`** — the figure standing on its own line
    beneath, quoted here as two fragments rather than joined into one sentence
    the instrument does not contain.
    """

    def test_the_core_holds_exactly_the_eleven_frozen_boundaries(self):
        present = {p.name for p in CORE.iterdir()
                   if p.is_dir() and not p.name.startswith("__")}
        self.assertEqual(present, set(FROZEN_BOUNDARIES))

    def test_the_p11_organizational_layer_lives_outside_the_core(self):
        """`DP-04 §8.3` places Delegation outside the frozen Native Core."""
        for boundary in sorted(FROZEN_BOUNDARIES):
            with self.subTest(boundary=boundary):
                self.assertFalse((CORE / boundary / "delegation.py").exists())


class MemoryMustNotBecomeAuthority(unittest.TestCase):
    """`DP-01 §3 W7` — *"convert memory into authority"*. Coverage: STRUCTURAL.

    `DP-01 §3 W5`: **`MEMORY ≠ AUTHORITY`**, and *"No memory mechanism may
    create, elevate, or infer authority that has not otherwise been granted."*
    `INV-8` routes Memory→Knowledge only through governed promotion.

    The structural form: **Governance imports Memory; Memory must not import
    Governance.** If Memory could reach Governance, a memory record could
    participate in producing a decision.
    """

    def test_memory_does_not_import_governance(self):
        self.assertNotIn("governance", _boundary_imports("memory"))

    def test_governance_does_import_memory(self):
        """The direction is asserted in both directions, so the test above
        cannot pass merely because neither boundary imports anything."""
        self.assertIn("memory", _boundary_imports("governance"))


class ObservationMustNotBecomeAuthorization(unittest.TestCase):
    """`DP-01 §3 W7` — *"convert operational success into authorization"* and
    *"convert performance evidence into authority"*. Coverage: REPRESENTATIVE.

    **What is controlled:** Optimization's inverted dependency. Its boundary
    states *"It depends on Governance in no way"*, so that *"automation cannot
    acquire a decision path"*. `DP-03 §8.3` confirms `W6` Performance in this
    same surface as **`DETECT-ONLY`**, and holds the prioritization, ranking and
    decision-heuristic frontier reserved.

    **What is NOT controlled:** that no future consumer reads a publication and
    treats it as a decision. The boundary prevents Optimization from reaching
    Governance; it cannot prevent a reader elsewhere from misusing what it
    publishes. That remains a review obligation.
    """

    def test_optimization_does_not_import_governance(self):
        self.assertNotIn("governance", _boundary_imports("optimization"))

    def test_no_subsystem_imports_optimization(self):
        """No inversion, no cycle — so nothing can pull a decision path back in."""
        for boundary in sorted(FROZEN_BOUNDARIES - {"optimization"}):
            with self.subTest(boundary=boundary):
                self.assertNotIn("optimization", _boundary_imports(boundary))

    def test_the_reserved_scoring_frontier_is_still_unimplemented(self):
        """`DP-03 §8.3`: prioritization / ranking / decision-heuristic
        capabilities remain reserved. A scoring surface appearing inside a
        detect-only boundary is how *"performance evidence"* becomes authority."""
        reserved = ("rank", "score", "prioriti", "recommend", "heuristic")
        found = []
        for path in sorted((CORE / "optimization").glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                     ast.ClassDef)):
                    lowered = node.name.lower()
                    if any(word in lowered for word in reserved):
                        found.append(f"{path.name}:{node.name}")
        self.assertEqual(found, [], f"reserved scoring surface appeared: {found}")


class DelegationMustNotCreateAuthority(unittest.TestCase):
    """`DP-01 §3 W7` — *"convert delegation into authority creation"*.
    Coverage: REPRESENTATIVE.

    **What is controlled:** the organizational delegation layer holds no
    resident record, and the frozen core holds no delegation implementation, so
    there is currently no delegation anywhere that could create authority.

    **What is NOT controlled:** the semantics of a delegation record that does
    not yet exist. The checks in `tools/delegation_catalog.py` are what will
    constrain the first one; this asserts only that none has appeared.
    """

    def test_the_resident_delegation_population_is_empty(self):
        self.assertEqual(read_delegations(), [])

    def test_the_core_defines_no_delegation_class(self):
        found = []
        for path in sorted(CORE.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and "delegation" in node.name.lower():
                    found.append(f"{path.relative_to(CORE)}:{node.name}")
        self.assertEqual(found, [], f"delegation entered the frozen core: {found}")


PLANNING = REPO_ROOT / "tools" / "planning"

#: Every P11 organizational-layer surface across which authority may travel.
#:
#: Declared as a set rather than a directory because **the directory was the
#: bug**. `ACT-CC-P11-006` fixed two forgeable authority fields inside
#: `tools/planning/` and generalized the control — but only over that package.
#: `ACT-CC-P11-007 §8` requires the control to cover *"the class of defect
#: rather than one known instance"*, and a probe proved it did not: adding an
#: ``authority_cited: str`` field to `tools/performance_evidence.py`, a genuine
#: P11 handoff surface, produced **no failure at all**.
#:
#: The membership guard below is what keeps this honest. A hand-maintained list
#: rots the moment someone adds a surface and forgets it — which is the same
#: failure one level up.
P11_SURFACES = (
    REPO_ROOT / "tools" / "planning",
    REPO_ROOT / "tools" / "performance_evidence.py",
    # Declared because the completeness guard below caught it, not because it was
    # remembered. `ACT-CC-P11-007` created this surface and the guard failed on
    # the same run — which is the whole argument for having written the guard
    # rather than the lesson.
    REPO_ROOT / "tools" / "escalation_register.py",
    REPO_ROOT / "tools" / "planning_continuity.py",
)


def _p11_modules():
    """Every module on a declared P11 surface."""
    for surface in P11_SURFACES:
        if surface.is_dir():
            yield from sorted(surface.glob("*.py"))
        elif surface.is_file():
            yield surface


class TheBoundaryAlsoConstrainsCapabilityBuiltAfterIt(unittest.TestCase):
    """`ACT-CC-P11-006 §15` — W7 must hold against newly constructed capability.

    **When this class was written, it did not.** W7 was built before W2 and did
    not import the planning surface, so every control here described a system in
    which Planning did not exist. A governance boundary that only constrains the
    capability present when it was written stops being a boundary the moment the
    next package lands — and `§15` says plainly: *"Do not weaken W7 to enable
    capability."* The inverse obligation is this class.
    """

    def _surface(self):
        surface = PlanningSurface()
        authority = AuthorityProvenance(
            "DP-01 §3 W2",
            "docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md")
        surface.declare(Goal("g", "Intent.", authority))
        plan = surface.adopt(Plan(
            key="p", goal_key="g", authority=authority,
            steps=(PlanStep("a", "A.", requires_delegation=True),)))
        return surface, plan

    def test_the_planning_surface_grants_no_permission(self):
        """`W7`: *"self-authorize"*, applied to the newest capability."""
        offenders = []
        for path in sorted(PLANNING.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                     ast.ClassDef)):
                    if any(v in node.name.lower() for v in
                           ("authorize", "authorise", "approve", "permit",
                            "grant")):
                        offenders.append(f"{path.name}:{node.name}")
        self.assertEqual(offenders, [])

    def test_a_history_of_successful_planning_authorizes_nothing(self):
        """`W7`: *"convert operational success into authorization"*.

        The W2 suite asserts this from inside Planning. Asserted here too,
        because the prohibition belongs to the governance boundary and must not
        depend on the constrained package testing itself.
        """
        surface, plan = self._surface()
        current = plan
        for i in range(5):
            current = surface.adapt(current, steps=current.steps,
                                    reason=f"Successful change {i}.")
        with self.assertRaises(EscalationRequired):
            surface.adapt(current, steps=current.steps, reason="Now?",
                          required_authority="DP-02")

    def test_planning_cannot_convert_a_plan_into_a_delegation(self):
        """`W7`: *"convert delegation into authority creation"*."""
        surface, plan = self._surface()
        requirement = surface.delegation_requirements(plan)[0]
        with self.assertRaises(NotImplementedError):
            requirement.as_delegation_record()
        self.assertEqual(read_delegations(), [])

    def test_the_declared_p11_surface_set_is_complete(self):
        """A surface missing from the list is a surface nothing checks.

        Any module under `tools/` that imports the planning package participates
        in a P11 handoff and must be declared. Without this, the provenance
        control silently narrows every time a new surface is added — which is
        exactly how it came to miss `performance_evidence.py`.
        """
        declared = {p.resolve() for p in _p11_modules()}
        undeclared = []
        for path in sorted((REPO_ROOT / "tools").rglob("*.py")):
            if "tests" in path.parts or path.resolve() in declared:
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module \
                        and "planning" in node.module:
                    undeclared.append(str(path.relative_to(REPO_ROOT)))
                    break
        self.assertEqual(undeclared, [],
                         f"P11 handoff surfaces not declared: {undeclared}")

    def test_every_authority_field_crossing_a_boundary_is_a_verified_citation(self):
        """The generalization of a defect, not a patch for one instance.

        `ACT-CC-P11-006 §17` found that both P11 handoff types carried
        ``authority_cited: str`` — a **validated citation flattened into free
        text** at the moment authority crossed a boundary. Anything could be
        constructed saying anything, and no consumer could tell it from a
        genuine handoff.

        Fixing the two instances would leave the *class* of defect open, and the
        next handoff type would reintroduce it. So this asserts the rule: **any
        field named for authority, on any type in the planning package, must be
        annotated `AuthorityProvenance`** — the type that refuses a record which
        does not resolve. A `str` there is unverifiable provenance, and
        unverifiable provenance is fabricated provenance.
        """
        offenders = []
        for path in sorted(_p11_modules()):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not isinstance(node, ast.ClassDef):
                    continue
                for item in node.body:
                    if not (isinstance(item, ast.AnnAssign)
                            and isinstance(item.target, ast.Name)):
                        continue
                    if not item.target.id.lower().startswith("authority"):
                        continue
                    annotation = ast.unparse(item.annotation)
                    if "AuthorityProvenance" not in annotation:
                        offenders.append(
                            f"{path.name}:{node.name}.{item.target.id}"
                            f": {annotation}")
        self.assertEqual(offenders, [], f"unverifiable provenance: {offenders}")


class WhatThisSuiteDoesNotEstablish(unittest.TestCase):
    """Stated as a test so it is read, and so it cannot be quietly dropped.

    `DP-01 §13`: authorization is **not** construction, operational, verified,
    exhausted, complete or certified. Passing this suite establishes that eight
    named prohibitions have controls, four of them representative. **It does not
    establish that P11 is constructed, that `E11` is met, or that the
    organization is safe to operate autonomously.** `DP-01 §20` reserves `E11`
    ratification to `DP-02` and the Founder.
    """

    def test_p11_is_not_claimed_constructed(self):
        """One of seven work packages has a mechanism, and it has no population."""
        self.assertEqual(read_delegations(), [])

    def test_the_representative_controls_are_named_not_merely_counted(self):
        """Relabeling a control must require editing this list, visibly.

        My first version of this test scanned the module's own source for the
        string it was asserting absent — which the assertion itself contained,
        so it could never pass. It was a gimmick, not a control: it constrained
        nothing and would have read as coverage. Replaced with the set that
        actually matters, spelled out, so that promoting a REPRESENTATIVE
        control to STRUCTURAL shows up as a diff on a named line rather than as
        a count that still says four.
        """
        self.assertEqual(
            {k for k, v in COVERAGE.items() if v == "REPRESENTATIVE"},
            {
                "modify Founder Reserved Authority",
                "convert operational success into authorization",
                "convert performance evidence into authority",
                "convert delegation into authority creation",
            },
        )

    def test_no_prohibition_is_left_without_a_declared_limit(self):
        """Every prohibition carries one of exactly two coverage labels, and
        neither of them means *proven everywhere*."""
        self.assertEqual(set(COVERAGE.values()), {"STRUCTURAL", "REPRESENTATIVE"})
        self.assertEqual(len(COVERAGE), 8)


if __name__ == "__main__":
    unittest.main()
