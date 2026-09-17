"""P12-W6 — negative controls (`§19` scope: `NEGATIVE CONTROLS`).

`§19` lists `NEGATIVE CONTROLS` as a verification scope of its own, beside
`MUTATION` and `REGRESSION`. It is not the same question as either.

The question is about the **verifiers**, not the system: *can each P12
verification instrument report a negative result at all?* An instrument that
structurally cannot fail is not a verifier — it is a formatted assertion, and
its green output carries no information. `§19` closes with the sentence that
makes this scope necessary: *"P12-W6 tidak boleh dianggap selesai hanya karena
unit tests individual hijau."*

**Every negative here is driven at runtime, in this process.** Citing an
instrument's own conformance suite would establish only that two surfaces exist
— Blueprint `§48` — and would let a verifier that has since stopped being able
to fail keep its demonstration. So each control constructs the condition, calls
the instrument, and checks the value that comes back.

**Nothing resident is altered.** Where a negative needs a different world, the
instrument is pointed at a temporary one.

A `NOT DEMONSTRATED` result is a finding about that instrument, not a failure of
this module.
"""

from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

DEMONSTRATED = "DEMONSTRATED"
NOT_DEMONSTRATED = "NOT DEMONSTRATED"
UNAVAILABLE = "UNAVAILABLE"


@dataclass(frozen=True)
class ControlResult:
    instrument: str
    status: str
    negative_sought: str
    detail: str


def _runtime_observation() -> Tuple[bool, str]:
    """`what_is_running` must be able to answer that it cannot answer."""
    from tools import p12_runtime_observation as obs
    with tempfile.TemporaryDirectory() as tmp:
        answer = obs.what_is_running(Path(tmp))
    if not answer["answerable"]:
        return True, "an empty observation root yields answerable=False"
    return False, ("an empty observation root still reported an answer: "
                   f"{answer!r}")


def _trace_registry() -> Tuple[bool, str]:
    """`what_has_run` must report nothing when nothing has run."""
    from tools import p12_trace_registry as reg
    with tempfile.TemporaryDirectory() as tmp:
        answer = reg.what_has_run(Path(tmp))
        failures = reg.what_has_failed(Path(tmp))
    if answer["records"] == 0 and not failures:
        return True, "an empty store root yields 0 records and 0 failures"
    return False, f"an empty store root reported {answer['records']} records"


def _certified_evidence_guard() -> Tuple[bool, str]:
    """The guard must refuse to guess when certification is undeterminable."""
    from tools import p12_certified_evidence_guard as guard
    original = guard.PHASE_EVIDENCE_ROOTS
    try:
        guard.PHASE_EVIDENCE_ROOTS = {}
        try:
            guard.protected_roots()
        except guard.CertificationUndeterminable as exc:
            return True, f"raised rather than returning an empty set: {str(exc)[:50]}"
        return False, ("with no declared evidence root the guard returned a "
                       "protected set instead of refusing")
    finally:
        guard.PHASE_EVIDENCE_ROOTS = original


def _cross_phase() -> Tuple[bool, str]:
    """Cross-phase verification must be able to say NOT EXERCISED.

    **This control used to read the live corpus and pass because a phase
    happened to be un-crossed.** That worked only while the system was
    incomplete: `ACT-CC-P12-015` crossed the last phase, the live count of
    NOT EXERCISED went to zero, and the control reported the verifier
    undemonstrated — when nothing about the verifier had changed. A control
    whose negative depends on the system still having a hole is not a control.

    Re-grounded structurally: the predicates are pointed at an empty evidence
    world, where nothing has ever run, and every phase must come back NOT
    EXERCISED. That negative stays reachable however complete the system gets.
    """
    from unittest import mock

    from tools import p12_cross_phase_verification as cross
    from tools import p12_runtime_observation as observation
    from tools import p12_trace_registry as traces

    live = cross.summary()
    if live["exercised"] != live["phases"]:
        return False, (f"{live['not_exercised']} of {live['phases']} phases are "
                       "un-crossed on the live corpus; this control assumes "
                       "they are all crossed and must be re-grounded")
    with tempfile.TemporaryDirectory() as tmp:
        with mock.patch.object(traces, "STORE_ROOT", Path(tmp) / "traces"), \
                mock.patch.object(observation, "OBSERVATION_ROOT",
                                  Path(tmp) / "observations"):
            empty = cross.summary()
    if empty["not_exercised"] != empty["phases"]:
        return False, (f"an empty evidence world still reported "
                       f"{empty['exercised']} phase(s) exercised")
    return True, (f"moves both ways: {live['exercised']} of {live['phases']} "
                  "exercised on the live corpus, and all "
                  f"{empty['phases']} NOT EXERCISED against an empty "
                  "evidence world")


def _cross_pd() -> Tuple[bool, str]:
    """Currency checking must drift when the registry does."""
    from tools import p12_cross_pd_verification as xpd
    original = xpd.REGISTRY
    try:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "absent-registry.md"
            xpd.REGISTRY = missing
            summary = xpd.summary()
        if summary["current"] == 0 and summary["unavailable"] > 0:
            return True, ("a missing registry yields "
                          f"{summary['unavailable']} UNAVAILABLE, 0 CURRENT")
        return False, (f"a missing registry still reported "
                       f"{summary['current']} checks CURRENT")
    finally:
        xpd.REGISTRY = original


def _fresh_process() -> Tuple[bool, str]:
    """Fresh-process verification must be able to report DIVERGED."""
    from tools import p12_fresh_process_verification as fresh
    original = fresh._there
    try:
        fresh._there = lambda expr: "'a value the parent process never computed'"
        results = fresh.verify()
        diverged = [r for r in results if r.status == fresh.DIVERGED]
        if diverged:
            return True, (f"a subprocess answering differently yields "
                          f"{len(diverged)} DIVERGED of {len(results)}")
        return False, ("a subprocess answering differently was still reported "
                       "as reproduced")
    finally:
        fresh._there = original


def _mutation() -> Tuple[bool, str]:
    """The mutation suite must report MISSED where nothing detects."""
    from tools import p12_mutation_verification as mutation
    summary = mutation.summary()
    if summary["missed"] > 0:
        return True, (f"{summary['missed']} of {summary['mutations']} report "
                      f"MISSED on the live corpus: "
                      f"{', '.join(summary['missed_mutations'])}")
    return False, ("every mutation reports DETECTED; the negative is not "
                   "demonstrated by this run")


def _regression() -> Tuple[bool, str]:
    """Regression verification must reach REGRESSED when a control is lost."""
    from unittest import mock
    from tools import p12_regression_verification as regression
    before = {"a.py::C::test_one": 3, "a.py::C::test_two": 2}
    after = {"a.py::C::test_one": 3}
    with mock.patch.object(regression, "inventory", side_effect=[before, after]):
        result = regression.structural()
    if result["status"] == regression.REGRESSED and result["removed"]:
        return True, ("a removed control drives the structural comparison to "
                      f"REGRESSED: {result['removed'][0]}")
    return False, "a removed control did not drive the comparison to REGRESSED"


