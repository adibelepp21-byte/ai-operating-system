"""The post-construction reconciliation: FE-1, FE-2, and E13-05 Cases A–D.

The instruction is `acts/P13-POST-CONSTRUCTION-RECONCILIATION-AND-E13-05-EXIT-BLOCKER-INSTRUCTION.md`.

**Cases A and D are TEST-VERIFIED, not LIVE-VERIFIED.** They run a fixture
state-changing action under a fixture envelope, written into a *temporary copy*
of the Delegation Register, against a temporary sandbox. Nothing here adds a
production action type. Since `FDR-3`, the production catalog holds exactly
two executable state-changing types, the S-OPS transitions that `P13-ENV-02`
permits. They are tested in `test_s_ops.py`. `EXECUTION CAPABLE ≠ EXECUTION
AUTHORIZED`.
"""

from __future__ import annotations

import hashlib
import json
import re
import tempfile
import unittest
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from tools import authority_citation
from tools import p12_self_model as model
from tools.derived_views import REGISTER as DECISION_REGISTER
from tools.governance_index import GovernanceIndex, tracked_markdown
from tools.p13 import cycle
from tools.p13.authority import AuthorityGate, authority_dimensions, load_envelopes
from tools.p13.catalog import CATALOG, READ_ONLY, STATE_CHANGING, ActionType
from tools.p13.evaluation import CRITERIA, Criterion
from tools.p13.execution import BoundedExecution
from tools.p13.model import (ESCALATE, EXECUTE, REFUSE, UNKNOWN, VERIFIED,
                             ActionProposal, Citation)
from tools.p13.paths import REPO_ROOT, Paths
from tools.p13.state import SOURCES, Source

P13_018 = "docs/governance/acts/P13-018-FOUNDER-CONSTRUCTION-AUTHORITY-GATE-DECISION.md"
PREP_018 = "docs/architecture/p13-preparation/P13-018-CONSTRUCTION-AUTHORITY-GATE.md"
ENVELOPE = REPO_ROOT / "docs/governance/p13-envelopes/P13-ENV-01.json"
DELEGATIONS = REPO_ROOT / "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md"
FIXTURE = "fixture.write_marker"
TARGET = "sandbox/marker.txt"


# ---------------------------------------------------------------------------
# FE-1 — P13-018 is machine-discoverable, deterministically
# ---------------------------------------------------------------------------

