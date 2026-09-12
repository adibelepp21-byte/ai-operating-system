"""P12-W1 integration graph conformance and falsification (`§8`–`§12`, `§14`).

Four verified edges of eight is a claim; these controls make each classification
move, and run `ACT-CC-P12-W1-001 §11`'s falsification tests A–J.
"""

from __future__ import annotations

import unittest
from unittest import mock

from tools import p12_integration_graph as w1


class TheScopeIsCanonical(unittest.TestCase):
    def test_the_eight_integration_classes_are_section_8s_in_order(self):
        self.assertEqual(
            list(w1.INTEGRATION_CLASSES),
            ["phase ↔ phase", "platform ↔ phase", "governance ↔ execution",
             "organization ↔ runtime", "workflow ↔ runtime", "memory ↔ state",
             "evidence ↔ verification", "authority ↔ execution"])

    def test_the_relationship_classes_are_section_9s_in_order(self):
        self.assertEqual(
            list(w1.RELATIONSHIP_CLASSES),
            ["CONSUMES", "PROVIDES", "CALLS", "PUBLISHES", "OBSERVES",
             "VERIFIES", "DELEGATES", "ESCALATES", "OWNS", "DEPENDS_ON",
             "COMPOSES", "SYNCHRONIZES"])

    def test_the_dependency_classes_are_section_12s_in_order(self):
        self.assertEqual(
            list(w1.DEPENDENCY_CLASSES),
            ["DIRECT", "INDIRECT", "EVIDENCE", "RUNTIME", "AUTHORITY",
             "COMPLETION", "VERIFICATION", "EXTERNAL", "NONE"])

    def test_every_integration_class_has_a_derivation(self):
        self.assertEqual(set(w1._DERIVATIONS), set(w1.INTEGRATION_CLASSES))

    def test_every_edge_uses_a_declared_relationship_and_dependency(self):
        for edge in w1.graph():
            with self.subTest(edge.integration_class):
                self.assertIn(edge.relationship, w1.RELATIONSHIP_CLASSES)
                self.assertIn(edge.dependency, w1.DEPENDENCY_CLASSES)

    def test_every_edge_carries_the_full_section_9_model(self):
        for edge in w1.graph():
            with self.subTest(edge.integration_class):
                for field in ("source", "target", "relationship", "owner",
                              "authority", "contract", "state", "evidence",
                              "verification", "lifecycle"):
                    self.assertTrue(getattr(edge, field),
                                    f"{field} is empty")


class AnImportIsNotAnEdge(unittest.TestCase):
    """`§8`: do not count an edge because two modules can import one another."""

    def test_no_edge_uses_imports_as_its_relationship(self):
        for edge in w1.graph():
            with self.subTest(edge.integration_class):
                self.assertNotEqual(edge.relationship.lower(), "imports")

    def test_the_native_core_import_graph_is_not_this_graph(self):
        from tools import derived_views as views
        structural = views.interface_graph()
        self.assertTrue(structural)
        self.assertEqual({e.relationship for e in structural}, {"imports"})
        self.assertNotIn("imports", {e.relationship for e in w1.graph()})


class TestA_SemanticLoss(unittest.TestCase):
    """Does W2 omit what a `§9` edge requires?"""

    def test_w2_cannot_supply_most_edge_attributes(self):
        from tools import p12_operational_state as w2
        required = {"source", "target", "relationship", "owner", "authority",
                    "contract", "state", "evidence", "verification",
                    "lifecycle"}
        available = set(w2.StateEntry.__dataclass_fields__)
        missing = required - available
        self.assertGreaterEqual(
            len(missing), 8,
            "W2 is a per-state projection; a §9 edge is a per-edge record")
        for name in ("target", "relationship", "contract", "evidence",
                     "verification", "lifecycle", "owner"):
            self.assertIn(name, missing)


class TestB_SourceBypass(unittest.TestCase):
    """Does W1 already read authoritative sources directly?"""

    def test_w1_does_not_import_the_w2_projection(self):
        import ast
        source = (w1.REPO_ROOT / "tools" / "p12_integration_graph.py"
                  ).read_text(encoding="utf-8")
        imported = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
                imported.update(f"{node.module}.{a.name}" for a in node.names)
            elif isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
        self.assertFalse([m for m in imported if "operational_state" in m])

    def test_w1_reads_the_sources_themselves(self):
        import ast
        source = (w1.REPO_ROOT / "tools" / "p12_integration_graph.py"
                  ).read_text(encoding="utf-8")
        # `from tools import p12_runtime_observation as obs` puts the module
        # under test in `names`, not in `node.module`. The first version of this
        # control joined only `node.module` and saw nothing but "tools".
        parts = []
        for n in ast.walk(ast.parse(source)):
            if isinstance(n, ast.ImportFrom) and n.module:
                parts.append(n.module)
                parts.extend(a.name for a in n.names)
        text = " ".join(parts)
        for expected in ("p12_runtime_observation", "p12_provenance_verification",
                         "p12_execution_chain_reader"):
            self.assertIn(expected, text)


class TestC_FreshnessMismatch(unittest.TestCase):
    def test_the_graph_is_re_derived_not_cached(self):
        first = w1.graph()
        second = w1.graph()
        self.assertIsNot(first, second)
        self.assertEqual([e.integration_class for e in first],
                         [e.integration_class for e in second])

    def test_an_edge_state_follows_its_source(self):
        with mock.patch("tools.p12_cross_phase_verification.summary",
                        return_value={"phases": 8, "exercised": 8,
                                      "not_exercised": 0, "unknown": 0,
                                      "exercised_only_by_a_demonstrator": ()}):
            edge = w1._phase_to_phase()
        self.assertEqual(edge.classification, w1.VERIFIED)


