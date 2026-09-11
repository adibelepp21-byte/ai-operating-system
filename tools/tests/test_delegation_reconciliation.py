"""`ACT-CC-P11-013` — the W3 ↔ operational ledger reconciliation, attacked.

`§18` requires six probes, `§19` requires every control to be mutation-tested,
and `§20` requires the controls not to report legitimate history as corruption.
The order matters: a control that fires on everything satisfies `§18` and fails
`§20`, and a control that fires on nothing satisfies `§20` and fails `§18`.

Each probe below builds a **real inconsistency on disk or in the object graph**
and asserts the specific defect kind. Asserting merely that *some* defect fired
would pass for any of the eight, which is the shape of proxy control this
programme has now corrected ten times.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from tools.delegation_reconciliation import (  # noqa: E402
    ACTIVE,
    CURRENT,
    DEFECT_KINDS,
    HISTORICAL,
    INVALID,
    LedgerGrant,
    MISSING,
    Projection,
    REVOKED,
    ReconciliationError,
    SUPERSEDED,
    UNKNOWN,
    read_ledger,
    read_projections,
    reconcile,
    project,
    project_all,
)

FD_RECORD = ("docs/governance/acts/"
             "FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md")


def grant(delegation_id="a" * 16, lifecycle=ACTIVE, instance="inst-1",
          scope=("cap-1",), source="ledger/x.delegation.json"):
    return LedgerGrant(
        delegation_id=delegation_id, lifecycle=lifecycle,
        recipient_instance=instance, capability_scope=tuple(scope),
        authority_instrument="FD-P11-001 §9", authority_record=FD_RECORD,
        accountable_party="Claude Code / AIOS Co-Founder", source=source)


def projection(key="rec", grant_id="a" * 16, role=CURRENT, instance="inst-1",
               scope="cap-1"):
    return Projection(key=key, record=f"{key}.md", grant_id=grant_id,
                      role=role, authorized_scope=scope,
                      delegated_actor=instance)


def kinds(result):
    return [kind for kind, _, _ in result["defects"]]


class Probe_A_ActiveGrantMissingFromW3(unittest.TestCase):
    """`§18` Probe A — an `ACTIVE` grant with no `CURRENT` projection."""

    def test_unrepresented_active_grant_is_detected(self):
        result = reconcile(projections=[], grants={"a" * 16: grant()})
        self.assertIn("unrepresented-active-grant", kinds(result))

    def test_mutation_representing_it_clears_exactly_that_defect(self):
        """`§19` — the same state, made consistent, must stop firing."""
        result = reconcile(projections=[projection()],
                           grants={"a" * 16: grant()})
        self.assertNotIn("unrepresented-active-grant", kinds(result))
        self.assertEqual([], result["defects"])

    def test_the_check_starts_from_the_ledger_not_from_a_record(self):
        """The direction nothing was looking in. With **zero** projections the
        defect must still fire — a record that does not exist cannot be
        inspected into existence."""
        result = reconcile(projections=[], grants={"a" * 16: grant()})
        self.assertEqual(["unrepresented-active-grant"], kinds(result))


class Probe_B_W3PointsToRevokedGrant(unittest.TestCase):
    """`§18` Probe B — the defect `ACT-CC-P11-012` found on disk."""

    def test_current_projection_of_a_revoked_grant_is_stale(self):
        result = reconcile(
            projections=[projection()],
            grants={"a" * 16: grant(lifecycle=REVOKED)})
        self.assertIn("stale-active-claim", kinds(result))

    def test_it_fires_for_superseded_and_invalid_too(self):
        """`§8` — every non-`ACTIVE` lifecycle, not just the one word."""
        for lifecycle in (REVOKED, SUPERSEDED, INVALID, UNKNOWN):
            with self.subTest(lifecycle=lifecycle):
                result = reconcile(
                    projections=[projection()],
                    grants={"a" * 16: grant(lifecycle=lifecycle)})
                self.assertIn("stale-active-claim", kinds(result))

    def test_mutation_reclassifying_as_history_clears_it(self):
        """`§19` + `§20` — the *record's* role is what changes, not the grant's
        status, which W3 has no authority to change."""
        result = reconcile(
            projections=[projection(role=HISTORICAL)],
            grants={"a" * 16: grant(lifecycle=REVOKED)})
        self.assertNotIn("stale-active-claim", kinds(result))


class Probe_C_W3ReferencesNonexistentGrant(unittest.TestCase):
    """`§18` Probe C / `§11` — a reference to a grant no ledger holds."""

    def test_unknown_grant_is_rejected(self):
        result = reconcile(projections=[projection(grant_id="f" * 16)],
                           grants={})
        self.assertIn("unknown-grant", kinds(result))

    def test_it_is_not_read_as_a_valid_delegation(self):
        """`§11`: *"It must not be interpreted as a valid delegation."* So it
        must not also count as representing anything."""
        result = reconcile(projections=[projection(grant_id="f" * 16)],
                           grants={"a" * 16: grant()})
        self.assertEqual([], result["represented_active"])
        self.assertIn("unrepresented-active-grant", kinds(result))

    def test_mutation_pointing_at_the_real_grant_clears_it(self):
        result = reconcile(projections=[projection(grant_id="a" * 16)],
                           grants={"a" * 16: grant()})
        self.assertEqual([], result["defects"])


class Probe_D_InvalidProvenance(unittest.TestCase):
    """`§18` Probe D / `§12` — a delegation does not become valid because a
    record exists on either side."""

    def test_an_active_grant_whose_authority_record_is_gone_is_invalid(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "ops"
            root.mkdir()
            (root / "aaaa.delegation.json").write_text(json.dumps({
                "delegation_id": "a" * 16, "status": ACTIVE,
                "recipient_instance": "inst-1", "capability_scope": ["cap-1"],
                "authority_instrument": "FD-P11-001 §9",
                "authority_record": "docs/governance/acts/NOT-A-FILE.md",
                "accountable_party": "Claude Code / AIOS Co-Founder",
            }), encoding="utf-8")
            grants = read_ledger((root,), Path(tmp))
            self.assertEqual(INVALID, grants["a" * 16].lifecycle)

    def test_projection_contradicting_its_grants_recipient_is_a_mismatch(self):
        result = reconcile(
            projections=[projection(instance="someone-else")],
            grants={"a" * 16: grant(instance="inst-1")})
        self.assertIn("provenance-mismatch", kinds(result))

    def test_projection_claiming_a_scope_the_grant_lacks_is_a_mismatch(self):
        result = reconcile(
            projections=[projection(scope="cap-9")],
            grants={"a" * 16: grant(scope=("cap-1",))})
        self.assertIn("provenance-mismatch", kinds(result))

    def test_mutation_matching_the_grant_clears_it(self):
        result = reconcile(projections=[projection(instance="inst-1",
                                                   scope="cap-1")],
                           grants={"a" * 16: grant()})
        self.assertNotIn("provenance-mismatch", kinds(result))


class Probe_E_DuplicateRepresentation(unittest.TestCase):
    """`§18` Probe E — two `CURRENT` projections of one grant."""

    def test_duplicate_current_projections_are_detected(self):
        result = reconcile(
            projections=[projection(key="one"), projection(key="two")],
            grants={"a" * 16: grant()})
        self.assertIn("duplicate-representation", kinds(result))

    def test_one_current_and_one_historical_is_not_a_duplicate(self):
        """`§20` false-positive control — history beside a live projection is
        the state `§16` explicitly requires be possible."""
        result = reconcile(
            projections=[projection(key="one"),
                         projection(key="two", role=HISTORICAL,
                                    grant_id="b" * 16)],
            grants={"a" * 16: grant(),
                    "b" * 16: grant(delegation_id="b" * 16,
                                    lifecycle=SUPERSEDED)})
        self.assertEqual([], result["defects"])

    def test_mutation_removing_one_clears_it(self):
        result = reconcile(projections=[projection(key="one")],
                           grants={"a" * 16: grant()})
        self.assertNotIn("duplicate-representation", kinds(result))


class Probe_F_ValidSynchronizedState(unittest.TestCase):
    """`§18` Probe F — the consistent case must actually pass."""

    def test_no_defects_when_ledger_and_w3_agree(self):
        result = reconcile(projections=[projection()],
                           grants={"a" * 16: grant()})
        self.assertEqual([], result["defects"])

    def test_the_resident_corpus_is_currently_reconciled(self):
        """The real thing, not a fixture. This is the `§35` gap-closure state."""
        result = reconcile()
        self.assertEqual([], result["defects"], result["defects"])
        self.assertEqual(result["active_grants"], result["represented_active"])


class FalsePositiveControls(unittest.TestCase):
    """`§20` — legitimate historical state is not corruption."""

    def test_a_revoked_grant_with_no_projection_is_not_a_defect(self):
        result = reconcile(projections=[],
                           grants={"a" * 16: grant(lifecycle=REVOKED)})
        self.assertEqual([], result["defects"])

    def test_historical_projection_of_a_superseded_grant_is_clean(self):
        result = reconcile(
            projections=[projection(role=HISTORICAL)],
            grants={"a" * 16: grant(lifecycle=SUPERSEDED)})
        self.assertEqual([], result["defects"])

    def test_history_may_not_claim_a_live_grant(self):
        """The other side of the same boundary: `HISTORICAL` is a claim too, and
        a false one when the grant is still `ACTIVE`."""
        result = reconcile(projections=[projection(role=HISTORICAL)],
                           grants={"a" * 16: grant(lifecycle=ACTIVE)})
        self.assertIn("history-claims-live-grant", kinds(result))
        self.assertIn("unrepresented-active-grant", kinds(result))

    def test_the_resident_historical_record_is_not_reported_as_a_defect(self):
        """The real preserved record — `fd1f1302b0224b97` is `SUPERSEDED` and
        its record says `HISTORICAL`. If `§20` were unimplemented this would be
        the first thing to fire."""
        result = reconcile()
        historical = [p for p in result["projections"]
                      if p.role == HISTORICAL]
        self.assertTrue(historical, "no resident HISTORICAL record to test")
        for p in historical:
            self.assertNotIn(p.key, [key for _, key, _ in result["defects"]])


class LifecycleDerivation(unittest.TestCase):
    """`§8` — every state derived from resident data, none invented."""

    def _ledger(self, tmp, *records, evidence=None):
        root = Path(tmp) / "ops"
        root.mkdir(exist_ok=True)
        for name, payload in records:
            (root / name).write_text(json.dumps(payload), encoding="utf-8")
        if evidence is not None:
            (root / "run.evidence.json").write_text(json.dumps(evidence),
                                                    encoding="utf-8")
        return read_ledger((root,), REPO_ROOT)

    def test_active_and_revoked_come_from_the_ledgers_own_vocabulary(self):
        with tempfile.TemporaryDirectory() as tmp:
            grants = self._ledger(
                tmp,
                ("a.delegation.json", {"delegation_id": "a" * 16,
                                       "status": ACTIVE,
                                       "authority_record": FD_RECORD}),
                ("b.delegation.json", {"delegation_id": "b" * 16,
                                       "status": REVOKED}))
            self.assertEqual(ACTIVE, grants["a" * 16].lifecycle)
            self.assertEqual(REVOKED, grants["b" * 16].lifecycle)

    def test_superseded_is_derived_from_the_evidence_trail(self):
        with tempfile.TemporaryDirectory() as tmp:
            grants = self._ledger(
                tmp,
                ("b.delegation.json", {"delegation_id": "b" * 16,
                                       "status": REVOKED}),
                evidence={"superseded_grants": ["b" * 16]})
            self.assertEqual(SUPERSEDED, grants["b" * 16].lifecycle)

    def test_unknown_is_corruption_and_is_not_absence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "ops"
            root.mkdir()
            (root / "broken.delegation.json").write_text("{not json",
                                                         encoding="utf-8")
            grants = read_ledger((root,), REPO_ROOT)
            self.assertEqual(1, len(grants))
            self.assertEqual(UNKNOWN, next(iter(grants.values())).lifecycle)

    def test_missing_is_a_reconciliation_finding_not_a_stored_status(self):
        """`MISSING` describes a reference, so it must not appear as a grant
        lifecycle anywhere in the resident ledger."""
        self.assertNotIn(MISSING,
                         set(reconcile()["lifecycles"].values()))


class NoAuthorityCreation(unittest.TestCase):
    """`§13` — reconciliation is observational and corrective, never creative."""

    def test_projecting_a_revoked_grant_is_refused(self):
        with self.assertRaises(ReconciliationError) as caught:
            project("a" * 16, grants={"a" * 16: grant(lifecycle=REVOKED)},
                    root=Path(tempfile.mkdtemp()))
        self.assertIn("may not convert", str(caught.exception))

    def test_projecting_an_unknown_grant_is_refused(self):
        with self.assertRaises(ReconciliationError):
            project("f" * 16, grants={}, root=Path(tempfile.mkdtemp()))

    def test_projecting_a_grant_with_unresolvable_provenance_is_refused(self):
        broken = LedgerGrant(
            delegation_id="a" * 16, lifecycle=ACTIVE, recipient_instance="i",
            capability_scope=("c",), authority_instrument="FD-P11-001 §9",
            authority_record="docs/governance/acts/NOT-A-FILE.md",
            accountable_party="acc", source="x")
        with self.assertRaises(ReconciliationError) as caught:
            project("a" * 16, grants={"a" * 16: broken},
                    root=Path(tempfile.mkdtemp()))
        self.assertIn("does not\nresolve".replace("\n", " "),
                      " ".join(str(caught.exception).split()))

    def test_a_historical_record_is_never_rewritten(self):
        """`§16` — the one file class the writer refuses to touch."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # Key gained an operational-context segment under
            # `DP-02 §11` item 10; the invariant is unchanged.
            path = root / "w3-current-ledger-inst-1.md"
            path.write_text("# kept\n\n## Representation\n\nHISTORICAL\n",
                            encoding="utf-8")
            before = path.read_text(encoding="utf-8")
            with self.assertRaises(ReconciliationError) as caught:
                project("a" * 16, grants={"a" * 16: grant()}, root=root)
            self.assertIn("preserved history", str(caught.exception))
            self.assertEqual(before, path.read_text(encoding="utf-8"))

    def test_the_module_holds_no_grant_registry_of_its_own(self):
        """`§6` — one canonical delegation. A second store would be the
        duplicate model, and the easiest one to build by accident.

        Read by **AST, not substring**. The first version of this control
        matched raw source and failed on the module docstring, which names
        `W4DelegationRegistry` precisely to explain that the *ledger* owns
        identity. A control that cannot tell a citation from a call would have
        forced that explanation out of the file to stay green — punishing the
        documentation for describing the boundary it enforces.
        """
        import ast
        source = (REPO_ROOT / "tools/delegation_reconciliation.py").read_text(
            encoding="utf-8")
        tree = ast.parse(source)
        referenced = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                referenced.add(node.id)
            elif isinstance(node, ast.Attribute):
                referenced.add(node.attr)
            elif isinstance(node, ast.Import):
                referenced.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom):
                referenced.add((node.module or "").split(".")[-1])
                referenced.update(a.name for a in node.names)
        for forbidden in ("W4DelegationRegistry", "AgentInstanceRegistry",
                          "uuid", "revoke", "issue", "w4_delegation"):
            self.assertNotIn(forbidden, referenced, forbidden)


