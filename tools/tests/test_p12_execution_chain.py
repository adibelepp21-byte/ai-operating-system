"""P12-W4 execution chain conformance and falsification (`§23`, `§24`).

`§23` requires that every newly constructed relationship be attacked. Each class
here is one of its named tests, and each attacks the **reader**, because the
reader is what issues the verdict: a join that only the writer believes in is
not a join.

The reader resolves references against the records they point at rather than
checking that they are well-formed, so these tests plant references that are
well-formed and wrong.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_execution_chain_reader as reader
from tools import p12_execution_provenance as writer


def _live_manifest() -> dict:
    found = writer.manifests()
    assert found, "the integrated execution must have been run"
    return dict(found[0])


def _manifest_by_status(status: str) -> dict:
    for payload in writer.manifests():
        if payload.get("status") == status:
            return dict(payload)
    raise AssertionError(f"no persisted manifest with status {status!r}")


class TheChainHoldsOnTheLiveCorpus(unittest.TestCase):
    def test_the_seven_canonical_edges_are_read(self):
        self.assertEqual(
            list(reader.CHAIN_EDGES),
            [("INTENT", "DECISION"), ("DECISION", "WORK"),
             ("WORK", "DELEGATION"), ("DELEGATION", "EXECUTION"),
             ("EXECUTION", "OBSERVATION"), ("OBSERVATION", "VERIFICATION"),
             ("VERIFICATION", "EVIDENCE")])

    def test_the_real_execution_joins_every_edge(self):
        verdict = reader.verify_manifest(_live_manifest())
        self.assertTrue(verdict.joined, [
            (e.source, e.target, e.detail) for e in verdict.edges
            if e.status != reader.JOINED])
        self.assertEqual(len(verdict.edges), 7)

    def test_the_reader_shares_no_code_with_the_writer(self):
        """`§24`: implementation → self-report → pass is forbidden."""
        import ast
        source = (reader.REPO_ROOT / "tools"
                  / "p12_execution_chain_reader.py").read_text(encoding="utf-8")
        imported = set()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module)
            elif isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
        self.assertNotIn("tools.p12_execution_provenance", imported)
        self.assertFalse([m for m in imported if "provenance" in m])


class TestA_WrongDelegation(unittest.TestCase):
    """Can an execution be attributed to a delegation that did not authorize it?"""

    def test_a_delegation_that_does_not_exist_is_dangling(self):
        payload = dict(_live_manifest(), delegation_id="0" * 16)
        verdict = reader.verify_manifest(payload)
        self.assertFalse(verdict.joined)
        edge = [e for e in verdict.edges if e.target == "DELEGATION"][0]
        self.assertEqual(edge.status, reader.DANGLING)

    def test_a_real_delegation_issued_to_another_recipient_is_refused(self):
        """The join must be an authorization, not a label."""
        from tools import p12_provenance_verification as prov
        others = [d for d in prov.delegation_records()
                  if d.get("recipient_instance")
                  != _live_manifest()["agent_instance"]]
        self.assertTrue(others, "precondition: a grant to another recipient")
        payload = dict(_live_manifest(),
                       delegation_id=others[0]["delegation_id"])
        verdict = reader.verify_manifest(payload)
        self.assertFalse(verdict.joined)


class TestB_WrongWork(unittest.TestCase):
    """Can execution be joined to work the delegation never granted?"""

    def test_work_outside_the_granted_scope_is_refused(self):
        payload = dict(_live_manifest(),
                       work_scope=["something-nobody-granted"])
        verdict = reader.verify_manifest(payload)
        edge = [e for e in verdict.edges if e.target == "DELEGATION"][0]
        self.assertEqual(edge.status, reader.DANGLING)
        self.assertFalse(verdict.joined)

    def test_the_granted_scope_is_read_from_the_delegation_record(self):
        payload = _live_manifest()
        edge = [e for e in reader.verify_manifest(payload).edges
                if e.target == "DELEGATION"][0]
        self.assertIn("grants", edge.detail)


class TestC_MissingExecution(unittest.TestCase):
    """Can a manifest claim an execution that was never recorded?"""

    def test_a_trace_ordinal_past_the_end_is_dangling(self):
        payload = dict(_live_manifest(), trace_ordinal=9999)
        verdict = reader.verify_manifest(payload)
        edge = [e for e in verdict.edges if e.target == "EXECUTION"][0]
        self.assertEqual(edge.status, reader.DANGLING)

    def test_a_trace_store_that_does_not_exist_is_dangling(self):
        payload = dict(_live_manifest(), trace_store="no-such-store")
        verdict = reader.verify_manifest(payload)
        self.assertFalse(verdict.joined)


class TestD_MissingObservation(unittest.TestCase):
    """Can verification claim success for an execution nobody observed?"""

    def test_an_unobserved_subject_gives_no_verified_closure(self):
        payload = dict(_live_manifest(),
                       observation_subject="never-observed-runtime")
        verdict = reader.verify_manifest(payload)
        observation = [e for e in verdict.edges if e.target == "OBSERVATION"][0]
        verification = [e for e in verdict.edges
                        if e.target == "VERIFICATION"][0]
        self.assertEqual(observation.status, reader.DANGLING)
        self.assertEqual(verification.status, reader.DANGLING,
                         "verification must not close over a missing observation")

    def test_an_observation_of_a_different_runtime_is_refused(self):
        from tools import p12_runtime_observation as obs
        others = [o for o in obs.observations(obs.OBSERVATION_ROOT)
                  if o.runtime_id != _live_manifest()["runtime_id"]]
        self.assertTrue(others, "precondition: another observed runtime")
        payload = dict(_live_manifest(),
                       observation_subject=others[0].runtime_id)
        verdict = reader.verify_manifest(payload)
        edge = [e for e in verdict.edges if e.target == "OBSERVATION"][0]
        self.assertEqual(edge.status, reader.DANGLING)


class TestE_MissingEvidence(unittest.TestCase):
    """Can the system claim verified completion with no persisted evidence?"""

    def test_a_manifest_that_is_not_persisted_gives_no_closure(self):
        payload = dict(_live_manifest(), execution_id="never-persisted")
        verdict = reader.verify_manifest(payload)
        edge = [e for e in verdict.edges if e.target == "EVIDENCE"][0]
        self.assertEqual(edge.status, reader.DANGLING)
        self.assertFalse(verdict.joined)

    def test_an_incomplete_manifest_is_never_written(self):
        from tools.p12_execution_provenance import (
            ExecutionManifest, ProvenanceIncomplete, record)
        payload = _live_manifest()
        fields = {k: v for k, v in payload.items()
                  if k not in ("contract_elements", "recorded_at")}
        fields["goal"] = ""
        fields["work_scope"] = tuple(fields["work_scope"])
        fields["capability_scope"] = tuple(fields["capability_scope"])
        fields["authority_chain"] = tuple(fields["authority_chain"])
        manifest = ExecutionManifest(**fields)
        self.assertIn("intent", manifest.missing_elements())
        with self.assertRaises(ProvenanceIncomplete):
            record(manifest)


class TestF_ProcessRestart(unittest.TestCase):
    """Does the relationship survive a process boundary?"""

    def test_the_chain_verifies_in_a_fresh_interpreter(self):
        import subprocess
        result = subprocess.run(
            ["python3", "-c",
             "from tools.p12_execution_chain_reader import summary;"
             "print(summary()['joined'], summary()['dangling'])"],
            cwd=reader.REPO_ROOT, capture_output=True, text=True, check=True)
        joined, dangling = result.stdout.split()
        self.assertGreaterEqual(int(joined), 1)
        self.assertEqual(int(dangling), 0)


class TestG_DuplicateActor(unittest.TestCase):
    """Two executions by one actor must stay distinguishable."""

    def test_the_same_actor_holds_more_than_one_grant(self):
        from tools import p12_provenance_verification as prov
        actor = _live_manifest()["agent_instance"]
        grants = [d for d in prov.delegation_records()
                  if d.get("recipient_instance") == actor]
        self.assertGreater(len(grants), 1,
                           "precondition: actor name cannot be a join")

    def test_the_join_is_the_delegation_id_not_the_actor(self):
        """Swapping in another of this actor's own grants must not verify."""
        from tools import p12_provenance_verification as prov
        live = _live_manifest()
        actor = live["agent_instance"]
        others = [d for d in prov.delegation_records()
                  if d.get("recipient_instance") == actor
                  and d["delegation_id"] != live["delegation_id"]]
        self.assertTrue(others)
        payload = dict(live, delegation_id=others[0]["delegation_id"])
        verdict = reader.verify_manifest(payload)
        self.assertFalse(
            verdict.joined,
            "a grant held by the same actor must not satisfy the join")


