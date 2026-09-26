"""The Platform Organization status registry and completion gate.

Built under `ACT-CC-POST-P13-PLATFORM-ORG-001` (`§32`–`§35`, `§46`, `§57`).
**Read-only.** It reads the certified Platform Organization corpus (the P10
root), the two resident volumes, the Decision Register and the governance
machinery. It never writes, and it grants, certifies, closes and canonicalizes
nothing: every report carries `certifies`, `grants_authority` and
`canonical` as False.

**What it computes, each run, from the resident sources:**

- the ten divisions and their identities (`G1`, `G2`);
- a per-division matrix over the Act's eleven dimensions (`§31`), each cell
  with its status and source;
- each division's `§33` state, by the rule in `division_state()`;
- the open reserved items, each checked still to be recorded where it is
  recorded, and closed only by a registered decision of the right holder;
- the cross-division ownership, authority, dependency and interface maps,
  with ownership conflicts detected (`§24`);
- the gate `G1`–`G14` and the `§57` outcome.

**The rule that governs everything else (`§22`, `§35`):** a cell the evidence
does not support stays as it is (ABSENT, MODEL-LEVEL ONLY, and so on), and a
division reaches COMPLETE only through an authoritative completion contract.
For a division, that contract is a resident corpus whose bytes verify,
frozen and activated by registered Founder decisions. No text a division
record states about itself (its "Maturity" line, a status label) can raise
its state. So the certified corpus can only report on the state here, never
decide it.

**Why the dimension matrix for `PD-03`…`PD-10` is mapped, not read.** The
certified Evidence Ledger (`§2`) measures twelve dimensions per division. The
Act names eleven. The mapping in `_LEDGER_MAP` is derived here and declared,
not taken from a source. Where the Ledger has no dimension (Operation,
Performance), the division-level status is MODEL-LEVEL ONLY. The P10 model
layer answers those dimensions for every division, but it *"assigns nothing"*
to any one of them.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

PO_ROOT = "docs/architecture/platform-organization"
DIVISIONS_DIR = f"{PO_ROOT}/divisions"
LEDGER = f"{PO_ROOT}/EVIDENCE-LEDGER.md"
VOLUME_MATRIX = f"{PO_ROOT}/VOLUME-SECTION-STATUS-MATRIX.md"
GAP_MAP = f"{PO_ROOT}/SYSTEMIC-GAP-MAP.md"
MASTER_MAP = f"{PO_ROOT}/PLATFORM-ORGANIZATION-MASTER-MAP.md"
INTERFACE_REGISTRY = f"{PO_ROOT}/CROSS-PD-INTERFACE-REGISTRY.md"
POST_P10 = f"{PO_ROOT}/POST-P10-TRANSITION-REGISTER.md"
ACTIVATION_MODEL = "docs/governance/AIOS_VOLUME_ACTIVATION_MODEL_v1.0.md"
REGISTER = "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
LINEAGE = "docs/governance/platform-organization/PD-01-VOLUME-1-BODY-LINEAGE.json"
P7_I99_RESULT = "docs/governance/AIOS_PD01_P7_I99_REVIEW_RESULT_v1.0.md"
VOLUME_1 = "docs/architecture/volume-1/pd-01-executive-office"
VOLUME_2 = "docs/architecture/volume-2/pd-02-architecture-office"
VOLUME_2_MANIFEST = f"{VOLUME_2}/RESIDENCY-MANIFEST.md"

CPIDS = tuple(f"PD-{n:02d}" for n in range(1, 11))
DIMENSIONS = ("Identity", "Authority", "Ownership", "Capability", "Architecture",
              "Operation", "Performance", "Lifecycle", "Integration", "Evolution",
              "Evidence")

# Cell statuses.
EVIDENCED = "EVIDENCED"
PARTIAL = "PARTIAL"
DECLARED = "DECLARED — interface undefined"
MODEL_LEVEL = "MODEL-LEVEL ONLY"
ABSENT = "ABSENT"
CLASSIFIED = "CLASSIFIED UNRESOLVED"
TRACED = "TRACED"
CONTESTED = "CONTESTED"

# `§33` states.
COMPLETE = "COMPLETE"
COMPLETE_RESIDUAL = "COMPLETE WITH CLASSIFIED RESIDUAL"
INCOMPLETE = "INCOMPLETE"
BLOCKED = "BLOCKED"
FOUNDER_DECISION = "REQUIRES FOUNDER DECISION"
ARCHITECT_DECISION = "REQUIRES ARCHITECT DECISION"
UNKNOWN = "UNKNOWN"
CONFLICTED = "CONFLICTED"

# Holders.
FOUNDER = "FOUNDER"
ARCHITECT = "ARCHITECT"
FOUNDER_OR_ARCHITECT = "FOUNDER / ARCHITECT"

# `§57` outcomes.
OUTCOME_A = "A. PLATFORM ORGANIZATION COMPLETE"
OUTCOME_B = "B. PLATFORM ORGANIZATION COMPLETE WITH CLASSIFIED NON-BLOCKING RESIDUALS"
OUTCOME_C = "C. PLATFORM ORGANIZATION NOT COMPLETE WITH EXPLICIT BLOCKERS"
OUTCOME_D = "D. FOUNDER / ARCHITECT DECISION REQUIRED"
OUTCOME_E = "E. CONSTRUCTION BLOCKED"

PASS = "PASS"
FAIL = "FAIL"
PARTIAL_GATE = "PARTIAL"


@dataclass(frozen=True)
class OpenItem:
    """A reserved or supply matter that holds a division back.

    `anchor` must still be found in `source`: an item whose record has
    disappeared is reported as such, never silently dropped. It closes only
    by a registered decision of `holder` whose entry names it under
    **Closes** (`_closing_decision`).
    """
    identifier: str
    holder: str
    divisions: Tuple[str, ...]
    matter: str
    source: str
    anchor: str
    blocking: bool
    basis: str


ALL = CPIDS

#: Every item is recorded in a resident source, named here with the text that
#: records it. `blocking` follows the source: `SYSTEMIC-GAP-MAP` names G-01
#: alone as *"Blocking a canonical Platform Organization baseline"*, so G-06
#: and G-07 are not blocking.
OPEN_ITEMS: Tuple[OpenItem, ...] = (
    OpenItem("ESC-C7-01", FOUNDER, ("PD-03", "PD-04"),
             "the PD-03 and PD-04 canonical volumes exist and are verified, and are not "
             "resident: authorize their residency", VOLUME_MATRIX, "`ESC-C7-01`", True,
             "Founder supply (VOLUME-SECTION-STATUS-MATRIX §5)"),
    OpenItem("G-01", FOUNDER, ("PD-05", "PD-06", "PD-07", "PD-08", "PD-09", "PD-10"),
             "no definitional corpus exists for PD-05 … PD-10: supply it", GAP_MAP,
             "## G-01 — Eight platform divisions have no definitional corpus", True,
             "Founder supply (SYSTEMIC-GAP-MAP, Summary)"),
    OpenItem("G-02", FOUNDER_OR_ARCHITECT, ("PD-10",),
             "PD-10 carries two names in resident sources: Developer Experience and "
             "Developer Enablement", GAP_MAP, "## G-02 —", False,
             "SYSTEMIC-GAP-MAP G-02: Blocking NO. Holder: the gap map says Founder "
             "(which source governs naming); DIVISION-LIFECYCLE-AND-AUTHORITY-MODEL says "
             "renaming a division is architect approval (Domain Model §6)"),
    OpenItem("FDP-P10-001", FOUNDER, ("PD-08",),
             "bind the Security Owner role to PD-08, or record non-binding (G-03)",
             POST_P10, "**`FDP-P10-001`**", False,
             "FD-P10-005 §4: open after certification. Not blocking: SYSTEMIC-GAP-MAP "
             "G-03 Blocking NO; the Founder's P12 policy D2 = CONDITIONAL-BLOCKING "
             "(only work with a proven direct dependency stops)"),
    OpenItem("FDP-P10-002", FOUNDER, ("PD-09",),
             "bind the Quality Authority to PD-09, or record non-binding", POST_P10,
             "**`FDP-P10-002`**", False,
             "FD-P10-005 §4. Not blocking: G-03 extends to PD-09, Blocking NO"),
    OpenItem("FDP-P10-003", FOUNDER, ("PD-03",),
             "Governance Authority binding; activation reserved", POST_P10,
             "**`FDP-P10-003`**", False,
             "FD-P10-005 §4. Not blocking: POST-P10 Gate D, P10 relevance NONE; the "
             "Founder's P12 policy D3 = CONDITIONAL-BLOCKING"),
    OpenItem("ADP-P10-001", ARCHITECT, ALL,
             "ADR-0029 (Proposed): Department ≠ PD as entity type or population; until it "
             "is decided, INV-10 exposure of the declared edges cannot be evaluated",
             POST_P10, "**`ADP-P10-001`**", False,
             "Domain Model semantics: REG-CFV2-001 C-2 excludes it from the CEO's A05. It "
             "holds cross-division interface evaluation (G14), not a division's own "
             "construction (POST-P10-TRANSITION-REGISTER Gate D: P10 relevance NONE)"),
    OpenItem("C6-A1", ARCHITECT, ALL,
             "division volume structure: the A–E spine or Parts A–H", VOLUME_MATRIX,
             "**`C6-A1`**", False,
             "cross-division structure: REG-CFV2-001 C-3 excludes it from the CEO's A05"),
    OpenItem("G-10", ARCHITECT, ("PD-01",),
             "PD-01 assigns Capability ownership to Sub Divisions: internal structure, "
             "or a fourth Spine level", GAP_MAP, "## G-10 —", True,
             "Domain Model §8: REG-CFV2-001 C-2. The source states no blocking "
             "classification; held as blocking for PD-01, the reference pattern, as the "
             "conservative reading"),
    OpenItem("P7-I99", FOUNDER, ("PD-01",),
             "PD-01's integrated review under the adopted R1–R11 contract ran: RESULT B — "
             "NOT ELIGIBLE (R11 NOT APPROVED; G-10, FN-1). A re-run needs a new Founder "
             "invocation", P7_I99_RESULT, "P7-I99 VOLUME 1 / PD-01 RESULT B — NOT ELIGIBLE",
             True, "DEL-F03-015-P7I99-001 invoked by FD-PO-003-01; exclusion 8 (no "
             "self-invocation). Evidence only: no freeze, no activation"),
    OpenItem("FN-1", FOUNDER, ("PD-01",),
             "PD-01 exercises Enterprise Governance Authority; PD-03's Governance Authority "
             "is not resident and unbound: the boundary cannot be assessed (P7-I99 R5)",
             P7_I99_RESULT, "**FN-1:**", True,
             "P7-I99 R5 BLOCKED. Assessable once ESC-C7-01 or FDP-P10-003 is decided"),
    OpenItem("RG-1", FOUNDER, ("PD-01",),
             "PD-01 activation: the conditions beyond Freeze and the activation "
             "authorization are Founder-reserved (AG-08, AG-10)", ACTIVATION_MODEL,
             "**RG-1**", True, "ACT-CC-F03-014 §3"),
    OpenItem("G-06", FOUNDER, ALL,
             "Volumes 0, 0.1, 0.2 and 0.3 are referenced and not resident", GAP_MAP,
             "## G-06 —", False, "Founder supply; not blocking (SYSTEMIC-GAP-MAP Summary)"),
    OpenItem("G-07", FOUNDER, ALL,
             "the canonical Master Map, Platform Encyclopedia and gap inventory are "
             "referenced and not resident", GAP_MAP, "## G-07 —", False,
             "Founder supply; not blocking (SYSTEMIC-GAP-MAP Summary)"),
)

#: Authority claims, each with the text that states it and where.
AUTHORITY_CLAIMS = (
    ("PD-02", "Architecture Authority", f"{VOLUME_2}/A1.md",
     "Platform Authority: Architecture Authority", "RESIDENT (frozen)"),
    ("PD-03", "Governance Authority", VOLUME_MATRIX,
     "`Platform Authority: Governance Authority`", "NOT RESIDENT (ESC-C7-01)"),
    ("PD-04", "Knowledge Authority", VOLUME_MATRIX,
     "`Platform Authority: Knowledge Authority`", "NOT RESIDENT (ESC-C7-01)"),
)

#: Ledger `§2` (twelve dimensions) → the Act's dimensions. Derived and declared.
_LEDGER_MAP = {
    "Identity": ("Identity",),
    "Authority": ("Authority",),
    "Ownership": ("Ownership",),
    "Capability": ("Capability",),
    "Architecture": ("Organization", "Boundary"),
    "Lifecycle": ("Lifecycle",),
    "Integration": ("Interface", "Dependency"),
    "Evolution": ("Change Control",),
}
_SYMBOL = {"◆": EVIDENCED, "◐": PARTIAL, "○": ABSENT}
_OWNERSHIP = re.compile(r"\b(PD-\d{2}) (?:owns|tetap memiliki ownership atas) ([A-Za-z]+)")
_NOT_OBJECTS = {"none", "it", "its", "the", "a", "an"}


# ─── reading ────────────────────────────────────────────────────────────────

def _read(root: Path, relative: str) -> Optional[str]:
    try:
        return (root / relative).read_text(encoding="utf-8")
    except OSError:
        return None


def _contains(text: Optional[str], anchor: str) -> bool:
    """Whether `anchor` is in `text`, whitespace collapsed: sources wrap lines."""
    if text is None:
        return False
    return " ".join(anchor.split()) in " ".join(text.split())


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _division_files(root: Path) -> Dict[str, Path]:
    found = {}
    for path in sorted((root / DIVISIONS_DIR).glob("PD-*.md")):
        match = re.match(r"(PD-\d{2})-", path.name)
        if match:
            found.setdefault(match.group(1), path)
    return found


def _header(text: str, field: str) -> Optional[str]:
    match = re.search(r"^\| \*\*" + re.escape(field) + r"\*\* \| (.+?) \|\s*$", text, re.M)
    return match.group(1).strip() if match else None


def divisions(root: Path = REPO_ROOT) -> Dict[str, dict]:
    """The division records, as they state themselves (`G1`, `G2`)."""
    out = {}
    for cpid, path in _division_files(root).items():
        text = path.read_text(encoding="utf-8")
        established = text.split("## 1. Established", 1)
        established = established[1].split("\n## ", 1)[0] if len(established) > 1 else ""
        status = re.search(r"\*\*Status: ([A-Z][A-Z -]*[A-Z])", text)
        out[cpid] = {
            "record": path.relative_to(root).as_posix(),
            "cpid": (_header(text, "CPID") or "").startswith(f"`{cpid}`"),
            "name": _header(text, "Established name"),
            "maturity": _header(text, "Maturity"),
            "declared_status": status.group(1) if status else None,
            "ownership_claims": tuple(
                (m.group(1), m.group(2)) for m in _OWNERSHIP.finditer(established)
                if m.group(2).lower() not in _NOT_OBJECTS),
        }
    return out


def ledger_matrix(root: Path = REPO_ROOT) -> Dict[str, Dict[str, str]]:
    """The certified Evidence Ledger `§2` table, cell by cell."""
    text = _read(root, LEDGER) or ""
    section = text.split("## 2. Per-PD evidence baseline", 1)
    if len(section) < 2:
        return {}
    lines = [l for l in section[1].split("\n## ", 1)[0].splitlines() if l.startswith("|")]
    header = next((l for l in lines if l.startswith("| Dimension |")), None)
    if header is None:
        return {}
    columns = [c.strip() for c in header.strip("|").split("|")][1:]
    matrix: Dict[str, Dict[str, str]] = {c: {} for c in columns}
    for line in lines:
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells[0] in ("Dimension", "---") or cells[0].startswith("**") or set(cells[0]) <= {"-"}:
            continue
        for column, cell in zip(columns, cells[1:]):
            if cell in _SYMBOL:
                matrix[column][cells[0]] = _SYMBOL[cell]
    return matrix


def _manifest_rows(text: str) -> Dict[str, str]:
    """`section → sha256` from either resident volume manifest."""
    rows = {m.group(1): m.group(2) for m in re.finditer(
        r"^\| `?([A-E]\d+)(?:\.md)?`? \|.*?`([0-9a-f]{64})`", text, re.M)}
    return rows


def volume_integrity(root: Path = REPO_ROOT) -> Dict[str, dict]:
    """Whether each resident volume's bytes are the recorded ones.

    PD-02 against its residency manifest. PD-01 against the body lineage:
    the recovery manifest records the recovered bytes, and two authorized
    changes followed (`LINEAGE`)."""
    out = {}
    manifest = _read(root, VOLUME_2_MANIFEST)
    rows = _manifest_rows(manifest or "")
    bodies = sorted((root / VOLUME_2).glob("[A-E]*.md"))
    faults = [p.name for p in bodies if rows.get(p.stem) != _sha(p)]
    out["PD-02"] = {"bodies": len(bodies), "recorded": len(rows),
                    "verified": len(bodies) - len(faults), "faults": tuple(faults),
                    "holds": bool(bodies) and len(rows) == len(bodies) and not faults,
                    "against": VOLUME_2_MANIFEST}

    recovered = _manifest_rows(_read(root, f"{VOLUME_1}/RECOVERY-MANIFEST.md") or "")
    try:
        lineage = json.loads(_read(root, LINEAGE) or "")
    except ValueError:
        lineage = {}
    entries = {b["section"]: b for b in lineage.get("bodies", ())}
    allowed = {c["act"] for c in lineage.get("changes", ())}
    bodies = sorted((root / VOLUME_1).glob("[A-E]*.md"))
    faults = []
    for path in bodies:
        entry = entries.get(path.stem)
        if entry is None or entry["current_sha256"] != _sha(path):
            faults.append(f"{path.name}: bytes differ from the lineage record")
        elif entry["recovered_sha256"] != recovered.get(path.stem):
            faults.append(f"{path.name}: recovered hash differs from the recovery manifest")
        elif (entry["recovered_sha256"] != entry["current_sha256"]
              and not (entry["changed_by"] and set(entry["changed_by"]) <= allowed)):
            faults.append(f"{path.name}: changed with no recorded authorized change")
    out["PD-01"] = {"bodies": len(bodies), "recorded": len(entries),
                    "verified": len(bodies) - len(faults), "faults": tuple(faults),
                    "holds": bool(bodies) and len(entries) == len(bodies) and not faults,
                    "against": LINEAGE}
    return out


def resident_corpora(root: Path = REPO_ROOT) -> Dict[str, Path]:
    """Any resident volume for a division other than PD-01 and PD-02."""
    found = {}
    for n in range(3, 11):
        for path in sorted((root / "docs/architecture").glob(f"volume-{n}/pd-{n:02d}-*")):
            if path.is_dir():
                found[f"PD-{n:02d}"] = path
    return found


def _normalised(text: str) -> str:
    return re.sub(r"PD-\d{2}", "PD-XX", text)


def blind_copies(root: Path = REPO_ROOT) -> Dict[str, Tuple[str, ...]]:
    """`§5`, NC-05: bodies in another division's corpus that are PD-01's with
    the CPID changed. A byte-identical or near-identical body is a copy."""
    reference = {p.name: _normalised(p.read_text(encoding="utf-8"))
                 for p in sorted((root / VOLUME_1).glob("[A-E]*.md"))}
    out = {}
    for cpid, corpus in resident_corpora(root).items():
        copies = []
        for path in sorted(corpus.glob("*.md")):
            text = _normalised(path.read_text(encoding="utf-8"))
            for name, body in reference.items():
                if text == body or difflib.SequenceMatcher(None, text, body).quick_ratio() > 0.97 \
                        and difflib.SequenceMatcher(None, text, body).ratio() > 0.95:
                    copies.append(f"{path.name} ≈ PD-01 {name}")
                    break
        if copies:
            out[cpid] = tuple(copies)
    return out


def _entry(register: str, identifier: str) -> Optional[dict]:
    """A Register entry by identifier: its heading and who decided it."""
    heading = re.search(r"^### " + re.escape(identifier) + r" — (.+)$", register, re.M)
    if heading is None:
        return None
    rest = register[heading.end():]
    following = re.search(r"^#{1,3} ", rest, re.M)
    block = register[heading.start(): heading.end() + (following.start() if following else len(rest))]
    decided = re.search(r"(?:\| \*\*Decided by\*\* \||\*\*Decided by:\*\*) ([^|\n]+)", block)
    return {"heading": heading.group(1).strip(), "block": block,
            "decided_by": decided.group(1).strip() if decided else None}


def _decided_by(entry: dict, holder: str) -> bool:
    who = (entry.get("decided_by") or "").lower()
    founder = who.startswith("founder") or who.startswith("aios founder")
    architect = who.startswith("architect")
    if holder == FOUNDER:
        return founder
    if holder == ARCHITECT:
        return architect or founder  # Founder supremacy
    return founder or architect


def _closing_decision(register: str, item: OpenItem) -> Optional[str]:
    """A registered decision of the item's holder that names it under Closes."""
    for heading in re.finditer(r"^### (\S+) — (.+)$", register, re.M):
        entry = _entry(register, heading.group(1))
        if entry is None:
            continue
        closes = re.search(r"(?:\*\*Closes:\*\*|\| \*\*Closes\*\* \|)([^\n]+)", entry["block"])
        if closes and f"`{item.identifier}`" in closes.group(1) and _decided_by(entry, item.holder):
            return heading.group(1)
    return None


