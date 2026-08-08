"""
Regression tests for tools/bounded_exception/.

Standard library only (unittest) — no test dependency is added to the
repository. Every registration fixture is synthetic and built in a
temporary directory, including the governance registers that provenance
resolves against, so provenance enforcement is exercised without
creating any real governance entry (P7-I52 §9).

The real P7-F-2 sites are never used as registration fixtures. One
guard test asserts that the shipped register neither declares a scan
scope nor registers anything, which is what keeps MB-01 from touching
frozen Baseline 04A.

Run with:
    python3 -m unittest discover -s tools/bounded_exception/tests -t .
"""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.bounded_exception import identity, verifier
from tools.bounded_exception.provenance import (
    ProvenanceResolver,
    RegisterFileProvenance,
    authorizing_act_is_well_formed,
)
from tools.bounded_exception.register import load_register

FINDING = "P9-F-9"
DECISION = "GDR-9999"
ACT = "P9-I99"

SOURCE_ONE_SITE = '''
class Widget:
    def build(self):
        raise WidgetError(["a", "b"])
'''

SOURCE_TWO_SITES = '''
class Widget:
    def build(self):
        raise WidgetError(["a"])
        raise WidgetError(["b"])
'''

SOURCE_NO_SITE = '''
class Widget:
    def build(self):
        raise WidgetError("a plain message")
'''


class _AlwaysResolves(ProvenanceResolver):
    def finding_exists(self, finding_id):
        return True

    def decision_exists(self, decision_id):
        return True


class _NeverResolves(ProvenanceResolver):
    def finding_exists(self, finding_id):
        return False

    def decision_exists(self, decision_id):
        return False


class _Fixture:
    """A synthetic repository root with a source tree and a register."""

    def __init__(self):
        self.root = Path(tempfile.mkdtemp())
        (self.root / "pkg").mkdir()

    def write_source(self, text, name="mod.py"):
        (self.root / "pkg" / name).write_text(text, encoding="utf-8")

    def write_register(self, payload):
        path = self.root / "register.json"
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return path

    def write_raw_register(self, text):
        path = self.root / "register.json"
        path.write_text(text, encoding="utf-8")
        return path

    def cleanup(self):
        shutil.rmtree(self.root, ignore_errors=True)


def _entry(path="pkg/mod.py", qualname="Widget.build", exception="WidgetError", ordinal=0, **over):
    entry = {
        "identity": {
            "path": path,
            "qualname": qualname,
            "exception": exception,
            "ordinal": ordinal,
        },
        "category": "container-arg-halt",
        "rationale": "recorded for test purposes",
        "finding_id": FINDING,
        "governance_decision_id": DECISION,
        "authorizing_act": ACT,
    }
    entry.update(over)
    return entry


def _register(entries=(), scope=True):
    return {
        "version": 1,
        "scan_scope": [{"root": "pkg", "detector": "container_arg_raise"}] if scope else [],
        "entries": list(entries),
    }