class TestH_StaleObservation(unittest.TestCase):
    """Stale observation must be distinguishable from current state."""

    def test_the_observation_surface_classifies_staleness(self):
        from tools import p12_runtime_observation as obs
        found = [o for o in obs.observations(obs.OBSERVATION_ROOT)
                 if o.runtime_id == _live_manifest()["runtime_id"]]
        self.assertTrue(found)
        self.assertIn(found[0].classification,
                      {"LIVE", "STALE", "TERMINATED", "UNKNOWN"})

    def test_a_terminated_execution_is_not_reported_live(self):
        from tools import p12_runtime_observation as obs
        answer = obs.what_is_running(obs.OBSERVATION_ROOT)
        self.assertNotIn(_live_manifest()["runtime_id"], answer["live"])


class TheChainCarriesANonSuccessOutcome(unittest.TestCase):
    """`§26`: W4 must not assume only successful execution.

    A terminal state nothing has ever reached is not a state the system
    distinguishes, so a second real execution was run against an artifact the
    work genuinely fails against. The criteria are identical in both runs; only
    the subject differs, and the outcome is whatever the verification produced.
    """

    def test_a_failed_execution_is_recorded_and_joined(self):
        failed = _manifest_by_status("failure")
        verdict = reader.verify_manifest(failed)
        self.assertTrue(verdict.joined,
                        "a failure must carry the chain as fully as a success")

    def test_the_failure_is_real_not_injected(self):
        failed = _manifest_by_status("failure")
        outcome = failed["outcome"]
        self.assertGreater(len(outcome["unsatisfied"]), 0)
        self.assertEqual(outcome["criteria"],
                         outcome["satisfied"] + len(outcome["unsatisfied"]))

    def test_the_trace_record_carries_the_failure_status(self):
        from tools import p12_provenance_verification as prov
        failed = _manifest_by_status("failure")
        traces = [t for t in prov.trace_records()
                  if t.get("__store") == failed["trace_store"]
                  and t.get("__ordinal") == failed["trace_ordinal"]]
        self.assertEqual(len(traces), 1)
        self.assertEqual(traces[0]["status"], "failure")

    def test_success_and_failure_are_both_present(self):
        statuses = {m.get("status") for m in writer.manifests()}
        self.assertIn("success", statuses)
        self.assertIn("failure", statuses)


