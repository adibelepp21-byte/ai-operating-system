"""S-OPS (`FDR-3`): the surface, and P13 acting on it through the real path.

**Everything here is TEST evidence, never live evidence.** The S-OPS root is
temporary: `Paths(REPO_ROOT, <tmp>/live).s_ops` is `<tmp>/live/s-ops`, never
`docs/operations/s-ops`. Authority comes from temporary copies of the real
Delegation Register and the real `P13-ENV-01` and `P13-ENV-02` records. The
gate therefore resolves exactly what is recorded, and each negative control
changes only a copy.

What is real: the surface (`tools/s_ops/surface.py`), P13's `s_ops` Source, the
two `CR-SOPS-01-*` criteria, the `s_ops.open`/`s_ops.close` action types, the
gate, the executor, the cycle, and the evidence store. Memory and authority are
the real Sources. The corpus Sources are left out, only to keep the suite fast.

The negative controls are FDR-3 `§10`'s NC-01…NC-05. Each asserts the decision,
that the object's bytes are unchanged, and that the refusal is traced.
"""

from __future__ import annotations

import ast
import hashlib
import json
import tempfile
import unittest
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

from tools.p13 import cycle
from tools.p13.authority import AuthorityGate, authority_dimensions, load_envelopes
from tools.p13.catalog import CATALOG, STATE_CHANGING, ActionType
from tools.p13.evaluation import CRITERIA, Evaluation
from tools.p13.evidence import EvidenceStore, decision_provenance
from tools.p13.model import (ESCALATE, EXECUTE, PASS, REFUSE, VERIFIED,
                             ActionProposal)
from tools.p13.paths import REPO_ROOT, Paths
from tools.p13.state import SOURCES, Source
from tools.s_ops import surface

ENVELOPES = REPO_ROOT / "docs/governance/p13-envelopes"
DELEGATIONS = REPO_ROOT / "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md"
OPEN_CR = "CR-SOPS-01-OPEN-WITHIN-WINDOW"
CLOSED_CR = "CR-SOPS-01-CLOSED-OUTSIDE-WINDOW"
STATE_KEY = "s_ops.S-OPS-01.state"
#: The Delegation Register append that retires P13-ENV-02 (FDR-4 FD-B). The
#: proof-window tests run on the Register as it stood before it.
RETIREMENT = "\n---\n\n## 16. P13-ENV-02 Retirement Append"


def register_during_the_proof() -> str:
    text = DELEGATIONS.read_text(encoding="utf-8")
    assert RETIREMENT in text, "the retirement append moved; re-derive the proof-window Register"
    return text.split(RETIREMENT, 1)[0] + "\n"


S_OPS_SOURCES = tuple(s for s in SOURCES if s.name in ("memory", "authority", "s_ops"))
S_OPS_CRITERIA = tuple(c for c in CRITERIA if c.id.startswith("CR-SOPS-"))


def at(minutes: float, base: Optional[datetime] = None) -> str:
    return ((base or datetime.now(timezone.utc)) + timedelta(minutes=minutes)).isoformat()


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


# ---------------------------------------------------------------------------
# The surface alone
# ---------------------------------------------------------------------------

