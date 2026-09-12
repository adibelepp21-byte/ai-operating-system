"""P12-W2 unified operational state conformance and falsification (`§32`, `§33`).

Nine verified checks is what a verifier that checks nothing prints, so every
class here drives one to `VIOLATED`. Each is one of `§32`'s named tests.
"""

from __future__ import annotations

import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

from tools import p12_operational_state as state
from tools import p12_operational_state_verifier as verifier


def _source(**over):
    base = dict(
        state_id="probe.state", state_class="RUNTIME",
        semantics=state.SOURCE_OF_TRUTH, owner="probe",
        canonical_source="probe", read_path="tools",
        authority="none", freshness_model="none",
        owns_within_class="a probe portion")
    base.update(over)
    return state.StateSource(**base)


def _entry(**over):
    base = dict(
        state_id="probe.state", state_class="RUNTIME", status=state.CURRENT,
        value={"x": 1}, source="tools (probe)",
        observed_at=datetime.now(timezone.utc).isoformat(),
        transformation="probe", authority="none",
        provider=state.UNRESOLVED_PROVIDER, semantics=state.SOURCE_OF_TRUTH)
    base.update(over)
    return state.StateEntry(**base)


class TheSurfaceIsAProjectionNotAStore(unittest.TestCase):
    """`§13` names an integration surface and a projection chain."""

    def test_the_state_classes_are_section_14s_in_order(self):
        self.assertEqual(
            list(state.STATE_CLASSES),
            ["IDENTITY", "AUTHORITY", "ARCHITECTURE", "CAPABILITY",
             "ORGANIZATION", "RUNTIME", "WORK", "EXECUTION", "OBSERVATION",
             "VERIFICATION", "EVIDENCE", "GOVERNANCE", "CHANGE", "DEPENDENCY",
             "RISK", "UNKNOWN", "STALE"])

    def test_no_durable_copy_of_any_source_is_written(self):
        """A store would have a write path. This surface has none."""
        import ast
        source = (state.REPO_ROOT / "tools" / "p12_operational_state.py"
                  ).read_text(encoding="utf-8")
        writes = []
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in ("write_text", "write_bytes", "mkdir",
                                      "open", "dump", "touch"):
                    writes.append(node.func.attr)
        self.assertEqual(writes, [], f"a projection must not persist: {writes}")

    def test_two_consecutive_projections_carry_different_timestamps(self):
        first = {e.state_id: e.observed_at for e in state.project()}
        second = {e.state_id: e.observed_at for e in state.project()}
        self.assertNotEqual(first, second, "a cached value would repeat")

    def test_every_declared_source_has_a_projection(self):
        declared = {s.state_id for s in state.SOURCES}
        self.assertEqual(set(state._PROJECTIONS), declared)


class TestA_WrongSource(unittest.TestCase):
    """Can a projection consume state from a source that is not there?"""

    def test_a_declared_path_that_does_not_resolve_is_violated(self):
        broken = state.SOURCES + (_source(state_id="ghost",
                                          read_path="no/such/place"),)
        with mock.patch.object(state, "SOURCES", broken):
            result = verifier._check_declared_paths_resolve()
        self.assertEqual(result.status, verifier.VIOLATED)
        self.assertIn("ghost", result.detail)

    def test_a_source_with_no_projection_yields_unknown(self):
        with mock.patch.object(state, "SOURCES", (_source(state_id="orphan"),)), \
                mock.patch.object(state, "_PROJECTIONS", {}):
            entries = state.project()
        self.assertEqual(entries[0].status, state.UNKNOWN)