def open_items(root: Path = REPO_ROOT) -> Tuple[dict, ...]:
    register = _read(root, REGISTER) or ""
    out = []
    for item in OPEN_ITEMS:
        source = _read(root, item.source)
        closed_by = _closing_decision(register, item)
        out.append({
            "id": item.identifier, "holder": item.holder, "divisions": item.divisions,
            "matter": item.matter, "blocking": item.blocking, "basis": item.basis,
            "source": item.source,
            "recorded": _contains(source, item.anchor),
            "status": f"CLOSED by {closed_by}" if closed_by else "OPEN",
        })
    return tuple(out)


def lifecycle_decisions(root: Path = REPO_ROOT) -> Dict[str, dict]:
    """The registered decisions that set PD-01's and PD-02's lifecycle states."""
    register = _read(root, REGISTER) or ""
    wanted = {
        "PD-01": {"frozen": "GDR-0017"},
        "PD-02": {"frozen": "GDR-0026", "gate": "GDR-0035", "active": "GDR-0036"},
    }
    out = {}
    for cpid, states in wanted.items():
        out[cpid] = {}
        for state, identifier in states.items():
            entry = _entry(register, identifier)
            founder = entry is not None and (state == "gate" or _decided_by(entry, FOUNDER))
            out[cpid][state] = identifier if founder else None
    return out