class Idempotency(unittest.TestCase):
    """`§17` — repeated reconciliation against unchanged state changes nothing."""

    def test_reconcile_is_stable_across_repeated_calls(self):
        first = reconcile()
        for _ in range(3):
            again = reconcile()
            self.assertEqual(first["defects"], again["defects"])
            self.assertEqual(first["lifecycles"], again["lifecycles"])
            self.assertEqual(first["represented_active"],
                             again["represented_active"])

    def test_projection_writes_are_byte_stable_and_do_not_multiply(self):
        root = REPO_ROOT / "docs/architecture/organization/delegations"
        before = {p.name: p.read_text(encoding="utf-8")
                  for p in sorted(root.glob("*.md"))}
        for _ in range(3):
            project_all()
        after = {p.name: p.read_text(encoding="utf-8")
                 for p in sorted(root.glob("*.md"))}
        self.assertEqual(before, after)

    def test_a_mutated_record_is_restored_rather_than_duplicated(self):
        """The control that proves the previous test is not inspecting a state
        that was already clean — mutate, re-project, and require repair."""
        root = REPO_ROOT / "docs/architecture/organization/delegations"
        target = root / "w3-current-w4-engineering-intelligence-instance-001.md"
        original = target.read_text(encoding="utf-8")
        try:
            target.write_text(original.replace(
                "## Operational Grant\n\n4313bd2246124a94",
                "## Operational Grant\n\n" + "0" * 16), encoding="utf-8")
            self.assertIn("unknown-grant", kinds(reconcile()))
            names_before = sorted(p.name for p in root.glob("*.md"))
            project_all()
            self.assertEqual(original, target.read_text(encoding="utf-8"))
            self.assertEqual(names_before,
                             sorted(p.name for p in root.glob("*.md")))
        finally:
            target.write_text(original, encoding="utf-8")


