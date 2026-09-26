"""Construction verifier for the PD-05 … PD-10 construction volumes.

Built under `ACT-CC-POST-P13-PLATFORM-ORG-003` as amended by v1.1, authorized
for execution by `FD-PO-003-01`. **Read-only.** It reads the construction
volumes and the sources they cite. It never writes. It certifies, freezes,
activates and canonicalizes nothing: every report carries `certifies`,
`canonical` and `grants_authority` as False.

**What a construction volume must satisfy (v1.1 `§10`, `§11`, `§18`, `§20`,
`§23`).**

- Every section states one dimension and one epistemic class from the
  v1.1 `§10` vocabulary.
- All eleven v1.1 `§20` dimensions are present.
- Every `Source:` and `Reference:` line quotes text that is found in the
  cited file. A quotation that is not there fails.
- A SOURCE-DERIVED section cites at least one verified `Source:`.
- Roadmap and derived material is never a `Source:`. That covers ACT-003
  and its Amendment (their section lists are candidates, `§11`), the P10
  division records (DERIVED, `§18`) and the construction namespace itself.
  Such material may be a `Reference:`.
- A RESERVED-DECISION section names at least one reservation, and each
  reservation is still recorded where it is recorded. An UNKNOWN section
  states what is unknown.
- The header declares the volume not canonical, not frozen and not
  activated. For PD-10, the header holds the name open under `G-02`.
- No reserved binding is asserted:
  - Security Owner → PD-08, or Quality authority → PD-09;
  - Governance Authority → PD-03;
  - Sub Division as a structural unit (`G-10`);
  - a division bound to `native_core` or `tools/`.
- No line of a frozen PD-01 body is copied into a volume (`§5`).
- Each volume's bytes match `CONSTRUCTION-MANIFEST.json`.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from tools import platform_organization_gate as po

REPO_ROOT = po.REPO_ROOT
CONSTRUCTION_ROOT = "docs/architecture/platform-division-construction"
MANIFEST = f"{CONSTRUCTION_ROOT}/CONSTRUCTION-MANIFEST.json"

VOLUMES: Dict[str, str] = {
    "PD-05": f"{CONSTRUCTION_ROOT}/pd-05-runtime-and-execution/VOLUME.md",
    "PD-06": f"{CONSTRUCTION_ROOT}/pd-06-ai-engineering/VOLUME.md",
    "PD-07": f"{CONSTRUCTION_ROOT}/pd-07-infrastructure-and-platform/VOLUME.md",
    "PD-08": f"{CONSTRUCTION_ROOT}/pd-08-security/VOLUME.md",
    "PD-09": f"{CONSTRUCTION_ROOT}/pd-09-quality-and-evaluation/VOLUME.md",
    # The directory carries the CPID only: the name is held open (`G-02`).
    "PD-10": f"{CONSTRUCTION_ROOT}/pd-10/VOLUME.md",
}

SOURCE_DERIVED = "SOURCE-DERIVED"
INHERITED = "INHERITED-PATTERN"
ADAPTATION = "DOMAIN-ADAPTATION"
RECONSTRUCTION = "BOUNDED-RECONSTRUCTION"
UNKNOWN = "UNKNOWN"
RESERVED = "RESERVED-DECISION"
CLASSES = (SOURCE_DERIVED, INHERITED, ADAPTATION, RECONSTRUCTION, UNKNOWN, RESERVED)

#: v1.1 `§20`, in its order.
DIMENSIONS = ("Identity", "Boundary", "Authority", "Ownership", "Capability",
              "Architecture", "Operation", "Performance", "Lifecycle",
              "Integration", "Evolution")
#: Sections that carry no single dimension (internal organization, candidate
#: structure) state `—`.
NO_DIMENSION = "—"

#: Never a `Source:` (v1.1 `§11`, `§18`): roadmap, derived and self material.
NOT_SOURCE = (
    "docs/governance/acts/ACT-CC-POST-P13-PLATFORM-ORG-003",
    po.DIVISIONS_DIR + "/",
    CONSTRUCTION_ROOT + "/",
)

#: Reservations a volume may name besides the gate's open items. Each is
#: recorded, with this text, in this source.
RESERVATIONS: Dict[str, Tuple[str, str, str]] = {
    "FRZ-10": (po.ARCHITECT, "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
               "## 10. Deferred Architecture (Architect Reserved)"),
    "FRZ-2": (po.ARCHITECT, "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md",
              "**Reserved concepts** with no ratified entity"),
    "DM-6": (po.ARCHITECT, "docs/architecture/domain-model/canonical-domain-model-v1.md",
             "Created/retired via architectural decision, architect approval"),
    "DM-8": (po.ARCHITECT, "docs/architecture/domain-model/canonical-domain-model-v1.md",
             "The Spine is intentionally shallow (three levels) and is not to be "
             "deepened or bypassed without an architectural decision"),
}

#: The registered Founder decision that authorized construction (Register `§49`).
#: Preparation is not authorization (v1.1 `§18`): a volume must cite it.
AUTHORIZATION = "FD-PO-003-01"

#: `FD-PO-004` D1-A: the canonical construction baseline. The sections
#: certified are those verified at `5eb0eec`; this manifest records their bytes
#: and per-section classes. Certification preserves both (FD-PO-004 `§2`, `§9`).
CANONICAL_MANIFEST = f"{CONSTRUCTION_ROOT}/CANONICAL-BASELINE-MANIFEST.json"
CANONICAL_HEADER = {
    "Construction status": "CANONICAL CONSTRUCTION BASELINE — CERTIFIED WITH CLASSIFIED RESIDUAL",
    "Canonical": "YES — construction baseline",
    "Frozen": "NO",
    "Activated": "NO",
}
#: The open item whose closure by a registered Founder decision makes a volume
#: canonical, and the bindings a header may declare only once their item is
#: closed the same way.
CANONICALIZING_ITEM = "G-01"
BINDING_ITEMS = {"PD-08": "FDP-P10-001", "PD-09": "FDP-P10-002"}

REQUIRED_HEADER = {
    "Construction status": "CONSTRUCTED — NOT CANONICAL",
    "Canonical": "NO",
    "Frozen": "NO",
    "Activated": "NO",
}

FORBIDDEN: Tuple[Tuple[str, str], ...] = (
    (r"PD-08 (?:is|=|becomes|acts as) (?:the )?Security (?:Owner|owner|Authority|authority)",
     "Security Owner bound to PD-08 (FDP-P10-001)"),
    (r"Security (?:Owner|owner|Authority|authority) (?:is|=) PD-08",
     "Security Owner bound to PD-08 (FDP-P10-001)"),
    (r"PD-09 (?:is|=|becomes|acts as) (?:the )?Quality (?:Owner|owner|Authority|authority)",
     "Quality authority bound to PD-09 (FDP-P10-002)"),
    (r"Quality (?:Owner|owner|Authority|authority) (?:is|=) PD-09",
     "Quality authority bound to PD-09 (FDP-P10-002)"),
    (r"PD-03 (?:is|=|holds) (?:the )?Governance Authority",
     "Governance Authority bound to PD-03 (FDP-P10-003)"),
    (r"Sub[- ]?Divisions?\b", "Sub Division as a structural unit (G-10)"),
    (r"PD-\d{2} (?:owns|is bound to|governs|is the owner of) `?(?:native_core|tools/)",
     "division bound to an implementation boundary (correspondence ≠ ownership)"),
    (r"\bStatus: (?:CANONICAL|FROZEN|ACTIVE)\b", "canonical status claimed"),
    (r"PD-(?:0[5-9]|10) (?:holds|has|exercises) (?:the )?(?:Architecture|Governance|Executive|Founder) [Aa]uthority",
     "authority collision with PD-01, PD-02, PD-03 or the Founder"),
)

#: v1.1 `§21`. Sections whose content depends on an open binding: each must be
#: RESERVED-DECISION and name it.
BINDINGS: Dict[Tuple[str, str], str] = {
    ("PD-08", "A3"): "FDP-P10-001", ("PD-08", "A4"): "FDP-P10-001",
    ("PD-09", "A3"): "FDP-P10-002", ("PD-09", "A4"): "FDP-P10-002",
    ("PD-10", "A1"): "G-02",
}
#: The certified interface registry's declared edges into constructed volumes.
#: Each must be carried, and carried as undefined.
EDGES: Dict[str, str] = {"X-02": "PD-08", "X-03": "PD-09", "X-04": "PD-06", "X-05": "PD-05"}
#: The prose ownership statements in the frozen PD-02 corpus. A SOURCE-DERIVED
#: Ownership section cites its own, or says the owner is "not stated".
OWNERSHIP_STATEMENTS: Dict[str, str] = {
    "PD-05": "PD-05 owns Runtime.",
    "PD-06": "PD-06 owns implementation.",
    "PD-07": "PD-07 tetap memiliki ownership atas Infrastructure.",
}

_HEADER_ROW = re.compile(r"^\| \*\*(.+?)\*\* \| (.+?) \|\s*$", re.M)
_SECTION = re.compile(r"^## ([A-Z]\d+)\. (.+)$", re.M)
_META = re.compile(r"^\*\*Dimension:\*\* (.+?) · \*\*Class:\*\* ([A-Z-]+)\s*$", re.M)
_CITE = re.compile(r"^- (Source|Reference): `([^`]+)` — \"(.+)\"\s*$", re.M)
_RESERVED = re.compile(r"^- Reserved: (.+)$", re.M)
_UNKNOWN = re.compile(r"^- Unknown: \S.+$", re.M)


def _read(root: Path, relative: str) -> Optional[str]:
    try:
        return (root / relative).read_text(encoding="utf-8")
    except OSError:
        return None


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reservations(root: Path = REPO_ROOT) -> Dict[str, dict]:
    """Every reservation a volume may name, with whether it is still recorded."""
    out = {}
    for item in po.OPEN_ITEMS:
        out[item.identifier] = {"holder": item.holder, "source": item.source,
                                "recorded": po._contains(_read(root, item.source), item.anchor)}
    for identifier, (holder, source, anchor) in RESERVATIONS.items():
        out[identifier] = {"holder": holder, "source": source,
                           "recorded": po._contains(_read(root, source), anchor)}
    return out


def header(text: str) -> Dict[str, str]:
    head = text.split("\n## ", 1)[0]
    return {m.group(1): m.group(2).strip() for m in _HEADER_ROW.finditer(head)}


def sections(text: str) -> List[dict]:
    """The volume's sections, each with its dimension, class and citations."""
    marks = list(_SECTION.finditer(text))
    out = []
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(text)
        body = text[mark.end():end]
        meta = _META.search(body)
        out.append({
            "id": mark.group(1),
            "title": mark.group(2).strip(),
            "dimension": meta.group(1).strip() if meta else None,
            "class": meta.group(2) if meta else None,
            "citations": [(m.group(1), m.group(2), m.group(3)) for m in _CITE.finditer(body)],
            "reserved": [r.strip(" `") for line in _RESERVED.findall(body)
                         for r in line.split(",")],
            "unknown": bool(_UNKNOWN.search(body)),
            "body": body,
        })
    return out