# ─── the matrix ─────────────────────────────────────────────────────────────

def _cell(status: str, source: str, note: str = "") -> dict:
    return {"status": status, "source": source, "note": note}


def _volume_cells(cpid: str, decisions: dict, integrity: dict) -> Dict[str, dict]:
    """PD-01 and PD-02: their frozen, resident volumes (Parts A–E)."""
    frozen = decisions.get("frozen")
    volume = VOLUME_1 if cpid == "PD-01" else VOLUME_2
    by = f"{volume}, frozen by {frozen}" if frozen else f"{volume} (no registered freeze)"
    status = EVIDENCED if frozen else PARTIAL
    cells = {
        "Identity": _cell(status, f"{by} · A1"),
        "Authority": _cell(status, f"{by} · A5, Part C"),
        "Ownership": _cell(status, f"{by} · Part B"),
        "Capability": _cell(status, f"{by} · Part B"),
        "Architecture": _cell(status, f"{by} · Parts A–E"),
        "Operation": _cell(status, f"{by} · Part D"),
        "Performance": _cell(status, f"{by} · Part E"),
        "Integration": _cell(status, f"{by} · C8"),
        "Evolution": _cell(CLASSIFIED, f"{by} · no Evolution Part",
                           "Parts A–E carry no Evolution Part; the structure question is C6-A1"),
        "Evidence": _cell(TRACED if integrity.get("holds") else PARTIAL,
                          integrity.get("against", ""),
                          f"{integrity.get('verified', 0)}/{integrity.get('bodies', 0)} bodies verified"),
    }
    if decisions.get("active"):
        cells["Lifecycle"] = _cell(EVIDENCED, f"{frozen} FROZEN · {decisions['gate']} gate PASS "
                                              f"· {decisions['active']} ACTIVE")
    else:
        cells["Lifecycle"] = _cell(PARTIAL, f"{frozen} FROZEN; {ACTIVATION_MODEL} §7.1",
                                   "frozen; not activation-eligible")
    if cpid == "PD-01":
        cells["Capability"] = _cell(PARTIAL, f"{by} · B3",
                                    "Capability ownership assigned to Sub Divisions (G-10)")
    return cells