class FreshProcessContinuity(unittest.TestCase):
    """`§22` — a new process reconstructs the same relation, from files alone."""

    def test_a_separate_interpreter_sees_the_same_reconciliation(self):
        script = (
            "import sys, json; sys.path.insert(0, %r);"
            "from tools.delegation_reconciliation import reconcile;"
            "r = reconcile();"
            "print(json.dumps({'defects': [list(d) for d in r['defects']],"
            "'active': r['active_grants'],"
            "'represented': r['represented_active'],"
            "'lifecycles': r['lifecycles']}))" % str(REPO_ROOT))
        completed = subprocess.run(
            [sys.executable, "-c", script], capture_output=True, text=True,
            cwd=str(REPO_ROOT))
        self.assertEqual(0, completed.returncode, completed.stderr)
        fresh = json.loads(completed.stdout)
        here = reconcile()
        self.assertEqual([], fresh["defects"])
        self.assertEqual(here["active_grants"], fresh["active"])
        self.assertEqual(here["represented_active"], fresh["represented"])
        self.assertEqual(here["lifecycles"], fresh["lifecycles"])

    def test_a_fresh_process_does_not_resurrect_a_revoked_grant(self):
        """`§22`, stated as a prohibition rather than a property."""
        result = reconcile()
        for grant_id, lifecycle in result["lifecycles"].items():
            if lifecycle in (REVOKED, SUPERSEDED):
                self.assertNotIn(grant_id, result["represented_active"])