class TestG_DuplicateActorAtCorpusLevel(unittest.TestCase):
    """`§23` Test G against persisted records rather than a mutated copy."""

    def test_two_real_executions_share_one_actor(self):
        actors = {m["agent_instance"] for m in writer.manifests()}
        self.assertEqual(len(actors), 1,
                         "precondition: the actor name cannot distinguish them")
        self.assertGreaterEqual(len(writer.manifests()), 2)

    def test_they_are_distinguished_by_grant_not_by_actor(self):
        grants = [m["delegation_id"] for m in writer.manifests()]
        self.assertEqual(len(set(grants)), len(grants),
                         "each execution must carry its own grant")

    def test_each_addresses_its_own_trace_record(self):
        addresses = [(m["trace_store"], m["trace_ordinal"])
                     for m in writer.manifests()]
        self.assertEqual(len(set(addresses)), len(addresses))

    def test_swapping_the_two_real_grants_breaks_both_chains(self):
        first, second = writer.manifests()[0], writer.manifests()[1]
        swapped_first = dict(first, delegation_id=second["delegation_id"])
        swapped_second = dict(second, delegation_id=first["delegation_id"])
        self.assertFalse(reader.verify_manifest(swapped_first).joined)
        self.assertFalse(reader.verify_manifest(swapped_second).joined)


class WhatThisDoesNotEstablish(unittest.TestCase):
    def test_one_joined_chain_is_not_every_execution(self):
        from tools import p12_provenance_verification as prov
        summary = prov.summary()
        self.assertEqual(summary["assembly"], prov.NOT_ASSEMBLABLE,
                         "if every execution now joins, this control should "
                         "be updated to say so rather than deleted")


if __name__ == "__main__":
    unittest.main()