def _self_model() -> Tuple[bool, str]:
    """The Self-Model must answer UNKNOWN rather than echo the live corpus.

    Pointed at an empty root, the three questions answered from stores — what
    capabilities exist, what is running, what failed — must report that they
    cannot see anything. Before `§19`'s `NEGATIVE CONTROLS` scope was built they
    returned answers byte-identical to the live ones, because they read the
    other modules' root constants and ignored the parameter.

    The remaining questions are reported, not hidden: several raise against a
    root that is not a git repository, and one is answered from declared
    constants that no corpus can change.
    """
    from tools import p12_self_model as model
    store_backed = (model.capabilities, model.running, model.failed)
    others = (model.identity, model.ownership, model.authority,
              model.authoritative, model.incomplete, model.changed,
              model.stale, model.unknowns, model.decisions)

    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp)
        statuses = [fn(empty).status.upper() for fn in store_backed]
        raised = 0
        for fn in others:
            try:
                fn(empty)
            except Exception:
                raised += 1

    unknown = [s for s in statuses if s == "UNKNOWN"]
    detail = (f"{len(unknown)} of {len(store_backed)} store-backed questions "
              f"answer UNKNOWN against an empty root; {raised} of "
              f"{len(others)} others raise rather than answering")
    if len(unknown) == len(store_backed):
        return True, detail
    return False, ("a store-backed question answered from the live corpus "
                   f"while pointed at an empty root — {detail}")


def _provenance() -> Tuple[bool, str]:
    """Provenance verification must report ASSEMBLABLE when a join exists.

    This instrument's live result is already the non-positive one — `NOT
    ASSEMBLABLE`, because no execution names the delegation that authorized it.
    So the negative that needs demonstrating is the discriminating one: unless
    the checker can reach `ASSEMBLABLE`, its live answer is a constant rather
    than a measurement, and the finding it reports would be indistinguishable
    from a checker that always says no.

    Both directions are driven here on synthetic inputs, and the live corpus is
    not touched.
    """
    from tools import p12_provenance_verification as prov
    delegation = {"delegation_id": "d1", "delegator": "x",
                  "recipient_instance": "i-001", "authority_record": "a.md",
                  "objective": "o", "work_scope": ["w"],
                  "capability_scope": ["c"], "verification_requirement": "v"}
    trace = {"agent_instance": "i-001", "runtime": "r", "outputs": {"k": 1}}

    # Isolated from the live evidence and manifest surfaces: the probe is about
    # whether the checker discriminates, not about what the corpus contains.
    unjoined = prov.assembly(delegations=(delegation,), traces=(trace,),
                             evidence=(), manifests=())
    joined = prov.assembly(delegations=(delegation,),
                           traces=(dict(trace, delegation_id="d1"),),
                           evidence=(), manifests=())
    if unjoined["status"] != prov.NOT_ASSEMBLABLE:
        return False, ("an execution with no delegation reference was not "
                       "reported NOT ASSEMBLABLE")
    if joined["status"] != prov.ASSEMBLABLE:
        return False, ("an execution naming its delegation was still reported "
                       f"{joined['status']}; the live result is a constant")
    return True, ("moves both ways: unreferenced execution NOT ASSEMBLABLE, "
                  "referenced execution ASSEMBLABLE")


def _failure() -> Tuple[bool, str]:
    """Failure verification must promote a state when the system earns it.

    Its live result is already non-positive — four of seven states are not
    distinguished. So the negative that needs demonstrating is that the checker
    is not stuck there: given a Trace vocabulary containing `verified`, or an
    escalation record naming the refusal type, the corresponding state must
    become `DISTINGUISHED`. Otherwise the four findings are a constant.
    """
    from unittest import mock
    from tools import p12_failure_verification as fail

    live = {r.state: r.status for r in fail.verify()}
    if live.get("VERIFIED") != fail.UNREACHABLE:
        return False, f"VERIFIED is {live.get('VERIFIED')}; probe assumes the live state"
    with mock.patch.object(fail, "_trace_statuses",
                           return_value=frozenset({"success", "verified"})):
        promoted = fail._verified().status
    if promoted != fail.DISTINGUISHED:
        return False, ("a vocabulary containing 'verified' still reported "
                       f"{promoted}; the finding is a constant")
    return True, ("moves both ways: VERIFIED UNREACHABLE on the ratified "
                  "vocabulary, DISTINGUISHED on one that holds it")


def _governance_evidence() -> Tuple[bool, str]:
    """Governance-evidence coverage must move when the corpus does.

    Its live result is already non-positive — one of nine elements established.
    The negative that needs demonstrating is that it is not pinned there: a
    synthetic corpus in which every instrument carries a label must report that
    element `ESTABLISHED`, and one in which none does must report `ABSENT`.
    """
    from pathlib import Path as _Path
    from tools import p12_governance_evidence_verification as gov

    every = [(_Path("a.md"), "Status: ACTIVE\n") for _ in range(4)]
    none = [(_Path("a.md"), "nothing here\n")]
    high = {r.element: r.status for r in gov.coverage(population=every)}
    low = {r.element: r.status for r in gov.coverage(population=none)}
    if high.get("status") != gov.ESTABLISHED:
        return False, ("a corpus labelling every instrument still reported "
                       f"{high.get('status')}")
    if low.get("status") != gov.ABSENT:
        return False, f"a corpus labelling none still reported {low.get('status')}"
    return True, ("moves both ways: ESTABLISHED when every instrument carries "
                  "the label, ABSENT when none does")


def _runtime_integration() -> Tuple[bool, str]:
    """Runtime reachability must report REACHED when a package reaches an entry.

    The live answer is `HAND-INVOKED ONLY`. Unless the checker can reach
    `REACHED`, that answer is a shape rather than a measurement.
    """
    from unittest import mock
    from tools import p12_runtime_verification as rt

    if rt.reachability()["status"] != rt.HAND_INVOKED:
        return False, "the live system is no longer hand-invoked only"
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "entry.py").write_text("x = 1\n", encoding="utf-8")
        (root / "pkg").mkdir()
        (root / "pkg" / "c.py").write_text("import entry\n", encoding="utf-8")
        with mock.patch.object(rt, "REPO_ROOT", root):
            points = {p.module: p for p in rt.entry_points()}
    if points["entry.py"].status != rt.REACHED:
        return False, ("an entry point imported from a package was still "
                       f"{points['entry.py'].status}")
    return True, ("moves both ways: HAND-INVOKED ONLY live, REACHED when a "
                  "non-root surface imports the entry point")


def _workflow_chain() -> Tuple[bool, str]:
    """The workflow chain must connect when every join carries a reference."""
    from unittest import mock
    from tools import p12_workflow_verification as wf

    if wf.chain_is_connected():
        return False, "the live chain is already connected; probe assumes it is not"
    joined = tuple(wf.JoinResult(a, b, wf.EVIDENCED, "ref", "")
                   for a, b in wf.WORKFLOW_JOINS)
    with mock.patch.object(wf, "verify", return_value=joined):
        connected = wf.chain_is_connected()
    by_convention = (wf.JoinResult("A", "B", wf.BY_CONVENTION, "name", ""),)
    with mock.patch.object(wf, "verify", return_value=by_convention):
        convention_connects = wf.chain_is_connected()
    if not connected:
        return False, "a fully evidenced chain still reported disconnected"
    if convention_connects:
        return False, "a BY CONVENTION join was counted as connected"
    return True, ("moves both ways, and a shared name never counts as a "
                  "connection")