def _ledger_cells(cpid: str, column: Dict[str, str], edges: List[dict]) -> Dict[str, dict]:
    cells = {}
    for dimension, sources in _LEDGER_MAP.items():
        values = [column.get(s, ABSENT) for s in sources]
        if all(v == EVIDENCED for v in values):
            status = EVIDENCED
        elif any(v in (EVIDENCED, PARTIAL) for v in values):
            status = PARTIAL
        else:
            status = ABSENT
        cells[dimension] = _cell(status, f"{LEDGER} §2 ({' + '.join(sources)})")
    touching = [e["id"] for e in edges if cpid in (e["from"], e["to"])]
    if cells["Integration"]["status"] == ABSENT and touching:
        cells["Integration"] = _cell(DECLARED, INTERFACE_REGISTRY, ", ".join(touching))
    for dimension, model in (("Operation", "DIVISION-OPERATION-AND-PERFORMANCE-MODEL.md"),
                             ("Performance", "DIVISION-OPERATION-AND-PERFORMANCE-MODEL.md")):
        cells[dimension] = _cell(MODEL_LEVEL, f"{PO_ROOT}/{model}",
                                 "answered for every division; assigns nothing to this one")
    if cells["Lifecycle"]["status"] == ABSENT:
        cells["Lifecycle"] = _cell(MODEL_LEVEL, f"{PO_ROOT}/DIVISION-LIFECYCLE-AND-AUTHORITY-MODEL.md",
                                   "a division's lifecycle is architect-approved; assigns nothing")
    if cells["Evolution"]["status"] == ABSENT:
        cells["Evolution"] = _cell(CLASSIFIED, f"{PO_ROOT}/DIVISION-CAPABILITY-ARCHITECTURE-EVOLUTION-MODEL.md",
                                   "no division-level change control; held by the source gap")
    cells["Evidence"] = _cell(TRACED, f"{LEDGER} §2", "every cell traces to the certified ledger")
    return {d: cells[d] for d in DIMENSIONS}


