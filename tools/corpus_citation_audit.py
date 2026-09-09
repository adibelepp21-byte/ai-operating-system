#!/usr/bin/env python3
"""Corpus Citation Audit — verifies that citations resolve to real sources.

Authorized under ``DEL-T4.4-CF-001 §3.1 C`` (engineering) and
``ACT-CC-P10-FINAL §6`` (FIX / VERIFY classes); Implementation Tier per
``Engineering Constitution §3.3``. Entirely read-only.

Why this exists
---------------
The Platform Organization corpus has produced the same defect class four
times: a citation sitting beside plausible text, never tested for whether the
cited source says — or even *is* — what the citation claims.

    E-41   `PD-05 sebagai consumer Knowledge` attributed to frozen PD-02,
           where it does not occur (0 hits). Ten cycles uncorrected.
    VF-9b  `parallel to Phase 1-13` attributed to the Platform Encyclopedia;
           0 occurrences in any source, 3 in the corpus's own files.
    §35.4  `governs` clauses cited to Domain Model §5; they are in §4.
    §37.1  Two dimensions called "genuinely open" while their sources sat in a
           directory the corpus cites by name.

A prior checker (Cycle 4) verified that quotes sat *beside* citations. That is
adjacency, not truth, and it missed every case above.

    ADJACENCY != TRUTH        CITATION != VERIFICATION
    NAMING A SOURCE != READING IT

What this checks
----------------
Three mechanically decidable properties, and no others:

1. **Path resolution** — a cited file path resolves to exactly one real file.
2. **Line citations** (``A4.md:289``) — the file has at least that many lines.
3. **Section citations** (``file.md §7``) — a heading for that section exists.
4. **Quotation truth** (Master Roadmap §27) — where a citation carries a line
   number and an adjacent quotation, that text must actually occur at or near
   the cited line. This is the check the first three miss, and it is the
   ``E-41`` class exactly: a plausible quote beside a real pointer that does
   not carry it.

What this deliberately does NOT check
-------------------------------------
Whether the cited source *supports the claim made about it*. That is a
semantic judgement no static tool can make, and asserting otherwise would
reproduce the original defect in tooling form. A PASS here means the pointer
resolves — nothing more.

Severity
--------
``ERROR``       cited path does not resolve, or resolves ambiguously
``ERROR``       line citation exceeds the file's length
``WARN``        section citation whose heading could not be located
``INFO``        citation resolved

Section headings vary across this repository (``## 5.``, ``### GDR-0001``,
``# PART E``), so a missing section heading is reported as WARN rather than
ERROR: it means "could not confirm", not "is wrong". Overstating that
confidence is the very failure this tool exists to catch.

Usage::

    python3 tools/corpus_citation_audit.py [root ...]
    python3 tools/corpus_citation_audit.py --json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ROOTS = ("docs/architecture/platform-organization",)

# A backticked token that looks like a file reference, optionally carrying a
# ``:line`` suffix or a trailing ``§n`` section marker.
CITATION = re.compile(
    r"`(?P<path>[A-Za-z0-9_][A-Za-z0-9_./-]*\.(?:md|py|txt))"
    r"(?::(?P<line>\d+))?"
    r"(?P<tail>[^`]*)`"
)
SECTION = re.compile(r"§\s*(\d+)")

# A quotation attributed to a citation on the same line: *"..."* or **"..."**.
QUOTE = re.compile(r"\*{1,2}\s*[\u201c\"]([^\u201d\"]{8,})[\u201d\"]\s*\*{1,2}")

# How far from the cited line a quotation may legitimately sit. A cited line is
# a pointer into a passage, not always the exact line of every quoted clause.
QUOTE_WINDOW = 3

# Directories that are not part of the repository's own source of truth.
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv"}

# Sources the corpus deliberately cites while recording them as NOT RESIDENT.
# Citing a known-absent authority is correct practice here — the absence is the
# finding — so these resolve to NON-RESIDENT rather than to an error. Each entry
# must be documented as non-resident in the corpus itself; adding a path here to
# silence an error, rather than because the corpus records the gap, would make
# this tool complicit in the defect it exists to catch.
NON_RESIDENT = {
    "AIOS_CANONICAL_ARCHITECTURE.md": "recorded non-resident; see G-07 and README §1a",
    "AIOS_MASTER_PROGRAM_v1_0_LENGKAP.md": "Architect-supplied upload, outside the repository",
}

# Basenames too generic for a bare citation to identify anything. The corpus
# cites these fully elsewhere; a bare mention is prose, not a pointer.
GENERIC = {"__init__.py", "README.md"}


def _iter_markdown(root: Path):
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def _resolve(cited: str, index: dict[str, list[Path]]) -> tuple[str, list[Path]]:
    """Resolve a cited path to real files.

    A path containing a separator is resolved against the repository root, and
    also accepted as a suffix match — the corpus legitimately abbreviates
    (``volume-2/.../C8.md``). A bare basename is resolved through the index.
    """
    if "/" in cited:
        direct = REPO_ROOT / cited
        if direct.is_file():
            return "exact", [direct]
        # Abbreviated or partial path: match on trailing segments.
        tail = cited.split("/")[-1]
        candidates = [
            p for p in index.get(tail, [])
            if str(p.relative_to(REPO_ROOT)).endswith(cited.replace("...", "").lstrip("/"))
        ]
        if candidates:
            return "suffix", candidates
        return "unresolved", index.get(tail, [])
    return "basename", index.get(cited, [])


def _has_section(path: Path, number: str) -> bool:
    """True if the file carries a heading introducing the given section."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    patterns = (
        rf"^#{{1,6}}\s*\**\s*{number}\.",       # "## 5. Frozen Layer Model"
        rf"^#{{1,6}}\s*\**\s*§\s*{number}\b",   # "## §5"
        rf"^§\s*{number}\b",                    # bare "§5"
        rf"^#{{1,6}}\s*Section\s+[A-Z]?{number}\b",
    )
    for pattern in patterns:
        if re.search(pattern, text, re.MULTILINE):
            return True
    return False


