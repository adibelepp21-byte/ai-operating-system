"""FR-1 (FD-TD-001, FD-FR1-001): live operational ledger → P12-W2 → P13.

The live ledger owns the current disposition of delegations and the responses to
escalations (A2, B1, FD-CG7-001). P12-W2 projects that reading next to the
historical one and owns neither; P13 receives it only through P12-W2's
`project()` — the interface its certified Blueprint `§4` names — and is an
observed, registered consumer of it in the certified P12 consumer measurement
(FD-FR1-001). These tests pin that route and the boundaries both decisions set.
"""

import ast
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

import tools  # noqa: F401  -- installs the certified-write barrier
from tools import delegation_catalog
from tools import p12_operational_state as w2
from tools import p12_provenance_verification as prov
from tools import w4_continuity
from tools.p13 import state as p13_state
from tools.p13.model import INFERRED, UNKNOWN, VERIFIED
from tools.p13.paths import LIVE
from tools.p13.state import StateUnderstanding

REPO = Path(__file__).resolve().parents[2]

#: The 14 grants the TD gate found P12-W2 presenting as active: every one of
#: them already COMPLETED or REVOKED in the live ledger (TD `§C`, Register `§156`).
STALE_14 = ("08e14bd7aa584ea5", "0f7ac0785bd8442b", "2494015de36246fd",
            "332d42f021764ab6", "4313bd2246124a94", "4daebea9012d4cc7",
            "522e84af52444890", "632b256f8335434f", "84e94ea2f001444d",
            "a437cdbbd29940af", "aa591daf55ca4714", "b304c7ecb1024454",
            "e668a317fa494342", "e6a3d622cfb54b4f")
LIVE_2 = ("0a697039a63f4c17", "50367d99c2dd4708")


def _overview(grants=(), escalations=(), faults=None):
    """A minimal reading in the shape `operational_overview()` returns."""
    return {
        "roots": {"r": {"disposition_faults": faults or []}},
        "grants": {f"r/{g['delegation_id']}": dict(g) for g in grants},
        "escalations": {f"r/{e['escalation_id']}": dict(e) for e in escalations},
        "current_grants": sorted(g["delegation_id"] for g in grants if g["executable"]),
        "blocking_escalations": sorted(
            e["escalation_id"] for e in escalations
            if e["classification"].endswith("CURRENT WORK")),
    }


def _grant(gid, historical, operational, executable):
    return {"delegation_id": gid, "historical_status": historical,
            "operational_status": operational, "executable": executable}


class TheProjectionFollowsTheLedger(unittest.TestCase):
    """Live repository state, read once: `project()` is slow by design."""

    @classmethod
    def setUpClass(cls):
        cls.entries = {e.state_id: e for e in w2.project()}
        cls.overview = w4_continuity.operational_overview()

    def test_the_14_stale_grants_are_no_longer_current(self):
        value = self.entries["delegation.granted"].value
        self.assertFalse(set(STALE_14) & set(value["current"]))
        self.assertTrue(set(STALE_14) <= set(value["historical"]["recorded_active_not_current"]))

    def test_the_2_live_grants_are_current_and_active_counts_only_them(self):
        value = self.entries["delegation.granted"].value
        self.assertEqual(value["current"], sorted(LIVE_2))
        self.assertEqual(value["active"], len(value["current"]))

    def test_historical_completed_and_revoked_stay_historical(self):
        value = self.entries["delegation.granted"].value
        grants = list(self.overview["grants"].values())
        self.assertEqual(value["historical"]["completed"],
                         sum(g["operational_status"] == "COMPLETED" for g in grants))
        self.assertEqual(value["historical"]["revoked"],
                         sum(g["operational_status"] == "REVOKED" for g in grants))
        closed = {g["delegation_id"] for g in grants
                  if g["operational_status"] in ("COMPLETED", "REVOKED")}
        self.assertFalse(closed & set(value["current"]))

    def test_escalations_separate_blocking_historical_and_answered(self):
        value = self.entries["escalation.raised"].value
        self.assertEqual(value["blocking"], [])
        self.assertEqual(set(value["open_historical"]), {"0991300404cf44d8", "9d6bc0ad47294ef0"})
        self.assertEqual(set(value["answered"]), {"23f315ba9f504272", "9cb90fa0787a478c"})
        for key in ("records", "joined_by_structured_field", "joined_by_parsed_prose"):
            self.assertIn(key, value)       # the historical join is still carried

    def test_p13_receives_the_state_through_p12_w2(self):
        source = next(s for s in p13_state.SOURCES if s.name == "operational_state")
        with mock.patch.object(w2, "project", return_value=tuple(self.entries.values())) as called:
            snapshot = StateUnderstanding(LIVE, sources=(source,)).observe()
        called.assert_called_once()
        delegations = snapshot.get("operational_state.delegations")
        self.assertEqual(delegations.status, VERIFIED)
        self.assertEqual(delegations.value["current"], sorted(LIVE_2))
        self.assertIn("P12-W2 delegation.granted", delegations.source)
        self.assertEqual(snapshot.get("operational_state.escalations").value["blocking"], [])


