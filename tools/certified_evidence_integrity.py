"""Every certified phase's evidence, compared with the bytes it was certified with.

Built under `GOAL-V2-004`. `GOAL-V2-002` gave P12 a content manifest
(`tools/p12_certified_evidence_manifest.py`). P10 and P11 had none, so a change
to their evidence could be refused but never detected. This module generalizes
detection to every certified phase and closes the loop between certification
and detection in both directions:

```text
Decision Register → guard.certified_phases()   what IS certified
manifest index    → one manifest per phase     what is DETECTED
    certified but no manifest    → fault        (an undetected phase)
    manifest but not certified   → fault        (a reference that lost its warrant)
```

For each phase, and against the resident tree, it reports:

| Finding | Meaning |
|---|---|
| `MODIFIED` | a certified file is present, but its bytes differ |
| `MISSING` | a certified file no longer exists |
| `UNREADABLE` | a certified path exists but cannot be read as a file |
| `UNEXPECTED` | a file inside the root that the certification never held, and that the index does not declare |

**The certification reference itself is checked.** The index records the
sha256 of each manifest and of each certifying instrument. The index's own
sha256 must appear in the Decision Register, which is append-only. Changing a
manifest, an instrument or the index therefore produces a fault. It is not
silently accepted as the new truth.

**Declared additions.** A file added to a certified root after certification
is not evidence. The index can name one such file, with the basis for naming it
(for example, the P12 handoff record). An undeclared addition is `UNEXPECTED`.

**Which commit.** P12's commit is named by its handoff record `§1.2`. P10 and
P11's instruments name no evidence commit. For them, the index anchors each
manifest at the commit that persisted the certifying instrument, and says so. No
commit since has changed either root, so the choice of anchor does not change a
single byte. `from_commit` rebuilds any manifest from git history, so the
manifests never have to be taken on trust.

Nothing here authorizes anything, and nothing here writes.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
INDEX = REPO_ROOT / "docs/governance/AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX_v1.0.json"
REGISTER = REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"

INTACT = "INTACT"
MODIFIED = "MODIFIED"
MISSING = "MISSING"
UNREADABLE = "UNREADABLE"
UNEXPECTED = "UNEXPECTED"


class IntegrityUndeterminable(RuntimeError):
    """The index cannot be read, so nothing can be compared."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> Optional[str]:
    try:
        return sha256_bytes(path.read_bytes())
    except OSError:
        return None


@dataclass(frozen=True)
class PhaseResult:
    phase: str
    intact: Tuple[str, ...]
    modified: Tuple[str, ...]
    missing: Tuple[str, ...]
    unreadable: Tuple[str, ...]
    unexpected: Tuple[str, ...]
    declared_additions: Tuple[str, ...]
    reference_faults: Tuple[str, ...]

    @property
    def holds(self) -> bool:
        return not (self.modified or self.missing or self.unreadable
                    or self.unexpected or self.reference_faults)

    def as_reported(self) -> dict:
        return {
            "holds": self.holds,
            "intact": len(self.intact),
            MODIFIED: list(self.modified),
            MISSING: list(self.missing),
            UNREADABLE: list(self.unreadable),
            UNEXPECTED: list(self.unexpected),
            "declared_additions": list(self.declared_additions),
            "reference_faults": list(self.reference_faults),
        }


@dataclass(frozen=True)
class Report:
    phases: Dict[str, PhaseResult]
    faults: Tuple[str, ...] = field(default_factory=tuple)

    @property
    def holds(self) -> bool:
        return not self.faults and all(p.holds for p in self.phases.values())

    def as_reported(self) -> dict:
        return {
            "holds": self.holds,
            "faults": list(self.faults),
            "phases": {k: v.as_reported() for k, v in sorted(self.phases.items())},
        }