def _system_negative_controls() -> Tuple[bool, str]:
    """`§49`'s controls must be able to report ACCEPTED.

    Eleven refusals is what a module returning a constant would print, and two
    of the thirteen already report `ACCEPTED` on the live corpus — but a live
    `ACCEPTED` could equally be a probe that never refuses anything. Both
    directions are driven on synthetic attempts.
    """
    from unittest import mock
    from tools import p12_system_negative_controls as sysneg

    with mock.patch.object(sysneg, "CONTROLS",
                           (("probe", lambda: (True, False, "nothing objected")),)):
        accepted = sysneg.verify()[0].status
    with mock.patch.object(sysneg, "CONTROLS",
                           (("probe", lambda: (True, True, "refused")),)):
        refused = sysneg.verify()[0].status
    if accepted != sysneg.ACCEPTED or refused != sysneg.REFUSED:
        return False, f"statuses do not move: {accepted!r}, {refused!r}"
    live = sysneg.summary()
    if live["uncontrolled"]:
        return False, (f"{live['uncontrolled']} control(s) were never "
                       "attempted; a refusal count over them means nothing")
    return True, (f"moves both ways; live run attempts all {live['controls']} "
                  f"with {live['accepted']} ACCEPTED")


def _execution_chain() -> Tuple[bool, str]:
    """The chain reader must report DANGLING for a reference that does not resolve.

    Its live answer is `JOINED`, which is the positive. Unless it can be driven
    to `DANGLING`, a joined verdict says nothing — so a manifest is mutated in
    memory to name a delegation nobody issued, and the reader must refuse it.
    Nothing persisted is touched.
    """
    from tools import p12_execution_chain_reader as chain
    from tools import p12_execution_provenance as prov

    persisted = prov.manifests()
    if not persisted:
        return False, "no manifest is persisted; nothing to falsify"
    live = chain.verify_manifest(dict(persisted[0]))
    if not live.joined:
        return False, f"the live chain is already {live.status}"
    broken = chain.verify_manifest(dict(persisted[0], delegation_id="0" * 16))
    if broken.joined:
        return False, "a manifest naming a delegation nobody issued still joined"
    return True, ("moves both ways: JOINED on the persisted manifest, DANGLING "
                  "when its delegation reference is replaced")


def _execution_provenance_writer() -> Tuple[bool, str]:
    """The manifest writer must refuse an incomplete manifest and an overwrite.

    Its positive is writing a manifest. The negatives are the two refusals that
    make a written manifest mean something: a manifest missing a `§29` element
    would claim a contract the execution did not keep, and an overwrite would
    make a second execution look like the only one.
    """
    from tools import p12_execution_provenance as prov

    persisted = prov.manifests()
    if not persisted:
        return False, "no manifest is persisted; nothing to falsify"
    fields = {k: v for k, v in persisted[0].items()
              if k not in ("contract_elements", "recorded_at")}
    for key in ("work_scope", "capability_scope", "authority_chain"):
        fields[key] = tuple(fields[key])

    incomplete = prov.ExecutionManifest(**dict(fields, goal=""))
    if "intent" not in incomplete.missing_elements():
        return False, "a manifest with no intent did not report it missing"
    with tempfile.TemporaryDirectory() as tmp:
        try:
            prov.record(incomplete, root=Path(tmp))
            return False, "an incomplete manifest was written"
        except prov.ProvenanceIncomplete:
            pass
        complete = prov.ExecutionManifest(**fields)
        prov.record(complete, root=Path(tmp))
        try:
            prov.record(complete, root=Path(tmp))
            return False, "a manifest overwrote an existing one"
        except prov.ProvenanceIncomplete:
            pass
    return True, ("refuses an incomplete manifest and refuses to overwrite an "
                  "existing one")


def _governance_join_writer() -> Tuple[bool, str]:
    """The `P12-W3` join writer must refuse an unsanctioned refusal type and
    refuse to overwrite an existing join.

    Its positive is the real join `p12_w3_governance_escalation.py` left
    resident. The negatives are the two refusals that keep a written join
    meaning something: a join claiming a refusal type the register would
    never have accepted, and a second join overwriting the first.
    """
    from tools import p12_governance_escalation_join as join
    from tools.escalation_register import EscalationRegister

    root = REPO_ROOT / "docs/architecture/p12/w3-operations"
    escalations = sorted(root.glob("*.escalation.json"))
    if not escalations:
        return False, "no P12-W3 escalation is persisted; nothing to falsify"
    escalation_id = escalations[0].name.split(".")[0]
    register = EscalationRegister(root)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        (tmp_root / escalations[0].name).write_text(
            escalations[0].read_text(encoding="utf-8"), encoding="utf-8")
        tmp_register = EscalationRegister(tmp_root)
        try:
            join.join_escalation_to_grant(
                tmp_root, tmp_register, escalation_id,
                delegation_id="a" * 16, refusal_type="NotASanctionedRefusal")
            return False, "an unsanctioned refusal type was joined"
        except join.GovernanceJoinError:
            pass
        join.join_escalation_to_grant(
            tmp_root, tmp_register, escalation_id,
            delegation_id="a" * 16, refusal_type="ExecutionRefused")
        try:
            join.join_escalation_to_grant(
                tmp_root, tmp_register, escalation_id,
                delegation_id="b" * 16, refusal_type="ExecutionRefused")
            return False, "a second join overwrote the first"
        except join.GovernanceJoinError:
            pass
    return True, ("refuses an unsanctioned refusal type and refuses to "
                  "overwrite an existing join")


def _governance_join_reader() -> Tuple[bool, str]:
    """The `P12-W3` join reader must report `DANGLING` for a reference that
    does not resolve.

    Its live answer, over the resident population, is `JOINED`. Unless it can
    be driven to `DANGLING`, that verdict says nothing — so a copy of the real
    join is written naming a delegation nobody issued, in a temporary
    directory, and the reader must refuse it. Nothing persisted is touched.
    """
    from tools import p12_governance_join_reader as reader

    root = REPO_ROOT / "docs/architecture/p12/w3-operations"
    joins = sorted(root.glob("*.governance-join.json"))
    if not joins:
        return False, "no P12-W3 join is persisted; nothing to falsify"
    escalation_id = joins[0].name.split(".")[0]

    live = reader.resolve(root, root, escalation_id)
    if live["status"] != reader.JOINED:
        return False, f"the live join is already {live['status']}"

    import json
    with tempfile.TemporaryDirectory() as tmp:
        tmp_root = Path(tmp)
        (tmp_root / f"{escalation_id}.escalation.json").write_text(
            (root / f"{escalation_id}.escalation.json").read_text(
                encoding="utf-8"), encoding="utf-8")
        payload = json.loads(joins[0].read_text(encoding="utf-8"))
        payload["delegation_id"] = "0" * 16
        (tmp_root / f"{escalation_id}.governance-join.json").write_text(
            json.dumps(payload), encoding="utf-8")
        broken = reader.resolve(tmp_root, tmp_root, escalation_id)
        if broken["status"] == reader.JOINED:
            return False, "a join naming a delegation nobody issued still joined"
    return True, ("moves both ways: JOINED on the persisted join, DANGLING on "
                  "one naming a delegation nobody issued")


