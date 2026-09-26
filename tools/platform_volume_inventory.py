"""Identity and inventory of the received Volumes 3 and 4 (`ACT-CC-POST-P13-PLATFORM-ORG-004` §7, §9).

**Read-only.** Everything is read from the resident bodies, never from file
names (§7: *"Do not infer identity solely from filename"*):

- identity comes from each volume's own A1 header;
- the inventory lists each Part as actually present (§9: *"does not impose
  A–H"*, *"does not normalize the structure"*):
  - the section identifiers found;
  - how many times each section opens with a heading of its own;
  - its most frequent title, and how many title variants it has;
  - the statuses and source-fidelity modes each Part declares.

A section missing from a Part is reported missing; nothing is filled in (§5).
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path
from typing import Dict

from tools import platform_organization_gate as po

REPO_ROOT = po.REPO_ROOT
IDENTITY_FIELDS = ("Platform ID", "Official Name", "Platform Name", "Platform Authority",
                   "Volume", "Document Type", "Version", "Status")
_STATUS = re.compile(r"\*\*Status:\*\*\s*_?([^\n_]+?)_?\s*$", re.M)
_FIDELITY = re.compile(r"\*\*Source-Fidelity Mode:\*\*\s*([^\n]+?)\s*$", re.M)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\\", "")


def identity(directory: Path) -> Dict[str, str]:
    """The fields a volume's A1 header declares, first occurrence each."""
    part_a = sorted(directory.glob("*Part_A.md"))
    if not part_a:
        return {}
    head = _text(part_a[0])[:6000]
    out = {}
    for field in IDENTITY_FIELDS:
        match = re.search(rf"\*\*{re.escape(field)}:\*\*\s*([^\n]+?)\s*$", head, re.M)
        if match:
            out[field] = match.group(1).strip(" *_")
    return out


def inventory(directory: Path) -> Dict[str, dict]:
    out = {}
    for path in sorted(directory.glob("*Part_*.md")):
        part = re.search(r"Part_([A-Z])\.md$", path.name).group(1)
        text = _text(path)
        sections = {}
        for n in range(1, 100):
            sid = f"{part}{n}"
            titles = [" ".join(t.split()).strip(" ;.*_")
                      for t in re.findall(rf"(?<![A-Za-z0-9]){sid} — ([^\n|*]+)", text)]
            titles = [t for t in titles if 0 < len(t) <= 80 and " — " not in t]
            if not titles:
                if n > 10:
                    break
                sections[sid] = {"present": False}
                continue
            counts = collections.Counter(titles)
            openings = len(re.findall(rf"^#+\s*{sid}\s*[—–-]", text, re.M))
            sections[sid] = {"present": True, "title": counts.most_common(1)[0][0],
                             "title_variants": len(counts), "heading_openings": openings}
        out[part] = {
            "file": path.name,
            "sections_present": [s for s, v in sections.items() if v["present"]],
            "sections_missing": [s for s, v in sections.items() if not v["present"]],
            "sections": sections,
            "declared_statuses": dict(collections.Counter(
                s.strip() for s in _STATUS.findall(text)).most_common(8)),
            "source_fidelity_modes": dict(collections.Counter(
                s.strip(" *_") for s in _FIDELITY.findall(text)).most_common(6)),
        }
    return out


def report(root: Path = REPO_ROOT) -> dict:
    out = {}
    for cpid, relative in po.RECEIVED_VOLUMES.items():
        directory = root / relative
        if not directory.is_dir():
            out[cpid] = {"resident": False}
            continue
        parts = inventory(directory)
        out[cpid] = {
            "resident": True,
            "identity": identity(directory),
            "parts": sorted(parts),
            "section_identities": sum(len(p["sections_present"]) for p in parts.values()),
            "missing": [s for p in parts.values() for s in p["sections_missing"]],
            "inventory": parts,
        }
    return out


def main() -> int:
    print(json.dumps(report(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