def load_index(index: Path = INDEX) -> dict:
    try:
        return json.loads(index.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise IntegrityUndeterminable(f"{index}: {error}") from error


def _present(root: Path, repo_root: Path) -> Tuple[set, List[str]]:
    """Every file under `root`, and every directory that could not be listed."""
    present, unlisted = set(), []

    def failed(error: OSError) -> None:
        unlisted.append(os.path.relpath(error.filename, repo_root))

    for base, dirs, files in os.walk(root, onerror=failed):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for name in files:
            present.add(Path(os.path.relpath(os.path.join(base, name),
                                             repo_root)).as_posix())
    return present, unlisted


def verify_phase(phase: str, entry: dict, repo_root: Path = REPO_ROOT) -> PhaseResult:
    faults: List[str] = []
    manifest_path = repo_root / entry["manifest"]
    try:
        raw = manifest_path.read_bytes()
        record = json.loads(raw)
    except (OSError, ValueError) as error:
        return PhaseResult(phase, (), (), (), (), (), (),
                           (f"manifest unreadable: {entry['manifest']}: {error}",))
    if sha256_bytes(raw) != entry["manifest_sha256"]:
        faults.append(f"manifest altered: {entry['manifest']}")
    for key in ("evidence_root", "certified_commit", "certifying_instrument"):
        if record.get(key) != entry[key]:
            faults.append(f"manifest {key} disagrees with the index")
    instrument = sha256_file(repo_root / entry["certifying_instrument"])
    if instrument != entry["certifying_instrument_sha256"]:
        faults.append(f"certifying instrument altered or unreadable: "
                      f"{entry['certifying_instrument']}")

    files: Dict[str, str] = record.get("files", {})
    intact, modified, missing, unreadable = [], [], [], []
    for relative, expected in sorted(files.items()):
        path = repo_root / relative
        if not os.path.lexists(path):
            missing.append(relative)
            continue
        actual = sha256_file(path)
        if actual is None:
            unreadable.append(relative)
        elif actual != expected:
            modified.append(relative)
        else:
            intact.append(relative)

    root = repo_root / entry["evidence_root"]
    present, unlisted = _present(root, repo_root) if root.is_dir() else (set(), [])
    if not root.is_dir():
        faults.append(f"evidence root absent: {entry['evidence_root']}")
    unreadable.extend(sorted(unlisted))
    declared = tuple(sorted(entry.get("declared_additions", {})))
    unexpected = tuple(sorted(present - set(files) - set(declared)))
    return PhaseResult(phase, tuple(intact), tuple(modified), tuple(missing),
                       tuple(unreadable), unexpected, declared, tuple(faults))


def verify(repo_root: Path = REPO_ROOT, index: Optional[Path] = None,
           register: Optional[Path] = None,
           acts_root: Optional[Path] = None) -> Report:
    """Compare every certified phase with its manifest, and both with each other."""
    from tools import p12_certified_evidence_guard as sentinel

    index = index or repo_root / INDEX.relative_to(REPO_ROOT)
    register = register or repo_root / REGISTER.relative_to(REPO_ROOT)
    acts_root = acts_root or repo_root / "docs/governance/acts"
    faults: List[str] = []
    try:
        raw = index.read_bytes()
        record = json.loads(raw)
    except (OSError, ValueError) as error:
        return Report({}, (f"index unreadable: {error}",))

    try:
        register_text = register.read_text(encoding="utf-8")
    except OSError as error:
        register_text = ""
        faults.append(f"Decision Register unreadable: {error}")
    if sha256_bytes(raw) not in register_text:
        faults.append("index sha256 is not recorded in the Decision Register")

    try:
        certified = {f"P{n}" for n in sentinel.certified_phases(acts_root, register)}
    except Exception as error:
        certified = set()
        faults.append(f"certification undeterminable: {error}")
    indexed = set(record.get("phases", {}))
    for phase in sorted(certified - indexed):
        faults.append(f"{phase} is certified but has no manifest")
    for phase in sorted(indexed - certified):
        faults.append(f"{phase} has a manifest but is not certified")

    phases = {phase: verify_phase(phase, entry, repo_root)
              for phase, entry in sorted(record.get("phases", {}).items())}
    return Report(phases, tuple(faults))


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