class ContractBoundaries(unittest.TestCase):
    """`§21`, `§23`, `§24` — what reconciliation may not become."""

    def test_w3_representation_is_not_w4_execution_authority(self):
        """`§21` — W3 must not open an execution path of its own."""
        source = (REPO_ROOT / "tools/delegation_reconciliation.py").read_text(
            encoding="utf-8")
        for executor in ("W4Executor", "execute(", "ExecutionSession",
                         "AIOSRuntime"):
            self.assertNotIn(executor, source, executor)

    def test_the_result_is_evidence_and_carries_no_verdict_of_authority(self):
        """`§23` — W6 may observe a discrepancy; it may not resolve authority.
        The result therefore contains no approval-shaped key."""
        result = reconcile()
        for forbidden in ("authorized", "approved", "granted", "permitted"):
            self.assertNotIn(forbidden, result)

    def test_no_defect_kind_claims_to_repair_governance(self):
        """`§24` — a governance conflict is classified, never inferred away."""
        self.assertEqual(8, len(DEFECT_KINDS))
        self.assertEqual(len(DEFECT_KINDS), len(set(DEFECT_KINDS)))
        for kind in DEFECT_KINDS:
            self.assertNotIn("authorize", kind)
            self.assertNotIn("approve", kind)

    def test_every_declared_defect_kind_can_actually_fire(self):
        """A kind that no fixture can produce is a claim, not a control. Seven
        are proven by the probes above; this asserts the declared list and the
        reachable set are the same set."""
        produced = set()
        produced.update(kinds(reconcile(projections=[],
                                        grants={"a" * 16: grant()})))
        produced.update(kinds(reconcile(
            projections=[projection()],
            grants={"a" * 16: grant(lifecycle=REVOKED)})))
        produced.update(kinds(reconcile(projections=[projection(
            grant_id="f" * 16)], grants={})))
        produced.update(kinds(reconcile(projections=[projection(
            grant_id=None)], grants={})))
        produced.update(kinds(reconcile(projections=[projection(role="LIVE")],
                                        grants={"a" * 16: grant()})))
        produced.update(kinds(reconcile(
            projections=[projection(key="one"), projection(key="two")],
            grants={"a" * 16: grant()})))
        produced.update(kinds(reconcile(
            projections=[projection(role=HISTORICAL)],
            grants={"a" * 16: grant()})))
        produced.update(kinds(reconcile(
            projections=[projection(instance="other")],
            grants={"a" * 16: grant()})))
        self.assertEqual(set(DEFECT_KINDS), produced)


