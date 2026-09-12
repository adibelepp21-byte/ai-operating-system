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
    """Cross-phase verification must be able to say NOT EXERCISED."""
    from tools import p12_cross_phase_verification as cross
    summary = cross.summary()
    if summary["not_exercised"] > 0:
        return True, (f"{summary['not_exercised']} of {summary['phases']} "
                      "canonical phases report NOT EXERCISED on the live corpus")
    return False, ("every phase reports EXERCISED; the negative is not "
                   "demonstrated by this run")


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


def _state_chain() -> Tuple[bool, str]:
    """`§17` state verification must report SATISFIED when a consumer appears."""
    from unittest import mock
    from tools import p12_state_verification as sv

    live = {r.link: r.status for r in sv.verify()}
    if live.get("CONSUMER") != sv.UNSATISFIED:
        return False, f"CONSUMER is {live.get('CONSUMER')}; probe assumes it is not"
    with mock.patch.object(sv, "consumers_of",
                           return_value=("tools/somewhere.py",)):
        promoted = sv._link_consumer().status
    if promoted != sv.SATISFIED:
        return False, f"a real consumer still reported {promoted}"
    return True, ("moves both ways: CONSUMER UNSATISFIED with nothing reading "
                  "the projection, SATISFIED when something does")


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
    ("p12_operational_state_verifier", "a state property can fail",
     _operational_state),
    ("p12_state_verification", "a consumer is recognised", _state_chain),
    ("p12_operational_state", "an unreadable source yields UNKNOWN",
     _operational_state_projection),
    ("p12_self_model_contract", "a wrong binding is refused",
     _self_model_contract),
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