def _phase_authorization_reader() -> Tuple[bool, str]:
    """The phase-authorization reader must refuse an undeterminable corpus.

    `ACT-CC-P12-007 §9` turns on the difference between *"the Founder did not
    authorize it"* and *"no Founder instrument could be found"*. A reader that
    returned an empty result for the second would let a caller read it as the
    first, which is how a phase comes to look unauthorized because a directory
    was missing. It must raise, and it must still read the real corpus
    correctly — so both directions are driven here.
    """
    import tempfile
    from pathlib import Path
    from tools import p12_phase_authorization as phases

    live = phases.state_of("P13")
    if live is None or live.authorized is not False:
        return False, ("the live corpus no longer states P13 AUTHORIZED=FALSE; "
                       "this control cannot be trusted until that is explained")
    with tempfile.TemporaryDirectory() as tmp:
        empty = Path(tmp)
        (empty / "docs" / "governance" / "acts").mkdir(parents=True)
        try:
            phases.phase_states(empty)
        except phases.PhaseAuthorizationUnresolved:
            pass
        else:
            return False, ("an empty governance root produced a phase state "
                           "rather than reporting the corpus undeterminable")
        # A body that names the phase everywhere but carries no structured
        # state block must not yield a state — `§10`'s false-positive case.
        (empty / "docs" / "governance" / "acts" / "roadmap.md").write_text(
            "1. FUTURE WORK\n\nP13 is discussed here. P13 authorization is "
            "described as future work for P13.\n", encoding="utf-8")
        try:
            phases.phase_states(empty)
        except phases.PhaseAuthorizationUnresolved:
            pass
        else:
            return False, "prose naming the phase was accepted as a state source"
    return True, ("moves both ways: P13 AUTHORIZED=FALSE on the real "
                  "instrument, undeterminable on an empty root and on prose "
                  "that only names the phase")


def _phase_authorization_verifier() -> Tuple[bool, str]:
    """The independent verifier must report UNSATISFIED on a wrong report.

    Its live answer is six of six satisfied, which is also what a verifier
    checking nothing prints. The self-model's reported value is replaced with a
    forged one — right shape, wrong state, provenance pointing at a file that
    exists but does not state it — and the verifier must fail on it.
    """
    from unittest import mock
    from tools import p12_phase_authorization_verifier as verifier
    from tools import p12_self_model as model

    live = verifier.summary()
    if live["unsatisfied"] or live["unresolved"]:
        return False, f"the live representation already fails {live['not_satisfied']}"

    forged = {
        "resolved": True,
        "states": {"P13": {
            "entity": "P13", "authorized": True,
            "dimensions": {"AUTHORIZED": True},
            "unstated_dimensions": (), "stated_in": "§37 FINAL STATE TRANSITION",
            "corroborated_by": (),
            "authority": "a citation that resolves",
            "authority_record": "README.md"}},
        "issuance_contradiction": None,
    }
    answer = model.Answer("What authority do I have?",
                          {"phase_authorization": forged}, "VERIFIED", "forged")
    with mock.patch.object(model, "authority", return_value=answer):
        checks = verifier.verify("P13")
    failed = {c.name for c in checks if c.status != verifier.SATISFIED}
    expected = {"authoritative source", "authorization state",
                "provenance supports the claim"}
    if not expected <= failed:
        return False, (f"a forged authorization claim was not refused: only "
                       f"{sorted(failed)} failed")
    return True, ("moves both ways: six of six satisfied on the real "
                  "representation; a forged P13 AUTHORIZED=True citing a "
                  f"resolving but unsupporting record fails {sorted(failed)}")


def _operational_state() -> Tuple[bool, str]:
    """The W2 verifier must report VIOLATED when a property fails.

    Its live answer is nine of nine verified, which is what a verifier checking
    nothing prints. Two properties are driven to failure on synthetic input: an
    assigned `F-17` provider, and a projected value that reads as a permission.
    """
    from unittest import mock
    from tools import p12_operational_state as state
    from tools import p12_operational_state_verifier as verifier

    live = verifier.summary()
    if live["violated"]:
        return False, f"the live surface already violates {live['not_verified']}"

    probe = state.StateSource(
        state_id="probe", state_class="RUNTIME",
        semantics=state.SOURCE_OF_TRUTH, owner="probe",
        canonical_source="probe", read_path="tools", authority="none",
        freshness_model="none", owns_within_class="a probe portion",
        provider="some-department")
    with mock.patch.object(state, "SOURCES", (probe,)):
        assigned = verifier._check_providers_unresolved().status
    entry = state.StateEntry(
        state_id="probe", state_class="RUNTIME", status=state.CURRENT,
        value={"certified": True}, source="probe", observed_at="now",
        transformation="probe", authority="none",
        provider=state.UNRESOLVED_PROVIDER, semantics=state.SOURCE_OF_TRUTH)
    with mock.patch.object(state, "project", return_value=(entry,)):
        impersonation = verifier._check_no_entry_reads_as_authority().status
    if assigned != verifier.VIOLATED:
        return False, f"an assigned F-17 provider reported {assigned}"
    if impersonation != verifier.VIOLATED:
        return False, f"a projected certification flag reported {impersonation}"
    return True, ("moves both ways: an assigned provider and a projected "
                  "permission both report VIOLATED")


def _consumer_evidence_verifier() -> Tuple[bool, str]:
    """The independent consumer verifier must be able to report DISAGREES.

    Its live answer is four of four agreeing, which is also what a verifier
    that compares nothing prints. Two wrong claims are fed to it — one that
    omits a real consumer, one that invents a consumer out of the module
    observed reading only its own fixture — and it must reject both.
    """
    from tools import p12_consumer_evidence_verifier as cev
    from tools import p12_state_verification as sv

    claimed = sv.consumers_of(sv.SURFACE)
    importers = sv.importers_of(sv.SURFACE)
    live = cev.summary(claimed, importers)
    if live["disagrees"] or live["unobservable"]:
        return False, f"the live claim already fails {live['not_agreeing']}"

    omitted = cev.verify(claimed[:1], importers)
    if not [c for c in omitted if c.status == cev.DISAGREES]:
        return False, "a claim omitting a real consumer was not rejected"

    invented = cev.verify(
        claimed + ("tools/p12_mutation_verification.py",), importers)
    names = {c.name for c in invented if c.status == cev.DISAGREES}
    if "a substituted read is not counted" not in names:
        return False, ("a claim counting the fixture-only reader as a consumer "
                       f"was not rejected; only {sorted(names)} disagreed")
    return True, ("moves both ways: 4 of 4 agree on the measured claim; a "
                  "claim omitting a real consumer and a claim counting the "
                  "fixture-only reader are both rejected")