class TestD_AuthorityContamination(unittest.TestCase):
    """`§15`: W1 must not become the authority for what it integrates."""

    def test_no_function_creates_authority(self):
        import ast
        source = (w1.REPO_ROOT / "tools" / "p12_integration_graph.py"
                  ).read_text(encoding="utf-8")
        names = [n.name for n in ast.walk(ast.parse(source))
                 if isinstance(n, ast.FunctionDef)]
        for name in names:
            with self.subTest(name):
                self.assertFalse(name.lower().startswith(
                    ("authorize", "authorise", "certify", "approve", "permit",
                     "grant", "own")))

    def test_every_owner_is_read_not_assigned(self):
        """`§11`: P12 may integrate a surface without owning it."""
        for edge in w1.graph():
            with self.subTest(edge.integration_class):
                self.assertEqual(edge.owner, w1.UNRESOLVED_OWNER)


class TestE_ConsumerIllusion(unittest.TestCase):
    def test_test_modules_are_not_counted_as_consumers(self):
        from tools.p12_state_verification import consumers_of
        found = consumers_of("tools.p12_integration_graph")
        self.assertFalse([c for c in found if "test" in c])


class TestF_Directionality(unittest.TestCase):
    def test_each_edge_declares_a_direction(self):
        for edge in w1.graph():
            with self.subTest(edge.integration_class):
                self.assertNotEqual(edge.source, "")
                self.assertNotEqual(edge.target, "")

    def test_platform_provides_to_phase_not_the_reverse(self):
        edge = {e.integration_class: e
                for e in w1.graph()}["platform ↔ phase"]
        self.assertEqual(edge.source, "Platform Organization")
        self.assertEqual(edge.target, "Phase")
        self.assertEqual(edge.relationship, "PROVIDES")


class TestG_Circularity(unittest.TestCase):
    def test_w1_and_w2_do_not_depend_on_each_other(self):
        from tools.p12_state_verification import consumers_of
        self.assertFalse([c for c in consumers_of("tools.p12_integration_graph")
                          if "operational_state" in c])


class TestH_HistoricalContamination(unittest.TestCase):
    def test_the_graph_writes_nothing(self):
        import ast
        source = (w1.REPO_ROOT / "tools" / "p12_integration_graph.py"
                  ).read_text(encoding="utf-8")
        names = {n.func.attr for n in ast.walk(ast.parse(source))
                 if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
        for forbidden in ("write_text", "mkdir", "unlink", "replace", "touch"):
            self.assertNotIn(forbidden, names)


class TestI_ProviderInference(unittest.TestCase):
    """`§16`: F-17 must not be resolved by an edge existing."""

    def test_the_platform_phase_edge_is_reserved_not_verified(self):
        edge = {e.integration_class: e
                for e in w1.graph()}["platform ↔ phase"]
        self.assertEqual(edge.classification, w1.RESERVED)
        self.assertIn("F-17", edge.authority)

    def test_no_edge_assigns_a_provider(self):
        summary = w1.summary()
        self.assertEqual(summary["owners_unresolved"], summary["edges"])


class TestJ_OperationalIllusion(unittest.TestCase):
    def test_callable_is_not_reachable(self):
        """The graph runs; that says nothing about a resident caller."""
        self.assertTrue(w1.graph())
        from tools.p12_state_verification import consumers_of
        self.assertEqual(consumers_of("tools.p12_integration_graph"), ())


class ClassificationsCanMove(unittest.TestCase):
    """Four verified of eight is a measurement only if each can change."""

    def test_an_unverified_edge_becomes_verified_when_its_source_does(self):
        class _Obs:
            def __init__(self, kind, rid):
                self.kind, self.runtime_id = kind, rid

        shared = [_Obs("workflow", "r-1"), _Obs("runtime", "r-1")]
        with mock.patch("tools.p12_runtime_observation.observations",
                        return_value=shared):
            edge = w1._workflow_to_runtime()
        self.assertEqual(edge.classification, w1.VERIFIED)

    def test_the_live_workflow_runtime_edge_is_unverified(self):
        edge = {e.integration_class: e
                for e in w1.graph()}["workflow ↔ runtime"]
        self.assertEqual(edge.classification, w1.UNVERIFIED)
        self.assertIn("two observations are not", edge.detail)

    def test_memory_state_is_unverified_because_nothing_populates_it(self):
        edge = {e.integration_class: e for e in w1.graph()}["memory ↔ state"]
        self.assertEqual(edge.classification, w1.UNVERIFIED)
        self.assertIn("empty memory_consumed", edge.detail)

    def test_a_raising_derivation_is_invalid_not_verified(self):
        def explode():
            raise RuntimeError("source unreadable")

        with mock.patch.dict(w1._DERIVATIONS, {"memory ↔ state": explode}):
            edge = {e.integration_class: e for e in w1.graph()}["memory ↔ state"]
        self.assertEqual(edge.classification, w1.INVALID)

    def test_dangling_evidence_is_detected(self):
        broken = w1.IntegrationEdge(
            source="a", target="b", relationship="DEPENDS_ON", owner="x",
            authority="x", contract="x", state="x",
            evidence="docs/no/such/path", verification="x", lifecycle="x",
            integration_class="phase ↔ phase", dependency="NONE",
            classification=w1.UNVERIFIED, detail="x")
        with mock.patch.object(w1, "graph", return_value=(broken,)):
            self.assertEqual(len(w1.dangling()), 1)

    def test_a_module_reference_is_not_reported_dangling(self):
        """The check compared a module name to the filesystem and misfired."""
        self.assertEqual(w1.dangling(), ())


if __name__ == "__main__":
    unittest.main()