class TheConsumerIsMeasuredHonestly(unittest.TestCase):
    """FD-FR1-001 `§4`: P13 is visible to the certified scanner and observed by
    the independent verifier — never hidden, never merely claimed."""

    def test_p13_is_an_importer_and_an_evidenced_consumer(self):
        from tools import p12_state_verification as sv
        self.assertIn("tools/p13/state.py", sv.importers_of("tools.p12_operational_state"))
        self.assertIn("tools/p13/state.py", sv.consumers_of("tools.p12_operational_state"))

    def test_the_independent_verifier_agrees_with_the_measurement(self):
        from tools import p12_consumer_evidence_verifier as cv
        from tools import p12_state_verification as sv
        surface = "tools.p12_operational_state"
        summary = cv.summary(sv.consumers_of(surface), sv.importers_of(surface))
        self.assertEqual(summary["disagrees"], 0, summary["not_agreeing"])
        self.assertIn("tools/p13/state.py", summary["observed_consumers"])

    def test_p13_binds_the_surface_statically_not_by_name(self):
        text = (REPO / "tools/p13/state.py").read_text(encoding="utf-8")
        self.assertIn("from tools import p12_operational_state as w2", text)
        self.assertNotIn("import_module", text)

    def test_the_independent_verifier_observes_p13_reading_resident_sources(self):
        from tools import p12_consumer_evidence_verifier as cv
        observation = cv.observe("tools.p13.state", "_operational_state")
        self.assertIsNone(observation.error)
        self.assertTrue(observation.consumes)
        self.assertIn("project", observation.resident_reads)

class OwnershipAndPopulationsAreUnchanged(unittest.TestCase):
    """FD-TD-001 `§3`: no ownership transfer, no verifier population moved, no F-17."""

    def test_the_declared_contract_keeps_class_semantics_owner_portion_provider(self):
        sources = {s.state_id: s for s in w2.SOURCES}
        self.assertEqual(len(sources), 8)
        d, e = sources["delegation.granted"], sources["escalation.raised"]
        self.assertEqual((d.state_class, d.semantics, d.owner, d.owns_within_class),
                         ("AUTHORITY", w2.SOURCE_OF_TRUTH, "FD-P11-001 authorized delegator",
                          "operational grants and their lifecycle"))
        self.assertEqual((e.state_class, e.semantics, e.owner),
                         ("GOVERNANCE", w2.SOURCE_OF_TRUTH, "escalation register"))
        self.assertTrue(all(s.provider == w2.UNRESOLVED_PROVIDER for s in w2.SOURCES))

    def test_certified_verifier_populations_do_not_move(self):
        self.assertEqual([str(r.relative_to(REPO)) for r in prov.DELEGATION_ROOTS], [
            "docs/architecture/p11/w1-operations", "docs/architecture/p11/w4-operations",
            "docs/architecture/p11/x-department-operations",
            "docs/architecture/p12/w4-operations"])
        self.assertTrue(all("docs/architecture/p11/" in str(r)
                            for r in delegation_catalog.operation_roots()))

    def test_the_projection_has_no_write_path(self):
        tree = ast.parse((REPO / "tools/p12_operational_state.py").read_text(encoding="utf-8"))
        writes = [n.func.attr for n in ast.walk(tree) if isinstance(n, ast.Call)
                  and isinstance(n.func, ast.Attribute)
                  and n.func.attr in ("write_text", "write_bytes", "record_disposition",
                                      "record_response", "issue", "revoke")]
        self.assertEqual(writes, [])

    def test_p13_reads_no_agency_reader_of_its_own(self):
        """Only the certified P12-W2 path: no direct Agency → P13 (FD-TD-001 `§5`)."""
        for path in sorted((REPO / "tools/p13").glob("*.py")):
            text = path.read_text(encoding="utf-8")
            for name in ("w4_continuity", "w4_delegation", "plan_outcome", "LIVE_LEDGER",
                         "LIVE_RESPONSES", "operational_overview", "planning_continuity"):
                self.assertNotIn(name, text, f"{path.name} reads {name} directly")