def _e12_acceptance() -> Tuple[bool, str]:
    """The ratified `E12-06` measurement must be able to report SATISFIED.

    Its live answer is `NOT SATISFIED`, and a verifier that can only report one
    verdict measures nothing. The risk here runs opposite to the usual one: the
    control drives it **up**, on synthetic evidence in which every phase is
    crossed by real work, and also confirms it refuses a reading it does not
    implement rather than defaulting to one.
    """
    from unittest import mock
    from tools import p12_e12_acceptance as acc
    from tools import p12_cross_phase_verification as cross

    live = acc.determination()
    if live["verdict"] != acc.SATISFIED:
        return False, (f"the live corpus now reports {live['verdict']}; this "
                       "control assumes it does not, and must be re-grounded")

    # The live answer moved to SATISFIED under `ACT-CC-P12-015`, so the risk
    # inverted with it: a measurement that can only print the verdict the
    # corpus currently earns is still measuring nothing. The control now
    # drives it **down** — synthetic evidence in which a phase was crossed
    # only by a demonstrator, and synthetic evidence in which one was never
    # crossed at all — and both must fall back to NOT SATISFIED.
    demonstrator_only = tuple(
        cross.PhaseResult(phase=p, name=p, status=cross.EXERCISED,
                          evidence="runtime 'p12-f11-workflow-observation'",
                          locator="probe")
        for p in ("P4", "P5"))
    with mock.patch.object(cross, "verify", return_value=demonstrator_only), \
            mock.patch.object(cross, "summary",
                              return_value={"exercised_only_by_a_demonstrator": ("P4", "P5")}):
        demoted = acc.determination()["verdict"]
    if demoted != acc.NOT_SATISFIED:
        return False, f"demonstrator-only evidence still reported {demoted}"

    never_crossed = tuple(
        cross.PhaseResult(phase=p, name=p, status=cross.NOT_EXERCISED,
                          evidence="nothing crossed it", locator="probe")
        for p in ("P4", "P5"))
    with mock.patch.object(cross, "verify", return_value=never_crossed), \
            mock.patch.object(cross, "summary",
                              return_value={"exercised_only_by_a_demonstrator": ()}):
        absent = acc.determination()["verdict"]
    if absent != acc.NOT_SATISFIED:
        return False, f"evidence of no consumption still reported {absent}"

    all_real = tuple(
        cross.PhaseResult(phase=p, name=p, status=cross.EXERCISED,
                          evidence="authored by engineering-intelligence-instance-001",
                          locator="probe")
        for p in ("P4", "P5"))
    with mock.patch.object(cross, "verify", return_value=all_real), \
            mock.patch.object(cross, "summary",
                              return_value={"exercised_only_by_a_demonstrator": ()}):
        promoted = acc.determination()["verdict"]
    if promoted != acc.SATISFIED:
        return False, f"evidence of real consumption still reported {promoted}"

    import tempfile
    from pathlib import Path
    with tempfile.TemporaryDirectory() as tmp:
        (Path(tmp) / "docs" / "governance" / "acts").mkdir(parents=True)
        try:
            acc.determination(Path(tmp))
        except acc.AcceptanceBoundaryUnresolved:
            pass
        else:
            return False, ("a corpus with no ratified instrument produced an "
                           "acceptance verdict rather than refusing")
    return True, ("moves both ways: SATISFIED on the live corpus "
                  f"({len(live['consumed_by_real_work'])} of 8 phases consumed "
                  "by real work), NOT SATISFIED on demonstrator-only evidence "
                  "and on no evidence at all, and refused outright when no "
                  "ratified boundary exists")


def _state_chain() -> Tuple[bool, str]:
    """`§17` state verification must be able to report CONSUMER either way.

    **Inverted by `ACT-CC-P12-008`, not weakened.** This probe used to assume
    the live link was UNSATISFIED and drive it up; the corrected measurement
    made the live link SATISFIED, so it now asserts the live evidence and
    drives it *down*. A probe left pointing at the old live value would have
    reported `not demonstrated` for a control that works — and one edited to
    accept whichever value it finds would demonstrate nothing at all.

    The demotion is driven by removing the *evidence*, not by removing the
    importer: a module that imports the surface without reading it must not
    satisfy `§16`, which is the distinction the corrected link exists to make.
    """
    from unittest import mock
    from tools import p12_state_verification as sv

    live = {r.link: r.status for r in sv.verify()}
    if live.get("CONSUMER") != sv.SATISFIED:
        return False, (f"CONSUMER is {live.get('CONSUMER')}; probe assumes the "
                       "live corpus carries evidenced consumers")
    importer_only = (sv.ConsumerEvidence("tools/imports-but-never-reads.py",
                                         reads=(), fixture_reads=("project",)),)
    with mock.patch.object(sv, "consumption_evidence",
                           return_value=importer_only):
        demoted = sv._link_consumer().status
    if demoted != sv.UNSATISFIED:
        return False, f"an importer that never reads still reported {demoted}"
    with mock.patch.object(sv, "consumption_evidence", return_value=()):
        empty = sv._link_consumer().status
    if empty != sv.UNSATISFIED:
        return False, f"an empty corpus still reported {empty}"
    return True, ("moves both ways: CONSUMER SATISFIED on the live corpus "
                  "(2 evidenced consumers of 3 importers), UNSATISFIED when "
                  "the only importer never reads the projection and when "
                  "nothing imports it at all")


def _operational_state_projection() -> Tuple[bool, str]:
    """The projection must report UNKNOWN, never a value, when a source fails.

    Its live answer is eight sources CURRENT. The negative that matters is the
    one `§14` of the Act names: absence must not become a negative state. A
    projection whose source raises must yield UNKNOWN with no value, not a zero
    that a consumer would read as "nothing is running".
    """
    from unittest import mock
    from tools import p12_operational_state as state

    live = state.summary()
    if live["unknown"]:
        return False, f"the live projection already reports {live['unknown_states']}"

    def explode(_source):
        raise RuntimeError("source unreadable")

    probe = state.StateSource(
        state_id="probe", state_class="RUNTIME",
        semantics=state.SOURCE_OF_TRUTH, owner="probe",
        canonical_source="probe", read_path="tools", authority="none",
        freshness_model="none", owns_within_class="a probe portion")
    with mock.patch.object(state, "SOURCES", (probe,)), \
            mock.patch.object(state, "_PROJECTIONS", {"probe": explode}):
        entries = state.project()
    if entries[0].status != state.UNKNOWN or entries[0].value is not None:
        return False, (f"an unreadable source produced {entries[0].status} "
                       f"with value {entries[0].value!r}")
    return True, ("moves both ways: CURRENT on readable sources, UNKNOWN with "
                  "no value when a source raises")


def _self_model_contract() -> Tuple[bool, str]:
    """The binding checker must be able to report UNBOUND.

    Twelve bound answers is what a checker following every alias would print
    whether or not the binding existed, so a deliberately wrong binding is
    planted and must come back `UNBOUND`.
    """
    from unittest import mock
    from tools import p12_self_model_contract as contract

    live = contract.summary()
    if live["unbound_answers"]:
        return False, f"the live contract already reports {live['unbound_answers']}"
    wrong = contract.QuestionContract(
        "What is running?", "running", "tools.nothing_reads_this",
        contract.AUTHORITATIVE, "none", "none", "a deliberately wrong binding")
    with mock.patch.object(contract, "CONTRACT", (wrong,)):
        bindings = dict(contract.answers_bound_to_their_source())
    if bindings.get("running") != contract.UNBOUND:
        return False, f"a wrong binding still reported {bindings.get('running')}"
    return True, ("moves both ways: all twelve BOUND on the real contract, "
                  "UNBOUND when a binding is wrong")