def _pd01_lines(root: Path) -> set:
    lines = set()
    for path in sorted((root / po.VOLUME_1).glob("[A-E]*.md")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = " ".join(po._normalised(line).split())
            if len(line) >= 40:
                lines.add(line)
    return lines


def closing_decisions(root: Path = REPO_ROOT) -> Dict[str, Optional[str]]:
    """The registered Founder decision, if any, that closes each item this
    verifier acts on. Only the gate's own rule decides: a `### <id> —` entry
    decided by the item's holder that names it under **Closes**."""
    register = _read(root, po.REGISTER) or ""
    items = {i.identifier: i for i in po.OPEN_ITEMS}
    wanted = [CANONICALIZING_ITEM, *BINDING_ITEMS.values()]
    return {w: po._closing_decision(register, items[w]) for w in wanted}


def section_text(text: str) -> str:
    """Everything from the first section on: what certification covers. The
    header above it records status and may change with a decision."""
    index = text.find("\n## ")
    return text[index + 1:] if index >= 0 else ""


def verify_volume(root: Path, cpid: str, known: Dict[str, dict],
                  pd01: set, manifest: dict, closed: Optional[Dict[str, Optional[str]]] = None,
                  canonical_manifest: Optional[dict] = None) -> dict:
    closed = closed or {}
    canonical_manifest = canonical_manifest or {}
    relative = VOLUMES[cpid]
    text = _read(root, relative)
    errors: List[str] = []
    if text is None:
        return {"cpid": cpid, "path": relative, "present": False,
                "errors": ["volume not present"], "passes": False}

    fields = header(text)
    if fields.get("CPID", "").strip("`") != cpid:
        errors.append(f"header CPID {fields.get('CPID')!r} ≠ {cpid}")
    if AUTHORIZATION not in fields.get("Authority", ""):
        errors.append(f"header Authority does not cite the authorizing decision {AUTHORIZATION}")
    certified_by = closed.get(CANONICALIZING_ITEM)
    expected = CANONICAL_HEADER if certified_by else REQUIRED_HEADER
    for field, value in expected.items():
        if fields.get(field) != value:
            errors.append(f"header {field} must be {value!r}, is {fields.get(field)!r}")
    if certified_by:
        if certified_by not in fields.get("Certified by", ""):
            errors.append(f"header Certified by does not cite {certified_by}")
        pinned = canonical_manifest.get("volumes", {}).get(cpid, {})
        body = section_text(text)
        if pinned.get("sections_sha256") != hashlib.sha256(body.encode("utf-8")).hexdigest():
            errors.append("certified sections changed after certification")
        classes_now = [[x["id"], x["class"]] for x in sections(text)]
        if pinned.get("classes") != classes_now:
            errors.append("a section's class differs from its certified class")
    elif "Certified by" in fields:
        errors.append("header claims certification without a registered Founder decision")
    if cpid in BINDING_ITEMS:
        item = BINDING_ITEMS[cpid]
        binding = fields.get("Binding", "")
        if closed.get(item):
            if "BOUND" not in binding or closed[item] not in binding:
                errors.append(f"header Binding does not record {item} as bound by {closed[item]}")
        elif "BOUND" in binding:
            errors.append(f"header Binding declares {item} bound without a registered Founder decision")
    if cpid == "PD-10":
        name = fields.get("Name", "")
        title = text.splitlines()[0] if text else ""
        if "G-02" not in name or "Experience" in name or "Enablement" in name:
            errors.append("PD-10 name must be held open under G-02")
        if "Experience" in title or "Enablement" in title:
            errors.append("PD-10 title declares a name")

    found = sections(text)
    if not found:
        errors.append("no sections")
    classes: Dict[str, int] = {c: 0 for c in CLASSES}
    dimensions = set()
    for section in found:
        where = f"{section['id']}"
        if section["class"] not in CLASSES:
            errors.append(f"{where}: class {section['class']!r} not in the v1.1 §10 vocabulary")
            continue
        classes[section["class"]] = classes.get(section["class"], 0) + 1
        if section["dimension"] in DIMENSIONS:
            dimensions.add(section["dimension"])
        elif section["dimension"] != NO_DIMENSION:
            errors.append(f"{where}: dimension {section['dimension']!r} unknown")
        sources = [c for c in section["citations"] if c[0] == "Source"]
        for kind, path, anchor in section["citations"]:
            if kind == "Source" and path.startswith(NOT_SOURCE):
                errors.append(f"{where}: {path} is roadmap or derived material, not source")
            if not po._contains(_read(root, path), anchor):
                errors.append(f"{where}: {kind} not found in {path}: {anchor[:60]!r}")
        if section["class"] == SOURCE_DERIVED and not sources:
            errors.append(f"{where}: SOURCE-DERIVED without a Source")
        if section["class"] == RESERVED and not section["reserved"]:
            errors.append(f"{where}: RESERVED-DECISION names no reservation")
        if section["class"] == UNKNOWN and not section["unknown"]:
            errors.append(f"{where}: UNKNOWN states nothing unknown")
        for reservation in section["reserved"]:
            if reservation not in known:
                errors.append(f"{where}: reservation {reservation} is not recorded anywhere")
            elif not known.get(reservation, {}).get("recorded"):
                errors.append(f"{where}: reservation {reservation} no longer recorded in its source")

    missing = [d for d in DIMENSIONS if d not in dimensions]
    if missing:
        errors.append(f"dimensions missing: {', '.join(missing)}")

    for pattern, meaning in FORBIDDEN:
        for match in re.finditer(pattern, text):
            errors.append(f"forbidden assertion: {meaning}: {match.group(0)!r}")

    copied = [line for line in (" ".join(po._normalised(l).split()) for l in text.splitlines())
              if line in pd01]
    if copied:
        errors.append(f"{len(copied)} line(s) copied from frozen PD-01, e.g. {copied[0][:60]!r}")

    recorded = manifest.get("volumes", {}).get(cpid, {}).get("sha256")
    actual = _sha(root / relative)
    if recorded != actual:
        errors.append(f"bytes do not match the manifest ({(recorded or 'none')[:12]} ≠ {actual[:12]})")

    return {"cpid": cpid, "path": relative, "present": True, "sha256": actual,
            "sections": len(found), "classes": classes,
            "dimensions": sorted(dimensions, key=DIMENSIONS.index),
            "reserved": sorted({r for s in found for r in s["reserved"]}),
            "errors": errors, "passes": not errors}


def verify(root: Path = REPO_ROOT) -> dict:
    known = reservations(root)
    pd01 = _pd01_lines(root)
    try:
        manifest = json.loads(_read(root, MANIFEST) or "{}")
    except ValueError:
        manifest = {}
    try:
        canonical_manifest = json.loads(_read(root, CANONICAL_MANIFEST) or "{}")
    except ValueError:
        canonical_manifest = {}
    closed = closing_decisions(root)
    canonical = bool(closed.get(CANONICALIZING_ITEM))
    volumes = {cpid: verify_volume(root, cpid, known, pd01, manifest, closed, canonical_manifest)
               for cpid in VOLUMES}
    resident = [str(p.relative_to(root)) for p in sorted(root.glob("docs/architecture/volume-*/pd-*"))
                if re.search(r"pd-(0[5-9]|10)", p.name)]
    errors = [f"{c}: {e}" for c, v in volumes.items() for e in v["errors"]]
    if resident:
        errors.append(f"construction placed in a resident-corpus namespace: {resident}")
    reconciliation = reconcile(root)
    errors += [f"reconciliation: {c['check']}: {c['detail']}"
               for c in reconciliation["checks"] if not c["passes"]]
    return {
        "volumes": volumes,
        "reconciliation": reconciliation,
        "passes": not errors,
        "errors": errors,
        "state": {c: ((CANONICAL_STATE if canonical else "CONSTRUCTED — VERIFIED") if v["passes"] else
                      "CONSTRUCTED — FAILS VERIFICATION" if v["present"] else "NOT CONSTRUCTED")
                  for c, v in volumes.items()},
        "closing_decisions": closed,
        "certifies": False,
        "canonical": canonical,
        "grants_authority": False,
    }


def reconcile(root: Path = REPO_ROOT) -> dict:
    """Cross-division checks over the constructed volumes (v1.1 `§21`)."""
    texts = {cpid: _read(root, path) for cpid, path in VOLUMES.items()}
    found = {cpid: {s["id"]: s for s in sections(text)} for cpid, text in texts.items() if text}
    checks: List[dict] = []

    def check(name: str, ok: bool, detail: str) -> None:
        checks.append({"check": name, "passes": ok, "detail": detail})

    for (cpid, section), reservation in BINDINGS.items():
        entry = found.get(cpid, {}).get(section)
        ok = bool(entry) and entry["class"] == RESERVED and reservation in entry["reserved"]
        check("reserved binding kept reserved", ok, f"{cpid} {section} ↔ {reservation}")

    for edge, cpid in EDGES.items():
        text = texts.get(cpid) or ""
        ok = f"`{edge}`" in text and "interface undefined" in text
        check("declared edge carried as undefined", ok, f"{edge} in {cpid}")

    anchors: Dict[str, str] = {}
    for cpid, entries in found.items():
        for entry in entries.values():
            if entry["dimension"] != "Ownership" or entry["class"] != SOURCE_DERIVED:
                continue
            own = OWNERSHIP_STATEMENTS.get(cpid)
            cited = [a for k, _, a in entry["citations"] if k == "Source"]
            ok = (own in cited) if own else po._contains(entry["body"], "not stated")
            check("ownership sourced to its own statement", ok, f"{cpid} {entry['id']}")
            for other, statement in OWNERSHIP_STATEMENTS.items():
                if other != cpid and statement in cited:
                    check("no ownership collision", False, f"{cpid} cites {other}'s ownership")
            if own:
                anchors[own] = cpid
    check("every prose ownership statement carried by its own volume",
          set(anchors) == set(OWNERSHIP_STATEMENTS.values()),
          f"{len(anchors)} of {len(OWNERSHIP_STATEMENTS)}")

    return {"checks": checks, "passes": all(c["passes"] for c in checks)}


CANONICAL_STATE = "CANONICAL BASELINE — VERIFIED"


def write_canonical_manifest(commit: str, root: Path = REPO_ROOT) -> dict:
    """Record the certified sections. Used once, when `FD-PO-004` D1-A is
    applied; never by `verify`."""
    data = {
        "nature": "canonical construction baseline: CERTIFIED WITH CLASSIFIED RESIDUAL; "
                  "NOT FROZEN, NOT ACTIVATED",
        "decision": "FD-PO-004 D1-A",
        "sections_verified_at": commit,
        "volumes": {},
    }
    for cpid, path in VOLUMES.items():
        text = _read(root, path) or ""
        data["volumes"][cpid] = {
            "path": path,
            "sections_sha256": hashlib.sha256(section_text(text).encode("utf-8")).hexdigest(),
            "classes": [[x["id"], x["class"]] for x in sections(text)],
        }
    (root / CANONICAL_MANIFEST).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                                           encoding="utf-8")
    return data


def write_manifest(root: Path = REPO_ROOT) -> dict:
    """Record the volumes' bytes. Used by the constructor, never by `verify`."""
    data = {
        "nature": "construction manifest: NOT CANONICAL, NOT FROZEN, NOT ACTIVATED",
        "authority": "ACT-CC-POST-P13-PLATFORM-ORG-003 v1.1, authorized by FD-PO-003-01",
        "volumes": {cpid: {"path": path, "sha256": _sha(root / path)}
                    for cpid, path in VOLUMES.items() if (root / path).exists()},
    }
    (root / MANIFEST).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                                 encoding="utf-8")
    return data


def main() -> int:
    import sys
    if sys.argv[1:2] == ["--write-canonical-manifest"] and len(sys.argv) == 3:
        print(json.dumps(write_canonical_manifest(sys.argv[2]), indent=2, ensure_ascii=False))
        return 0
    if sys.argv[1:] == ["--write-manifest"]:
        print(json.dumps(write_manifest(), indent=2, ensure_ascii=False))
        return 0
    report = verify()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passes"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
