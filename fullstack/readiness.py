"""FS-09 — the Production Readiness Gate, evaluated rather than asserted.

    python -m fullstack.readiness evaluate [--runs N]

Every criterion of Act `§20` (and ACT-003 `§19`) gets one of:

* **PASS**: met, on the evidence named in the criterion;
* **FAIL**: affirmatively tested and found not met, or a check that was
  recorded as not passing (a gap to close). *Not verified is not failed*
  (ACT-007 `§15`): a recording the served code has outgrown is BLOCKED;
* **BLOCKED**: cannot be met until a named decision is taken (an Architect
  package ratified, a Founder decision recorded), or an external dependency
  is supplied;
* **OBSERVED**: measured, with no stated requirement to hold it to.

Each criterion also says **which evidence** it rests on (``evidence_class``):

* ``local-current``: measured now, in-process, on this tree. The functional,
  security and data criteria start the real application in a temporary
  directory and exercise it; nothing is copied from an earlier run.
* ``preview-recorded``: the live Preview checks recorded at FS-08
  (`docs/fullstack/evidence/FS-08-LIVE-PREVIEW-2026-09-27.json`). They are
  **historical**: read from that file, never re-measured here, and never
  relabelled as local. They count only while the code the Preview serves is
  unchanged since the recorded commit; any change there turns the criterion
  to BLOCKED on `LIVE-REVERIFICATION` until the Preview is verified again. It
  never passes on the old recording.
* ``operator-recorded``: taken by the operator on the live store and persisted
  as evidence (the FS-09 logical export and its server-computed digests).
* ``local-recorded``: measured locally once and recorded in a document, not
  re-run by this gate.

A local result never stands in for live evidence: a criterion that needs the
deployment passes only when the recorded Preview checks it names are PASS.

A decision package counts as ratified only when the Decision Register holds an
entry for it with `| **Ratifies** |` and `| **Decided by** |` rows. Preparation
is not ratification (`FD-FS-001` D2-A), so no document in
`docs/fullstack/decision-packages/` can ratify itself.

**PRODUCTION READY** requires every criterion PASS or OBSERVED. Even then,
release waits for a separate Founder decision (`FD-FS-001` D4-A): this gate
never releases.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import re
import statistics
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Dict, List, Optional, Sequence

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER = REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
PACKAGES = {
    "FS-DP-01": "Database implementation",
    "FS-DP-02": "Identity and Authentication",
    "FS-DP-03": "Networking",
    "FS-DP-04": "Deployment",
    "FS-DP-05": "Scaling",
    "FS-DP-06": "Observability implementation",
    "FS-DP-07": "Agent creation (Agent Factory boundary)",
    "FS-09-ENV": "Environment separation",
    "FS-09-RUNTIME": "Python runtime reproducibility",
}
PASS, FAIL, BLOCKED, OBSERVED = "PASS", "FAIL", "BLOCKED", "OBSERVED"
READY, NOT_READY = "PRODUCTION READY", "NOT PRODUCTION READY"

#: What a criterion can wait on besides an FS-DP package: Founder decisions and
#: execution-permission dependencies (ACT-005 `§9`), each recorded in
#: `docs/fullstack/FS-09-DECISION-REGISTER.md` and the ACT-005 execution record.
OTHER_DECISIONS = {
    "ALERTING-SELECTION": "FS-DP-06 alerting (H1, H2 or H3). ACT-004 ratified L1/M1/R2; R2 "
                          "is the readiness signal, so no alerting option is selected by it "
                          "(Register §92, §93). Decided by ACT-007 (Register §98) when an "
                          "entry there carries it",
    "SCENARIO-A-RESIDUAL": "Founder, or delegated under ACT-007 (Register §98): under A1 "
                           "(ratified), whether mandatory Scenario A "
                           "(ACT-001 §18) stands as a classified non-blocking residual",
    "LIVE-REVERIFICATION": "Execution access: the code the Preview serves changed since the "
                           "recorded Preview commit, so the live suites must be run again on "
                           "the new one. That needs Founder-authorized temporary access to "
                           "the Preview. ACT-006/ACT-007 forbid creating a new bypass, and "
                           "this session cannot load the existing one (NC-16)",
    "BYPASS-REVOCATION": "Execution permission: the temporary automation bypass created "
                         "2026-09-30 for the 297e8b8 re-verification (ACT-004 §56) has no "
                         "recorded revocation (ACT-005, ACT-006). The host's revoke call "
                         "takes the secret, and loading it into the session was denied by "
                         "the permission classifier twice; the connector cannot list bypass "
                         "entries, so its absence cannot be observed from a session. The "
                         "Founder/user revokes it in Vercel (Deployment Protection, "
                         "Protection Bypass for Automation) or allows the load (NC-16, "
                         "ACT-005 §9, ACT-006 §4.4)",
}
#: Dependencies that are facts about the world, listed only while a criterion
#: is actually blocked on them.
EXECUTION_DEPENDENCIES = ("LIVE-REVERIFICATION", "BYPASS-REVOCATION")
#: Recorded live evidence the gate reads. It is never written here.
PREVIEW_EVIDENCE = REPO_ROOT / "docs/fullstack/evidence/FS-09-LIVE-PREVIEW-2026-09-30-ACT-008.json"
#: The a4a11cf recording (2026-09-28), kept as history; the citation repair (297e8b8)
#: changed a served docstring, so it no longer covers the tree.
FS09_A4A11CF_EVIDENCE = REPO_ROOT / "docs/fullstack/evidence/FS-09-LIVE-PREVIEW-2026-09-28.json"
#: Where the revocation of the temporary bypass is recorded (ACT-007 `§8`). The
#: Preview recording above keeps `access_revoked: false`: that was true when it
#: was made, and history is not rewritten. The revocation is a later fact.
REVOCATION_EVIDENCE = REPO_ROOT / "docs/fullstack/evidence/FS-09-ACT-008-REVOCATION-2026-09-30.json"
#: The FS-08 recording, kept as history; superseded for this gate by the FS-09 one.
FS08_EVIDENCE = REPO_ROOT / "docs/fullstack/evidence/FS-08-LIVE-PREVIEW-2026-09-27.json"
OWNERSHIP = REPO_ROOT / "docs/fullstack/FS-09-OPERATIONAL-OWNERSHIP.md"
PYTHON_VERSION = REPO_ROOT / ".python-version"
#: FS-09-RUNTIME P2 (ACT-004 DG-05).
PINNED_PYTHON = "3.12"
BACKUP_EXPORT = REPO_ROOT / "docs/fullstack/evidence/FS-09-BACKUP-EXPORT-2026-09-30.jsonl"
BACKUP_MANIFEST = REPO_ROOT / "docs/fullstack/evidence/FS-09-BACKUP-MANIFEST-2026-09-30.json"
RUNBOOK = REPO_ROOT / "docs/fullstack/FS-09-OPERATIONAL-RUNBOOK.md"
MIGRATIONS = REPO_ROOT / "fullstack/deploy/supabase/migrations"
#: Operator inspection of the live store (Supabase `list_migrations`, 2026-09-27,
#: Register `§87` and `§88`): the migrations applied there.
APPLIED_MIGRATIONS = ("20260927062422_aios_records",)
#: The same migration on the Production store (FS-09-ENV E1), applied 2026-09-28
#: with the repository's SQL unchanged; the host stamped its own version.
PRODUCTION_MIGRATIONS = ("20260928051800_aios_records",)
OWNERSHIP_SECTIONS = ("Roles", "Credentials", "Deployment", "Backup and restore",
                      "Rollback", "Monitoring", "Incidents", "Escalation")
#: What the Vercel function serves: its entry point, configuration and the code
#: it imports. A change here since the recorded Preview commit makes the
#: recording stale. Operator tools the function never imports are excluded.
SERVED_PATHS = ("api", "vercel.json", ".python-version", "fullstack/__init__.py", "fullstack/deploy/__init__.py",
                "fullstack/deploy/vercel.py", "fullstack/backend", "fullstack/frontend",
                "native_core", "consumers", "tools/__init__.py",
                "tools/certified_write_barrier.py",
                ":(exclude)fullstack/backend/__main__.py", ":(exclude)**/tests/**")
#: The runbook sections the ACT-003 continuation requires (FS-09 C).
RUNBOOK_SECTIONS = ("Startup and health", "Authentication failure", "Dependency failure",
                    "Persistence failure", "Failed execution", "Trace and audit investigation",
                    "Backup", "Restore", "Rollback", "Rollback compatibility boundaries",
                    "Incident handling", "Monitoring and alerting", "Operator responsibilities",
                    "Escalation boundaries")

#: Supplied by the operator's own inspection; each stays until it is resolved
#: and this list is edited with the evidence of resolution. EXT-01 (Supabase
#: unreachable, 2026-09-26) was resolved on 2026-09-27: the AIOS project is
#: reachable and healthy (docs/fullstack/FS-08-VERCEL-SUPABASE-EXECUTION.md §J).
#: EXT-05 (no server-side key) was resolved at FS-08: the Founder re-entered the
#: key and the Preview wrote to and read from the store (Register `§86`). EXT-06
#: (deployment protection observed disabled, 2026-09-27 19:57Z, Register `§89`)
#: was an accidental Founder configuration change, corrected by the Founder and
#: verified read-only (Register `§90`); protection was on throughout FS-09 live.
EXTERNAL_DEPENDENCIES = (
    {"id": "EXT-02", "what": "S-01 AIOS Transition Manifest not supplied (FD-FS-001 D5-A)",
     "needs": "the Founder to supply the exact document"},
    {"id": "EXT-03", "what": "authenticated live checks need access past Vercel protection: "
     "FS-08 (Register §86) and FS-09 (ACT-004 §56, 2026-09-28) each used a temporary "
     "automation bypass, revoked after the suite (protectionBypass: {}); the one created "
     "2026-09-30 for the 297e8b8 re-verification was revoked under ACT-007 "
     "(docs/fullstack/evidence/FS-09-ACT-008-REVOCATION-2026-09-30.json)",
     "needs": "a Founder-authorized temporary, revocable mechanism for the live "
              "re-verification the changed served code now requires (LIVE-REVERIFICATION); "
              "none is active and ACT-007 forbids creating one"},
    {"id": "EXT-04", "what": "the project-scoped Supabase connector is denied permission and "
     "was bound to a ref not in the account (2026-09-27); the account connector reaches the "
     "AIOS project scfymftfzkpilqbgmfwv, which is healthy",
     "needs": "the project-scoped connector re-bound to scfymftfzkpilqbgmfwv (non-blocking)"},
)


def ratified(register_text: str) -> Dict[str, str]:
    """Package id → the Register entry that ratifies it."""
    found = {}
    # Split at every section heading, so an entry's rows are its own: a `##`
    # section never borrows the `Decided by` row of the `###` entry before it.
    for block in re.split(r"(?m)^(?=#{2,3} )", register_text):
        if not block.startswith("### ") or not re.search(r"(?m)^\| \*\*Decided by\*\* \|", block):
            continue
        row = re.search(r"(?m)^\| \*\*Ratifies\*\* \|([^\n]*)\|\s*$", block)
        if row:
            heading = block.splitlines()[0][4:].strip()
            for package in re.findall(r"FS-DP-0\d|FS-09-(?:ENV|RUNTIME)\b", row.group(1)):
                found[package] = heading
    return found


#: Non-package decisions a Register entry can take (ACT-007 `§5`, `§6`; ACT-008
#: `§7`, `§8`), by their `Ratifies` row. Only an entry whose `Decided by` row
#: names ACT-007 or ACT-008 counts: the delegation is FS-09-only and expires at
#: that Act's terminal state. The latest entry for an id is the decision in force.
DELEGATED_IDS = ("SCENARIO-A-RESIDUAL", "ALERTING-SELECTION")


def delegated(register_text: str) -> Dict[str, dict]:
    """Decision id → {"entry": heading, "option": the option named in its
    `Decision` row}, for the ACT-007 delegated decisions in the Register."""
    found = {}
    for block in re.split(r"(?m)^(?=#{2,3} )", register_text):
        if not block.startswith("### "):
            continue
        by = re.search(r"(?m)^\| \*\*Decided by\*\* \|([^\n]*)\|\s*$", block)
        ratifies = re.search(r"(?m)^\| \*\*Ratifies\*\* \|([^\n]*)\|\s*$", block)
        decision = re.search(r"(?m)^\| \*\*Decision\*\* \|([^\n]*)\|\s*$", block)
        if not (by and ratifies and decision and re.search(r"ACT-00[78]", by.group(1))):
            continue
        for ident in DELEGATED_IDS:
            if re.search(rf"(?<![A-Z-]){ident}(?![A-Z-])", ratifies.group(1)):
                option = re.search(r"\*\*(?:Alerting = )?(H[123]|A[123])\b", decision.group(1))
                found[ident] = {"entry": block.splitlines()[0][4:].strip(),
                                "option": option.group(1) if option else None}
    return found


LOCAL, PREVIEW = "local-current", "preview-recorded"
OPERATOR, LOCAL_RECORDED = "operator-recorded", "local-recorded"


def _criterion(area, name, status, evidence, blocked_by=(), classes=(), residual=None):
    return {"area": area, "criterion": name, "status": status, "evidence": evidence,
            "evidence_class": list(classes), "blocked_by": list(blocked_by),
            "residual": residual}


def _blocked(area, name, decisions, decided, evidence=""):
    """BLOCKED on every listed decision not yet taken, else None."""
    open_ = [d for d in decisions if d not in decided]
    if not open_:
        return None
    return _criterion(area, name, BLOCKED, "awaits " + ", ".join(open_)
                      + (f"; {evidence}" if evidence else ""), open_)


def _blocked_unless(area, name, packages, decided, evidence_if_ratified):
    return (_blocked(area, name, packages, decided)
            or _criterion(area, name, FAIL, evidence_if_ratified))


def preview_record(path: Path = PREVIEW_EVIDENCE) -> dict:
    """The recorded live checks (FS-09, 2026-09-30), and whether they still
    cover this tree. The FS-08 and a4a11cf recordings are history."""
    data = json.loads(path.read_text(encoding="utf-8"))
    passed = {r["check"] for r in data["results"] + data.get("fs09_checks", [])
              if r["result"] == "PASS"}
    if str(data.get("database_after", {}).get("update_attempt", "")).startswith("refused"):
        passed.add("store refuses UPDATE")
    observed = data.get("observability", {})
    if observed.get("function_requests_with_request_id") and (
            observed.get("found_in_host_log") == observed.get("function_requests_with_request_id")):
        passed.add("L1 lines observed in the host log for every request")
    if observed.get("m1_metrics_derived", {}).get("total", {}).get("requests"):
        passed.add("M1 metrics derived from the host log")
    drill = data.get("rollback_drill", {})
    if all(drill.get(p, {}).get("scenario_b", [0])[0] == 201
           and drill.get(p, {}).get("reads_other_version_run", [0, False])[1]
           for p in ("rolled_back", "rolled_forward")) and drill:
        passed.add("rollback drill: back and forward, each reads the other's records")
    if "production_hmljfyqycxcueulhsjae" in data.get("database_after", {}) and \
            data["database_after"]["production_hmljfyqycxcueulhsjae"].get("rows") == 0:
        passed.add("Production store untouched by Preview traffic")
    if "Using Python " + PINNED_PYTHON + " from .python-version" in \
            data.get("build", {}).get("runtime_line", ""):
        passed.add("build ran the pinned runtime")
    diff = subprocess.run(["git", "diff", "--quiet", data["commit"], "--", *SERVED_PATHS],
                          cwd=str(REPO_ROOT), capture_output=True, text=True)
    current = {0: True, 1: False}.get(diff.returncode)   # None: commit not available
    return {"file": path.relative_to(REPO_ROOT).as_posix(), "date": data["date"],
            "commit": data["commit"], "deployment": data["deployment"],
            "access_revoked": data.get("access_revoked") is True,
            "after_revocation": data.get("after_revocation"),
            "passed": passed, "current": current}


def revocation_record(path: Path = REVOCATION_EVIDENCE) -> dict:
    """Whether the temporary bypass is recorded revoked, with first-hand proof:
    the control's own response (`protectionBypass` empty), Deployment Protection
    still enabled, and the revoked secret refused at the edge. A record that
    says less is not a revocation."""
    if not path.is_file():
        return {"revoked": False, "why": "no revocation record"}
    data = json.loads(path.read_text(encoding="utf-8")).get("bypass_revocation") or {}
    statuses = data.get("old_secret_http_status") or {}
    revoked = (data.get("control_response") == {"protectionBypass": {}}
               and data.get("protection_enabled") is True
               and bool(statuses) and all(v == 302 for v in statuses.values()))
    return {"revoked": revoked, "at": data.get("revoked_at"), "note": data.get("note"),
            "why": None if revoked else "the record lacks the control response, protection "
                                        "state or the edge refusal of the revoked secret"}


def _live(area, name, local_ok, local_evidence, checks, preview, residual=None):
    """PASS needs the local measurement now (when there is one) **and** the
    named Preview checks recorded PASS on code the Preview still serves."""
    classes = ([LOCAL] if local_ok is not None else []) + ([PREVIEW] if checks else [])
    where = (f"Preview {preview['deployment']}, commit {preview['commit']}, "
             f"{preview['date']} (recorded, not re-measured)")
    evidence = "; ".join(filter(None, [
        f"local now: {local_evidence}" if local_ok is not None else "",
        f"{where}: " + ", ".join(checks) if checks else ""]))
    missing = [c for c in checks if c not in preview["passed"]]
    blocked_by = ()
    if local_ok is False:
        status = FAIL
    elif missing and preview["current"] is True:
        status, evidence = FAIL, evidence + "; not recorded PASS: " + ", ".join(missing)
    elif missing:
        # A recording the tree has outgrown cannot have recorded a check the
        # tree added since: that is re-verification owed, not a failure.
        status, blocked_by = BLOCKED, ["LIVE-REVERIFICATION"]
        evidence += ("; not in the recording, which no longer covers this tree: "
                     + ", ".join(missing))
    elif checks and preview["current"] is not True:
        status, blocked_by = BLOCKED, ["LIVE-REVERIFICATION"]
        evidence += ("; the served code changed since the recorded commit, so the recording "
                     "no longer covers this tree" if preview["current"] is False else
                     "; the recorded commit is not available to compare with this tree")
    else:
        status = PASS
    return _criterion(area, name, status, evidence, blocked_by, classes=classes,
                      residual=residual)


def _restore_drill() -> dict:
    """Restore the operator's recorded export into a fresh store now, and compare
    it with the export and with the digests the live database computed."""
    from fullstack.backend.aios import AIOSApplication
    from fullstack.deploy import backup
    from native_core.core.infrastructure import LocalAppendOnlyStorage
    entries = backup.read_file(BACKUP_EXPORT)
    manifest = json.loads(BACKUP_MANIFEST.read_text(encoding="utf-8"))
    summary = backup.summary(entries)
    digests = all(summary.get(name, {}).get("sha256_joined") == p["sha256_joined_server"]
                  and summary[name]["records"] == p["records"]
                  for name, p in manifest["partitions"].items())
    with tempfile.TemporaryDirectory() as tmp:
        store = LocalAppendOnlyStorage(Path(tmp) / "storage")
        store.provision()
        backup.restore(entries, store)
        identical = not backup.differences(entries, store)
        aios = AIOSApplication(Path(tmp), REPO_ROOT)
        aios.start()
        runs = aios.runs()
        traced = all(len(aios.run_trace(r["run_id"])) == r["trace"]["count"] for r in runs)
        from fullstack.backend.agents import AgentRegistry, GovernedDefinitions
        agents_read = len(AgentRegistry(aios.storage, GovernedDefinitions(REPO_ROOT)).instances())
        aios.stop()
    return {"records": len(entries), "digests_match_server": digests,
            "restored_identical": identical, "runs_read": len(runs),
            "every_run_trace_resolved": traced, "agent_instances_read": agents_read,
            "ok": digests and identical and traced and len(runs) == manifest[
                "partitions"]["fullstack-runs"]["records"]}


def _sections_missing(path: Path, required) -> List[str]:
    """The required `##` sections a document lacks (numbering ignored)."""
    if not path.is_file():
        return list(required)
    headings = {line.lstrip("#").strip().split(". ", 1)[-1]
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.startswith("## ")}
    return [s for s in required if s not in headings]


#: The two Supabase projects of FS-09-ENV E1, as recorded (Register `§93` DG-04).
PREVIEW_PROJECT = "https://scfymftfzkpilqbgmfwv.supabase.co"
PRODUCTION_PROJECT = "https://hmljfyqycxcueulhsjae.supabase.co"


def _environment_wiring() -> dict:
    """Measured now: what the deployed function selects for each environment.
    It runs the real resolver; it calls no database and reads no key."""
    from fullstack.deploy import vercel
    facts = {}
    for name in ("preview", "production"):
        try:
            store = vercel.storage_from_environment(
                {"VERCEL_ENV": name, "SUPABASE_SECRET_KEY": "gate-probe-not-a-key"})
            facts[name] = repr(store)
        except Exception as error:               # pragma: no cover - reported, not raised
            facts[name] = f"refused: {type(error).__name__}"
    refused = []
    for bad in ({}, {"VERCEL_ENV": "development"}, {"VERCEL_ENV": "Production"},
                {"VERCEL_ENV": ""}, {"VERCEL_ENV": "staging"}):
        try:
            vercel.storage_from_environment({**bad, "SUPABASE_SECRET_KEY": "gate-probe-not-a-key"})
            refused.append(False)
        except vercel.UnknownEnvironment:
            refused.append(True)
    ok = (facts["preview"] == f"SupabaseStorage('{PREVIEW_PROJECT}/rest/v1')"
          and facts["production"] == f"SupabaseStorage('{PRODUCTION_PROJECT}/rest/v1')"
          and PREVIEW_PROJECT != PRODUCTION_PROJECT and all(refused))
    return {"ok": ok, "facts": facts, "unresolved_refused": f"{sum(refused)} of {len(refused)}"}


#: What runbook `§12.1` must hold for the H3 selection to be implemented.
H3_MARKERS = ("### 12.1 Manual monitoring checks (H3)", "readiness (R2)", "error rate (M1)",
              "refusals before the Application", "backup freshness", "temporary access",
              "**When:**", "**Who:**", "Residual: a failure is", "Not an alert")


def _h3_missing() -> List[str]:
    text = RUNBOOK.read_text(encoding="utf-8") if RUNBOOK.is_file() else ""
    return [m for m in H3_MARKERS if m not in text]


SCENARIO_A_LIVE = "Scenario A: agent instance registered and persisted"


def _a2_holds() -> bool:
    """A2 (Register `§101`): the state-changing routes are exactly a run and an
    Agent Instance registration, and no route authors, edits or retires a
    Definition (that is A3, not built)."""
    from fullstack.backend import contract
    writes = [(r.method, r.template) for r in contract.ROUTES if r.method != "GET"]
    return (writes == [("POST", "/api/v1/runs"), ("POST", "/api/v1/agent-instances")]
            and not [r for r in contract.ROUTES
                     if r.method != "GET" and "definition" in r.template.lower()])


def _scenario_a_row(decision: Optional[dict], scenario: dict, a2_holds: bool,
                    preview: dict) -> Optional[dict]:
    """Scenario A is mandatory (ACT-001 `§18`; ACT-008 `§7.2`, `§16`): it passes
    only by being executed, locally now and on the Preview the recording covers.
    A1 cannot execute it, so a decision for A1 fails the row rather than
    classifying it away."""
    area, name = "Functionality", "agent creation (Scenario A)"
    option = decision["option"] if decision else None
    who = decision["entry"].split(" — ")[0] if decision else "-"
    if option == "A2":
        local = (f"registered in-process: {scenario.get('status')} created, persisted and "
                 f"listed ({scenario.get('listed')}), observer refused "
                 f"({scenario.get('observer')}), duplicate refused ({scenario.get('duplicate')}), "
                 f"an unknown Definition refused ({scenario.get('unknown_definition')}); "
                 "only instance registration exists, no Definition authoring")
        return _live(area, name, bool(a2_holds and scenario.get("ok")), local,
                     [SCENARIO_A_LIVE], preview,
                     residual=f"A2 was selected by the delegated decision {who} (Register §101); a "
                              "registration grants no authority (AGENT INSTANCE ≠ AUTHORITY); "
                              "Definitions stay governed documents the application only reads")
    if option in ("A1", "A3"):
        return _criterion(area, name, FAIL,
                          f"{option} is the decision in force ({who}): "
                          + ("the application creates no Agent, so the mandatory Scenario A is not "
                             "executed (ACT-008 §7.2)" if option == "A1" else
                             "the Agent Factory is not built"), classes=[LOCAL])
    return None


def _alerting_row(decision: Optional[dict], h3_missing: List[str]) -> dict:
    """The alerting criterion once an option is selected. Only H3 is
    implementable inside FS-09 (Register `§98` `ACT-007-DG-02`); H1 and H2 need
    a Founder-reserved spending, recipient or external-service decision."""
    option = decision["option"] if decision else None
    residual = ("no automatic alert: failures are found only when a person runs the checks "
                "(FS-DP-06 R2.10); R2 is readiness, not alerting; H1/H2 remain for the "
                "Founder (spending, recipient, external service, an edge path)")
    if option == "H3" and not h3_missing:
        return _criterion("Observability", "alerting", PASS,
                          f"H3 (none; manual checks) selected by {decision['entry'].split(' — ')[0]} "
                          "(ACT-007 §6; Register §98); runbook §12.1 holds the checks",
                          classes=[LOCAL], residual=residual)
    if option == "H3":
        return _criterion("Observability", "alerting", FAIL,
                          "H3 selected; runbook §12.1 lacks: " + ", ".join(h3_missing),
                          classes=[LOCAL], residual=residual)
    return _criterion("Observability", "alerting", FAIL,
                      f"{option or 'an option'} selected; not implemented: it needs a "
                      "Founder-reserved decision (spending, recipient, external service, edge)")


def _runbook_sections() -> List[str]:
    """The required runbook sections that are missing."""
    return _sections_missing(RUNBOOK, RUNBOOK_SECTIONS)


def _dependency_failure() -> Dict[str, int]:
    """The deployed composition with no key, and with an unreachable store."""
    from fullstack.backend.supabase_storage import SupabaseStorage
    from fullstack.deploy.vercel import make_app
    from wsgiref.util import setup_testing_defaults
    from fullstack.backend.security import NoAuthenticator

    def unreachable(*_):
        raise OSError("connection refused")

    def status(factory):
        env = {"REQUEST_METHOD": "GET", "PATH_INFO": "/api/v1/health"}
        setup_testing_defaults(env)
        seen = {}
        with contextlib.redirect_stderr(io.StringIO()):   # the expected refusal's log line
            make_app(factory, NoAuthenticator(), telemetry_sink=None)(
                env, lambda s, h: seen.update(s=int(s.split()[0])))
        return seen["s"]

    return {"no_key": status(lambda: None),
            "unreachable": status(lambda: SupabaseStorage(
                "https://example.invalid", "k", transport=unreachable))}


def _measure(runs: int) -> dict:
    """Exercise the real application in a throwaway directory."""
    from fullstack.backend.api import create_app
    from fullstack.backend.telemetry import Collector
    from fullstack.backend.security import (AGENT_REGISTER, AUDIT, OBSERVE, RUN_WORKFLOW,
                                            Authenticator, Principal)
    from wsgiref.util import setup_testing_defaults

    class _Gate(Authenticator):
        mechanism = "readiness-gate probe"
        principals = {"gate-operator": Principal("gate-operator", {OBSERVE, RUN_WORKFLOW, AUDIT,
                                                                     AGENT_REGISTER}),
                      "gate-observer": Principal("gate-observer", {OBSERVE})}

        def authenticate(self, headers):
            return self.principals.get(headers.get("x-gate-principal", ""))

    made = []

    def call(app, method, path, who=None, body=None):
        made.append(path)
        data = json.dumps(body).encode() if body is not None else b""
        path, _, query = path.partition("?")
        env = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": query,
               "wsgi.input": io.BytesIO(data),
               "CONTENT_LENGTH": str(len(data)), "CONTENT_TYPE": "application/json"}
        if who:
            env["HTTP_X_GATE_PRINCIPAL"] = who
        setup_testing_defaults(env)
        seen = {}
        out = b"".join(app(env, lambda s, h: seen.update(status=int(s.split()[0]),
                                                           headers=dict(h))))
        return seen["status"], seen["headers"], json.loads(out)

    body = lambda doc: {"workflow": "document-conformance-review",  # noqa: E731
                        "inputs": {"document": doc, "criteria": ["INV-4"]}}
    with tempfile.TemporaryDirectory() as tmp:
        log = Collector()
        app, aios = create_app(Path(tmp), REPO_ROOT, _Gate(), telemetry_sink=log)
        latencies, first = [], None
        store = Path(tmp) / "storage"
        for _ in range(runs):
            started = time.perf_counter()
            status, _, ok = call(app, "POST", "/api/v1/runs", "gate-operator",
                                 body("docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md"))
            latencies.append((time.perf_counter() - started) * 1000)
            if first is None:
                first = {p.name: p.read_bytes() for p in store.iterdir()}
        _, _, failed = call(app, "POST", "/api/v1/runs", "gate-operator", body("docs/absent.md"))
        refused = call(app, "POST", "/api/v1/runs", "gate-observer", body("docs/x.md"))[0]
        anonymous = call(app, "GET", "/api/v1/runs")[0]
        _, headers, _ = call(app, "GET", "/api/v1/health")
        traces = call(app, "GET", "/api/v1/traces", "gate-observer")[2]["total"]
        # Scenario A (FS-DP-07 A2): User -> Create Agent -> Backend -> AIOS Agent
        # Capability -> Persist -> Result, then every refusal that matters.
        agent = {"definition": "engineering-intelligence-agent", "instance_key": "gate-probe-01",
                 "capabilities": ["engineering-intelligence"]}
        a_status, _, a_created = call(app, "POST", "/api/v1/agent-instances", "gate-operator", agent)
        a_observer = call(app, "POST", "/api/v1/agent-instances", "gate-observer", agent)[0]
        a_anonymous = call(app, "POST", "/api/v1/agent-instances", None, agent)[0]
        a_duplicate = call(app, "POST", "/api/v1/agent-instances", "gate-operator", agent)[0]
        a_unknown = call(app, "POST", "/api/v1/agent-instances", "gate-operator",
                         dict(agent, definition="no-such-agent", instance_key="gate-probe-02"))[0]
        a_listed = [i["instance_key"] for i in
                    call(app, "GET", "/api/v1/agent-instances", "gate-observer")[2]["instances"]]
        a_traces = call(app, "GET", "/api/v1/traces", "gate-observer")[2]["total"]
        scenario_a = {"status": a_status, "observer": a_observer, "anonymous": a_anonymous,
                      "duplicate": a_duplicate, "unknown_definition": a_unknown,
                      "listed": a_listed,
                      "ok": (a_status == 201 and a_created.get("lifecycle") == "REGISTERED"
                             and a_created.get("grants_authority") is False
                             and (a_observer, a_anonymous, a_duplicate, a_unknown)
                             == (403, 401, 409, 400)
                             and a_listed == ["gate-probe-01"] and a_traces == traces)}
        audit = call(app, "GET", "/api/v1/audit?limit=200", "gate-operator")[2]["entries"]
        aios.stop()
        final = {p.name: p.read_bytes() for p in store.iterdir()}
        appended_only = all(final[name].startswith(data) for name, data in first.items())
        _, restarted = create_app(Path(tmp), REPO_ROOT, _Gate(), telemetry_sink=None)
        survived = len(restarted.runs())
        restarted.stop()
    return {"success": ok.get("state") == "succeeded" and status == 201,
            "failure_state": failed.get("state"), "failure_reason": failed.get("failure_reason"),
            "observer_post": refused, "anonymous_get": anonymous,
            "headers": headers, "traces": traces, "expected_traces": 3 * runs + 2,
            "audit_entries": len(audit), "appended_only": appended_only,
            "runs_after_restart": survived, "runs_made": runs + 1,
            "requests_made": len(made), "log_lines": list(log.lines), "scenario_a": scenario_a,
            "latency_ms": {"runs": runs, "p50": round(statistics.median(latencies), 2),
                           "max": round(max(latencies), 2)}}


def _no_shipped_credential() -> bool:
    """FS-DP-02 B3: both compositions build the authenticator from the
    environment, which holds hashes only. Unconfigured, it accepts nobody, and
    a configuration carrying anything but a hash is refused whole."""
    from fullstack.backend.security import OperatorTokenAuthenticator
    served = (REPO_ROOT / "fullstack/backend/__main__.py").read_text(encoding="utf-8")
    function = (REPO_ROOT / "fullstack/deploy/vercel.py").read_text(encoding="utf-8")
    unconfigured = OperatorTokenAuthenticator.from_environment({})
    plaintext = OperatorTokenAuthenticator.from_configuration(
        '[{"subject": "x", "token": "plaintext"}]')
    return ("OperatorTokenAuthenticator.from_environment(os.environ)" in served
            and "OperatorTokenAuthenticator.from_environment(environment)" in function
            and unconfigured.authenticate({"authorization": "Bearer any"}) is None
            and plaintext.configuration_error is not None)


def evaluate(runs: int = 20, register_text: Optional[str] = None,
             preview: Optional[dict] = None, decisions: Sequence[str] = (),
             revocation: Optional[dict] = None) -> dict:
    """`preview` replaces the recorded Preview checks (tests only); `decisions`
    names non-package decisions to treat as taken (tests only: none is taken)."""
    text = register_text if register_text is not None else REGISTER.read_text(encoding="utf-8")
    delegated_now = delegated(text)
    decided = dict(ratified(text), **{d: v["entry"] for d, v in delegated_now.items()},
                   **{d: "test" for d in decisions})
    preview = preview if preview is not None else preview_record()
    revocation = revocation if revocation is not None else revocation_record()
    m = _measure(runs)
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT),
                          capture_output=True, text=True).stdout.strip()
    security_headers = all(m["headers"].get(h) for h in (
        "X-Content-Type-Options", "Content-Security-Policy", "X-Frame-Options",
        "Referrer-Policy"))
    drill = _restore_drill()
    dependency = _dependency_failure()
    missing_sections = _runbook_sections()
    in_repo = sorted(p.stem for p in MIGRATIONS.glob("*.sql"))
    from fullstack.deploy.request_metrics import derive
    a2_holds = _a2_holds()
    wiring = _environment_wiring()
    h3_missing = _h3_missing()
    joined = "\n".join(m["log_lines"])
    l1_local = (len(m["log_lines"]) == m["requests_made"]
                and "gate-operator" not in joined and "docs/absent.md" not in joined)
    m1 = derive(m["log_lines"])
    m1_local = m1["total"]["requests"] == m["requests_made"]
    pinned = PYTHON_VERSION.read_text(encoding="utf-8").strip() if PYTHON_VERSION.is_file() else None
    missing_ownership = _sections_missing(OWNERSHIP, OWNERSHIP_SECTIONS)
    only_scope = ("refusal for a missing scope (403) is evidenced locally only: the Preview "
                  "holds one principal with every scope")
    c: List[dict] = [
        _live("Functionality", "core functions work (Scenario B)", m["success"],
              f"{runs} runs succeeded", ["authenticated POST creates a run"], preview),
        _live("Functionality", "failure is a meaningful state (Scenario C)",
              m["failure_state"] == "failed",
              f"state {m['failure_state']!r}: {m['failure_reason']}",
              ["failure paths are meaningful states"], preview),
        _blocked("Functionality", "agent creation (Scenario A)",
                 ["FS-DP-07", "SCENARIO-A-RESIDUAL"], decided,
                 "FS-DP-07 is decided but no entry selects A1, A2 or A3 for Scenario A")
        or _scenario_a_row(delegated_now.get("SCENARIO-A-RESIDUAL"), m["scenario_a"],
                           a2_holds, preview)
        or _criterion("Functionality", "agent creation (Scenario A)", FAIL,
                      "the decision names no A1, A2 or A3", classes=[LOCAL]),
        _criterion("Functionality", "A2: instances are registered, Definitions are never authored",
                   PASS if a2_holds else FAIL,
                   "the state-changing routes are POST /api/v1/runs and POST "
                   "/api/v1/agent-instances; no route writes a Definition; runs show the acting "
                   "Agent Instances", classes=[LOCAL]),
        _blocked("Security", "authentication", ["FS-DP-02"], decided) or _live(
            "Security", "authentication", _no_shipped_credential(),
            "B3 is the composition's authenticator; unconfigured it accepts nobody",
            ["missing Authorization rejected", "invalid and malformed Authorization rejected",
             "valid B3 bearer authenticates"], preview),
        _live("Security", "authorization and least privilege",
              (m["observer_post"], m["anonymous_get"]) == (403, 401),
              f"observer POST → {m['observer_post']}; anonymous GET → {m['anonymous_get']}",
              ["missing Authorization rejected", "valid B3 bearer authenticates"], preview,
              residual=only_scope),
        _live("Security", "secrets not exposed", _no_shipped_credential(),
              "the compositions hold token hashes only (AIOS_OPERATOR_TOKENS)",
              ["audit records subjects and decisions, no credential"], preview),
        _criterion("Security", "temporary access revoked", PASS,
                   "the temporary bypass (note "
                   f"{revocation.get('note') or '297e8b8 re-verification'!r}) is revoked: the "
                   "control returned an empty protectionBypass, Deployment Protection is "
                   f"enabled, and the revoked secret is refused at the edge "
                   f"({revocation.get('at')})", classes=[OPERATOR])
        if revocation["revoked"] else
        (_blocked("Security", "temporary access revoked", ["BYPASS-REVOCATION"], decided,
                  f"the bypass used for the {preview['commit']} recording has no recorded "
                  "revocation; it cannot be observed absent from a session (NC-16)")
         or _criterion("Security", "temporary access revoked", FAIL,
                       "the recording says the temporary bypass is still active")),
        _live("Security", "attack-surface controls", security_headers,
              "security headers present; 64 KiB body limit; Tool confined to docs/", [],
              preview),
        _live("Security", "audit", m["audit_entries"] > 0,
              f"{m['audit_entries']} decisions recorded",
              ["audit records subjects and decisions, no credential"], preview),
        _live("Reliability", "failure handling", m["failure_state"] == "failed",
              "a failed Tool drives the Workflow to FAILED; nothing is left RUNNING",
              ["failure paths are meaningful states"], preview),
        _live("Reliability", "dependency failure fails closed",
              dependency == {"no_key": 503, "unreachable": 503},
              f"deployed composition: no key → {dependency['no_key']}, unreachable store → "
              f"{dependency['unreachable']}", [], preview,
              residual="exercised in-process only; not induced on the live store"),
        _live("Reliability", "recovery (state outlives its Runtime)",
              m["runs_after_restart"] == m["runs_made"],
              f"{m['runs_after_restart']} of {m['runs_made']} runs after restart",
              ["persisted in Supabase, read by a later Runtime"], preview),
        _live("Reliability", "concurrent runs keep distinct identities (C1)", None, "",
              ["8 concurrent POSTs", "distinct runtime-derived identities",
               "no duplicate identity in the store"], preview),
        _blocked("Reliability", "rollback of a deployment", ["FS-DP-01", "FS-DP-04"], decided)
        or _live("Reliability", "rollback of a deployment", None, "",
                 ["rollback drill: back and forward, each reads the other's records"], preview,
                 residual="drilled on Preview by alias (same store, same credentials, same "
                          "B3 posture); a rollback below the L1 commit loses request logs. "
                          "Production rollback is Founder-only (FD-FS-001 D4-A). Floors: below "
                          "0706446 (C1) duplicate run ids return; below 215248f (B3) the API "
                          "authenticates nobody; below 8d088fb there is no API. None is "
                          "production-safe because its data reads"),
        _criterion("Performance", "latency of Scenario B (local, in-process)", OBSERVED,
                   f"p50 {m['latency_ms']['p50']} ms, max {m['latency_ms']['max']} ms over "
                   f"{runs} runs. Live (recorded, Preview): see the evidence file's "
                   "observed_latency_ms and M1 figures. No canonical workload or latency "
                   "requirement exists; OBSERVED is not PASS (ACT-004 §39)",
                   classes=[LOCAL, PREVIEW]),
        _live("Observability", "tracing (Trace)", m["traces"] == m["expected_traces"],
              f"{m['traces']} Trace records for {runs} successful and 1 failed run",
              ["Trace associated with the run"], preview),
        _blocked("Observability", "logging (L1)", ["FS-DP-06"], decided) or _live(
            "Observability", "logging (L1)", l1_local,
            f"{len(m['log_lines'])} lines for {m['requests_made']} requests; no credential "
            "or raw path in them", ["L1 lines observed in the host log for every request"],
            preview),
        _blocked("Observability", "metrics (M1)", ["FS-DP-06"], decided) or _live(
            "Observability", "metrics (M1)", m1_local,
            f"derived from the lines: {m1['total']['requests']} requests, status classes "
            f"{m1['total']['status_classes']}", ["M1 metrics derived from the host log"],
            preview),
        _blocked("Observability", "readiness signal (R2)", ["FS-DP-06"], decided) or _live(
            "Observability", "readiness signal (R2)",
            dependency == {"no_key": 503, "unreachable": 503},
            "deployed /health is 200 only after a Runtime started on the store, else 503",
            ["health through the bypass"], preview),
        _blocked("Observability", "alerting", ["ALERTING-SELECTION"], decided,
                 "no H1/H2/H3 option is selected by any canonical source")
        or _alerting_row(delegated_now.get("ALERTING-SELECTION"), h3_missing),
        _live("Data", "integrity (append-only)", m["appended_only"],
              "every partition's earlier bytes are a prefix of its later bytes",
              ["store refuses UPDATE"], preview),
        _blocked("Data", "persistence on the ratified store", ["FS-DP-01"], decided) or _live(
            "Data", "persistence on the ratified store",
            m["runs_after_restart"] == m["runs_made"], "the store outlives the Runtime",
            ["authenticated POST creates a run",
             "persisted in Supabase, read by a later Runtime"], preview),
        _blocked("Data", "backup and restore", ["FS-DP-01"], decided) or _criterion(
            "Data", "backup and restore", PASS if drill["ok"] and drill["agent_instances_read"] > 0 else FAIL,
            f"operator export of the live store ({drill['records']} records, current at "
            f"2026-09-30) matches the database's digests: {drill['digests_match_server']}; "
            f"restored now into a fresh store byte-identical: {drill['restored_identical']}; "
            f"the application reads {drill['runs_read']} runs, resolves every run's Trace: "
            f"{drill['every_run_trace_resolved']}, and reads {drill['agent_instances_read']} "
            "Agent Instance registrations", classes=[OPERATOR, LOCAL],
            residual="backups exist only when the operator runs one (free plan: no "
                     "downloadable backup); cadence and owner are defined in the ownership "
                     "model; each environment is backed up and restored on its own"),
        _criterion("Data", "migration",
                   PASS if in_repo == list(APPLIED_MIGRATIONS)
                   and [m_.split("_", 1)[1] for m_ in PRODUCTION_MIGRATIONS]
                   == [m_.split("_", 1)[1] for m_ in in_repo] else FAIL,
                   f"in the repository: {in_repo}; applied on the Preview store: "
                   f"{list(APPLIED_MIGRATIONS)}; on the Production store: "
                   f"{list(PRODUCTION_MIGRATIONS)} (operator inspection)",
                   classes=[LOCAL, OPERATOR],
                   residual="the Production store's version stamp is the host's own; the SQL "
                            "is the repository's, and the schemas compare equal"),
        _blocked("Data", "environment separation", ["FS-09-ENV"], decided,
                 "E1: Production project hmljfyqycxcueulhsjae created and migrated") or _live(
            "Data", "environment separation", wiring["ok"],
            f"the deployed function selects by VERCEL_ENV: preview → {wiring['facts']['preview']}; "
            f"production → {wiring['facts']['production']}; an unresolved environment is refused "
            f"({wiring['unresolved_refused']}); Production store 0 rows (recorded, operator "
            "inspection)", ["Production store untouched by Preview traffic"], preview,
            residual="no Production key or deployment exists (FS-10); Production wiring is "
                     "verified by the resolver and recording fakes, not live"),
        _criterion("Operations", "runbook", FAIL if missing_sections else PASS,
                   ("missing sections: " + ", ".join(missing_sections)) if missing_sections
                   else f"{RUNBOOK.relative_to(REPO_ROOT).as_posix()} covers every required "
                        "section", classes=[LOCAL],
                   residual="written, not yet exercised in an incident; alerting is H3 "
                            "(none; manual checks, runbook §12.1)"),
        _criterion("Operations", "operational ownership",
                   PASS if not missing_ownership else FAIL,
                   ("missing sections: " + ", ".join(missing_ownership)) if missing_ownership
                   else f"{OWNERSHIP.relative_to(REPO_ROOT).as_posix()}: the model defined "
                        "under ACT-004 §37", classes=[LOCAL]),
        _criterion("Reproducibility", "known artifact", PASS if head else FAIL,
                   f"commit {head}; no build step", classes=[LOCAL]),
        _blocked("Reproducibility", "runtime version pinned", ["FS-09-RUNTIME"], decided)
        or _live("Reproducibility", "runtime version pinned", pinned == PINNED_PYTHON,
                 f".python-version = {pinned!r}", ["build ran the pinned runtime"], preview),
        _blocked("Reproducibility", "reproducible deployment", ["FS-DP-03", "FS-DP-04"],
                 decided) or _live(
            "Reproducibility", "reproducible deployment", pinned == PINNED_PYTHON,
            "the build is the commit, the pinned runtime and vercel.json; no dependency",
            ["build ran the pinned runtime", "HSTS on HTTPS responses",
             "no cross-origin grant on the API", "CORS preflight not honoured"], preview),
    ]
    blocking = [x for x in c if x["status"] in (FAIL, BLOCKED)]
    awaiting = sorted({p for x in c for p in x["blocked_by"]})
    return {
        "gate": "FS-09 Production Readiness",
        "commit": head,
        "result": READY if not blocking else NOT_READY,
        "criteria": c,
        "blocking": [f"{x['area']}: {x['criterion']}" for x in blocking],
        "residuals": [f"{x['area']}: {x['criterion']}: {x['residual']}"
                      for x in c if x["residual"]],
        "preview_evidence": {k: v for k, v in preview.items() if k != "passed"},
        "decision_packages": {p: ("RATIFIED by " + decided[p]) if p in decided
                              else "PROPOSED — NOT RATIFIED" for p in PACKAGES},
        "other_decisions": {d: OTHER_DECISIONS[d] for d in OTHER_DECISIONS
                            if d not in decided
                            and (d not in EXECUTION_DEPENDENCIES or d in awaiting)},
        "awaiting": awaiting,
        "external_dependencies": list(EXTERNAL_DEPENDENCIES),
        "release": "not due: the Founder release decision follows a PASS of this gate "
                   "(FD-FS-001 D4-A); this gate never releases",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="python -m fullstack.readiness")
    commands = parser.add_subparsers(dest="command")
    run = commands.add_parser("evaluate", help="evaluate the gate and print JSON")
    run.add_argument("--runs", type=int, default=20)
    args = parser.parse_args(argv)
    if args.command != "evaluate":
        parser.print_help()
        return 0
    print(json.dumps(evaluate(args.runs), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import sys
    sys.path.insert(0, str(REPO_ROOT))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
