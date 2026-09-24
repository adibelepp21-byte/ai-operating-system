"""P12 certified evidence, fixed by content and verified by comparison.

Built under `GOAL-V2-002`. `tools/p12_certified_evidence_guard.py` refuses
writes that go through it. That makes it a **preventive** control, and it sees
only writers that call it. The static coverage check in its tests sees only
writers that call `write_text` or `write_bytes`. Stores written by Native Core
backends, `open()` or `json.dump` escape both. The observed corruption (`B-02`)
also passed unrefused for six days, because the guard did not yet recognize
P12's certification.

This module is the **outcome** control that does not depend on how a write was
made. It holds the sha256 of every file under `docs/architecture/p12/` as it
stood at the certified commit, and compares the working tree against that
record. Any change to certified evidence then becomes loud, whatever caused it:

```text
PREVENTION  (guard)       refuses a write that routes through it
DETECTION   (manifest)    reports any certified file whose bytes changed
```

**The certified commit is named by the certification record.** It is not
chosen here. `AIOS-P12-FINAL-CERTIFICATION-AND-P13-TRANSITION-HANDOFF-RECORD.md
§1.2` names `6968c6e` as *"final measured certified state"*. The manifest does
not ask to be trusted either: `from_commit` rebuilds it from git history, and
the suite compares the two.

**Additions are reported, not refused.** A file under the P12 root that did not
exist at certification (the handoff record is one) is not certified evidence.
It is listed so that it cannot be mistaken for evidence, and so that nothing
can hide inside the root without showing up.

Nothing here authorizes anything, and nothing here writes.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = REPO_ROOT / "docs/governance/AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json"
EVIDENCE_ROOT = "docs/architecture/p12"

INTACT = "INTACT"
MODIFIED = "MODIFIED"
MISSING = "MISSING"


class ManifestUnavailable(RuntimeError):
    """The manifest cannot be read, so certified content cannot be compared."""


@dataclass(frozen=True)
class Verification:
    intact: Tuple[str, ...]
    modified: Tuple[str, ...]
    missing: Tuple[str, ...]
    additions: Tuple[str, ...]

    @property
    def holds(self) -> bool:
        return not self.modified and not self.missing

    def as_reported(self) -> dict:
        return {
            "holds": self.holds,
            "intact": len(self.intact),
            "modified": list(self.modified),
            "missing": list(self.missing),
            "post_certification_additions": list(self.additions),
        }


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(manifest: Path = MANIFEST) -> dict:
    try:
        return json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ManifestUnavailable(f"{manifest}: {error}") from error


def verify(repo_root: Path = REPO_ROOT, manifest: Path = MANIFEST) -> Verification:
    """Compare every certified file with the bytes it was certified with."""
    record = load(manifest)
    files: Dict[str, str] = record["files"]
    intact, modified, missing = [], [], []
    for relative, expected in sorted(files.items()):
        path = repo_root / relative
        if not path.is_file():
            missing.append(relative)
        elif _sha256(path.read_bytes()) != expected:
            modified.append(relative)
        else:
            intact.append(relative)
    root = repo_root / record["evidence_root"]
    present = {
        str(p.relative_to(repo_root)) for p in root.rglob("*")
        if p.is_file() and "__pycache__" not in p.parts
    } if root.is_dir() else set()
    additions = sorted(present - set(files))
    return Verification(tuple(intact), tuple(modified), tuple(missing),
                        tuple(additions))


def from_commit(commit: str, repo_root: Path = REPO_ROOT,
                evidence_root: str = EVIDENCE_ROOT) -> Optional[Dict[str, str]]:
    """Rebuild the file → sha256 map from git history, or None without it."""
    try:
        names = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", commit, evidence_root],
            cwd=repo_root, capture_output=True, check=True, text=True,
        ).stdout.split("\n")
    except (OSError, subprocess.CalledProcessError):
        return None
    files = {}
    for name in names:
        if not name:
            continue
        blob = subprocess.run(
            # A git revision spec (`<commit>:<path>`), built by concatenation so
            # it is not mistaken for a `path:line` citation locator.
            ["git", "cat-file", "blob", commit + ":" + name],
            cwd=repo_root, capture_output=True, check=True,
        ).stdout
        files[name] = _sha256(blob)
    return files


def main() -> int:
    report = verify().as_reported()
    print(json.dumps(report, indent=2))
    return 0 if report["holds"] else 1


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