class TestB_WrongOwner(unittest.TestCase):
    """Two sources must not claim the same portion of one class."""

    def test_a_duplicate_portion_is_violated(self):
        dupes = (_source(state_id="a"), _source(state_id="b"))
        with mock.patch.object(state, "SOURCES", dupes):
            result = verifier._check_no_duplicate_portion()
            found = state.conflicts()
        self.assertEqual(result.status, verifier.VIOLATED)
        self.assertTrue([c for c in found if c["kind"] == "CONFLICT"])

    def test_a_class_collision_alone_is_not_a_conflict(self):
        """The false positive the first detector produced."""
        distinct = (_source(state_id="a", owns_within_class="one thing"),
                    _source(state_id="b", owns_within_class="another thing"))
        with mock.patch.object(state, "SOURCES", distinct):
            found = state.conflicts()
        self.assertEqual([c for c in found if c["kind"] == "CONFLICT"], [])

    def test_an_unstated_claim_is_reported(self):
        with mock.patch.object(state, "SOURCES",
                               (_source(owns_within_class=""),)):
            found = state.conflicts()
            result = verifier._check_sources_declare_their_portion()
        self.assertEqual(found[0]["kind"], "UNDECLARED")
        self.assertEqual(result.status, verifier.VIOLATED)


class TestC_StaleState(unittest.TestCase):
    """Can stale state be reported as current?"""

    def test_a_cached_timestamp_is_violated(self):
        old = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
        with mock.patch.object(state, "project",
                               return_value=(_entry(observed_at=old),)):
            result = verifier._check_observed_at_is_fresh()
        self.assertEqual(result.status, verifier.VIOLATED)

    def test_a_stale_governance_source_projects_stale_not_current(self):
        class _Index:
            records = (1,)
            def stale_sources(self, root):
                return ("docs/x.md",)

        with mock.patch("tools.governance_index.GovernanceIndex.build",
                        return_value=(_Index(), mock.Mock(parsed=1))):
            entry = state._project_governance(
                [s for s in state.SOURCES
                 if s.state_id == "governance.declared"][0])
        self.assertEqual(entry.status, state.STALE)

    def test_the_runtime_projection_reports_unknown_on_an_empty_root(self):
        with mock.patch("tools.p12_runtime_observation.what_is_running",
                        return_value={"answerable": False, "reason": "empty"}):
            entry = state._project_runtime(
                [s for s in state.SOURCES
                 if s.state_id == "runtime.observed"][0])
        self.assertEqual(entry.status, state.UNKNOWN)


class TestD_MissingSource(unittest.TestCase):
    """Can state appear without source evidence?"""

    def test_an_entry_without_provenance_is_violated(self):
        with mock.patch.object(state, "project",
                               return_value=(_entry(source=""),)):
            result = verifier._check_every_entry_has_provenance()
        self.assertEqual(result.status, verifier.VIOLATED)

    def test_a_value_with_no_source_cannot_be_current(self):
        with mock.patch.object(state, "project",
                               return_value=(_entry(value=None),)):
            result = verifier._check_absence_is_not_negative()
        self.assertEqual(result.status, verifier.VIOLATED)

    def test_a_raising_projection_yields_unknown_not_a_negative(self):
        def explode(_source):
            raise RuntimeError("source unreadable")

        with mock.patch.object(state, "SOURCES", (_source(),)), \
                mock.patch.object(state, "_PROJECTIONS",
                                  {"probe.state": explode}):
            entries = state.project()
        self.assertEqual(entries[0].status, state.UNKNOWN)
        self.assertIsNone(entries[0].value)


class TestE_HistoricalRewrite(unittest.TestCase):
    """Can reconciliation modify historical evidence?"""

    def test_the_surface_has_no_write_path_at_all(self):
        import ast
        source = (state.REPO_ROOT / "tools" / "p12_operational_state.py"
                  ).read_text(encoding="utf-8")
        names = {n.func.attr for n in ast.walk(ast.parse(source))
                 if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Attribute)}
        self.assertNotIn("write_text", names)
        self.assertNotIn("unlink", names)
        self.assertNotIn("replace", names)

    def test_a_full_projection_leaves_the_corpus_unchanged(self):
        import subprocess
        before = subprocess.run(["git", "status", "--porcelain"],
                                cwd=state.REPO_ROOT, capture_output=True,
                                text=True).stdout
        state.project()
        after = subprocess.run(["git", "status", "--porcelain"],
                               cwd=state.REPO_ROOT, capture_output=True,
                               text=True).stdout
        self.assertEqual(before, after)