def interface_edges(root: Path = REPO_ROOT) -> List[dict]:
    text = _read(root, INTERFACE_REGISTRY) or ""
    edges = []
    for match in re.finditer(r"^\|\s*`(X-\d+)`\s*\|(.*)\|\s*$", text, re.M):
        cells = [c.strip() for c in match.group(2).split("|")]
        ends = [re.search(r"PD-\d{2}", c) for c in cells[:2]]
        if not all(ends):
            continue
        edges.append({"id": match.group(1), "from": ends[0].group(0), "to": ends[1].group(0),
                      "subject": cells[2], "interface": cells[3].strip("*"),
                      "verification": cells[-1].replace("*", "").strip()})
    return edges


def dimension_matrix(root: Path = REPO_ROOT) -> Dict[str, Dict[str, dict]]:
    ledger = ledger_matrix(root)
    decisions = lifecycle_decisions(root)
    integrity = volume_integrity(root)
    edges = interface_edges(root)
    records = divisions(root)
    matrix = {}
    for cpid in CPIDS:
        if cpid in ("PD-01", "PD-02"):
            matrix[cpid] = {d: _volume_cells(cpid, decisions[cpid], integrity[cpid])[d]
                            for d in DIMENSIONS}
        else:
            matrix[cpid] = _ledger_cells(cpid, ledger.get(cpid, {}), edges)
        if cpid in records and records[cpid]["name"] is None:
            matrix[cpid]["Identity"] = _cell(CONTESTED, records[cpid]["record"],
                                             "CPID stable; the name is contested (G-02)")
    return matrix