def _integration_graph() -> Tuple[bool, str]:
    """The W1 graph must move an edge in both directions with its source.

    Seven verified edges of eight is what a graph asserting its own edges would
    print. **This control used to lean on `workflow ↔ runtime` being live-
    `UNVERIFIED`** — it drove that one edge up and passed. `ACT-CC-P12-016`
    recorded the hosting relation the edge had always contracted for and the
    edge became `VERIFIED`, so the control reported the graph undemonstrated
    when nothing about the graph had changed. A control whose negative depends
    on the system still having a hole is not a control.

    Re-grounded on the edge's own inputs, both ways: a workflow that names a
    host an observation covers must verify, and one that names none — the
    `§48` case, two observations that are not a relationship — must not.
    """
    from unittest import mock
    from tools import p12_integration_graph as graph

    live = {e.integration_class: e.classification for e in graph.graph()}
    if live.get("workflow ↔ runtime") != graph.VERIFIED:
        return False, (f"workflow ↔ runtime is "
                       f"{live.get('workflow ↔ runtime')}; probe assumes VERIFIED")

    class _Obs:
        def __init__(self, kind, rid, hosted_by=None):
            self.kind, self.runtime_id = kind, rid
            self.hosted_by = hosted_by

    joined = [_Obs("workflow", "w-1", hosted_by="r-1"), _Obs("runtime", "r-1")]
    with mock.patch("tools.p12_runtime_observation.observations",
                    return_value=joined):
        promoted = graph._workflow_to_runtime().classification
    if promoted != graph.VERIFIED:
        return False, f"a recorded, resolved host still reported {promoted}"

    unhosted = [_Obs("workflow", "w-1"), _Obs("runtime", "r-1")]
    with mock.patch("tools.p12_runtime_observation.observations",
                    return_value=unhosted):
        demoted = graph._workflow_to_runtime().classification
    if demoted != graph.UNVERIFIED:
        return False, f"two observations with no hosting relation reported {demoted}"
    return True, ("moves both ways: VERIFIED when a workflow names a host an "
                  "observation covers, UNVERIFIED when it names none")


def _governance_index() -> Tuple[bool, str]:
    """The index must report a source as stale once it changes underneath."""
    from tools.governance_index import GovernanceIndex, tracked_markdown
    paths = tracked_markdown(REPO_ROOT)[:12]
    index, _ = GovernanceIndex.build(paths, REPO_ROOT)
    if not index.sources:
        return False, "the index recorded no sources; staleness cannot arise"
    with tempfile.TemporaryDirectory() as tmp:
        shadow = Path(tmp)
        for relative in index.sources:
            target = shadow / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("changed underneath\n", encoding="utf-8")
        stale = index.stale_sources(shadow)
    if len(stale) == len(index.sources):
        return True, (f"all {len(stale)} sources report stale once their bytes "
                      "differ from the hash recorded at build")
    return False, (f"only {len(stale)} of {len(index.sources)} sources "
                   "reported stale after every one of them changed")


#: One entry per P12 verification instrument, with the negative each must reach.
def _knowledge_admission_writer() -> Tuple[bool, str]:
    """The admission executor must refuse an admission nobody authorized.

    It succeeded once on the live corpus, which is also what a module that
    admits unconditionally would do. Three authorizations are removed in turn
    — the issued status, the human authority, and the candidate the instrument
    names — and each must stop it before the Governance gate is even reached.
    """
    import shutil
    import tempfile
    from pathlib import Path
    from tools import p12_knowledge_admission as ka

    live = ka.founder_authorization()
    body = (ka.REPO_ROOT / live.instrument).read_text(encoding="utf-8")
    source = ka.REPO_ROOT / ka.CANDIDATE_SOURCE

    def _world(tmp: Path, text: str) -> Path:
        (tmp / ka.DECISION_ROOT).mkdir(parents=True, exist_ok=True)
        (tmp / ka.DECISION_ROOT / "FD.md").write_text(text, encoding="utf-8")
        shutil.copy(source, tmp / ka.CANDIDATE_SOURCE)
        return tmp

    with tempfile.TemporaryDirectory() as tmp:
        root = _world(Path(tmp), body)
        if ka.founder_authorization(root).admission != "AUTHORIZED":
            return False, "the control's own copy of the instrument is not issued"

    for label, mutated in (
        ("an unissued status",
         body.replace("FINAL / ISSUED", "PENDING FOUNDER DECISION")),
        ("no human authority",
         body.replace("HumanAuthority:\nFounder", "HumanAuthority:\n")),
    ):
        with tempfile.TemporaryDirectory() as tmp:
            root = _world(Path(tmp), mutated)
            try:
                ka.founder_authorization(root)
            except ka.AdmissionAuthorityUnresolved:
                continue
            return False, f"{label} was still read as an authorization"

    with tempfile.TemporaryDirectory() as tmp:
        root = _world(Path(tmp), body.replace(
            "Candidate:\nP12 Corpus-Health Assessment Criteria",
            "Candidate:\nP12 Release Notes"))
        try:
            ka.admit(root, store_root=Path(tmp) / "r",
                     decision_root=Path(tmp) / "d",
                     provenance_root=Path(tmp) / "p")
        except ka.AdmissionRefused:
            pass
        else:
            return False, ("an approval naming a different candidate was still "
                           "spent on this one")

    return True, ("moves both ways: the issued instrument authorizes; an "
                  "unissued status, an absent human authority and an approval "
                  "of another candidate are each refused")


def _knowledge_admission_verifier() -> Tuple[bool, str]:
    """The independent admission verifier must be able to report UNSATISFIED.

    Its live answer is ten of ten, which is also what a verifier that checks
    nothing prints. It is pointed at an empty world, where the admission chain
    does not exist, and must fail rather than pass by absence.
    """
    import tempfile
    from pathlib import Path
    from tools import p12_knowledge_admission_verifier as kav

    live = kav.summary()
    if live["failing"]:
        return False, f"the live chain already fails {live['failing']}"

    with tempfile.TemporaryDirectory() as tmp:
        empty = kav.summary(Path(tmp))
    if empty["satisfied"] == len(kav._CHECKS):
        return False, "an empty world still satisfied every check"
    if not empty["failing"]:
        return False, "an empty world reported nothing failing"
    return True, (f"moves both ways: 10 of 10 on the live chain; "
                  f"{len(empty['failing'])} of {len(kav._CHECKS)} fail against "
                  "a world holding no admission")


