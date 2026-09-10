"""Tests for the delegation catalog — the first P11 construction step.

`FD-P10-003 §17`: *"No evidence means no completion claim."* The same rule
applies to P11, and it applies hardest here, because this module's resident
population is **empty**. A loader that reads nothing returns no defects, and
"zero defects" from an empty corpus is not evidence of anything.

So every defect class below is proven able to fire against a fixture built in a
temporary directory. `DP-01 §16` binds construction to surfacing conflicts
rather than resolving them silently; a check that has never failed cannot
surface anything.
"""

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.delegation_catalog import (  # noqa: E402
    DELEGATION_ROOT,
    REQUIRED_SECTIONS,
    read_delegations,
    report,
    verify,
)
from tools.organization_catalog import (  # noqa: E402
    NON_DEPARTMENT_DIRS,
    ORGANIZATION_ROOT,
    read_departments,
)

#: A fixture organization: two Departments, each owning one Capability, one of
#: them with an Agent Definition. Deliberately mirrors the resident shape so the
#: cross-checks exercise the same code path the real corpus would.
FIXTURE = {
    "engineering": {
        "capabilities": ["engineering-intelligence"],
        "agent-definitions": ["engineering-intelligence-agent"],
    },
    "platform": {
        "capabilities": ["governance-artifact-integrity"],
        "agent-definitions": [],
    },
}


def _build_organization(root: Path) -> None:
    for key, spec in FIXTURE.items():
        directory = root / key
        directory.mkdir(parents=True)
        (directory / "README.md").write_text(
            f"# {key.title()}\n\n## Name\n\n{key.title()}\n\n"
            f"This Department was established by [ADR-0008](../../adr/x.md).\n",
            encoding="utf-8")
        for kind, keys in spec.items():
            if not keys:
                continue
            sub = directory / kind
            sub.mkdir()
            for name in keys:
                (sub / f"{name}.md").write_text(
                    f"# {name}\n\n## Owner\n\n{key.title()}\n\n"
                    f"## Owning Department\n\n{key.title()}\n\n"
                    f"## Implemented Capability\n\n{spec['capabilities'][0]}\n\n"
                    f"Established by [ADR-0008](../../../adr/x.md).\n",
                    encoding="utf-8")


def _record(**overrides) -> str:
    """A delegation record that is **valid**, with named fields overridden.

    The positive control is written once and mutated per test, so a test that
    fails proves the *override* caused it. If the base record were rebuilt by
    hand for each case, a typo would look like the defect under test.
    """
    fields = {
        "Authority Source": "engineering",
        "Authorized Scope": "engineering-intelligence",
        "Delegated Actor": "engineering-intelligence-agent",
        "Boundary": "Bounded to the named Capability. Creates no new authority.",
        "Accountability": "engineering",
        "Verification": "See [the mechanism](../../instrument.md).",
        "Authorizing Instrument": "[DP-01](../../instrument.md) §3 W3.",
    }
    fields.update({k: v for k, v in overrides.items() if v is not None})
    dropped = {k for k, v in overrides.items() if v is None}
    body = "# A delegation\n\n"
    for heading in REQUIRED_SECTIONS:
        if heading in dropped:
            continue
        body += f"## {heading}\n\n{fields[heading]}\n\n"
    return body