# ─── cross-division ─────────────────────────────────────────────────────────

def ownership_map(root: Path = REPO_ROOT) -> dict:
    claims: Dict[str, set] = {}
    stated_in: Dict[Tuple[str, str], List[str]] = {}
    for cpid, record in divisions(root).items():
        for owner, obj in record["ownership_claims"]:
            claims.setdefault(obj.lower(), set()).add(owner)
            stated_in.setdefault((owner, obj.lower()), []).append(record["record"])
    conflicts = {obj: tuple(sorted(owners)) for obj, owners in claims.items() if len(owners) > 1}
    return {"claims": {obj: tuple(sorted(o)) for obj, o in sorted(claims.items())},
            "conflicts": conflicts,
            "scope_unknown": ("implementation",) if "implementation" in claims else (),
            "stated_in": {f"{k[0]} → {k[1]}": v for k, v in sorted(stated_in.items())}}


def authority_map(root: Path = REPO_ROOT) -> Tuple[dict, ...]:
    out = []
    for cpid, authority, source, anchor, residency in AUTHORITY_CLAIMS:
        text = _read(root, source)
        out.append({"division": cpid, "authority": authority, "source": source,
                    "residency": residency, "recorded": _contains(text, anchor)})
    return tuple(out)


def coherence(root: Path, matrix: Dict[str, Dict[str, dict]], items: Tuple[dict, ...]) -> dict:
    """`G14` and the `§34` reconciliation: PASS needs every declared interface
    defined and verified, no ownership conflict, and no open conflict item."""
    edges = interface_edges(root)
    owners = ownership_map(root)
    defined = [e for e in edges if "not declared" not in e["interface"]]
    reasons = []
    if len(defined) < len(edges):
        reasons.append(f"{len(edges) - len(defined)} of {len(edges)} declared edges have no "
                       "defined interface; none is verified")
    if owners["conflicts"]:
        reasons.append(f"ownership conflicts: {owners['conflicts']}")
    for item in items:
        if item["status"] == "OPEN" and item["id"] in ("G-02", "ADP-P10-001"):
            reasons.append(f"{item['id']} open: {item['matter']}")
    silent = [c for c in CPIDS if not any(c in (e["from"], e["to"]) for e in edges)]
    if silent:
        reasons.append(f"divisions in no declared edge: {', '.join(silent)}")
    return {"result": PASS if not reasons else "NOT PASS", "reasons": tuple(reasons),
            "edges": edges, "interfaces_defined": len(defined), "interfaces_verified": 0}


# ─── states and the gate ────────────────────────────────────────────────────