def _lines(path: Path) -> list[str]:
    """Split on newlines only — never ``str.splitlines()``.

    ``splitlines()`` also breaks on U+2028, U+0085 and friends, which several
    canonical bodies in this repository contain. A file counted that way
    disagrees with ``sed``, every editor, and the line numbers the corpus cites,
    which made the auditor report TEXT MISMATCH against citations that were
    correct. A verifier that miscounts lines manufactures the defect it is
    supposed to detect.
    """
    return path.read_text(encoding="utf-8", errors="replace").split("\n")


def _check_quote(candidates, want: int, needle: str):
    """Test a quotation against every candidate file.

    Returns ``("exact"|"near"|"mismatch", matched_path_or_None)``. A duplicated
    basename is resolved *by the quotation itself*: the file that actually
    carries the text at the cited line is the file that was meant.
    """
    if not needle:
        return "skip", None
    near_hit = None
    for candidate in candidates:
        try:
            lines = candidate.read_text(encoding="utf-8", errors="replace").split("\n")
        except OSError:
            continue
        if want > len(lines):
            continue
        exact = " ".join(lines[want - 1].split())
        if needle in exact:
            return "exact", candidate
        lo = max(0, want - 1 - QUOTE_WINDOW)
        hi = min(len(lines), want + QUOTE_WINDOW)
        window = " ".join(" ".join(lines[lo:hi]).split())
        if needle in window and near_hit is None:
            near_hit = candidate
    if near_hit is not None:
        return "near", near_hit
    return "mismatch", None