class _Fixture(unittest.TestCase):
    """Builds an organization and a delegations directory in a temp tree."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.org = Path(self._tmp.name) / "organization"
        self.org.mkdir()
        _build_organization(self.org)
        self.delegations = self.org / "delegations"
        self.delegations.mkdir()
        # The target the positive control's two pointers resolve to. It lives in
        # the fixture tree, not the repository, so these tests stay hermetic:
        # a resolvable pointer must not depend on a real file that some later
        # change could move out from under them.
        (Path(self._tmp.name) / "instrument.md").write_text(
            "# Fixture instrument\n", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def defects(self, text: str, name: str = "d1.md"):
        (self.delegations / name).write_text(text, encoding="utf-8")
        records = read_delegations(self.delegations)
        return verify(records, self.org, self.delegations)

    def kinds(self, text: str, name: str = "d1.md"):
        return sorted({kind for kind, _, _ in self.defects(text, name)})


class ThePositiveControlPasses(_Fixture):
    """Without this, every negative control below could pass for the wrong reason.

    A fixture that never validates makes every "defect detected" result
    meaningless — the checks would be firing on the fixture's own breakage
    rather than on the property under test.
    """

    def test_a_well_formed_delegation_produces_no_defects(self):
        self.assertEqual(self.defects(_record()), [])

    def test_it_is_read_as_one_record_with_its_fields_resolved(self):
        (self.delegations / "d1.md").write_text(_record(), encoding="utf-8")
        records = read_delegations(self.delegations)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].authority_source, "engineering")
        self.assertEqual(records[0].authorized_scope, "engineering-intelligence")
        self.assertEqual(records[0].delegated_actor, "engineering-intelligence-agent")


class DelegationCannotCreateAuthority(_Fixture):
    """`DP-04 §8.3` — delegation *"does not create authority"*.

    **This is the load-bearing test of the increment.** Everything else in this
    module is structure; this is the one that makes a delegation record a
    governed relation rather than a place to write claims.
    """

    def test_delegating_a_capability_the_source_does_not_own_fails(self):
        # Platform owns governance-artifact-integrity. Engineering does not.
        kinds = self.kinds(_record(**{
            "Authorized Scope": "governance-artifact-integrity"}))
        self.assertIn("scope-not-owned", kinds)

    def test_the_same_capability_delegated_by_its_actual_owner_passes(self):
        """The mirror. Without it, the test above could be failing on the
        Capability's *name* rather than on ownership."""
        kinds = self.kinds(_record(**{
            "Authority Source": "platform",
            "Authorized Scope": "governance-artifact-integrity",
            "Delegated Actor": "engineering",
            "Accountability": "platform",
        }))
        self.assertNotIn("scope-not-owned", kinds)

    def test_an_unestablished_authority_source_fails(self):
        kinds = self.kinds(_record(**{"Authority Source": "marketing"}))
        self.assertIn("authority-source-unknown", kinds)

    def test_an_unknown_delegated_actor_fails(self):
        kinds = self.kinds(_record(**{"Delegated Actor": "nobody-in-particular"}))
        self.assertIn("actor-unknown", kinds)


class DelegationCannotTransferUltimateAccountability(_Fixture):
    """`DP-04 §8.3` and `DP-01 §3 W3`, both explicit.

    Tested structurally: the record names who remains accountable, and that name
    is compared against the delegate. No prose is matched, so no wording can
    satisfy it.
    """

    def test_naming_the_delegate_as_accountable_fails(self):
        kinds = self.kinds(_record(**{
            "Accountability": "engineering-intelligence-agent"}))
        self.assertIn("accountability-transferred", kinds)

    def test_naming_the_delegator_as_accountable_passes(self):
        kinds = self.kinds(_record(**{"Accountability": "engineering"}))
        self.assertNotIn("accountability-transferred", kinds)


class DelegationCannotAuthorizeItself(_Fixture):
    """`DP-04 §8.3` — *"does not authorize itself"*, repeated in `DP-01 §3 W3`.

    A record with no pointer outside itself is self-authorizing. The check is
    resolution, not presence: a link to a file that does not exist is a pointer
    to nothing, which is the rule the corpus citation audit applies everywhere
    else in this repository.
    """

    def test_a_missing_authorizing_instrument_fails(self):
        kinds = self.kinds(_record(**{"Authorizing Instrument": None}))
        self.assertIn("missing-section", kinds)

    def test_an_authorizing_instrument_naming_no_pointer_fails(self):
        kinds = self.kinds(_record(**{
            "Authorizing Instrument": "Authorized under my own terms."}))
        self.assertIn("authorizing-instrument-unresolvable", kinds)

    def test_an_authorizing_instrument_pointing_at_nothing_fails(self):
        kinds = self.kinds(_record(**{
            "Authorizing Instrument": "[DP-01](./does-not-exist.md)"}))
        self.assertIn("authorizing-instrument-unresolvable", kinds)

    def test_an_unresolvable_verification_fails(self):
        kinds = self.kinds(_record(**{
            "Verification": "See [nothing](./absent.md)."}))
        self.assertIn("verification-unresolvable", kinds)