class ResidentState(unittest.TestCase):
    """`§33` success criteria, asserted against the real corpus."""

    def test_S1_every_active_grant_is_reconciled(self):
        result = reconcile()
        self.assertEqual(sorted(result["active_grants"]),
                         sorted(result["represented_active"]))
        # Re-anchored: this asserted exactly two live grants, which encoded the
        # number of operational roots at the time. An instance may now hold one
        # live grant per root, so the invariant is the correspondence, not the
        # count.
        self.assertTrue(result["active_grants"])

    def test_S6_history_stays_distinguishable_from_live(self):
        lifecycles = reconcile()["lifecycles"]
        self.assertIn(SUPERSEDED, lifecycles.values())
        self.assertIn(ACTIVE, lifecycles.values())

    def test_S13_no_new_native_core_boundary(self):
        core = REPO_ROOT / "native_core" / "core"
        boundaries = sorted(p.name for p in core.iterdir()
                            if p.is_dir() and not p.name.startswith("_"))
        self.assertEqual(11, len(boundaries), boundaries)

    def test_the_existing_w3_verifier_still_reports_no_defects(self):
        """The generated records must satisfy the checks that already existed,
        not only the new ones."""
        from tools.delegation_catalog import report
        self.assertEqual([], report()["defects"])


if __name__ == "__main__":
    unittest.main()