class TheProjectionIsHonestUnderChange(unittest.TestCase):
    """Synthetic ledger readings, so the rules are exercised without the live repo."""

    def project(self, overview):
        with mock.patch.object(w4_continuity, "operational_overview", return_value=overview):
            return {e.state_id: e for e in w2.project()}

    def test_a_recorded_active_grant_closed_by_the_ledger_is_history(self):
        entry = self.project(_overview(grants=(
            _grant("a", "ACTIVE", "COMPLETED", False),
            _grant("b", "ACTIVE", "ACTIVE", True))))["delegation.granted"]
        self.assertEqual(entry.status, w2.CURRENT)
        self.assertEqual(entry.value["current"], ["b"])
        self.assertEqual(entry.value["active"], 1)
        self.assertEqual(entry.value["historical"]["recorded_active_not_current"], ["a"])

    def test_disposition_faults_are_not_presented_as_current(self):
        entry = self.project(_overview(grants=(_grant("a", "ACTIVE", "ACTIVE", True),),
                                       faults=["a: basis changed"]))["delegation.granted"]
        self.assertEqual(entry.status, w2.CONFLICTING)
        self.assertIn("disposition_faults", entry.value)

    def test_an_open_escalation_behind_a_current_grant_is_blocking(self):
        entry = self.project(_overview(escalations=(
            {"escalation_id": "x", "operational_state": "OPEN",
             "classification": "OPEN — BLOCKING CURRENT WORK"},
            {"escalation_id": "y", "operational_state": "OPEN",
             "classification": "OPEN — HISTORICAL (its grant is not current)"},
            {"escalation_id": "z", "operational_state": "ANSWERED",
             "classification": "ANSWERED"})))["escalation.raised"]
        self.assertEqual((entry.value["blocking"], entry.value["open_historical"],
                          entry.value["answered"]), (["x"], ["y"], ["z"]))

    def test_one_ledger_reading_per_pass_and_a_fresh_one_per_call(self):
        with mock.patch.object(w4_continuity, "operational_overview",
                               return_value=_overview()) as read:
            w2.project()
            w2.project()
        self.assertEqual(read.call_count, 2)

    def test_p13_carries_a_non_current_entry_as_inferred_and_absence_as_unknown(self):
        source = next(s for s in p13_state.SOURCES if s.name == "operational_state")
        conflicting = w2.StateEntry(
            state_id="delegation.granted", state_class="AUTHORITY", status=w2.CONFLICTING,
            value={"current": []}, source="s", observed_at="t", transformation="x",
            authority="a", provider=w2.UNRESOLVED_PROVIDER, semantics=w2.SOURCE_OF_TRUTH)
        with mock.patch.object(w2, "project", return_value=(conflicting,)):
            snapshot = StateUnderstanding(LIVE, sources=(source,)).observe()
        self.assertEqual(snapshot.get("operational_state.delegations").status, INFERRED)
        self.assertEqual(snapshot.get("operational_state.escalations").status, UNKNOWN)
        with mock.patch.object(w2, "project", side_effect=RuntimeError("down")):
            snapshot = StateUnderstanding(LIVE, sources=(source,)).observe()
        self.assertEqual(snapshot.get("operational_state.delegations").status, UNKNOWN)

class FreshProcess(unittest.TestCase):
    def test_a_second_interpreter_reconstructs_the_same_projection(self):
        program = ("import sys,json;sys.path.insert(0,sys.argv[1]);import tools;"
                   "from tools import p12_operational_state as w;"
                   "e={x.state_id:x.value for x in w.project()};"
                   "print(json.dumps([e['delegation.granted'],e['escalation.raised']],"
                   "sort_keys=True))")
        out = subprocess.run([sys.executable, "-c", program, str(REPO)], cwd=REPO,
                             capture_output=True, text=True, check=True).stdout
        here = {e.state_id: e.value for e in w2.project()}
        self.assertEqual(json.loads(out), json.loads(json.dumps(
            [here["delegation.granted"], here["escalation.raised"]], sort_keys=True)))


if __name__ == "__main__":
    unittest.main()
