"""FS-09 — the Production Readiness Gate, evaluated rather than asserted.

    python -m fullstack.readiness evaluate [--runs N]

Every criterion of Act `§20` (and ACT-003 `§19`) gets one of:

* **PASS**: met, on the evidence named in the criterion;
* **FAIL**: not met, or not verified (a gap to close);
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
  to FAIL until the Preview is verified again.
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
}
PASS, FAIL, BLOCKED, OBSERVED = "PASS", "FAIL", "BLOCKED", "OBSERVED"
READY, NOT_READY = "PRODUCTION READY", "NOT PRODUCTION READY"

#: Decisions a criterion can wait on that are not FS-DP packages. None has a
#: package yet; each is recorded in `docs/fullstack/FS-09-DECISION-REGISTER.md`.
OTHER_DECISIONS = {
    "ENVIRONMENT-SEPARATION": "Architect: how Production data is kept apart from Preview "
                              "data in the ratified Supabase arrangement (ACT-003 §19)",
    "PYTHON-RUNTIME-VERSION": "Architect: which Python the host must run. FS-02 names 3.11 "
                              "(every local and certified run); the FS-08 Preview ran 3.12, "
                              "the host default, because nothing pins it",
    "OPERATIONAL-OWNERSHIP": "Founder: who operates AIOS, holds the production operator "
                             "token, runs backups and answers incidents (ACT-003 §19)",
}
#: Recorded live evidence the gate reads. It is never written here.
PREVIEW_EVIDENCE = REPO_ROOT / "docs/fullstack/evidence/FS-08-LIVE-PREVIEW-2026-09-27.json"
BACKUP_EXPORT = REPO_ROOT / "docs/fullstack/evidence/FS-09-BACKUP-EXPORT-2026-09-27.jsonl"
BACKUP_MANIFEST = REPO_ROOT / "docs/fullstack/evidence/FS-09-BACKUP-MANIFEST-2026-09-27.json"
RUNBOOK = REPO_ROOT / "docs/fullstack/FS-09-OPERATIONAL-RUNBOOK.md"
MIGRATIONS = REPO_ROOT / "fullstack/deploy/supabase/migrations"
#: Operator inspection of the live store (Supabase `list_migrations`, 2026-09-27,
#: Register `§87` and `§88`): the migrations applied there.
APPLIED_MIGRATIONS = ("20260927062422_aios_records",)
#: What the Vercel function serves: its entry point, configuration and the code
#: it imports. A change here since the recorded Preview commit makes the
#: recording stale. Operator tools the function never imports are excluded.
SERVED_PATHS = ("api", "vercel.json", "fullstack/__init__.py", "fullstack/deploy/__init__.py",
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
#: key and the Preview wrote to and read from the store (Register `§86`).
EXTERNAL_DEPENDENCIES = (
    {"id": "EXT-02", "what": "S-01 AIOS Transition Manifest not supplied (FD-FS-001 D5-A)",
     "needs": "the Founder to supply the exact document"},
    {"id": "EXT-03", "what": "Vercel SSO protects every Preview and the connector cannot pass "
     "it; FS-08 reached the Preview through a Founder-authorized, temporary automation bypass, "
     "revoked after the suite (Register §86). The connector reads build logs (2026-09-27)",
     "needs": "a new, equally temporary Founder authorization for any further live Preview "
     "check (FS-09: performance, a live 403, a rollback drill)"},
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
            for package in re.findall(r"FS-DP-0\d", row.group(1)):
                found[package] = heading
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
    """The recorded FS-08 live checks, and whether they still cover this tree."""
    data = json.loads(path.read_text(encoding="utf-8"))
    passed = {r["check"] for r in data["results"] if r["result"] == "PASS"}
    if str(data.get("database_after", {}).get("update_attempt", "")).startswith("refused"):
        passed.add("store refuses UPDATE")
    diff = subprocess.run(["git", "diff", "--quiet", data["commit"], "--", *SERVED_PATHS],
                          cwd=str(REPO_ROOT), capture_output=True, text=True)
    current = {0: True, 1: False}.get(diff.returncode)   # None: commit not available
    return {"file": path.relative_to(REPO_ROOT).as_posix(), "date": data["date"],
            "commit": data["commit"], "deployment": data["deployment"],
            "passed": passed, "current": current}


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
    if local_ok is False:
        status = FAIL
    elif missing:
        status, evidence = FAIL, evidence + "; not recorded PASS: " + ", ".join(missing)
    elif checks and preview["current"] is not True:
        status = FAIL
        evidence += ("; the served code changed since the recorded commit, so the recording "
                     "no longer covers this tree" if preview["current"] is False else
                     "; the recorded commit is not available to compare with this tree")
    else:
        status = PASS
    return _criterion(area, name, status, evidence, classes=classes, residual=residual)


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
        aios.stop()
    return {"records": len(entries), "digests_match_server": digests,
            "restored_identical": identical, "runs_read": len(runs),
            "every_run_trace_resolved": traced,
            "ok": digests and identical and traced and len(runs) == manifest[
                "partitions"]["fullstack-runs"]["records"]}


def _runbook_sections() -> List[str]:
    """The required runbook sections that are missing."""
    if not RUNBOOK.is_file():
        return list(RUNBOOK_SECTIONS)
    headings = {line.lstrip("#").strip().split(". ", 1)[-1]
                for line in RUNBOOK.read_text(encoding="utf-8").splitlines()
                if line.startswith("## ")}
    return [s for s in RUNBOOK_SECTIONS if s not in headings]


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
            make_app(factory, NoAuthenticator())(
                env, lambda s, h: seen.update(s=int(s.split()[0])))
        return seen["s"]

    return {"no_key": status(lambda: None),
            "unreachable": status(lambda: SupabaseStorage(
                "https://example.invalid", "k", transport=unreachable))}


def _measure(runs: int) -> dict:
    """Exercise the real application in a throwaway directory."""
    from fullstack.backend.api import create_app
    from fullstack.backend.security import (AUDIT, OBSERVE, RUN_WORKFLOW, Authenticator,
                                            Principal)
    from wsgiref.util import setup_testing_defaults

    class _Gate(Authenticator):
        mechanism = "readiness-gate probe"
        principals = {"gate-operator": Principal("gate-operator", {OBSERVE, RUN_WORKFLOW, AUDIT}),
                      "gate-observer": Principal("gate-observer", {OBSERVE})}

        def authenticate(self, headers):
            return self.principals.get(headers.get("x-gate-principal", ""))

    def call(app, method, path, who=None, body=None):
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
        app, aios = create_app(Path(tmp), REPO_ROOT, _Gate())
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
        audit = call(app, "GET", "/api/v1/audit?limit=200", "gate-operator")[2]["entries"]
        aios.stop()
        final = {p.name: p.read_bytes() for p in store.iterdir()}
        appended_only = all(final[name].startswith(data) for name, data in first.items())
        _, restarted = create_app(Path(tmp), REPO_ROOT, _Gate())
        survived = len(restarted.runs())
        restarted.stop()
    return {"success": ok.get("state") == "succeeded" and status == 201,
            "failure_state": failed.get("state"), "failure_reason": failed.get("failure_reason"),
            "observer_post": refused, "anonymous_get": anonymous,
            "headers": headers, "traces": traces, "expected_traces": 3 * runs + 2,
            "audit_entries": len(audit), "appended_only": appended_only,
            "runs_after_restart": survived, "runs_made": runs + 1,
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
             preview: Optional[dict] = None, decisions: Sequence[str] = ()) -> dict:
    """`preview` replaces the recorded Preview checks (tests only); `decisions`
    names non-package decisions to treat as taken (tests only: none is taken)."""
    text = register_text if register_text is not None else REGISTER.read_text(encoding="utf-8")
    decided = dict(ratified(text), **{d: "test" for d in decisions})
    preview = preview if preview is not None else preview_record()
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
    only_scope = ("refusal for a missing scope (403) is evidenced locally only: the Preview "
                  "holds one principal with every scope")
    c: List[dict] = [
        _live("Functionality", "core functions work (Scenario B)", m["success"],
              f"{runs} runs succeeded", ["authenticated POST creates a run"], preview),
        _live("Functionality", "failure is a meaningful state (Scenario C)",
              m["failure_state"] == "failed",
              f"state {m['failure_state']!r}: {m['failure_reason']}",
              ["failure paths are meaningful states"], preview),
        _blocked_unless("Functionality", "agent creation (Scenario A)", ["FS-DP-07"], decided,
                        "ratified but not implemented"),
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
        or _criterion(
            "Reliability", "rollback of a deployment", FAIL,
            "NOT VERIFIED: no deployment rollback has been exercised. Data compatibility only "
            "(FS-09 discovery: 6e31092 reads fullstack.run/2). Floors: below 0706446 (C1) "
            "brings back duplicate run ids under concurrency; below 215248f (B3) the API "
            "authenticates nobody. Neither target is production-safe because its data "
            "reads", classes=[LOCAL_RECORDED]),
        _criterion("Performance", "latency of Scenario B (local, in-process)", OBSERVED,
                   f"p50 {m['latency_ms']['p50']} ms, max {m['latency_ms']['max']} ms over "
                   f"{runs} runs. No canonical workload or latency requirement exists; a "
                   "formal one needs a Founder decision. Live latency not measured",
                   classes=[LOCAL]),
        _live("Observability", "tracing (Trace)", m["traces"] == m["expected_traces"],
              f"{m['traces']} Trace records for {runs} successful and 1 failed run",
              ["Trace associated with the run"], preview),
        _blocked_unless("Observability", "logging, metrics, alerting", ["FS-DP-06"], decided,
                        "ratified but not implemented"),
        _live("Data", "integrity (append-only)", m["appended_only"],
              "every partition's earlier bytes are a prefix of its later bytes",
              ["store refuses UPDATE"], preview),
        _blocked("Data", "persistence on the ratified store", ["FS-DP-01"], decided) or _live(
            "Data", "persistence on the ratified store",
            m["runs_after_restart"] == m["runs_made"], "the store outlives the Runtime",
            ["authenticated POST creates a run",
             "persisted in Supabase, read by a later Runtime"], preview),
        _blocked("Data", "backup and restore", ["FS-DP-01"], decided) or _criterion(
            "Data", "backup and restore", PASS if drill["ok"] else FAIL,
            f"operator export of the live store ({drill['records']} records) matches the "
            f"database's digests: {drill['digests_match_server']}; restored now into a fresh "
            f"store byte-identical: {drill['restored_identical']}; the application reads "
            f"{drill['runs_read']} runs and resolves every run's Trace: "
            f"{drill['every_run_trace_resolved']}", classes=[OPERATOR, LOCAL],
            residual="backups exist only when the operator runs one (free plan: no "
                     "downloadable backup); cadence and owner are unset "
                     "(OPERATIONAL-OWNERSHIP); restore into a second live project waits "
                     "on ENVIRONMENT-SEPARATION"),
        _criterion("Data", "migration", PASS if in_repo == list(APPLIED_MIGRATIONS) else FAIL,
                   f"in the repository: {in_repo}; applied on the live store (operator "
                   f"inspection): {list(APPLIED_MIGRATIONS)}", classes=[LOCAL, OPERATOR],
                   residual="never replayed on a second environment"),
        _blocked("Data", "environment separation", ["ENVIRONMENT-SEPARATION"], decided,
                 "Preview and a future Production would share one table") or _criterion(
            "Data", "environment separation", FAIL, "decided; not implemented"),
        _criterion("Operations", "runbook", FAIL if missing_sections else PASS,
                   ("missing sections: " + ", ".join(missing_sections)) if missing_sections
                   else f"{RUNBOOK.relative_to(REPO_ROOT).as_posix()} covers every required "
                        "section", classes=[LOCAL],
                   residual="written, not yet exercised in an incident; its monitoring and "
                            "alerting part waits on FS-DP-06"),
        _blocked("Operations", "operational ownership", ["OPERATIONAL-OWNERSHIP"], decided)
        or _criterion("Operations", "operational ownership", FAIL, "decided; not recorded"),
        _criterion("Reproducibility", "known artifact", PASS if head else FAIL,
                   f"commit {head}; no build step", classes=[LOCAL]),
        _blocked("Reproducibility", "runtime version pinned", ["PYTHON-RUNTIME-VERSION"],
                 decided, "nothing pins it; the host chose 3.12 for the FS-08 Preview "
                 "(build log bld_8ubuwdj02) while every local run is 3.11")
        or _criterion("Reproducibility", "runtime version pinned", FAIL,
                      "decided; not yet pinned"),
        _blocked_unless("Reproducibility", "reproducible deployment",
                        ["FS-DP-03", "FS-DP-04"], decided,
                        "each push builds a READY Preview (recorded at FS-08); networking "
                        "rules not yet verified against a ratified FS-DP-03"),
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
                            if d not in decided},
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
