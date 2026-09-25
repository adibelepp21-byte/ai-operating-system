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

**Prepared manifests (`FDR-6` `CR-1`).** A phase that is phase-authorized
but not certified can have a manifest *prepared* for its eventual
certification. It is named `AIOS_P<n>_CERTIFICATION_MANIFEST_v*.json`. That
name does not match the barrier's `MANIFEST_GLOB`, so preparing it protects
nothing. It is verified here like a certified manifest:

* its sha256 must be in the Decision Register;
* its evidence root must be the guard's root for the phase;
* it must claim no certification;
* the phase must be phase-authorized;
* the root must still match it byte for byte.

Any fault is reported. A certified phase whose manifest is only prepared is a
fault until the manifest is promoted.

**Promotion never rewrites the registered index.** Further index files
(`AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX*.json`) are read beside it. Each
must have its sha256 in the Decision Register, and a phase may be indexed only
once per version. Promoting a prepared manifest at certification therefore
creates files, and the barrier then protects them. It changes no certified
reference.

**Successor versions (`FDR-G1` `FD-G1`).** A certified phase may gain a
successor certified version. The earlier version is never rewritten: it stays
indexed, stays verified against its own bytes, and is reported `SUPERSEDED`.
Exactly one version per phase is `CURRENT`. A successor is an index entry in a
new index file, carrying:

```text
certified_version        2, 3, … — consecutive, one entry per number
supersedes_certified     {manifest, manifest_sha256} of the version before it
evidence_root            a new root, neither equal to nor nested with any other
certifying_instrument    its own Founder certification: an instrument, not an
                         earlier version's, that the guard reads as certifying
                         this phase and that resolves in the Register
change_authorization     {instrument, instrument_sha256}: the Founder's
                         authorization of the change, resolving in the Register
supersession_reason      why (a non-empty statement)
verification_record      {path, sha256}: the verification that supported it
```

A successor that lacks any of these, breaks the chain, forks it, reuses a
root, or cites no certification of its own is a fault. It is never `CURRENT`.
Together with the earlier version's entry, these fields answer what was
certified, when, under which decision, what succeeded it, why, and on what
verification. The key names are new on purpose: a manifest's own `version`
is its format, and a prepared manifest's `supersedes` names the prepared
manifest it rebuilt (`ACT-CC-P13-CERT-GATE-003`), not a certified version. A
prepared successor (`AIOS_P<n>_CERTIFICATION_MANIFEST_v*.json` carrying
`supersedes_certified`) is verified the same way before promotion, and it
claims no certification.

This module recognises a successor. It never creates, certifies or promotes
one. Certifying a successor stays with the Founder (`FDR-G1` `§7`).

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
#: `FDR-6` `CR-1`. Neither matches only what it should: a prepared manifest's
#: name must never match the barrier's `MANIFEST_GLOB`, and a test holds that.
PREPARED_GLOB = "AIOS_P*_CERTIFICATION_MANIFEST_v*.json"
INDEX_GLOB = "AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX*.json"
PREPARED = "PREPARED"

#: `FDR-G1` `§6`, `§13`: a version is the current certified baseline, or a
#: historical one that a certified successor superseded.
CURRENT = "CURRENT"
SUPERSEDED = "SUPERSEDED"
#: What every index entry carries, and the provenance a successor entry must
#: add (`FDR-G1` `§13`).
ENTRY_FIELDS = ("manifest", "manifest_sha256", "evidence_root", "certified_commit",
                "certifying_instrument", "certifying_instrument_sha256")
