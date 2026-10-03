"""S-6 integrity baseline (directive `§24`). READ-ONLY: hashes, writes only its own JSON.

Captured before discovery; ``s6_frontier_discovery.py`` recaptures the same
surfaces afterwards and compares. The Register is captured as bytes so the
comparison can prove it was only appended to; the S-6 act itself is excluded
(it is the directive, persisted verbatim before the baseline).
"""
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO))

import tools  # noqa: E402,F401  -- installs the certified-write barrier

OUT = Path(__file__).parent / "S6-BASELINE-2026-10-03.json"
REGISTER = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
S6_ACT = "docs/governance/acts/DIR-AIOS-AGENCY-S6-SYSTEMIC-INTEGRATION-FRONTIER-DISCOVERY.md"
SKIP = ("__pycache__", ".pyc")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def files(where, pattern="*"):
    base = REPO / where
    return sorted(p for p in base.rglob(pattern) if p.is_file() and not any(s in str(p) for s in SKIP))


def digest(paths):
    t = {str(p.relative_to(REPO)): sha(p) for p in paths}
    return {"files": len(t), "digest": hashlib.sha256(json.dumps(t, sort_keys=True).encode()).hexdigest()}


def surfaces():
    """Every surface `§24` names, as {name: {files, digest}}."""
    s = {}
    for w in ("docs/architecture/p11", "docs/architecture/p12", "docs/architecture/p13",
              "docs/architecture/platform-organization", "docs/operations"):
        s[f"certified:{w}"] = digest(files(w))
    s["operational:agency/operations"] = digest(files("docs/architecture/agency/operations"))
    s["agent_registry:*.instance.json"] = digest(
        p for p in sorted(REPO.rglob("*.instance.json")) if ".git" not in p.parts)
    s["capability_catalog:docs/architecture/organization"] = digest(files("docs/architecture/organization"))
    s["candidates:docs/architecture/candidates"] = digest(files("docs/architecture/candidates"))
    s["governance:docs/governance (except Register and S-6 act)"] = digest(
        p for p in files("docs/governance") if str(p.relative_to(REPO)) not in (REGISTER, S6_ACT))
    s["agency_records:docs/architecture/agency/*.md"] = digest(
        sorted((REPO / "docs/architecture/agency").glob("*.md")))
    for w in ("tools", "native_core", "consumers", "api", "fullstack"):
        s[f"code:{w}"] = digest(files(w))
    s["deployment:vercel.json"] = digest([REPO / "vercel.json"])
    s["root_entry_points:*.py"] = digest(sorted(REPO.glob("*.py")))
    return s


def register_state():
    b = (REPO / REGISTER).read_bytes()
    return {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()}


if __name__ == "__main__":
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                          text=True).stdout.strip()
    OUT.write_text(json.dumps({
        "captured_at": datetime.now(timezone.utc).isoformat(), "head": head,
        "script_sha256": sha(__file__), "surfaces": surfaces(), "register": register_state(),
        "s6_act_sha256": sha(REPO / S6_ACT)}, indent=1) + "\n", encoding="utf-8")
    print(OUT.read_text(encoding="utf-8"))