def division_state(cpid: str, cells: Dict[str, dict], items: Tuple[dict, ...],
                   decisions: Dict[str, dict], integrity: Dict[str, dict],
                   resident: Dict[str, Path], copies: Dict[str, tuple],
                   conflicts: dict) -> dict:
    """The `§33` state of one division.

    COMPLETE needs the authoritative contract: a resident corpus that
    verifies, frozen and activated by registered Founder decisions. Open items
    then make it COMPLETE WITH CLASSIFIED RESIDUAL, because an open item that
    does not name the division's contract does not reopen a Founder-decided
    state. Short of that contract, the state is what holds the division back.
    Never COMPLETE from a record's own text."""
    mine = [i for i in items if cpid in i["divisions"] and i["status"] == "OPEN"]
    reasons, also = [], []
    conflicted = []
    if cpid in copies:
        conflicted.append(f"blind copy of PD-01: {', '.join(copies[cpid])}")
    if cpid in integrity and not integrity[cpid]["holds"]:
        conflicted.append(f"corpus bytes do not verify: {integrity[cpid]['faults'][:3]}")
    owned = [obj for obj, owners in conflicts.items() if cpid in owners]
    if owned:
        conflicted.append(f"ownership claimed by more than one division: {owned}")
    if any(i["id"] == "G-02" for i in mine):
        also.append(CONFLICTED)
    lifecycle = decisions.get(cpid, {})
    if conflicted:
        state, reasons = CONFLICTED, conflicted
    elif lifecycle.get("frozen") and lifecycle.get("active") and integrity.get(cpid, {}).get("holds"):
        state = COMPLETE_RESIDUAL if mine else COMPLETE
        reasons = [f"frozen {lifecycle['frozen']} · gate {lifecycle.get('gate')} · active "
                   f"{lifecycle.get('active')}; {integrity[cpid]['verified']} bodies verify"]
    elif cpid in resident:
        state = UNKNOWN
        reasons = [f"a resident corpus is present ({resident[cpid].as_posix()}) and has not "
                   "been assessed; residency is not completion"]
    elif not mine:
        state = INCOMPLETE
        reasons = ["no open reserved item holds it: constructible work would remain"]
    else:
        blocking = [i for i in mine if i["blocking"]]
        supply = [i for i in blocking if i["id"] == "G-01"]
        founder = [i for i in blocking if i["holder"] in (FOUNDER, FOUNDER_OR_ARCHITECT)
                   and i["id"] != "G-01"]
        architect = [i for i in blocking if i["holder"] == ARCHITECT]
        if supply:
            state = BLOCKED
        elif founder:
            state = FOUNDER_DECISION
        elif architect:
            state = ARCHITECT_DECISION
        else:
            state = FOUNDER_DECISION if blocking else INCOMPLETE
        reasons = [f"{i['id']} ({i['holder']}): {i['matter']}" for i in blocking]
        if state != FOUNDER_DECISION and founder:
            also.append(FOUNDER_DECISION)
        if state != ARCHITECT_DECISION and architect:
            also.append(ARCHITECT_DECISION)
    residual = [i["id"] for i in mine if state in (COMPLETE_RESIDUAL,) or not i["blocking"]]
    return {"state": state, "also": tuple(dict.fromkeys(also)), "reasons": tuple(reasons),
            "residual": tuple(residual),
            "absent_dimensions": tuple(d for d, c in cells.items() if c["status"] == ABSENT)}


def _governance(root: Path) -> dict:
    """The invariants this Act must not disturb: NC-01 … NC-04, NC-15."""
    from tools import certified_evidence_integrity as integrity
    from tools import p13_fresh_verification as fresh
    try:
        report = fresh.post_closure(root)
        failing = [i["state"] for i in report["items"] if i["status"] != fresh.PASS]
        failing += [c["id"] for c in report["fresh_verification"]["checks"]
                    if c["status"] != fresh.PASS]
        holds = bool(report["holds"])
    except Exception as error:  # reported, never assumed
        failing, holds = [f"UNDETERMINABLE: {error}"], False
    try:
        root_holds = bool(integrity.verify(root).holds)
    except Exception as error:  # reported, never assumed
        failing, root_holds = [*failing, f"integrity UNDETERMINABLE: {error}"], False
    return {"holds": holds and root_holds, "failing": tuple(failing),
            "certified_root_holds": root_holds}


def _construction(root: Path) -> dict:
    """The PD-05 … PD-10 construction volumes (ACT-003 v1.1), reported beside the
    `§33` states and never feeding them. A volume constructed and verified is
    not a supplied canonical corpus: `G-01` stays open until its holder closes
    it, so the states above do not move."""
    from tools import platform_division_construction as construction
    report = construction.verify(root)
    return {"state": report["state"], "passes": report["passes"],
            "reconciliation_passes": report["reconciliation"]["passes"],
            "errors": report["errors"], "canonical": False}