SUCCESSOR_FIELDS = ("supersedes_certified", "change_authorization", "supersession_reason",
                    "verification_record")

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
    #: The current certified version of each phase.
    phases: Dict[str, PhaseResult]
    faults: Tuple[str, ...] = field(default_factory=tuple)
    #: `FDR-6` `CR-1`: manifests prepared for phases not yet certified, and
    #: (`FDR-G1`) prepared successors, keyed `P<n> v<version>`.
    prepared: Dict[str, PhaseResult] = field(default_factory=dict)
    #: `FDR-G1`: superseded certified versions, keyed `P<n> v<version>`. They
    #: are verified as strictly as current ones: superseded is not editable.
    historical: Dict[str, PhaseResult] = field(default_factory=dict)
    #: `FDR-G1`: each phase's accepted version chain, oldest first.
    versions: Dict[str, Tuple[dict, ...]] = field(default_factory=dict)

    @property
    def holds(self) -> bool:
        return (not self.faults and all(p.holds for p in self.phases.values())
                and all(p.holds for p in self.prepared.values())
                and all(p.holds for p in self.historical.values()))

    def as_reported(self) -> dict:
        return {
            "holds": self.holds,
            "faults": list(self.faults),
            "phases": {k: v.as_reported() for k, v in sorted(self.phases.items())},
            "prepared": {k: v.as_reported() for k, v in sorted(self.prepared.items())},
            "historical": {k: v.as_reported()
                           for k, v in sorted(self.historical.items())},
            "versions": {k: [dict(v) for v in chain]
                         for k, chain in sorted(self.versions.items())},
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
    return _compare(phase, record.get("files", {}), entry["evidence_root"],
                    tuple(sorted(entry.get("declared_additions", {}))),
                    repo_root, faults)


def _compare(phase: str, files: Dict[str, str], evidence_root: str,
             declared: Tuple[str, ...], repo_root: Path,
             faults: List[str]) -> PhaseResult:
    """Compare a manifest's files with the tree under its evidence root."""
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

    root = repo_root / evidence_root
    present, unlisted = _present(root, repo_root) if root.is_dir() else (set(), [])
    if not root.is_dir():
        faults.append(f"evidence root absent: {evidence_root}")
    unreadable.extend(sorted(unlisted))
    unexpected = tuple(sorted(present - set(files) - set(declared)))
    return PhaseResult(phase, tuple(intact), tuple(modified), tuple(missing),
                       tuple(unreadable), unexpected, declared, tuple(faults))


def verify_prepared(manifest: Path, repo_root: Path = REPO_ROOT,
                    register_text: str = "") -> Tuple[str, PhaseResult]:
    """A manifest prepared under `FDR-6` `CR-1`, checked as strictly as a
    certified one, plus the conditions that make it *prepared*: it claims no
    certification, and its phase is phase-authorized."""
    from tools import p12_certified_evidence_guard as sentinel
    name = manifest.name
    try:
        raw = manifest.read_bytes()
        record = json.loads(raw)
        number = int(record["phase"])
    except (OSError, ValueError, KeyError, TypeError) as error:
        return name, PhaseResult(name, (), (), (), (), (), (), (
            f"prepared manifest unreadable: {name}: {error}",))
    phase = f"P{number}"
    faults: List[str] = []
    if sha256_bytes(raw) not in register_text:
        faults.append(f"prepared manifest sha256 is not recorded in the "
                      f"Decision Register: {name}")
    if (not str(record.get("status", "")).startswith(PREPARED)
            or record.get("certifying_instrument") is not None
            or record.get("certified_commit") is not None):
        faults.append(f"a prepared manifest claims a certification: {name}")
    root = sentinel.PHASE_EVIDENCE_ROOTS.get(number, f"docs/architecture/p{number}")
    if record.get("evidence_root") != root:
        faults.append(f"prepared evidence root {record.get('evidence_root')!r} "
                      f"is not {phase}'s root {root!r}")
    instrument = record.get("authorizing_instrument")
    if not isinstance(instrument, str) or sha256_file(repo_root / instrument) != \
            record.get("authorizing_instrument_sha256"):
        faults.append(f"authorizing instrument altered or unreadable: {instrument}")
    try:
        from tools import p12_phase_authorization as phases
        authorized = {s["entity"]: s["authorized"]
                      for s in phases.current_states(repo_root)}.get(phase)
    except Exception as error:  # undeterminable is not authorized
        authorized = f"undeterminable: {error}"
    if authorized is not True:
        faults.append(f"{phase} has a prepared manifest but is not "
                      f"phase-authorized ({authorized!r})")
    return phase, _compare(phase, record.get("files", {}), root, (),
                           repo_root, faults)


def _overlaps(a: str, b: str) -> bool:
    """Whether two evidence roots are the same directory or one holds the other."""
    first, second = Path(a).parts, Path(b).parts
    shorter = min(len(first), len(second))
    return first[:shorter] == second[:shorter]


def _resolving_instrument(reference: object, register_text: str,
                          repo_root: Path) -> Optional[str]:
    """A fault, or `None` when `{instrument, instrument_sha256}` names a file
    whose bytes match and whose identity the Decision Register records."""
    from tools import p12_certified_evidence_guard as sentinel
    if not isinstance(reference, dict) or not isinstance(reference.get("instrument"), str):
        return "names no instrument"
    instrument = reference["instrument"]
    if sha256_file(repo_root / instrument) != reference.get("instrument_sha256"):
        return f"instrument altered or unreadable: {instrument}"
    if sentinel._register_identity(Path(instrument).stem, register_text) is None:
        return f"instrument resolves against no Register entry: {instrument}"
    return None


def _successor_faults(phase: str, entry: dict, prior: dict, earlier: List[dict],
                      register_text: str, repo_root: Path,
                      certifying: set) -> List[str]:
    """Why `entry` cannot be accepted as the successor of `prior` (`FDR-G1`)."""
    label = f"{phase} v{entry.get('certified_version')}"
    faults = [f"{label} lacks {name}" for name in ENTRY_FIELDS + SUCCESSOR_FIELDS
              if not entry.get(name)]
    if faults:
        return faults
    supersedes = entry["supersedes_certified"]
    if (not isinstance(supersedes, dict)
            or supersedes.get("manifest") != prior["manifest"]
            or supersedes.get("manifest_sha256") != prior["manifest_sha256"]):
        faults.append(f"{label} does not supersede v{prior.get('certified_version', 1)}'s "
                      f"manifest")
    for other in earlier:
        if _overlaps(entry["evidence_root"], other["evidence_root"]):
            faults.append(f"{label} evidence root {entry['evidence_root']!r} reuses "
                          f"or nests with v{other.get('certified_version', 1)}'s root "
                          f"{other['evidence_root']!r}: a successor never edits "
                          "a certified baseline")
        if entry["certifying_instrument"] == other["certifying_instrument"]:
            faults.append(f"{label} cites v{other.get('certified_version', 1)}'s "
                          "certifying instrument: a successor needs its own "
                          "Founder certification")
    if (int(phase[1:]), Path(entry["certifying_instrument"]).name) not in certifying:
        faults.append(f"{label}'s certifying instrument does not certify {phase} "
                      "in an instrument the Register resolves")
    problem = _resolving_instrument(entry["change_authorization"], register_text,
                                    repo_root)
    if problem:
        faults.append(f"{label} change authorization {problem}")
    record = entry["verification_record"]
    if (not isinstance(record, dict) or not isinstance(record.get("path"), str)
            or sha256_file(repo_root / record["path"]) != record.get("sha256")):
        faults.append(f"{label} verification record altered or unreadable: "
                      f"{record.get('path') if isinstance(record, dict) else record}")
    return faults


def _version_chain(phase: str, listed: List[Tuple[str, dict]], register_text: str,
                   repo_root: Path, certifying: set) -> Tuple[List[dict], List[str]]:
    """The accepted versions of one phase, oldest first, and the faults.

    An entry without `certified_version` is version 1, which keeps every index written
    before `FDR-G1` valid unchanged. A second entry claiming a version already
    held is refused, as a phase indexed twice always was. The chain stops at
    the first version that cannot be accepted, so nothing after a broken link
    can become `CURRENT`.
    """
    faults: List[str] = []
    by_version: Dict[int, dict] = {}
    for source, entry in listed:
        version = entry.get("certified_version", 1)
        if not isinstance(version, int) or isinstance(version, bool) or version < 1:
            faults.append(f"{phase} has an invalid version {version!r} ({source})")
            continue
        if version in by_version:
            faults.append(f"{phase} is indexed more than once ({source})"
                          if version == 1 else
                          f"{phase} v{version} is indexed more than once ({source})")
            continue
        by_version[version] = entry
    chain: List[dict] = []
    for version in sorted(by_version):
        entry = by_version[version]
        if version != len(chain) + 1:
            faults.append(f"{phase} v{version} has no v{len(chain) + 1} before it")
            break
        if version > 1:
            problems = _successor_faults(phase, entry, chain[-1], chain,
                                         register_text, repo_root, certifying)
            if problems:
                faults.extend(problems)
                break
        chain.append(entry)
    return chain, faults


def verify_prepared_successor(manifest: Path, record: dict, raw: bytes,
                              chains: Dict[str, List[dict]], register_text: str,
                              repo_root: Path = REPO_ROOT) -> Tuple[str, PhaseResult]:
    """A successor prepared for certification (`FDR-G1`), before promotion.

    It must claim no certification, name the current version it would
    supersede, live in a root no certified version uses, and cite a Founder
    change authorization the Register resolves. Its root is compared byte for
    byte like any other. It protects nothing: its name is outside the barrier's
    `MANIFEST_GLOB`.
    """
    name = manifest.name
    try:
        phase = f"P{int(record['phase'])}"
        version = int(record["certified_version"])
    except (KeyError, TypeError, ValueError) as error:
        return name, PhaseResult(name, (), (), (), (), (), (), (
            f"prepared successor unreadable: {name}: {error}",))
    label = f"{phase} v{version}"
    faults: List[str] = []
    if sha256_bytes(raw) not in register_text:
        faults.append(f"prepared successor sha256 is not recorded in the Decision "
                      f"Register: {name}")
    if (not str(record.get("status", "")).startswith(PREPARED)
            or record.get("certifying_instrument") is not None
            or record.get("certified_commit") is not None):
        faults.append(f"a prepared successor claims a certification: {name}")
    chain = chains.get(phase, [])
    root = record.get("evidence_root")
    if not chain:
        faults.append(f"{label} is prepared as a successor, but {phase} has no "
                      "certified version to supersede")
    else:
        current = chain[-1]
        supersedes = record.get("supersedes_certified")
        if (version != len(chain) + 1 or not isinstance(supersedes, dict)
                or supersedes.get("manifest") != current["manifest"]
                or supersedes.get("manifest_sha256") != current["manifest_sha256"]):
            faults.append(f"{label} is not prepared as the successor of {phase}'s "
                          f"current version v{len(chain)}")
    problem = _resolving_instrument(record.get("change_authorization"),
                                    register_text, repo_root)
    if problem:
        faults.append(f"{label} change authorization {problem}")
    if not isinstance(root, str) or not root:
        return label, PhaseResult(label, (), (), (), (), (), (), tuple(
            faults + [f"{label} names no evidence root"]))
    for listed in chains.values():
        for other in listed:
            if _overlaps(root, other["evidence_root"]):
                faults.append(f"{label} evidence root {root!r} reuses or nests with "
                              f"the certified root {other['evidence_root']!r}")
    return label, _compare(label, record.get("files", {}), root, (),
                           repo_root, faults)


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

    # `FDR-6` `CR-1`: index files beside the registered one. Each is held to
    # the same Register rule. `FDR-G1`: a phase may be indexed again only as a
    # successor version, and the chain decides which version is current.
    listed: Dict[str, List[Tuple[str, dict]]] = {}
    for phase, entry in record.get("phases", {}).items():
        listed.setdefault(phase, []).append((index.name, entry))
    for supplement in sorted(index.parent.glob(INDEX_GLOB)):
        if supplement.resolve() == index.resolve():
            continue
        try:
            extra_raw = supplement.read_bytes()
            extra = json.loads(extra_raw)
        except (OSError, ValueError) as error:
            faults.append(f"index supplement unreadable: {supplement.name}: {error}")
            continue
        if sha256_bytes(extra_raw) not in register_text:
            faults.append(f"index supplement sha256 is not recorded in the "
                          f"Decision Register: {supplement.name}")
        for phase, entry in extra.get("phases", {}).items():
            listed.setdefault(phase, []).append((supplement.name, entry))

    try:
        certifying = set(sentinel.certification_provenance(acts_root)) if any(
            len(entries) > 1 for entries in listed.values()) else set()
        resolving = {(phase, name) for phase, name in certifying
                     if sentinel._register_identity(Path(name).stem,
                                                    register_text) is not None}
    except OSError as error:
        resolving = set()
        faults.append(f"certification provenance unreadable: {error}")
    chains: Dict[str, List[dict]] = {}
    for phase, entries_for_phase in sorted(listed.items()):
        chain, chain_faults = _version_chain(phase, entries_for_phase,
                                             register_text, repo_root, resolving)
        faults.extend(chain_faults)
        if chain:
            chains[phase] = chain
    roots = [(phase, entry.get("certified_version", 1), entry["evidence_root"])
             for phase, chain in chains.items() for entry in chain
             if isinstance(entry.get("evidence_root"), str) and entry["evidence_root"]]
    for position, (phase, version, root) in enumerate(roots):
        for other_phase, other_version, other_root in roots[position + 1:]:
            if other_phase != phase and _overlaps(root, other_root):
                faults.append(f"{phase} v{version} and {other_phase} v{other_version} "
                              f"share or nest evidence roots ({root!r}, {other_root!r})")
    entries = {phase: chain[-1] for phase, chain in chains.items()}
    promoted = set()
    for chain in chains.values():
        for entry in chain:
            try:
                origin = json.loads((repo_root / entry["manifest"]).read_bytes()
                                    ).get("promoted_from") or {}
            except (OSError, ValueError, AttributeError):
                continue
            if isinstance(origin, dict) and origin.get("manifest_sha256"):
                promoted.add(origin["manifest_sha256"])

    try:
        certified = {f"P{n}" for n in sentinel.certified_phases(acts_root, register)}
    except Exception as error:
        certified = set()
        faults.append(f"certification undeterminable: {error}")
    indexed = set(entries)
    prepared: Dict[str, PhaseResult] = {}
    for path in sorted((repo_root / "docs/governance").glob(PREPARED_GLOB)):
        try:
            raw_prepared = path.read_bytes()
            prepared_record = json.loads(raw_prepared)
        except (OSError, ValueError):
            prepared_record = None
        if isinstance(prepared_record, dict) and "supersedes_certified" in prepared_record:
            if sha256_bytes(raw_prepared) in promoted:
                continue  # promoted: its certified successor governs
            label, result = verify_prepared_successor(
                path, prepared_record, raw_prepared, chains, register_text, repo_root)
            if label in prepared:
                faults.append(f"{label} has more than one prepared manifest")
                continue
            prepared[label] = result
            continue
        phase, result = verify_prepared(path, repo_root, register_text)
        if phase in indexed:
            continue  # promoted: the certified manifest governs
        if phase in prepared:
            faults.append(f"{phase} has more than one prepared manifest")
            continue
        prepared[phase] = result
    for phase in sorted(certified - indexed):
        if phase in prepared:
            faults.append(f"{phase} is certified but its manifest is only "
                          "prepared; it must be promoted into an index under "
                          "the certification decision")
        else:
            faults.append(f"{phase} is certified but has no manifest")
    for phase in sorted(indexed - certified):
        faults.append(f"{phase} has a manifest but is not certified")

    phases = {phase: verify_phase(phase, entry, repo_root)
              for phase, entry in sorted(entries.items())}
    historical = {}
    for phase, chain in sorted(chains.items()):
        for entry in chain[:-1]:
            label = f"{phase} v{entry.get('certified_version', 1)}"
            historical[label] = verify_phase(label, entry, repo_root)
    versions = {
        phase: tuple(
            {"version": entry.get("certified_version", 1),
             "state": CURRENT if position == len(chain) - 1 else SUPERSEDED,
             "manifest": entry["manifest"],
             "evidence_root": entry["evidence_root"],
             "certifying_instrument": entry["certifying_instrument"],
             "superseded_by": (None if position == len(chain) - 1
                               else chain[position + 1]["manifest"])}
            for position, entry in enumerate(chain))
        for phase, chain in sorted(chains.items())}
    return Report(phases, tuple(faults), prepared, historical, versions)


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