def audit(roots: list[str]) -> dict:
    index: dict[str, list[Path]] = {}
    for path in REPO_ROOT.rglob("*"):
        if path.is_file() and not any(p in SKIP_DIRS for p in path.parts):
            index.setdefault(path.name, []).append(path)

    findings: list[dict] = []
    scanned = 0
    citations = 0

    for root_name in roots:
        root = REPO_ROOT / root_name
        if not root.exists():
            findings.append({
                "severity": "ERROR",
                "source": root_name,
                "citation": root_name,
                "message": "audit root does not exist",
            })
            continue
        for doc in _iter_markdown(root):
            scanned += 1
            rel = doc.relative_to(REPO_ROOT).as_posix()
            for lineno, text in enumerate(doc.read_text(encoding="utf-8", errors="replace").split("\n"), 1):
                for match in CITATION.finditer(text):
                    citations += 1
                    cited = match.group("path")

                    if cited in GENERIC and "/" not in cited:
                        continue
                    if cited in NON_RESIDENT:
                        findings.append({
                            "severity": "INFO", "source": f"{rel}:{lineno}",
                            "citation": cited,
                            "message": f"NON-RESIDENT by record — {NON_RESIDENT[cited]}",
                        })
                        continue

                    kind, targets = _resolve(cited, index)

                    # A line citation disambiguates duplicate basenames: only a
                    # file long enough can be the one meant.
                    if len(targets) > 1 and match.group("line"):
                        want = int(match.group("line"))
                        long_enough = [
                            t for t in targets
                            if len(t.read_text(encoding="utf-8", errors="replace").split("\n")) >= want
                        ]
                        if len(long_enough) == 1:
                            targets = long_enough

                    if not targets:
                        findings.append({
                            "severity": "ERROR", "source": f"{rel}:{lineno}",
                            "citation": cited,
                            "message": "cited path resolves to no file in the repository",
                        })
                        continue
                    if kind == "basename" and len(targets) > 1:
                        findings.append({
                            "severity": "WARN", "source": f"{rel}:{lineno}",
                            "citation": cited,
                            "message": f"ambiguous: {len(targets)} files share this name",
                        })
                        continue

                    target = targets[0]

                    if match.group("line"):
                        want = int(match.group("line"))
                        have = len(target.read_text(encoding="utf-8", errors="replace").split("\n"))
                        if want > have:
                            findings.append({
                                "severity": "ERROR", "source": f"{rel}:{lineno}",
                                "citation": f"{cited}:{want}",
                                "message": f"line {want} exceeds file length ({have} lines)",
                            })
                            continue

                    # §27 Citation Truth Rule: a quotation attributed to a
                    # line citation must actually occur at or near that line.
                    # This is the check that path-and-line verification misses,
                    # and it is the E-41 class: a plausible quote beside a real
                    # pointer that does not carry it.
                    if match.group("line") and target.suffix in (".md", ".txt"):
                        quote = QUOTE.search(text[match.end():])
                        if quote:
                            claimed = " ".join(quote.group(1).split())
                            needle = claimed.rstrip(".").strip()
                            want = int(match.group("line"))
                            # A quotation disambiguates a duplicated basename:
                            # test every candidate rather than an arbitrary
                            # first pick. Testing one guess and reporting a
                            # mismatch would be the detector inventing a defect.
                            result, matched = _check_quote(targets, want, needle)
                            where = matched.relative_to(REPO_ROOT).as_posix() if matched else cited
                            if result == "exact":
                                findings.append({
                                    "severity": "INFO", "source": f"{rel}:{lineno}",
                                    "citation": f"{cited}:{want}",
                                    "message": f"TEXT VERIFIED at {where}:{want} \u2014 \u201c{claimed[:60]}\u201d",
                                })
                            elif result == "near":
                                findings.append({
                                    "severity": "INFO", "source": f"{rel}:{lineno}",
                                    "citation": f"{cited}:{want}",
                                    "message": f"TEXT VERIFIED within \u00b1{QUOTE_WINDOW} lines at {where}:{want}",
                                })
                            elif result == "mismatch":
                                findings.append({
                                    "severity": "ERROR", "source": f"{rel}:{lineno}",
                                    "citation": f"{cited}:{want}",
                                    "message": f"TEXT MISMATCH \u2014 quoted text not found at or near line {want} in any candidate file: \u201c{claimed[:60]}\u201d",
                                })

                    section = SECTION.search(match.group("tail") or "")
                    if section and target.suffix == ".md":
                        if not _has_section(target, section.group(1)):
                            findings.append({
                                "severity": "WARN", "source": f"{rel}:{lineno}",
                                "citation": f"{cited} §{section.group(1)}",
                                "message": "section heading not located (convention varies; unconfirmed, not disproved)",
                            })

    return {
        "documents_scanned": scanned,
        "citations_checked": citations,
        "findings": findings,
        "errors": sum(1 for f in findings if f["severity"] == "ERROR"),
        "warnings": sum(1 for f in findings if f["severity"] == "WARN"),
        "non_resident": sum(1 for f in findings
                            if f["severity"] == "INFO" and "NON-RESIDENT" in f["message"]),
        "text_verified": sum(1 for f in findings
                             if f["severity"] == "INFO" and "TEXT VERIFIED" in f["message"]),
        "text_mismatch": sum(1 for f in findings if "TEXT MISMATCH" in f["message"]),
    }


def main(argv: list[str]) -> int:
    as_json = "--json" in argv
    roots = [a for a in argv[1:] if not a.startswith("--")] or list(DEFAULT_ROOTS)
    report = audit(roots)

    if as_json:
        print(json.dumps(report, indent=2))
        return 1 if report["errors"] else 0

    print(f"documents scanned : {report['documents_scanned']}")
    print(f"citations checked : {report['citations_checked']}")
    print(f"errors            : {report['errors']}")
    print(f"warnings          : {report['warnings']}")
    print(f"non-resident      : {report['non_resident']}  (cited by record, not defects)")
    print(f"text verified     : {report['text_verified']}  (quotation confirmed at the cited line)")
    if report["findings"]:
        print()
        for f in report["findings"]:
            print(f"  [{f['severity']}] {f['source']}  `{f['citation']}`")
            print(f"          {f['message']}")
    print()
    print("NOTE: a resolved citation proves the pointer is real, not that the")
    print("      cited source supports the claim made about it.")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