def _phase_verification_matrix() -> Tuple[bool, str]:
    """The `§46` matrix must be able to lose a cell it currently measures.

    49 of 80 cells are measured on the live corpus, which is also what a module
    printing constants would show. Two removals are applied — the Native Core
    tree it reads boundaries from, and the cross-phase verifier it reads state
    from — and the affected cells must fall to `UNKNOWN` rather than keep their
    values. The `OWNER` column is checked in the other direction: it is
    `UNKNOWN` everywhere and must stay so, because assigning one is `F-17`.
    """
    import tempfile
    from pathlib import Path
    from unittest import mock

    from tools import p12_cross_phase_verification as cross
    from tools import p12_phase_verification_matrix as m

    live = m.summary()
    if live["measured_cells"] == 0:
        return False, "the live matrix measures nothing; nothing can be lost"
    if live["complete"]:
        return False, ("the live matrix reports complete; this control assumes "
                       "it does not and must be re-grounded")

    with tempfile.TemporaryDirectory() as tmp:
        empty = m.summary(Path(tmp))
    if empty["measured_cells"] >= live["measured_cells"]:
        return False, (f"a world with no Native Core still measured "
                       f"{empty['measured_cells']} cells")

    absent = tuple(
        cross.PhaseResult(phase=p, name=n, status=cross.NOT_EXERCISED,
                          evidence="nothing crossed it", locator="")
        for p, n in cross.CANONICAL_PHASES)
    with mock.patch.object(cross, "verify", return_value=absent):
        rows = m.rows()
    # `NOT EXERCISED` contains `EXERCISED`; compare the status, never the
    # substring. The first version of this check did the latter and reported
    # the matrix undemonstrated against evidence it had correctly read.
    if any(not r.state.startswith(cross.NOT_EXERCISED) for r in rows):
        return False, "a phase still reported a crossing with no evidence"

    if any(not r.owner.startswith(m.UNKNOWN) for r in m.rows()):
        return False, "a phase was assigned an owner no resident source gives"

    return True, (f"moves both ways: {live['measured_cells']}/{live['cells']} "
                  f"cells measured live, {empty['measured_cells']} against an "
                  "empty world, every STATE falls to NOT EXERCISED when the "
                  "evidence does, and no OWNER is ever assigned")


def _e12_criteria() -> Tuple[bool, str]:
    """The `E12-01`…`E12-05` reader must be able to resolve, and to reject.

    Its live answer is five `UNRESOLVED`, which is also what a reader that
    parsed nothing would print. A filled instrument must resolve all five and
    yield their boundaries; a selection that is not the canonical package's
    proposed one must be `REJECTED`; and the sole-candidate case — the package
    proposes exactly one interpretation per criterion — must still not be
    adopted from the live instrument.
    """
    import shutil
    import tempfile
    from pathlib import Path
    from tools import p12_e12_criteria as ec

    live = ec.summary()
    if live["resolved"]:
        return False, (f"the live instrument already resolves "
                       f"{live['resolved']} criteria; this control assumes it "
                       "resolves none and must be re-grounded")

    section = ("\n{n}. FOUNDER DECISION — {c}\n\nFounder Selection\n\n"
               "Founder selects:\n\n{c}\n→ {sel}\n\n"
               "Founder Decision: RATIFIED\n\nAcceptance Boundary:\n\n"
               "{bound}\n")

    def _world(tmp: Path, chooser) -> Path:
        (tmp / ec.DECISION_ROOT).mkdir(parents=True, exist_ok=True)
        (tmp / ec.E12_PACKAGE).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ec.REPO_ROOT / ec.E12_PACKAGE, tmp / ec.E12_PACKAGE)
        proposals = ec.proposed_interpretations(ec.REPO_ROOT)
        body = "FD\n\nDecision Domain: E12-01 THROUGH E12-05\n"
        for index, criterion in enumerate(ec.CRITERIA, start=4):
            body += section.format(
                n=index, c=criterion,
                sel=chooser(proposals[criterion]["proposed"]),
                bound="a bounded, measurable statement")
        (tmp / ec.DECISION_ROOT / "FD.md").write_text(body, encoding="utf-8")
        return tmp

    with tempfile.TemporaryDirectory() as tmp:
        filled = ec.summary(_world(Path(tmp), lambda proposed: proposed))
        if filled["resolved"] != len(ec.CRITERIA) or not filled["measurable"]:
            return False, (f"a filled instrument resolved only "
                           f"{filled['resolved']} of {len(ec.CRITERIA)}")

    with tempfile.TemporaryDirectory() as tmp:
        wrong = ec.decisions(_world(
            Path(tmp),
            lambda proposed: "an interpretation nobody ever proposed here"))
        if any(d.status != ec.REJECTED for d in wrong):
            return False, ("a selection that is not the proposed one was not "
                           f"rejected: {[d.status for d in wrong]}")

    try:
        ec.boundaries()
    except ec.AcceptanceBoundaryUnavailable:
        pass
    else:
        return False, "the live unfilled instrument still yielded boundaries"

    return True, (f"moves both ways: 0 of {len(ec.CRITERIA)} resolved on the "
                  "live instrument and boundaries unavailable, all five "
                  "resolved when filled, all five REJECTED when the selection "
                  "is not the canonical proposal")


def _e12_source_discovery() -> Tuple[bool, str]:
    """The E12 source discovery must be able to report a gap and a contradiction.

    Five `RESOLVED` is what a module that checked nothing would print. Three
    removals are applied: the proposal package, a quotation attributed to a
    section that does not contain it, and a cited section replaced by a
    different one. Each must change the status. The `ratified` set is checked
    in the other direction — it is empty and must stay empty however the
    sources move, because a proposal is never a ratification.
    """
    import shutil
    import tempfile
    from pathlib import Path
    from tools import p12_e12_source_discovery as sd

    live = sd.summary()
    if live["resolved"] != 5:
        return False, (f"the live corpus resolves {live['resolved']} of 5; "
                       "this control assumes all five and must be re-grounded")
    if live["ratified"]:
        return False, "a proposal is reported ratified on the live corpus"

    def _world(tmp: Path, *, proposal: bool = True) -> Path:
        for source in (sd.REQUIREMENT_SOURCE, sd.PROPOSAL_SOURCE):
            if source == sd.PROPOSAL_SOURCE and not proposal:
                continue
            target = tmp / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(sd.REPO_ROOT / source, target)
        return tmp

    with tempfile.TemporaryDirectory() as tmp:
        gapped = sd.discover(_world(Path(tmp), proposal=False))
    if any(d.status != sd.SOURCE_GAP for d in gapped):
        return False, ("an absent proposal package did not yield SOURCE-GAP: "
                       f"{[d.status for d in gapped]}")

    with tempfile.TemporaryDirectory() as tmp:
        root = _world(Path(tmp))
        path = root / sd.PROPOSAL_SOURCE
        path.write_text(path.read_text(encoding="utf-8").replace(
            '*"Phase dan Platform Organization harus tetap dibedakan"*',
            '*"a sentence the cited section does not contain at all"*'),
            encoding="utf-8")
        forged = {d.criterion: d.status for d in sd.discover(root)}
    if forged.get("E12-01") != sd.CONTRADICTION:
        return False, (f"a quotation absent from its cited section reported "
                       f"{forged.get('E12-01')}")
    if any(v != sd.RESOLVED for k, v in forged.items() if k != "E12-01"):
        return False, "the provenance check is not per-criterion"

    with tempfile.TemporaryDirectory() as tmp:
        root = _world(Path(tmp))
        path = root / sd.REQUIREMENT_SOURCE
        path.write_text(path.read_text(encoding="utf-8").replace(
            "15. P12-W2 — UNIFIED OPERATIONAL STATE AUTHORITY",
            "15. AN ENTIRELY DIFFERENT SECTION"), encoding="utf-8")
        swapped = {d.criterion: d.status for d in sd.discover(root)}
    if swapped.get("E12-02") != sd.CONTRADICTION:
        return False, (f"a cited section that is a different section reported "
                       f"{swapped.get('E12-02')}")

    return True, ("moves both ways: 5 of 5 RESOLVED live with 0 ratified; "
                  "SOURCE-GAP with no proposal package; CONTRADICTION for a "
                  "quotation absent from its cited body and for a cited "
                  "section that is a different section")