class FE1TheDecisionResolvesTheSameWayEverywhere(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.index, _ = GovernanceIndex.build(tracked_markdown(REPO_ROOT), REPO_ROOT)

    def _records(self, identifier):
        return [r for r in self.index.records if r.identifier == identifier]

    def test_the_register_entry_is_exactly_one_index_record(self):
        records = self._records("P13-018")
        self.assertEqual([(r.source_path, r.title.split(" · ")[0]) for r in records],
                         [(DECISION_REGISTER, "P13-018 — Founder Decision")])

    def test_the_self_model_lists_it_as_a_decision_and_the_issuance_as_none(self):
        identifiers = model.decisions().value["identifiers"]
        self.assertIn("P13-018", identifiers)
        self.assertNotIn("FI-P13-004", identifiers)
        self.assertFalse([i for i in identifiers if i.startswith(("GOAL-", "ACT-"))])

    def test_the_issuance_is_indexed_as_itself(self):
        self.assertEqual(len(self._records("FI-P13-004")), 1)

    def test_neighbouring_entries_no_longer_absorb_the_next_one(self):
        fdr2 = self._records("FDR-2")[0]
        fd = next(r for r in self._records("FD-P13-002")
                  if r.source_path == DECISION_REGISTER)
        self.assertNotIn("FD-P12-002", fdr2.mentions)      # was P13-018's text
        self.assertNotIn("ACT-CC-P13-004", fd.mentions)    # was FI-P13-004's text

    def test_the_prepared_gate_is_not_a_record_and_not_an_authority(self):
        self.assertFalse([r for r in self._records("P13-018")
                          if r.source_path == PREP_018])
        self.assertIsNotNone(authority_citation.refusal("P13-018", PREP_018, "P13-018"))
        self.assertIsNone(authority_citation.refusal("P13-018 D-1", P13_018, "P13-018"))

    def test_an_instrument_without_an_identifier_is_not_given_one_by_its_record(self):
        """The persisted headers once read `**Identifier:** none stated`, and the
        index took that phrase as an identifier. Two such acts then collided."""
        for name in ("P13-POST-CONSTRUCTION-RECONCILIATION-AND-E13-05-EXIT-BLOCKER-INSTRUCTION.md",
                     "P13-E13-05-SEMANTIC-PROOF-SURFACE-DISCOVERY-INSTRUCTION.md",
                     "P13-CONTROLLED-OPERATIONAL-STATE-DEFINITION-INSTRUCTION.md"):
            with self.subTest(name):
                path = f"docs/governance/acts/{name}"
                self.assertTrue((REPO_ROOT / path).is_file())
                identifiers = {r.identifier for r in self.index.records
                               if r.source_path == path}
                self.assertLessEqual(identifiers, {"ABSENT"})

    def test_a_heading_is_a_declared_entry_only_when_the_register_declares_it(self):
        from tools.governance_index import _subrecord_spans
        declared = ["### X13-1 — Founder Decision · a", "", "| Field | Value |",
                    "|---|---|", "| **Identifier** | `X13-1` |",
                    "| **Decided by** | Founder |"]
        undecided = ["### X13-2 — Founder Decision · b", "",
                     "| **Identifier** | `X13-2` |"]
        mismatched = ["### X13-3 — Founder Decision · c", "",
                      "| **Identifier** | `X13-9` |", "| **Decided by** | Founder |"]
        spans = _subrecord_spans(declared + undecided + mismatched
                                 + [s.replace("X13-1", "X13-4") for s in declared])
        self.assertEqual([s[2] for s in spans], ["X13-1", "X13-4"])


# ---------------------------------------------------------------------------
# FE-2 — construction authority is not phase authorization
# ---------------------------------------------------------------------------

class FE2TheAuthorityDimensionsAreKeptApart(unittest.TestCase):

    def test_each_dimension_is_read_from_its_own_source(self):
        dims = authority_dimensions(Paths(REPO_ROOT))
        self.assertEqual({k: v["state"] for k, v in dims.items()}, {
            "phase_authorization": "NOT AUTHORIZED",
            "construction_authorization": "AUTHORIZED — bounded to Blueprint §10 IN",
            "operational_envelope": "EVIDENCE-ONLY + BOUNDED STATE-CHANGING",
            "state_changing_authority": dims["state_changing_authority"]["state"],
            "certification_authority": "NOT GRANTED",
        })
        # FDR-3 (Decision Register §23) → P13-ENV-02 (Delegation Register §15):
        # the only state-changing grants, each bounded to the one S-OPS object.
        grants = dims["state_changing_authority"]["grants"]
        self.assertEqual(sorted(g["action_type"] for g in grants),
                         ["s_ops.close", "s_ops.open"])
        for grant in grants:
            self.assertEqual((grant["envelope"], grant["instrument"], grant["targets"]),
                             ("P13-ENV-02", "FDR-3 §4",
                              ["docs/operations/s-ops/S-OPS-01.json"]))
        self.assertTrue(dims["state_changing_authority"]["state"].startswith("BOUNDED: "))
        self.assertEqual({v["verified"] for v in dims.values()}, {VERIFIED})
        self.assertIn("§37", dims["phase_authorization"]["source"])
        self.assertIn("§22", dims["construction_authorization"]["source"])

    def test_construction_authority_never_moves_the_phase_value(self):
        from tools import p12_phase_authorization as phases
        p13 = {s["entity"]: s for s in phases.current_states()}["P13"]
        self.assertIs(p13["authorized"], False)

    def test_a_state_changing_grant_would_show_as_one(self):
        dims = authority_dimensions(
            Paths(REPO_ROOT),
            catalog={**CATALOG, "verify.p13_evidence": ActionType(
                "verify.p13_evidence", False, effect=STATE_CHANGING)})
        state = dims["state_changing_authority"]["state"]
        # Declared without a target scope, so it is not BOUNDED, and the
        # projection says the gate refuses it.
        self.assertTrue(state.startswith("GRANTED: "), state)
        self.assertIn("verify.p13_evidence → no target scope, so the gate refuses it "
                      "(P13-ENV-01 · P13-018 D-2b)", state)


# ---------------------------------------------------------------------------
# E13-05 — Cases A–D, on a fixture action in a sandbox
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Governed(Paths):
    envelope_dir: Optional[Path] = None
    register: Optional[Path] = None

    @property
    def envelopes(self):
        return self.envelope_dir or super().envelopes

    @property
    def delegation_register(self):
        return self.register or super().delegation_register


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Sandbox:
    """A fixture boundary: `sandbox/` inside a temporary directory."""

    def __init__(self, root: Path, rogue: bool = False, lazy: bool = False,
                 precondition: bool = True):
        self.root = root
        (root / "sandbox").mkdir()
        (root / "sandbox/other.txt").write_text("untouched", encoding="utf-8")
        self.rogue, self.lazy, self.precondition = rogue, lazy, precondition

    def observe(self, paths, target):
        return {p.relative_to(self.root).as_posix(): _sha(p.read_bytes())
                for p in sorted((self.root / "sandbox").rglob("*")) if p.is_file()}

    def run(self, paths, target):
        if not self.lazy:
            (self.root / target).write_text("done", encoding="utf-8")
        if self.rogue:
            (self.root / "sandbox/other.txt").write_text("touched", encoding="utf-8")
        return {"sandbox.written": target}

    def verify(self, paths, target, before, after):
        holds = after.get(target) == _sha(b"done")
        return holds, f"{target} holds 'done'" if holds else f"{target} is not 'done'"

    def action(self, verifiable=True):
        return ActionType(
            FIXTURE, False, ("sandbox.written",), "tests: Sandbox.run", self.run,
            effect=STATE_CHANGING, observe=self.observe if verifiable else None,
            verify=self.verify,
            preconditions=((lambda p, t: None if self.precondition
                            else "the sandbox is sealed"),))

    def marker(self):
        path = self.root / TARGET
        return path.read_text(encoding="utf-8") if path.exists() else None

    def untouched(self):
        return (self.root / "sandbox/other.txt").read_text(encoding="utf-8") == "untouched"


class Fixture(unittest.TestCase):
    """A temporary Delegation Register copy holding one fixture envelope."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.envelope_dir = self.tmp / "envelopes"
        self.envelope_dir.mkdir()
        self.register = self.tmp / "delegations.md"
        self.register.write_text(DELEGATIONS.read_text(encoding="utf-8"), encoding="utf-8")
        self.paths = Governed(REPO_ROOT, self.tmp / "live", self.envelope_dir, self.register)
        self.sandbox = Sandbox(self.tmp)

    def tearDown(self):
        self._tmp.cleanup()

    def envelope(self, envelope_id="P13-ENV-T1", register=True, status="**ACTIVE**",
                 grant=None, **changes):
        record = json.loads(ENVELOPE.read_text(encoding="utf-8"))
        record["envelope_id"] = envelope_id
        record["action_types"] = {FIXTURE: grant if grant is not None
                                  else {"items": [0], "targets": [TARGET]}}
        record.update(changes)
        raw = json.dumps(record, indent=2).encode("utf-8")
        (self.envelope_dir / f"{envelope_id}.json").write_bytes(raw)
        if register:
            with open(self.register, "a", encoding="utf-8") as handle:
                handle.write(f"\n### {envelope_id} — fixture\n\n"
                             f"| **Record** | {_sha(raw)} |\n| **Status** | {status} |\n")
        return raw

    def decide(self, target=TARGET, action=None, catalog=None):
        catalog = catalog or {**CATALOG, FIXTURE: action or self.sandbox.action()}
        envelopes, anomalies = load_envelopes(self.paths)
        gate = AuthorityGate(self.paths, catalog, envelopes)
        proposal = ActionProposal(f"p:{FIXTURE}", FIXTURE, target, ("c:fixture",),
                                  "fixture", VERIFIED, (0, "", FIXTURE),
                                  expected=(("CR-FIXTURE", "PASS"),))
        decision = gate.decide(proposal)
        outcome = None
        if decision.decision == EXECUTE:
            outcome = BoundedExecution(self.paths, catalog).execute(decision, "t")
        return decision, outcome, anomalies


class CaseAAuthorityPresent(Fixture):

    def test_execute_verify_and_nothing_outside_the_scope_changes(self):
        self.envelope()
        decision, outcome, _ = self.decide()
        self.assertEqual((decision.decision, decision.scope), (EXECUTE, (TARGET,)))
        self.assertEqual(outcome.status, "success", outcome.detail)
        report = {f.key: f.value for f in outcome.produced}[f"execution.{FIXTURE}"]
        self.assertEqual(report["changed"], [TARGET])
        self.assertEqual((report["outside_scope"], report["verified"]), ([], True))
        self.assertEqual(self.sandbox.marker(), "done")
        self.assertTrue(self.sandbox.untouched())


class CaseBAuthorityAbsent(Fixture):

    def test_no_envelope_means_no_execution_and_no_state_change(self):
        decision, outcome, _ = self.decide()
        self.assertEqual(decision.decision, ESCALATE)
        self.assertFalse(decision.recorded()["executes"])
        self.assertIsNone(outcome)
        self.assertIsNone(self.sandbox.marker())


class CaseCAuthorityInvalid(Fixture):
    """Every mutation `§9` Case C and `§14` list: no execution, no state change."""

    def _refused(self, decision_expected=None, **kw):
        decision, outcome, anomalies = self.decide(**kw)
        self.assertNotEqual(decision.decision, EXECUTE, decision.reason)
        if decision_expected:
            self.assertEqual(decision.decision, decision_expected, decision.reason)
        self.assertIsNone(outcome)
        self.assertIsNone(self.sandbox.marker())
        self.assertTrue(self.sandbox.untouched())
        return decision, anomalies

    def test_unknown_citation(self):
        self.envelope(instrument="FD-P99-999 §1")
        _, anomalies = self._refused(ESCALATE)
        self.assertIn("not FD-P99-999's act", anomalies[0])

    def test_forged_citation(self):
        self.envelope(instrument="P13-018 D-2b", record="README.md")
        self.assertIn("not P13-018's act", self._refused(ESCALATE)[1][0])

    def test_missing_citation(self):
        self.envelope(instrument="")
        self.assertTrue(self._refused(ESCALATE)[1])

    def test_tampered_authority(self):
        raw = self.envelope()
        record = json.loads(raw)
        record["action_types"][FIXTURE]["targets"] = ["sandbox"]
        (self.envelope_dir / "P13-ENV-T1.json").write_text(json.dumps(record),
                                                          encoding="utf-8")
        self.assertIn("tampered", self._refused(ESCALATE)[1][0])

    def test_revoked_authority(self):
        self.envelope()
        with open(self.register, "a", encoding="utf-8") as handle:
            handle.write("\n| P13-ENV-T1 | REVOKED |\n")
        self.assertIn("revoked", self._refused(ESCALATE)[1][0])

    def test_expired_authority(self):
        self.envelope(expires="2026-01-01")
        self.assertIn("EXPIRED", self._refused(ESCALATE)[1][0])

    def test_an_unreadable_expiry_is_ambiguous(self):
        self.envelope(expires="soon")
        self.assertIn("AMBIGUOUS", self._refused(ESCALATE)[1][0])

    def test_inactive_authority(self):
        self.envelope(status="PENDING")
        self.assertIn("not ACTIVE", self._refused(ESCALATE)[1][0])

    def test_ambiguous_authority(self):
        self.envelope()
        with open(self.register, "a", encoding="utf-8") as handle:
            handle.write("\n### P13-ENV-T1 — a second entry\n\n| **Status** | **ACTIVE** |\n")
        self.assertIn("AMBIGUOUS", self._refused(ESCALATE)[1][0])

    def test_wrong_scope(self):
        self.envelope(designated_live_root="docs")
        self.assertIn("does not designate", self._refused(ESCALATE)[1][0])

    def test_wrong_action_type(self):
        self.envelope()
        record = json.loads((self.envelope_dir / "P13-ENV-T1.json").read_text())
        self.assertIn(FIXTURE, record["action_types"])
        other = ActionType("fixture.other", False, (), "tests", self.sandbox.run,
                           effect=STATE_CHANGING, observe=self.sandbox.observe,
                           verify=self.sandbox.verify)
        envelopes, _ = load_envelopes(self.paths)
        gate = AuthorityGate(self.paths, {**CATALOG, "fixture.other": other}, envelopes)
        decision = gate.decide(ActionProposal("p:o", "fixture.other", TARGET, ("c",), "r",
                                              VERIFIED, (0, "", "o")))
        self.assertEqual(decision.decision, ESCALATE)
        self.assertIsNone(self.sandbox.marker())

    def test_wrong_target(self):
        self.envelope()
        decision, _ = self._refused(REFUSE, target="sandbox/other.txt")
        self.assertIn("wrong target", decision.reason)

    def test_no_declared_target_scope(self):
        self.envelope(grant=[0])            # P13-ENV-01's form: items, no targets
        decision, _ = self._refused(REFUSE)
        self.assertIn("declares no target scope", decision.reason)

    def test_missing_precondition(self):
        self.envelope()
        sealed = Sandbox.__new__(Sandbox)
        sealed.__dict__.update(self.sandbox.__dict__, precondition=False)
        decision, _ = self._refused(REFUSE, action=sealed.action())
        self.assertIn("missing precondition", decision.reason)

    def test_no_verification_path(self):
        self.envelope()
        decision, _ = self._refused(REFUSE, action=self.sandbox.action(verifiable=False))
        self.assertIn("no verification path", decision.reason)

    def test_unknown_premise(self):
        self.envelope()
        envelopes, _ = load_envelopes(self.paths)
        gate = AuthorityGate(self.paths, {**CATALOG, FIXTURE: self.sandbox.action()}, envelopes)
        decision = gate.decide(ActionProposal("p", FIXTURE, TARGET, ("c",), "r", UNKNOWN,
                                              (0, "", "x")))
        self.assertEqual(decision.decision, UNKNOWN)
        self.assertIsNone(self.sandbox.marker())


class CaseDVerifiedStateChange(Fixture):

    def _cycle_parts(self):
        sandbox = self.sandbox
        sources = tuple(s for s in SOURCES if s.name not in ("self_model", "corpus")) + (
            Source("sandbox", "tests: sandbox marker", ("sandbox.marker",),
                   lambda p, c: {"sandbox.marker": (sandbox.marker(), VERIFIED)}),)
        criterion = Criterion(
            "CR-FIXTURE", "the sandbox marker reads 'done'",
            Citation("P13-018", "P13-018 (fixture)", P13_018), ("sandbox.marker",),
            lambda v: v["sandbox.marker"] == "done", "error", FIXTURE, TARGET)
        catalog = {**CATALOG, FIXTURE: sandbox.action()}
        return sources, (criterion,), catalog

    def test_a_cycle_executes_verifies_traces_updates_and_rediscovers(self):
        self.envelope()
        sources, criteria, catalog = self._cycle_parts()
        first = cycle.run_cycle(self.paths, intent="Case D", invoker="test",
                                sources=sources, criteria=criteria, catalog=catalog)
        self.assertEqual(first["executed"], FIXTURE)
        self.assertEqual(first["changes"], [{"criterion": "CR-FIXTURE", "before": "FAIL",
                                             "after": "PASS", "certainty_before": VERIFIED,
                                             "certainty_after": VERIFIED}])
        record = json.loads((self.paths.cycles / f"{first['cycle_id']}.json").read_text())
        after = {f["key"]: f for f in record["observation"]["after"]["facts"]}
        self.assertEqual(after["sandbox.marker"]["value"], "done")       # re-observed
        self.assertEqual(after["sandbox.marker"]["source"], "tests: sandbox marker")
        self.assertTrue(after[f"execution.{FIXTURE}"]["value"]["verified"])
        self.assertTrue(self.sandbox.untouched())
        # Rediscovery: the next cycle remembers, finds nothing to do, executes nothing.
        second = cycle.run_cycle(self.paths, intent="Case D rediscovery", invoker="test",
                                 sources=sources, criteria=criteria, catalog=catalog)
        self.assertNotEqual(second["executed"], FIXTURE)
        self.assertEqual(second["results"]["CR-FIXTURE"], "PASS/VERIFIED")
        from tools.p13.evidence import EvidenceStore
        self.assertTrue(EvidenceStore(self.paths).verify()["holds"])

    def test_a_change_outside_the_scope_is_a_failure_not_a_success(self):
        self.envelope()
        rogue = Sandbox.__new__(Sandbox)
        rogue.__dict__.update(self.sandbox.__dict__, rogue=True)
        decision, outcome, _ = self.decide(action=rogue.action())
        self.assertEqual(decision.decision, EXECUTE)
        self.assertEqual(outcome.status, "failure")
        self.assertIn("outside the authorized scope", outcome.detail)

    def test_a_postcondition_that_does_not_hold_is_a_failure(self):
        self.envelope()
        lazy = Sandbox.__new__(Sandbox)
        lazy.__dict__.update(self.sandbox.__dict__, lazy=True)
        decision, outcome, _ = self.decide(action=lazy.action())
        self.assertEqual(outcome.status, "failure")
        self.assertIn("postcondition does not hold", outcome.detail)

    def test_refusals_are_traced_not_only_recorded(self):
        # P13-ENV-01 alone: the cycle may run, and the fixture action is not permitted.
        (self.envelope_dir / "P13-ENV-01.json").write_bytes(ENVELOPE.read_bytes())
        sources, criteria, catalog = self._cycle_parts()
        result = cycle.run_cycle(self.paths, intent="Case B traced", invoker="test",
                                 sources=sources, criteria=criteria, catalog=catalog)
        self.assertIsNone(self.sandbox.marker())
        from native_core.core.infrastructure import LocalAppendOnlyStorage
        from native_core.core.trace import TraceReader
        storage = LocalAppendOnlyStorage(self.paths.trace)
        storage.provision()
        entry = list(TraceReader(storage).read())[-1]
        traced = {d["subject"]: d["decision"] for d in entry.outputs["decisions"]}
        self.assertEqual(traced[f"P13 {FIXTURE} {TARGET}"], ESCALATE)
        self.assertEqual(result["decisions"][f"P13 {FIXTURE} {TARGET}"], ESCALATE)


class TheProductionCatalogStaysReadOnly(unittest.TestCase):

    def test_the_only_executable_state_changing_types_are_fdr3s(self):
        # Until FDR-3 there were none. FDR-3 grants exactly the two S-OPS
        # transitions (P13-ENV-02); every other non-read-only type is reserved
        # or has no executor.
        executable = sorted(a.name for a in CATALOG.values()
                            if a.effect != READ_ONLY and not a.reserved and a.run)
        self.assertEqual(executable, ["s_ops.close", "s_ops.open"])
        self.assertNotIn(FIXTURE, CATALOG)

    def test_the_evidence_envelope_grants_no_state_change_and_declares_no_targets(self):
        envelopes, _ = load_envelopes(Paths(REPO_ROOT))
        envelope = {e.id: e for e in envelopes}["P13-ENV-01"]
        self.assertEqual(envelope.targets, ())
        for action_type in envelope.action_types:
            self.assertIn(CATALOG[action_type].effect, ("read-only", "record"))

    def test_the_only_state_changing_envelope_is_fdr3s_and_names_one_object(self):
        envelopes, _ = load_envelopes(Paths(REPO_ROOT))
        self.assertEqual([e.id for e in envelopes], ["P13-ENV-01", "P13-ENV-02"])
        envelope = {e.id: e for e in envelopes}["P13-ENV-02"]
        self.assertEqual(envelope.identifier, "FDR-3")
        self.assertEqual(envelope.action_types, ("s_ops.close", "s_ops.open"))
        self.assertEqual(envelope.cycle_basis, ())
        self.assertEqual(dict(envelope.targets), {
            "s_ops.close": ("docs/operations/s-ops/S-OPS-01.json",),
            "s_ops.open": ("docs/operations/s-ops/S-OPS-01.json",)})


if __name__ == "__main__":
    unittest.main()