def evaluate(root: Path = REPO_ROOT) -> dict:
    root = Path(root)
    records = divisions(root)
    matrix = dimension_matrix(root)
    items = open_items(root)
    decisions = lifecycle_decisions(root)
    integrity = volume_integrity(root)
    resident = resident_corpora(root)
    copies = blind_copies(root)
    owners = ownership_map(root)
    states = {cpid: division_state(cpid, matrix[cpid], items, decisions, integrity,
                                   resident, copies, owners["conflicts"])
              for cpid in CPIDS}
    cross = coherence(root, matrix, items)
    governance = _governance(root)

    def all_cells(dimension, ok):
        return all(ok(matrix[c][dimension]["status"]) for c in CPIDS)

    population_ok = set(records) == set(CPIDS) and all(r["cpid"] for r in records.values())
    extra = sorted(set(records) - set(CPIDS))
    canonical_claims = sorted(c for c, r in records.items() if r["declared_status"] not in ("DERIVED",))
    missing_records = [i["id"] for i in items if not i["recorded"]]
    ev = lambda s: s == EVIDENCED  # noqa: E731
    gate = [
        ("G1", "Scope", PASS if population_ok and not extra else FAIL,
         f"divisions: {sorted(records)}" + (f"; unauthorized: {extra}" if extra else "")),
        ("G2", "Identity", PASS if all_cells("Identity", ev) else PARTIAL_GATE
         if all_cells("Identity", lambda s: s in (EVIDENCED, CONTESTED)) else FAIL,
         "every CPID stable" + ("; PD-10 name contested (G-02)"
                                if matrix["PD-10"]["Identity"]["status"] == CONTESTED else "")),
    ]
    for gid, dimension in (("G3", "Authority"), ("G4", "Ownership"), ("G5", "Capability"),
                           ("G6", "Architecture"), ("G7", "Operation"), ("G8", "Performance"),
                           ("G9", "Lifecycle")):
        missing = [c for c in CPIDS if matrix[c][dimension]["status"] != EVIDENCED]
        status = PASS if not missing else PARTIAL_GATE if len(missing) < len(CPIDS) else FAIL
        gate.append((gid, dimension, status,
                     "evidenced for every division" if not missing else
                     f"not evidenced for {', '.join(missing)}"))
    gate.append(("G10", "Integration", PASS if cross["interfaces_defined"] == len(cross["edges"])
                 and cross["edges"] else FAIL,
                 f"{len(cross['edges'])} declared edges; {cross['interfaces_defined']} with a "
                 f"defined interface; {cross['interfaces_verified']} verified"))
    unclassified = [c for c in CPIDS if matrix[c]["Evolution"]["status"] not in (EVIDENCED, CLASSIFIED)]
    gate.append(("G11", "Evolution", PASS if not unclassified else FAIL,
                 "each division has an evolution model or a classified unresolved area"
                 if not unclassified else f"unclassified: {unclassified}"))
    bindings_open = [i["id"] for i in items if i["id"].startswith("FDP-") and i["status"] == "OPEN"]
    governance_ok = governance["holds"] and not owners["conflicts"] and not canonical_claims
    gate.append(("G12", "Governance", PARTIAL_GATE if governance_ok and bindings_open else
                 PASS if governance_ok else FAIL,
                 "consistent; authority bindings open: " + ", ".join(bindings_open)
                 if governance_ok else
                 f"governance invariants {governance['failing']}; ownership conflicts "
                 f"{owners['conflicts']}; unauthorized canonical claims {canonical_claims}"))
    traced = all(matrix[c]["Evidence"]["status"] == TRACED for c in CPIDS)
    gate.append(("G13", "Evidence", PASS if traced and not missing_records else PARTIAL_GATE,
                 "every cell cites a resident source" + (
                     f"; items whose record is gone: {missing_records}" if missing_records else "")))
    gate.append(("G14", "Cross-PD coherence", cross["result"] if cross["result"] == PASS else FAIL,
                 "; ".join(cross["reasons"]) or "coherent"))
    gate_passes = all(g[2] == PASS for g in gate)

    done = {COMPLETE, COMPLETE_RESIDUAL}
    not_done = [c for c in CPIDS if states[c]["state"] not in done]
    if not governance["holds"] or any(states[c]["state"] == CONFLICTED for c in CPIDS):
        outcome = OUTCOME_E
    elif not not_done and cross["result"] == PASS and gate_passes:
        outcome = OUTCOME_A if all(states[c]["state"] == COMPLETE for c in CPIDS) else OUTCOME_B
    elif any(states[c]["state"] in (INCOMPLETE, UNKNOWN) for c in not_done):
        outcome = OUTCOME_C
    else:
        outcome = OUTCOME_D
    return {
        "act": "ACT-CC-POST-P13-PLATFORM-ORG-001",
        "divisions": {c: {"name": records.get(c, {}).get("name"),
                          "record": records.get(c, {}).get("record"),
                          "declared_maturity": records.get(c, {}).get("maturity"),
                          **states[c], "dimensions": matrix[c]} for c in CPIDS},
        "open_items": items,
        "ownership": owners,
        "authority": authority_map(root),
        "coherence": cross,
        "volume_integrity": integrity,
        "governance": governance,
        "gate": tuple({"id": g[0], "dimension": g[1], "status": g[2], "evidence": g[3]}
                      for g in gate),
        "gate_passes": gate_passes,
        "outcome": outcome,
        "construction": _construction(root),
        "certifies": False,
        "grants_authority": False,
        "canonical": False,
        "statement": ("Evaluation only. It certifies, closes, canonicalizes and authorizes "
                      "nothing. A state here is computed from resident evidence; it is not "
                      "a decision."),
    }


def main() -> int:
    report = evaluate()
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    return 0 if report["outcome"] in (OUTCOME_A, OUTCOME_B) else 1


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