class TestF_GovernanceImpersonation(unittest.TestCase):
    """Can engineering state become authorization through field mutation?"""

    def test_a_projected_authorization_flag_is_violated(self):
        with mock.patch.object(
                state, "project",
                return_value=(_entry(value={"certified": True}),)):
            result = verifier._check_no_entry_reads_as_authority()
        self.assertEqual(result.status, verifier.VIOLATED)

    def test_no_entry_claims_to_be_authority(self):
        for entry in state.project():
            with self.subTest(entry.state_id):
                self.assertFalse(entry.is_authority())

    def test_declares_attributes_and_disclaims(self):
        declared = state.declares("governance.declared")
        self.assertIsNotNone(declared)
        self.assertFalse(declared["is_authority"])
        self.assertIn("declared_by", declared)
        self.assertIn("read the instrument", declared["note"])

    def test_no_accessor_returns_a_bare_permission(self):
        import ast
        source = (state.REPO_ROOT / "tools" / "p12_operational_state.py"
                  ).read_text(encoding="utf-8")
        names = [n.name for n in ast.walk(ast.parse(source))
                 if isinstance(n, ast.FunctionDef)]
        for name in names:
            with self.subTest(name):
                self.assertFalse(
                    name.lower().startswith(("authorize", "certify", "approve",
                                             "permit", "grant")),
                    f"{name} would make this surface an authority")


class TestG_ProviderInjection(unittest.TestCase):
    """Can an unresolved F-17 provider be silently assigned?"""

    def test_an_assigned_provider_is_violated(self):
        with mock.patch.object(state, "SOURCES",
                               (_source(provider="platform"),)):
            result = verifier._check_providers_unresolved()
        self.assertEqual(result.status, verifier.VIOLATED)

    def test_every_resident_provider_is_unresolved(self):
        for source in state.SOURCES:
            with self.subTest(source.state_id):
                self.assertEqual(source.provider, state.UNRESOLVED_PROVIDER)

    def test_the_unresolved_marker_names_f17(self):
        self.assertIn("F-17", state.UNRESOLVED_PROVIDER)


class TestH_ProjectionDrift(unittest.TestCase):
    """Can a source change without the projection noticing?"""

    def test_the_projection_follows_its_source(self):
        source = [s for s in state.SOURCES
                  if s.state_id == "architecture.boundaries"][0]
        with mock.patch("tools.derived_views._boundaries",
                        return_value=("a", "b")):
            drifted = state._project_architecture(source)
        live = state._project_architecture(source)
        self.assertEqual(drifted.value["boundaries"], 2)
        self.assertEqual(live.value["boundaries"], 11)


class TheVerifierIsIndependent(unittest.TestCase):
    """`§33`, and the one shared dependency is disclosed."""

    def test_the_verifier_does_not_import_the_writer_directly(self):
        import ast
        source = (state.REPO_ROOT / "tools"
                  / "p12_operational_state_verifier.py").read_text(
                      encoding="utf-8")
        imported = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
            elif isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
        self.assertNotIn("tools.p12_operational_state", imported)

    def test_the_shared_dependency_is_disclosed_in_the_docstring(self):
        self.assertIn("disclosure", verifier.__doc__)
        self.assertIn("importlib", verifier.__doc__)

    def test_the_verifier_redeclares_the_status_vocabulary(self):
        """Importing it would make agreement invisible."""
        self.assertEqual(verifier.PERMITTED_STATUSES,
                         frozenset({"CURRENT", "STALE", "UNKNOWN",
                                    "CONFLICTING", "RESERVED", "BLOCKED"}))

    def test_every_check_can_be_driven_to_violated(self):
        self.assertGreaterEqual(len(verifier.CHECKS), 9)

    def test_the_live_projection_passes_every_check(self):
        summary = verifier.summary()
        self.assertEqual(summary["violated"], 0, summary["not_verified"])
        self.assertEqual(summary["unavailable"], 0)


if __name__ == "__main__":
    unittest.main()