def _e12_measurement() -> Tuple[bool, str]:
    """The `E12-01`…`E12-05` measurement must be able to report NOT SATISFIED.

    Its live answer is five of five `SATISFIED`, which is what a module
    returning constants would print — and it reached that state only after
    three defects in its own first run were corrected, two of which produced a
    **false FAIL**. The control drives it both ways: a clause whose evidence is
    removed must fail, a clause whose evidence source raises must report
    `UNKNOWN` rather than `NOT SATISFIED`, and the decision record must remain
    load-bearing.
    """
    import tempfile
    from pathlib import Path
    from unittest import mock

    from tools import p12_e12_measurement as em

    live = em.determination()
    if live["satisfied"] != len(em.CRITERIA):
        return False, (f"the live corpus satisfies {live['satisfied']} of "
                       f"{len(em.CRITERIA)}; this control assumes all five and "
                       "must be re-grounded")

    # Evidence removed → NOT SATISFIED.
    from tools import p12_execution_provenance as provenance
    with mock.patch.object(provenance, "manifests", return_value=()):
        demoted = {r.criterion: r.verdict for r in em.measure()}
    if demoted.get("E12-04") != em.NOT_SATISFIED:
        return False, (f"an absent execution manifest still reported "
                       f"{demoted.get('E12-04')}")

    # Evidence unreadable → UNKNOWN, never NOT SATISFIED. `UNKNOWN != FALSE`.
    def _raise(root):
        raise RuntimeError("evidence source unavailable")
    with mock.patch.dict(em._CLAUSES, {"E12-01": _raise}):
        unreadable = {r.criterion: r.verdict for r in em.measure()}
    if unreadable.get("E12-01") != em.UNKNOWN:
        return False, (f"an unreadable evidence source reported "
                       f"{unreadable.get('E12-01')} rather than UNKNOWN")

    # The decision record is the only source of a boundary.
    with tempfile.TemporaryDirectory() as tmp:
        try:
            em.measure(Path(tmp))
        except em.AcceptanceBoundaryUnavailable:
            pass
        else:
            return False, "a world with no decision record still measured"

    return True, ("moves both ways: 5 of 5 SATISFIED live; NOT SATISFIED when "
                  "an execution manifest is removed; UNKNOWN (not NOT "
                  "SATISFIED) when an evidence source raises; and no boundary "
                  "at all without the decision record")


CONTROLS: Tuple[Tuple[str, str, Callable], ...] = (
    ("p12_runtime_observation", "cannot answer what is running",
     _runtime_observation),
    ("p12_trace_registry", "nothing has run", _trace_registry),
    ("p12_certified_evidence_guard", "certification undeterminable",
     _certified_evidence_guard),
    ("p12_cross_phase_verification", "a phase is NOT EXERCISED", _cross_phase),
    ("p12_cross_pd_verification", "the registry is UNAVAILABLE", _cross_pd),
    ("p12_fresh_process_verification", "a stage DIVERGED", _fresh_process),
    ("p12_mutation_verification", "a mutation is MISSED", _mutation),
    ("p12_regression_verification", "a class REGRESSED", _regression),
    ("p12_self_model", "a question answers UNKNOWN", _self_model),
    ("p12_provenance_verification", "a join is recognised when present",
     _provenance),
    ("p12_failure_verification", "a state is promoted when earned",
     _failure),
    ("p12_governance_evidence_verification",
     "coverage moves with the corpus", _governance_evidence),
    ("p12_runtime_verification", "reachability is recognised",
     _runtime_integration),
    ("p12_workflow_verification", "a connected chain is recognised",
     _workflow_chain),
    ("p12_system_negative_controls", "ACCEPTED is reachable",
     _system_negative_controls),
    ("p12_execution_chain_reader", "a dangling reference is refused",
     _execution_chain),
    ("p12_execution_provenance", "an incomplete manifest is refused",
     _execution_provenance_writer),
    ("p12_governance_escalation_join", "an unsanctioned refusal type is "
     "refused", _governance_join_writer),
    ("p12_governance_join_reader", "a dangling reference is refused",
     _governance_join_reader),
    ("p12_operational_state_verifier", "a state property can fail",
     _operational_state),
    ("p12_state_verification", "a consumer is recognised", _state_chain),
    ("p12_operational_state", "an unreadable source yields UNKNOWN",
     _operational_state_projection),
    ("p12_self_model_contract", "a wrong binding is refused",
     _self_model_contract),
    ("p12_integration_graph", "an edge is promoted when earned",
     _integration_graph),
    ("p12_phase_authorization", "an undeterminable corpus is refused",
     _phase_authorization_reader),
    ("p12_phase_authorization_verifier", "a forged authorization claim is "
     "refused", _phase_authorization_verifier),
    ("p12_consumer_evidence_verifier", "a wrong consumer claim is rejected",
     _consumer_evidence_verifier),
    ("p12_e12_acceptance", "an unearned SATISFIED is refused", _e12_acceptance),
    ("p12_knowledge_admission", "an unauthorized admission is refused",
     _knowledge_admission_writer),
    ("p12_knowledge_admission_verifier", "an unearned SATISFIED is refused",
     _knowledge_admission_verifier),
    ("p12_phase_verification_matrix", "an unearned measured cell is refused",
     _phase_verification_matrix),
    ("p12_e12_criteria", "an unfilled decision supplies no boundary",
     _e12_criteria),
    ("p12_e12_source_discovery", "an unsupported citation is refused",
     _e12_source_discovery),
    ("p12_e12_measurement", "an unearned SATISFIED is refused",
     _e12_measurement),
    ("governance_index", "a source is stale", _governance_index),
)


def verify() -> Tuple[ControlResult, ...]:
    results = []
    for instrument, sought, control in CONTROLS:
        try:
            demonstrated, detail = control()
        except Exception as exc:  # pragma: no cover - defensive
            results.append(ControlResult(instrument, UNAVAILABLE, sought,
                                         f"control raised: {exc}"))
            continue
        results.append(ControlResult(
            instrument, DEMONSTRATED if demonstrated else NOT_DEMONSTRATED,
            sought, detail))
    return tuple(results)


def summary() -> dict:
    results = verify()
    return {
        "instruments": len(results),
        "demonstrated": sum(1 for r in results if r.status == DEMONSTRATED),
        "not_demonstrated": sum(1 for r in results
                                if r.status == NOT_DEMONSTRATED),
        "unavailable": sum(1 for r in results if r.status == UNAVAILABLE),
        "undemonstrated_instruments": tuple(
            r.instrument for r in results if r.status != DEMONSTRATED),
    }


def main(argv=None) -> int:
    for result in verify():
        print(f"{result.instrument:<32} {result.status:<17} "
              f"{result.negative_sought:<34} {result.detail[:60]}")
    print()
    print("summary:", summary())
    print()
    print("This measures the verifiers, not the system. An instrument that")
    print("cannot report a negative is a formatted assertion, not a check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