class VerifierTest(unittest.TestCase):
    def setUp(self):
        self.fx = _Fixture()
        self.addCleanup(self.fx.cleanup)
        self.provenance = _AlwaysResolves()

    def verify(self, register_path):
        return verifier.verify(register_path, self.fx.root, self.provenance)

    def kinds(self, failures):
        return sorted({f.kind for f in failures})

    # 1 — empty register is valid
    def test_empty_register_is_valid(self):
        self.fx.write_source(SOURCE_NO_SITE)
        path = self.fx.write_register({"version": 1, "scan_scope": [], "entries": []})
        self.assertEqual(self.verify(path), ())

    # 2 — a valid registered site passes
    def test_registered_site_passes(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        path = self.fx.write_register(_register([_entry()]))
        self.assertEqual(self.verify(path), ())

    # 3 — an unregistered site fails
    def test_unregistered_site_fails(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        path = self.fx.write_register(_register())
        self.assertEqual(self.kinds(self.verify(path)), [verifier.UNREGISTERED_SITE])

    # 4 — a registered-but-absent site fails
    def test_registered_but_absent_site_fails(self):
        self.fx.write_source(SOURCE_NO_SITE)
        path = self.fx.write_register(_register([_entry()]))
        self.assertEqual(self.kinds(self.verify(path)), [verifier.ABSENT_REGISTERED_SITE])

    # 5 — duplicate identity fails
    def test_duplicate_identity_fails(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        path = self.fx.write_register(_register([_entry(), _entry()]))
        self.assertIn(verifier.DUPLICATE_IDENTITY, self.kinds(self.verify(path)))

    # 6 — malformed entries fail
    def test_malformed_register_fails(self):
        self.fx.write_source(SOURCE_NO_SITE)
        for payload in (
            "{not json",
            json.dumps({"version": 2, "scan_scope": [], "entries": []}),
            json.dumps({"version": 1, "entries": []}),
            json.dumps({"version": 1, "scan_scope": [], "entries": [], "extra": 1}),
        ):
            with self.subTest(payload=payload[:24]):
                path = self.fx.write_raw_register(payload)
                self.assertEqual(
                    self.kinds(self.verify(path)), [verifier.MALFORMED_REGISTER]
                )

    def test_entry_with_unknown_field_is_malformed(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        path = self.fx.write_register(_register([_entry(surprise="x")]))
        self.assertEqual(self.kinds(self.verify(path)), [verifier.MALFORMED_REGISTER])

    def test_entry_missing_required_field_is_malformed(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        entry = _entry()
        del entry["rationale"]
        path = self.fx.write_register(_register([entry]))
        self.assertEqual(self.kinds(self.verify(path)), [verifier.MALFORMED_REGISTER])

    # 7 — unauthorized growth is rejected
    def test_entry_outside_declared_scope_is_unauthorized_expansion(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        payload = _register([_entry(), _entry(path="elsewhere/other.py")])
        path = self.fx.write_register(payload)
        self.assertIn(verifier.UNAUTHORIZED_EXPANSION, self.kinds(self.verify(path)))

    def test_empty_scope_with_entry_is_unauthorized_expansion(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        path = self.fx.write_register(_register([_entry()], scope=False))
        self.assertIn(verifier.UNAUTHORIZED_EXPANSION, self.kinds(self.verify(path)))

    # 8 — provenance is enforced
    def test_unresolvable_provenance_fails(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        path = self.fx.write_register(_register([_entry()]))
        failures = verifier.verify(path, self.fx.root, _NeverResolves())
        self.assertIn(verifier.UNRESOLVED_PROVENANCE, self.kinds(failures))

    def test_malformed_authorizing_act_fails(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        path = self.fx.write_register(_register([_entry(authorizing_act="whenever")]))
        self.assertIn(verifier.UNRESOLVED_PROVENANCE, self.kinds(self.verify(path)))

    def test_provenance_resolves_against_synthetic_registers(self):
        findings = self.fx.root / "findings.md"
        decisions = self.fx.root / "decisions.md"
        findings.write_text(f"### {FINDING} — a synthetic finding\n", encoding="utf-8")
        decisions.write_text(f"### {DECISION} — a synthetic decision\n", encoding="utf-8")
        resolver = RegisterFileProvenance(findings, decisions)
        self.assertTrue(resolver.finding_exists(FINDING))
        self.assertTrue(resolver.decision_exists(DECISION))
        self.assertFalse(resolver.finding_exists("P9-F-8"))
        self.assertFalse(resolver.decision_exists("GDR-999"))

    def test_missing_provenance_file_resolves_to_failure(self):
        resolver = RegisterFileProvenance(
            self.fx.root / "absent.md", self.fx.root / "absent.md"
        )
        self.assertFalse(resolver.finding_exists(FINDING))
        self.assertFalse(resolver.decision_exists(DECISION))

    def test_authorizing_act_pattern(self):
        self.assertTrue(authorizing_act_is_well_formed("P7-I52"))
        self.assertFalse(authorizing_act_is_well_formed("P7I52"))
        self.assertFalse(authorizing_act_is_well_formed(""))


class IdentityTest(unittest.TestCase):
    def setUp(self):
        self.fx = _Fixture()
        self.addCleanup(self.fx.cleanup)

    def discover(self):
        return identity.discover_sites(
            self.fx.root / "pkg", "container_arg_raise", self.fx.root
        )

    def test_line_number_is_not_part_of_identity(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        before = self.discover()[0]
        self.fx.write_source("# a new comment line\n" + SOURCE_ONE_SITE)
        after = self.discover()[0]
        self.assertEqual(before.identity, after.identity)
        self.assertNotEqual(before.line, after.line)

    def test_ordinals_are_assigned_in_source_order_within_scope(self):
        self.fx.write_source(SOURCE_TWO_SITES)
        sites = self.discover()
        self.assertEqual([s.identity.ordinal for s in sites], [0, 1])
        self.assertEqual({s.identity.qualname for s in sites}, {"Widget.build"})

    def test_moving_a_site_changes_its_identity(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        before = self.discover()[0].identity
        self.fx.write_source(SOURCE_ONE_SITE.replace("def build", "def assemble"))
        after = self.discover()[0].identity
        self.assertNotEqual(before, after)

    def test_plain_message_is_not_a_site(self):
        self.fx.write_source(SOURCE_NO_SITE)
        self.assertEqual(self.discover(), ())

    def test_discovery_is_deterministic(self):
        self.fx.write_source(SOURCE_TWO_SITES)
        self.fx.write_source(SOURCE_TWO_SITES, name="other.py")
        self.assertEqual(self.discover(), self.discover())

    def test_unknown_detector_is_rejected(self):
        self.fx.write_source(SOURCE_ONE_SITE)
        with self.assertRaises(KeyError):
            identity.discover_sites(self.fx.root / "pkg", "no_such_detector", self.fx.root)


class ShippedRegisterGuardTest(unittest.TestCase):
    """MB-01 ships the register empty and applies it to nothing."""

    def test_shipped_register_is_empty_and_scopeless(self):
        register = load_register(verifier.DEFAULT_REGISTER)
        self.assertEqual(register.entries, ())
        self.assertEqual(register.scan_scope, ())

    def test_shipped_register_verifies_clean(self):
        provenance = RegisterFileProvenance(
            verifier.REPO_ROOT / "docs/governance/AIOS_FINDING_REGISTER_v1.0.md",
            verifier.REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md",
        )
        self.assertEqual(
            verifier.verify(verifier.DEFAULT_REGISTER, verifier.REPO_ROOT, provenance), ()
        )

    def test_mechanism_does_not_reference_native_core(self):
        package = Path(verifier.__file__).resolve().parent
        for module in sorted(package.glob("*.py")):
            with self.subTest(module=module.name):
                self.assertNotIn("native_core", module.read_text(encoding="utf-8"))

    def test_verifier_exposes_no_mutating_entry_point(self):
        import tools.bounded_exception as package

        for banned in ("update", "fix", "accept", "write", "save", "register_site"):
            self.assertNotIn(banned, package.__all__)

    def test_register_module_has_no_serializer(self):
        from tools.bounded_exception import register as register_module

        source = Path(register_module.__file__).read_text(encoding="utf-8")
        self.assertNotIn("json.dump", source)
        self.assertNotIn("write_text", source)


if __name__ == "__main__":
    unittest.main()
