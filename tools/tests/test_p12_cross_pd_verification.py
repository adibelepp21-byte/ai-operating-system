"""P12-W6 cross-PD currency verification conformance.

Six-of-six CURRENT is also what a checker that reads nothing would report, so
the controls here make it drift on demand — and hold the line the registry
itself draws: `DECLARED ≠ DEFINED ≠ VERIFIED ≠ OPERATIONAL`.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_cross_pd_verification as xpd


def _registry_copy(tmp: Path, replace=None) -> Path:
    text = xpd.REGISTRY.read_text(encoding="utf-8")
    if replace:
        old, new = replace
        assert old in text, f"anchor missing: {old!r}"
        text = text.replace(old, new, 1)
    path = tmp / "registry.md"
    path.write_text(text, encoding="utf-8")
    return path


class TheRegistryIsCurrent(unittest.TestCase):
    def test_nothing_has_drifted(self):
        summary = xpd.summary()
        self.assertEqual(summary["drifted"], 0, f"{summary['drifted_checks']}")

    def test_every_check_reports_both_sides(self):
        for check in xpd.verify():
            self.assertTrue(check.recorded, f"{check.name} has no recorded value")
            self.assertTrue(check.measured, f"{check.name} has no measured value")


class TheCheckerCanActuallyDrift(unittest.TestCase):
    """Mutation controls. A checker that always agrees verifies nothing."""

    def test_removing_an_edge_row_drifts_the_edge_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = _registry_copy(Path(tmp), replace=("| `X-05` |", "| `Z-05` |"))
            with mock.patch.object(xpd, "REGISTRY", path):
                summary = xpd.summary()
        self.assertGreater(summary["drifted"], 0)
        self.assertIn("evidenced edges", summary["drifted_checks"])

    def test_a_defined_interface_would_drift_the_interface_count(self):
        """If an edge ever acquires an interface, this must notice — that is the
        single change that would make cross-PD verification possible."""
        with tempfile.TemporaryDirectory() as tmp:
            path = _registry_copy(Path(tmp), replace=("*not declared*", "`IFACE-1 v1.0`"))
            with mock.patch.object(xpd, "REGISTRY", path):
                drifted = xpd.summary()["drifted_checks"]
        self.assertIn("edges with a defined interface", drifted)

    def test_an_unresolvable_evidence_identifier_drifts(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.md"
            ledger.write_text("no identifiers here", encoding="utf-8")
            with mock.patch.object(xpd, "LEDGER", ledger):
                drifted = xpd.summary()["drifted_checks"]
        self.assertIn("evidence identifiers resolve", drifted)

    def test_an_absent_registry_is_unavailable_not_current(self):
        with tempfile.TemporaryDirectory() as tmp:
            with mock.patch.object(xpd, "REGISTRY", Path(tmp) / "absent.md"):
                summary = xpd.summary()
        self.assertEqual(summary["unavailable"], 1)
        self.assertEqual(summary["current"], 0)


class DeclaredIsNeverConvertedToVerified(unittest.TestCase):
    """§5 of the registry: it does not convert DECLARED into VERIFIED, and
    neither does anything built on top of it."""

    def test_interfaces_verified_is_zero(self):
        self.assertEqual(xpd.summary()["interfaces_verified"], 0)

    def test_the_blocking_boundaries_are_named(self):
        blocked = xpd.summary()["verification_blocked_by"]
        self.assertIn("SOURCE GAP (ESC-C7-01)", blocked)
        self.assertIn("ARCHITECT-RESERVED (ADR-0029)", blocked)

    def test_no_check_claims_an_inv10_violation(self):
        """The registry records POSSIBLE INV-10 EXPOSURE — NOT ASSERTED. This
        module asserts none either, and rules none out."""
        rendered = repr(xpd.verify()).upper()
        self.assertNotIn("VIOLATION", rendered)
        self.assertNotIn("INV-10", rendered)

    def test_no_check_reports_an_interface_as_verified(self):
        for check in xpd.verify():
            self.assertNotIn("VERIFIED", check.status.upper().replace("CURRENT", ""))

    def test_the_module_states_what_it_cannot_verify(self):
        doc = xpd.__doc__ or ""
        self.assertIn("An undefined interface cannot", doc)
        self.assertIn("DECLARED ≠ DEFINED ≠ VERIFIED ≠ OPERATIONAL", doc)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