class ANullDelegationIsSeen(_Fixture):
    """A unit delegating to itself creates no boundary while presenting as one.

    It is indistinguishable in the record from an authority assertion, which is
    what `DP-04 §8.3`'s *"does not create authority"* forbids.
    """

    def test_self_delegation_fails(self):
        kinds = self.kinds(_record(**{
            "Delegated Actor": "engineering", "Accountability": "platform"}))
        self.assertIn("self-delegation", kinds)


class TheFixedShapeIsRequiredInFull(_Fixture):
    """`DP-04 §8.3` fixes six elements; the seventh enforces its own clause."""

    def test_every_required_section_is_individually_required(self):
        for heading in REQUIRED_SECTIONS:
            with self.subTest(heading=heading):
                kinds = self.kinds(_record(**{heading: None}), name="d2.md")
                self.assertIn("missing-section", kinds)

    def test_a_present_but_empty_section_is_a_different_defect(self):
        """Absent and empty must not collapse: a record could otherwise satisfy
        the shape while saying nothing."""
        kinds = self.kinds(_record(**{"Boundary": ""}))
        self.assertIn("empty-section", kinds)
        self.assertNotIn("missing-section", kinds)


class TheResidentPopulationIsEmptyAndSaysSo(unittest.TestCase):
    """The honest count, asserted rather than assumed.

    If a delegation record ever appears here, this test fails loudly — which is
    correct. Authoring one is an exercise of the authority being delegated, and
    this executor holds none of it. A record arriving silently is precisely the
    event that should stop a run.
    """

    def test_no_delegation_record_is_resident(self):
        self.assertEqual(read_delegations(), [], "a delegation record appeared")

    def test_the_report_says_the_population_is_empty(self):
        self.assertTrue(report()["population_empty"])

    def test_the_readme_is_not_read_as_a_delegation(self):
        self.assertTrue((DELEGATION_ROOT / "README.md").is_file())
        self.assertEqual([r.key for r in read_delegations()], [])

    def test_zero_defects_here_is_not_evidence_of_a_working_check(self):
        """States the limit rather than leaving the empty result to imply health.

        The defect count over the resident corpus is 0 because the corpus is
        empty. The classes above are what make that 0 meaningful.
        """
        self.assertEqual(report()["defects"], [])
        self.assertEqual(read_delegations(), [])


class TheDelegationsDirectoryIsNotADepartment(unittest.TestCase):
    """It carries a README with an H1 — the exact shape the P10 loader reads.

    Creating this directory made `test_no_directory_is_left_unaccounted_for`
    fail on the run that created it, before any README existed. Had the
    exclusion not been added, the first P11 construction step would have
    introduced an **unauthorized Department** — `FD-P10-004 §5` condition 3
    failing silently, by a directory nobody declared.
    """

    def test_it_is_explicitly_excluded(self):
        self.assertIn("delegations", NON_DEPARTMENT_DIRS)

    def test_it_does_not_appear_in_the_department_population(self):
        self.assertNotIn("delegations", {r.key for r in read_departments()})

    def test_it_would_otherwise_have_been_read_as_one(self):
        """The exclusion is load-bearing, not decorative — proven by removing it.

        A `README.md` with a resolvable name is all `read_departments` requires.
        This asserts the directory really does have that shape, so the exclusion
        is protecting against a live condition rather than a hypothetical.
        """
        readme = ORGANIZATION_ROOT / "delegations" / "README.md"
        self.assertTrue(readme.is_file())
        first = readme.read_text(encoding="utf-8").split("\n")[0]
        self.assertTrue(first.startswith("# "), first)


if __name__ == "__main__":
    unittest.main()