class TheSurface(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "s-ops"

    def tearDown(self):
        self._tmp.cleanup()

    def provision(self, opens=-5, closes=60):
        return surface.provision(self.root, opens_at=at(opens), closes_at=at(closes),
                                 actor="tests")

    def test_provisioning_creates_one_closed_object_once(self):
        made = self.provision()
        self.assertEqual((made["state"], made["owner"], made["object"]),
                         (surface.CLOSED, surface.OWNER, surface.OBJECT_ID))
        self.assertEqual(surface.read(self.root), made)
        with self.assertRaises(surface.SurfaceError):
            self.provision()
        self.assertEqual([p.name for p in self.root.iterdir()], ["S-OPS-01.json"])

    def test_the_phase_is_observed_from_the_window_and_the_clock(self):
        base = datetime.now(timezone.utc)
        window = {"opens_at": at(0, base), "closes_at": at(10, base)}
        now = datetime.fromisoformat(window["opens_at"])
        self.assertEqual(surface.phase(window, now - timedelta(seconds=1)), surface.BEFORE)
        self.assertEqual(surface.phase(window, now), surface.WITHIN)
        self.assertEqual(surface.phase(window, now + timedelta(minutes=10)), surface.AFTER)
        self.assertEqual(surface.observe(self.root, now)["phase"], surface.UNPROVISIONED)

    def test_open_only_within_and_close_only_outside(self):
        self.provision(opens=5, closes=60)                      # BEFORE
        with self.assertRaisesRegex(surface.SurfaceError, "BEFORE"):
            surface.transition(self.root, "open", actor="t", basis="t")
        inside = datetime.now(timezone.utc) + timedelta(minutes=10)
        surface.transition(self.root, "open", actor="t", basis="t", at=inside)
        with self.assertRaisesRegex(surface.SurfaceError, "WITHIN"):
            surface.transition(self.root, "close", actor="t", basis="t", at=inside)
        after = datetime.now(timezone.utc) + timedelta(minutes=61)
        surface.transition(self.root, "close", actor="t", basis="t", at=after)
        self.assertEqual(surface.read(self.root)["state"], surface.CLOSED)

    def test_compare_and_set_on_the_recorded_state(self):
        self.provision()
        with self.assertRaisesRegex(surface.SurfaceError, "is CLOSED, not OPEN"):
            surface.transition(self.root, "close", actor="t", basis="t")
        surface.transition(self.root, "open", actor="t", basis="t")
        with self.assertRaisesRegex(surface.SurfaceError, "is OPEN, not CLOSED"):
            surface.transition(self.root, "open", actor="t", basis="t")

    def test_no_other_transition_exists(self):
        self.provision()
        for name in ("delete", "reopen", "set", "OPEN", ""):
            with self.assertRaises(surface.SurfaceError):
                surface.transition(self.root, name, actor="t", basis="t")
        self.assertEqual(set(surface.TRANSITIONS), {"open", "close"})

    def test_history_is_appended_and_never_rewritten(self):
        self.provision()
        first = surface.read(self.root)["history"]
        surface.transition(self.root, "open", actor="t", basis="t")
        second = surface.read(self.root)["history"]
        after = datetime.now(timezone.utc) + timedelta(minutes=61)
        surface.transition(self.root, "close", actor="t", basis="t", at=after)
        third = surface.read(self.root)["history"]
        self.assertEqual((second[:1], third[:2]), (first, second))
        self.assertEqual([h["event"] for h in third], ["provisioned", "open", "close"])

    def test_a_foreign_or_malformed_object_is_not_s_ops_state(self):
        self.provision()
        for change in ({"owner": "P11"}, {"object": "S-OPS-02"}, {"state": "HALF"},
                       {"window": {"opens_at": at(5), "closes_at": at(1)}},
                       {"history": []}):
            record = json.loads(surface.path(self.root).read_text(encoding="utf-8"))
            surface.path(self.root).write_text(json.dumps({**record, **change}),
                                               encoding="utf-8")
            with self.assertRaises(surface.SurfaceError, msg=change):
                surface.read(self.root)
            surface.path(self.root).write_text(json.dumps(record), encoding="utf-8")

    def test_writes_stay_in_the_root_and_leave_no_temporary_file(self):
        self.provision()
        surface.transition(self.root, "open", actor="t", basis="t")
        self.assertEqual(sorted(p.name for p in Path(self._tmp.name).rglob("*")),
                         ["S-OPS-01.json", "s-ops"])

    def test_the_surface_has_no_writer_but_provision_and_transition(self):
        tree = ast.parse(Path(surface.__file__).read_text(encoding="utf-8"))
        public = sorted(n.name for n in tree.body
                        if isinstance(n, ast.FunctionDef) and not n.name.startswith("_"))
        self.assertEqual(public, ["main", "observe", "path", "phase", "provision",
                                  "read", "transition", "utcnow"])

        def writes(call):
            name = getattr(call.func, "attr", getattr(call.func, "id", ""))
            owner = getattr(getattr(call.func, "value", None), "id", "")
            # `str.replace` is not a write; `os.replace` is.
            return (name in ("open", "mkstemp", "mkdir", "write_text", "write_bytes",
                             "unlink", "remove", "rename", "rmtree")
                    or (name == "replace" and owner == "os"))
        writers = sorted({f.name for f in tree.body if isinstance(f, ast.FunctionDef)
                          for n in ast.walk(f) if isinstance(n, ast.Call) and writes(n)})
        self.assertEqual(writers, ["_replace", "provision"])

    def test_the_surface_imports_nothing_from_p13(self):
        for path in Path(surface.__file__).parent.glob("*.py"):
            self.assertNotIn("tools.p13", path.read_text(encoding="utf-8"), path.name)


# ---------------------------------------------------------------------------
# P13 on S-OPS, through the real path
# ---------------------------------------------------------------------------

class Loop(unittest.TestCase):

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.envelope_dir = self.tmp / "envelopes"
        self.envelope_dir.mkdir()
        for name in ("P13-ENV-01.json", "P13-ENV-02.json"):
            (self.envelope_dir / name).write_bytes((ENVELOPES / name).read_bytes())
        self.register = self.tmp / "delegations.md"
        # Authority as recorded during the proof window: P13-ENV-02 ACTIVE,
        # before FDR-4 FD-B retired it. `Retired` below tests the Register now.
        self.register.write_text(register_during_the_proof(), encoding="utf-8")
        self.paths = Governed(REPO_ROOT, self.tmp / "live", self.envelope_dir,
                              self.register)
        self.assertTrue(str(self.paths.s_ops).startswith(str(self.tmp)))

    def tearDown(self):
        self._tmp.cleanup()

    # -- environment (the operator's part; never the decision) -------------
    def provision(self, opens=-5, closes=60):
        surface.provision(self.paths.s_ops, opens_at=at(opens), closes_at=at(closes),
                          actor="tests (operator)")

    def move_window(self, opens, closes):
        """Time passing, from the object's point of view. The operator's part."""
        record = json.loads(surface.path(self.paths.s_ops).read_text(encoding="utf-8"))
        record["window"] = {"opens_at": at(opens), "closes_at": at(closes)}
        surface.path(self.paths.s_ops).write_text(json.dumps(record), encoding="utf-8")

    def raw(self):
        path = surface.path(self.paths.s_ops)
        return path.read_bytes() if path.exists() else None

    def state(self):
        return surface.read(self.paths.s_ops)["state"]

    def reregister(self, name, record):
        """Replace an envelope copy and fix its new sha256 in the Register copy."""
        old = hashlib.sha256((self.envelope_dir / name).read_bytes()).hexdigest()
        raw = json.dumps(record, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
        (self.envelope_dir / name).write_bytes(raw)
        text = self.register.read_text(encoding="utf-8")
        self.assertIn(old, text)
        self.register.write_text(text.replace(old, hashlib.sha256(raw).hexdigest()),
                                 encoding="utf-8")

    def env02(self):
        return json.loads((self.envelope_dir / "P13-ENV-02.json").read_text(encoding="utf-8"))

    # -- P13 -----------------------------------------------------------------
    def run_cycle(self, intent="S-OPS test cycle", sources=S_OPS_SOURCES, **kw):
        return cycle.run_cycle(self.paths, intent=intent,
                               invoker="tools/tests/test_s_ops.py",
                               sources=sources, criteria=S_OPS_CRITERIA, **kw)

    def record(self, result):
        path = Path(result["record"])
        return json.loads((path if path.is_absolute() else REPO_ROOT / path)
                          .read_text(encoding="utf-8"))

    def traced(self, cycle_id):
        from native_core.core.infrastructure import LocalAppendOnlyStorage
        from native_core.core.trace import TraceReader
        storage = LocalAppendOnlyStorage(self.paths.trace)
        storage.provision()
        entries = [e for e in TraceReader(storage).read()
                   if (e.outputs or {}).get("cycle_id") == cycle_id]
        self.assertEqual(len(entries), 1)
        return entries[0]

    def s_ops_decisions(self, result):
        return {s: d for s, d in result["decisions"].items() if "s_ops." in s}

    def assert_refused_untouched_and_traced(self, result, before, decision, reason=""):
        self.assertEqual(self.raw(), before)
        decisions = self.s_ops_decisions(result)
        self.assertEqual(list(decisions.values()), [decision], result["decisions"])
        self.assertIsNone(result["executed"])
        entry = self.traced(result["cycle_id"])
        traced = [d for d in entry.outputs["decisions"] if "s_ops." in d["subject"]]
        self.assertEqual([d["decision"] for d in traced], [decision])
        self.assertIn(reason, traced[0]["reason"])
        return traced[0]

    def gate(self, catalog=CATALOG):
        envelopes, _ = load_envelopes(self.paths)
        return AuthorityGate(self.paths, catalog, envelopes)

    def proposal(self, action="s_ops.open", target=surface.OBJECT):
        return ActionProposal(f"p:{action}:{target}", action, target, ("c:test",),
                              "tests", VERIFIED, (0, "", action),
                              expected=((OPEN_CR, PASS),))


class CaseAValid(Loop):
    """FDR-3 `§9`: the full loop, TEST-VERIFIED on a temporary S-OPS."""

    def test_p13_decides_opens_verifies_traces_and_rediscovers(self):
        self.provision(opens=-5, closes=60)                      # WITHIN, CLOSED
        first = self.run_cycle()
        self.assertEqual(first["executed"], "s_ops.open")
        self.assertEqual(self.state(), surface.OPEN)
        self.assertEqual(first["consequence"]["expected"], {OPEN_CR: "PASS"})
        self.assertEqual(first["consequence"]["actual"], {OPEN_CR: "PASS/VERIFIED"})
        self.assertIs(first["consequence"]["matched"], True)
        record = self.record(first)
        self.assertEqual(decision_provenance(record), [])
        (executed,) = [d for d in record["decisions"] if d["decision"] == EXECUTE]
        self.assertIn("P13-ENV-02 (FDR-3 §4)", executed["reason"])
        (proposal,) = [p for p in record["proposals"] if p["action_type"] == "s_ops.open"]
        self.assertEqual((proposal["target"], proposal["derived_from"]),
                         (surface.OBJECT, [f"c:defect:{OPEN_CR}"]))
        before = {f["key"]: f["value"] for f in record["observation"]["before"]["facts"]}
        after = {f["key"]: f["value"] for f in record["observation"]["after"]["facts"]}
        self.assertEqual((before[STATE_KEY], after[STATE_KEY]), ("CLOSED", "OPEN"))
        report = next(f["value"] for f in record["executed"]["produced"]
                      if f["key"] == "execution.s_ops.open")
        self.assertEqual((report["changed"], report["outside_scope"], report["verified"]),
                         ([surface.OBJECT], [], True))
        last = surface.read(self.paths.s_ops)["history"][-1]
        self.assertEqual((last["event"], last["from"], last["to"]), ("open", "CLOSED", "OPEN"))
        self.assertIn("P13-ENV-02", last["basis"])
        entry = self.traced(first["cycle_id"])
        self.assertEqual(entry.status, "success")
        self.assertEqual((entry.outputs["execution"]["envelope"],
                          entry.outputs["execution"]["authority"],
                          list(entry.outputs["execution"]["scope"])),
                         ("P13-ENV-02", "FDR-3 §4", [surface.OBJECT]))

        second = self.run_cycle("S-OPS test cycle: rediscovery")
        self.assertEqual(self.s_ops_decisions(second), {})
        self.assertEqual(second["results"][OPEN_CR], "PASS/VERIFIED")
        self.assertEqual(self.state(), surface.OPEN)
        rediscovered = {f["key"]: f["value"] for f in
                        self.record(second)["observation"]["before"]["facts"]}
        self.assertEqual(rediscovered[STATE_KEY], "OPEN")
        self.assertTrue(EvidenceStore(self.paths).verify()["holds"])

    def test_before_the_window_p13_does_nothing(self):
        self.provision(opens=30, closes=60)
        before = self.raw()
        result = self.run_cycle()
        self.assertEqual(self.s_ops_decisions(result), {})
        self.assertEqual(result["results"], {OPEN_CR: "PASS/VERIFIED",
                                             CLOSED_CR: "PASS/VERIFIED"})
        self.assertEqual(self.raw(), before)

    def test_after_the_window_p13_reverses_and_the_history_survives(self):
        self.provision(opens=-5, closes=60)
        self.run_cycle()
        opened = surface.read(self.paths.s_ops)["history"]
        self.move_window(-60, -1)                                # AFTER, OPEN
        result = self.run_cycle("S-OPS test cycle: after the window")
        self.assertEqual(result["executed"], "s_ops.close")
        self.assertIs(result["consequence"]["matched"], True)
        self.assertEqual(result["consequence"]["expected"], {CLOSED_CR: "PASS"})
        history = surface.read(self.paths.s_ops)["history"]
        self.assertEqual(history[:2], opened)
        self.assertEqual([h["event"] for h in history], ["provisioned", "open", "close"])
        again = self.run_cycle("S-OPS test cycle: after the reversal")
        self.assertEqual(self.s_ops_decisions(again), {})
        self.assertTrue(EvidenceStore(self.paths).verify()["holds"])

    def test_an_unprovisioned_surface_asks_for_nothing(self):
        result = self.run_cycle()
        self.assertEqual(self.s_ops_decisions(result), {})
        self.assertIsNone(self.raw())


class NC01InvalidAuthority(Loop):

    def test_without_the_s_ops_envelope_p13_escalates_and_nothing_changes(self):
        (self.envelope_dir / "P13-ENV-02.json").unlink()
        self.provision()
        before = self.raw()
        self.assert_refused_untouched_and_traced(
            self.run_cycle(), before, ESCALATE, "no recorded envelope permits")

    def test_an_envelope_the_founder_did_not_issue_is_no_authority(self):
        self.reregister("P13-ENV-02.json", {**self.env02(), "issued_by": "Claude Code — CEO"})
        self.provision()
        before = self.raw()
        result = self.run_cycle()
        self.assert_refused_untouched_and_traced(result, before, ESCALATE,
                                                 "no recorded envelope permits")
        self.assertTrue(any("only a Founder-issued envelope" in a
                            for a in self.record(result)["authority"]["anomalies"]))

    def test_an_action_the_envelope_does_not_name_is_refused(self):
        self.provision()
        before = self.raw()
        gate = self.gate()
        self.assertEqual(gate.decide(self.proposal("s_ops.delete")).decision, REFUSE)
        self.assertEqual(gate.decide(self.proposal("change.governance")).decision, ESCALATE)
        self.assertEqual(self.raw(), before)


class NC02AmbiguousAuthority(Loop):

    def test_two_envelopes_granting_the_same_transition_conflict(self):
        twin = {**self.env02(), "envelope_id": "P13-ENV-T2"}
        raw = json.dumps(twin, indent=2).encode("utf-8")
        (self.envelope_dir / "P13-ENV-T2.json").write_bytes(raw)
        with open(self.register, "a", encoding="utf-8") as handle:
            handle.write(f"\n### P13-ENV-T2 — twin\n\n| **Record** | "
                         f"{hashlib.sha256(raw).hexdigest()} |\n| **Status** | **ACTIVE** |\n")
        self.provision()
        before = self.raw()
        self.assert_refused_untouched_and_traced(self.run_cycle(), before, ESCALATE,
                                                 "envelopes conflict")

    def test_an_envelope_recorded_twice_is_ambiguous(self):
        text = self.register.read_text(encoding="utf-8")
        section = text[text.index("### P13-ENV-02 —"):]
        self.register.write_text(text + "\n" + section, encoding="utf-8")
        self.provision()
        before = self.raw()
        result = self.run_cycle()
        self.assert_refused_untouched_and_traced(result, before, ESCALATE,
                                                 "no recorded envelope permits")
        self.assertTrue(any("AMBIGUOUS" in a
                            for a in self.record(result)["authority"]["anomalies"]))

    def test_an_expiry_that_is_not_a_date_is_ambiguous(self):
        self.reregister("P13-ENV-02.json", {**self.env02(), "expires": "after the proof"})
        self.provision()
        before = self.raw()
        result = self.run_cycle()
        self.assert_refused_untouched_and_traced(result, before, ESCALATE)
        self.assertTrue(any("AMBIGUOUS" in a
                            for a in self.record(result)["authority"]["anomalies"]))


class NC03InvalidTarget(Loop):

    def test_a_target_the_envelope_does_not_name_is_refused(self):
        record = self.env02()
        for grant in record["action_types"].values():
            grant["targets"] = ["docs/operations/s-ops/S-OPS-02.json"]
        self.reregister("P13-ENV-02.json", record)
        self.provision()
        before = self.raw()
        self.assert_refused_untouched_and_traced(self.run_cycle(), before, REFUSE,
                                                 "wrong target")

    def test_the_gate_refuses_every_other_path(self):
        self.provision()
        before = self.raw()
        gate = self.gate()
        for target in ("docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md",
                       "docs/operations/s-ops", "docs/operations/s-ops/S-OPS-01.json.bak",
                       "docs/operations/s-ops/S-OPS-DEFINITION.md",
                       "docs/operations/p13/cycles", "S-OPS-01.json"):
            decision = gate.decide(self.proposal(target=target))
            self.assertEqual(decision.decision, REFUSE, target)
            self.assertIn("wrong target", decision.reason)
        self.assertEqual(self.raw(), before)


class NC04FailedPrecondition(Loop):

    def test_the_window_had_not_opened_when_the_gate_decided(self):
        # P13 observes at an instant inside the window, but when the gate
        # decides, the window has not opened yet: the precondition is re-checked
        # against the world, not against the observation.
        self.provision(opens=30, closes=60)
        before = self.raw()
        inside = at(45)
        result = self.run_cycle(clock=lambda: inside)
        self.assertEqual(result["results"][OPEN_CR], "FAIL/VERIFIED")
        self.assert_refused_untouched_and_traced(result, before, REFUSE,
                                                 "missing precondition: S-OPS-01's window "
                                                 "phase is now BEFORE")

    def test_the_state_had_changed_when_the_gate_decided(self):
        self.provision()
        surface.transition(self.paths.s_ops, "open", actor="tests (operator)", basis="t")
        before = self.raw()
        stale = Source("s_ops", "tests: a stale observation of S-OPS-01",
                       ("s_ops.S-OPS-01.state", "s_ops.S-OPS-01.phase",
                        "s_ops.S-OPS-01.window"),
                       lambda p, c: {"s_ops.S-OPS-01.state": ("CLOSED", VERIFIED),
                                     "s_ops.S-OPS-01.phase": ("WITHIN", VERIFIED),
                                     "s_ops.S-OPS-01.window": ({}, VERIFIED)})
        sources = tuple(stale if s.name == "s_ops" else s for s in S_OPS_SOURCES)
        self.assert_refused_untouched_and_traced(
            self.run_cycle(sources=sources), before, REFUSE,
            "missing precondition: S-OPS-01 is OPEN, not CLOSED")

    def test_an_object_the_surface_does_not_own_fails_the_precondition(self):
        self.provision()
        path = surface.path(self.paths.s_ops)
        path.write_text(json.dumps({**json.loads(path.read_text(encoding="utf-8")),
                                    "owner": "P11"}), encoding="utf-8")
        before = self.raw()
        decision = self.gate().decide(self.proposal())
        self.assertEqual(decision.decision, REFUSE)
        self.assertIn("not the surface's own", decision.reason)
        self.assertEqual(self.raw(), before)


class NC05ConsequenceMismatch(Loop):
    """The environment fails; the implementation is not changed to pass."""

    def revert(self):
        """A concurrent operator puts the window back to CLOSED, outside the API."""
        path = surface.path(self.paths.s_ops)
        record = json.loads(path.read_text(encoding="utf-8"))
        path.write_text(json.dumps({**record, "state": "CLOSED"}), encoding="utf-8")

    def test_a_change_undone_before_re_observation_is_a_mismatch_not_a_success(self):
        self.provision()
        calls = []
        real = next(s for s in S_OPS_SOURCES if s.name == "s_ops")

        def world(paths, context):
            calls.append(1)
            if len(calls) == 2:          # after the execution, before re-observation
                self.revert()
            return real.read(paths, context)
        sources = tuple(Source(s.name, s.describe, s.keys, world)
                        if s.name == "s_ops" else s for s in S_OPS_SOURCES)
        first = self.run_cycle(sources=sources)
        self.assertEqual(first["executed"], "s_ops.open")
        self.assertEqual(self.record(first)["executed"]["status"], "success")
        self.assertIs(first["consequence"]["matched"], False)
        self.assertEqual(first["consequence"]["actual"], {OPEN_CR: "FAIL/VERIFIED"})
        self.assertEqual(self.traced(first["cycle_id"]).status, "failure")

        second = self.run_cycle("S-OPS test cycle: after a mismatch")
        self.assertIsNone(second["executed"])
        decisions = second["decisions"]
        self.assertEqual(decisions.get(f"P13 review.consequence s_ops.open:{surface.OBJECT}"),
                         ESCALATE, decisions)
        self.assertNotIn(f"P13 s_ops.open {surface.OBJECT}", decisions)
        self.assertEqual(self.state(), surface.CLOSED)

    def test_a_postcondition_that_does_not_hold_is_never_a_success(self):
        self.provision()
        real = CATALOG["s_ops.open"]

        def run(paths, target):
            produced = real.run(paths, target)
            self.revert()
            return produced
        catalog = {**CATALOG, "s_ops.open": ActionType(
            real.name, False, real.produces, real.executor, run, effect=STATE_CHANGING,
            observe=real.observe, verify=real.verify, preconditions=real.preconditions)}
        result = self.run_cycle(catalog=catalog)
        self.assertEqual(self.record(result)["executed"]["status"], "failure")
        self.assertIn("postcondition does not hold", self.record(result)["executed"]["detail"])
        self.assertIs(result["consequence"]["matched"], False)
        self.assertEqual(self.traced(result["cycle_id"]).status, "failure")

    def test_a_change_outside_the_object_is_a_failure(self):
        self.provision()
        real = CATALOG["s_ops.open"]

        def run(paths, target):
            produced = real.run(paths, target)
            (paths.s_ops / "stray.json").write_text("{}", encoding="utf-8")
            return produced
        catalog = {**CATALOG, "s_ops.open": ActionType(
            real.name, False, real.produces, real.executor, run, effect=STATE_CHANGING,
            observe=real.observe, verify=real.verify, preconditions=real.preconditions)}
        result = self.run_cycle(catalog=catalog)
        executed = self.record(result)["executed"]
        self.assertEqual(executed["status"], "failure")
        self.assertIn("docs/operations/s-ops/stray.json", executed["detail"])
        self.assertIs(result["consequence"]["matched"], False)


# ---------------------------------------------------------------------------
# What P13 holds, and what it cannot reach
# ---------------------------------------------------------------------------

class TheBoundary(unittest.TestCase):

    def test_a_test_never_reaches_the_real_s_ops_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(Paths(REPO_ROOT, Path(tmp) / "live").s_ops,
                             Path(tmp) / "live" / "s-ops")
        self.assertEqual(Paths(REPO_ROOT).s_ops, REPO_ROOT / "docs/operations/s-ops")

    def test_the_criteria_cite_fdr3_and_resolve(self):
        evaluation = Evaluation(Paths(REPO_ROOT), S_OPS_CRITERIA)
        self.assertEqual([c.id for c in evaluation.admitted], [OPEN_CR, CLOSED_CR])
        self.assertEqual(evaluation.refused, [])
        for criterion in S_OPS_CRITERIA:
            self.assertEqual(criterion.citation.identifier, "FDR-3")
            self.assertEqual(criterion.remedy_target, surface.OBJECT)
        self.assertEqual([c.remedy for c in S_OPS_CRITERIA], ["s_ops.open", "s_ops.close"])

    def test_the_contract_is_the_surfaces_not_p13s(self):
        self.assertEqual(surface.REQUIRED, {"BEFORE": "CLOSED", "WITHIN": "OPEN",
                                            "AFTER": "CLOSED"})

    def test_the_two_types_are_state_changing_verifiable_and_preconditioned(self):
        for name in ("s_ops.open", "s_ops.close"):
            action = CATALOG[name]
            self.assertEqual((action.effect, action.reserved, action.verifiable,
                              len(action.preconditions), action.executor),
                             (STATE_CHANGING, False, True, 3,
                              "tools.s_ops.surface.transition"))
        changing = sorted(n for n, a in CATALOG.items()
                          if a.effect != "read-only" and not a.reserved and a.run)
        self.assertEqual(changing, ["s_ops.close", "s_ops.open"])

    def test_the_boundary_covers_the_authority_records(self):
        keys = CATALOG["s_ops.open"].observe(Paths(REPO_ROOT), surface.OBJECT)
        for key in ("docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md",
                    "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md",
                    "docs/governance/p13-envelopes/P13-ENV-01.json",
                    "docs/governance/p13-envelopes/P13-ENV-02.json",
                    "docs/governance/acts/FDR-3-S-OPS-DEDICATED-BOUNDED-OPERATIONAL-"
                    "PROOF-SURFACE-FOR-E13-05.md",
                    "docs/operations/s-ops/S-OPS-DEFINITION.md"):
            self.assertIn(key, keys)
            self.assertNotEqual(keys[key], "absent", key)

    def test_the_projection_shows_no_state_changing_authority_and_the_retirement(self):
        dims = authority_dimensions(Paths(REPO_ROOT))["state_changing_authority"]
        self.assertEqual((dims["state"], dims["grants"], dims["retired"]),
                         ("NONE", [], [{"envelope": "P13-ENV-02", "retired_by": "FDR-4"}]))


# ---------------------------------------------------------------------------
# FDR-4 FD-B: P13-ENV-02 is spent. Its authority is gone; its evidence stays.
# ---------------------------------------------------------------------------

class Retired(Loop):
    """The Register as it is now, with the §16 retirement line."""

    def setUp(self):
        super().setUp()
        self.register.write_text(DELEGATIONS.read_text(encoding="utf-8"), encoding="utf-8")

    def test_p13_can_no_longer_open_s_ops_it_escalates_instead(self):
        self.provision()                              # WITHIN, CLOSED: the contract fails
        before = self.raw()
        result = self.run_cycle()
        self.assertEqual(result["results"][OPEN_CR], "FAIL/VERIFIED")
        self.assert_refused_untouched_and_traced(result, before, ESCALATE,
                                                 "no recorded envelope permits")
        self.assertEqual(self.record(result)["authority"]["anomalies"], [])

    def append(self, line):
        with open(self.register, "a", encoding="utf-8") as handle:
            handle.write("\n" + line + "\n")

    def test_retirement_needs_a_resolving_founder_decision(self):
        # These all leave P13-ENV-02 without authority. Only a REVOKED line
        # naming a resolving decision is "retired"; the rest are anomalies.
        for line in ("| `P13-ENV-02` | **REVOKED** |",
                     "| `P13-ENV-02` | **REVOKED** under `FDR-99` |",
                     "| `P13-ENV-02` | **SUSPENDED** under `FDR-4` |"):
            self.register.write_text(register_during_the_proof(), encoding="utf-8")
            self.append(line)
            envelopes, anomalies = load_envelopes(self.paths)
            self.assertNotIn("P13-ENV-02", [e.id for e in envelopes], line)
            self.assertTrue(any("revoked or suspended" in a for a in anomalies), line)

    def test_a_decision_the_decision_register_does_not_hold_retires_nothing(self):
        # FDR-4's act exists, but read against a Decision Register without §24
        # it does not resolve: the REVOKED line is then an anomaly.
        decisions = self.tmp / "decisions.md"
        text = (REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
                ).read_text(encoding="utf-8")
        marker = "\n---\n\n## 24. FDR-4 Append"
        self.assertIn(marker, text)
        decisions.write_text(text.split(marker, 1)[0] + "\n", encoding="utf-8")

        @dataclass(frozen=True)
        class WithoutFDR4(Governed):
            @property
            def decision_register(self):
                return decisions
        paths = WithoutFDR4(REPO_ROOT, self.tmp / "live", self.envelope_dir, self.register)
        envelopes, anomalies = load_envelopes(paths)
        self.assertNotIn("P13-ENV-02", [e.id for e in envelopes])
        self.assertTrue(any("P13-ENV-02" in a and "revoked" in a for a in anomalies))

    def test_the_proof_evidence_is_retained(self):
        self.assertTrue((REPO_ROOT / "docs/operations/s-ops/S-OPS-DEFINITION.md").is_file())
        self.assertTrue((ENVELOPES / "P13-ENV-02.json").is_file())
        real = json.loads((REPO_ROOT / surface.OBJECT).read_text(encoding="utf-8"))
        self.assertEqual([h["event"] for h in real["history"]],
                         ["provisioned", "open", "close"])
        self.assertEqual(real["state"], surface.CLOSED)


if __name__ == "__main__":
    unittest.main()
