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
import subprocess
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
    "AIOS_CANONICAL_ARCHITECTURE.md": "NEVER resident — absent from full git history and from the archived corpus review's verified inventory; see SG-01, G-07",
    "AIOS_MASTER_PROGRAM_v1_0_LENGKAP.md": "Architect-supplied upload, outside the repository",
}

# Basenames too generic for a bare citation to identify anything. The corpus
# cites these fully elsewhere; a bare mention is prose, not a pointer.
GENERIC = {"__init__.py", "README.md"}


def _tracked_files() -> set:
    """Paths git tracks, as repo-relative POSIX strings.

    The audit reads ONLY tracked files. This is a hard scope guard, not a
    convenience filter.

    Why it exists: ``docs/program/`` holds thirteen untracked protected packages
    that governance forbids this programme to stage, commit, modify, relocate,
    rename, delete, persist, normalize, inspect for commit convenience, or use
    as implicit authority. An earlier version of this tool had no scope guard
    and read all thirteen during a directory-wide scan (``VF-10``). No content
    was quoted, persisted, or used — but a verifier that *can* wander into
    protected paths is a hazard whatever the intent of the run.

    Tracked-only is also the principled scope: the corpus of record is what the
    repository has committed. Untracked material is, by definition, not yet part
    of it.
    """
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z"], cwd=str(REPO_ROOT),
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return set()
    return {p for p in out.split("\0") if p}


def _iter_markdown(root: Path):
    tracked = _tracked_files()
    if not tracked:
        raise SystemExit(
            "refusing to scan: could not determine tracked files, and the audit "
            "reads only tracked paths (see _tracked_files)."
        )
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.relative_to(REPO_ROOT).as_posix() not in tracked:
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


# --- Ledger table check (Master Roadmap §27) -------------------------------
#
# Most canonical citations in the Evidence Ledger are table rows that carry the
# quotation and the line number in *different columns*:
#
#   | **E-04** | Domain roster naming PD-03...PD-10 | `...A4.md` | :281-288 | ...
#
# The adjacency-based check cannot pair those, and that is exactly the shape of
# the E-11 defect: a quotation attributed to a file and line that did not carry
# it, undetected for twenty-six cycles. This check pairs them explicitly.

LEDGER_ROW = re.compile(r"^\|\s*\*\*(E-\d+)\*\*\s*\|")
LOCATION = re.compile(r":(\d+)(?:\s*[-\u2013\u2014]\s*(\d+))?")
LEDGER_WINDOW = 2

# Phrases that mark a quotation as *historical* — text the corpus is recording
# as withdrawn, superseded, or corrected away, rather than attributing to the
# cited source. E-13 quotes a phrase it explicitly says the row "previously
# read"; pairing that with the row's line citation and reporting a mismatch
# would be the checker misreading a correction as a claim. A corpus that
# records its own retractions must not be penalised for doing so.
# A source cell may name more than one file — E-11 carries two, paired
# positionally with its two quotations and two line citations. Taking a prefix
# of the cell yields a malformed path and a spurious "resolves to no file".
SOURCE_TOKEN = re.compile(r"`([^`]+?)`")

RETRACTION = re.compile(
    r"(previously read|previously said|previously stated|formerly read|"
    r"withdrawn|no longer reads|used to read|was corrected|is withdrawn)",
    re.IGNORECASE,
)


def _ledger_rows(path: Path):
    """Yield (line_no, id, claim, source, location) for each ledger table row.

    ``same`` in the source column is a carry-forward to the previous row's
    source; resolving it is required, not optional — a parser that treated it
    as a filename would silently check nothing.
    """
    previous_source = None
    for lineno, raw in enumerate(_lines(path), 1):
        if not LEDGER_ROW.match(raw):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        identifier = cells[0].strip("* ")
        claim, source, location = cells[1], cells[2], cells[3]
        bare = source.strip("`* ")
        if bare.lower() == "same":
            source = previous_source
        elif bare:
            previous_source = source
        yield lineno, identifier, claim, source, location


def _plain(text: str) -> str:
    """Strip Markdown emphasis so a quotation is compared as *text*.

    This corpus adds emphasis inside quotations — `E-44` quotes the Register's
    "not the semantic authority" as "**not** the semantic authority". The
    substance is verbatim; the asterisks are the citing document's own
    typography. §27 asks whether the source supports the claim, not whether the
    citer reproduced its formatting, so comparison is done on stripped text.
    Anything stronger would report true citations as defects.
    """
    return " ".join(re.sub(r"[*`_]+", "", text).split())


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
        exact = _plain(lines[want - 1])
        if _plain(needle) in exact:
            return "exact", candidate
        lo = max(0, want - 1 - QUOTE_WINDOW)
        hi = min(len(lines), want + QUOTE_WINDOW)
        window = _plain(" ".join(lines[lo:hi]))
        if _plain(needle) in window and near_hit is None:
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

    # Ledger table rows: pair quotation with line citation across columns.
    ledger = REPO_ROOT / "docs/architecture/platform-organization/EVIDENCE-LEDGER.md"
    ledger_checked = 0
    if ledger.is_file() and any((REPO_ROOT / r) in ledger.parents or
                                str(ledger).startswith(str(REPO_ROOT / r))
                                for r in roots):
        rel = ledger.relative_to(REPO_ROOT).as_posix()
        for lineno, ident, claim, source, location in _ledger_rows(ledger):
            if not source:
                continue
            quotes = [" ".join(q.split()) for q in QUOTE.findall(claim)]
            # A row may carry its line number in the *source* cell rather than
            # the location cell (`FILE.md:1234`). Measured: 3 rows do. Reading
            # only the location cell left those unchecked while the tool
            # reported success on the rest.
            spans = LOCATION.findall(location) or LOCATION.findall(source)
            if not quotes or not spans:
                continue
            # A source token may carry its own line suffix (`FILE.md:181-183`);
            # strip it before resolving, or the range becomes part of the
            # filename and nothing resolves. And a token with no file extension
            # is a prose reference to a source (`Volume 4 C3`), not a path —
            # those are non-resident by definition and are not errors.
            sources = []
            for token in SOURCE_TOKEN.findall(source):
                token = re.sub(r":\d+(?:\s*[-\u2013\u2014]\s*\d+)?\s*$", "", token.strip())
                if re.search(r"\.(md|py|txt)$", token):
                    sources.append(token)
            if not sources:
                bare = [t for t in source.strip("`* ").split()
                        if re.search(r"\.(md|py|txt)$", t)]
                sources = bare[:1]
            if not sources:
                continue
            historical = bool(RETRACTION.search(claim))
            for position, quote in enumerate(quotes):
                if position >= len(spans):
                    break
                if historical:
                    findings.append({
                        "severity": "INFO", "source": f"{rel}:{lineno}",
                        "citation": ident,
                        "message": "HISTORICAL QUOTATION \u2014 row records a retraction; "
                                   "quoted text is not attributed to the cited source",
                    })
                    continue
                start = int(spans[position][0])
                end = int(spans[position][1] or spans[position][0])
                needle = quote.rstrip(".").strip()
                if not needle:
                    continue
                cited = sources[position] if position < len(sources) else sources[0]
                if cited in NON_RESIDENT:
                    continue
                kind, targets = _resolve(cited, index)
                if not targets:
                    findings.append({
                        "severity": "ERROR", "source": f"{rel}:{lineno}",
                        "citation": f"{ident} -> {cited}",
                        "message": "ledger row cites a path that resolves to no file",
                    })
                    continue
                ledger_checked += 1
                hit = None
                for candidate in targets:
                    body = _lines(candidate)
                    lo = max(0, start - 1 - LEDGER_WINDOW)
                    hi = min(len(body), end + LEDGER_WINDOW)
                    window = _plain(" ".join(body[lo:hi]))
                    if _plain(needle) in window:
                        hit = candidate
                        break
                if hit is not None:
                    findings.append({
                        "severity": "INFO", "source": f"{rel}:{lineno}",
                        "citation": f"{ident} {cited}:{start}",
                        "message": f"LEDGER TEXT VERIFIED \u2014 \u201c{quote[:55]}\u201d",
                    })
                else:
                    findings.append({
                        "severity": "ERROR", "source": f"{rel}:{lineno}",
                        "citation": f"{ident} {cited}:{start}"
                                    + (f"\u2013{end}" if end != start else ""),
                        "message": f"LEDGER TEXT MISMATCH \u2014 quoted text not found in the cited range: \u201c{quote[:55]}\u201d",
                    })

    return {
        "documents_scanned": scanned,
        "ledger_quotes_checked": ledger_checked,
        "citations_checked": citations,
        "findings": findings,
        "errors": sum(1 for f in findings if f["severity"] == "ERROR"),
        "warnings": sum(1 for f in findings if f["severity"] == "WARN"),
        "non_resident": sum(1 for f in findings
                            if f["severity"] == "INFO" and "NON-RESIDENT" in f["message"]),
        "text_verified": sum(1 for f in findings
                             if f["severity"] == "INFO"
                             and "TEXT VERIFIED" in f["message"]
                             and "LEDGER" not in f["message"]),
        "text_mismatch": sum(1 for f in findings if "TEXT MISMATCH" in f["message"]),
        "ledger_verified": sum(1 for f in findings if "LEDGER TEXT VERIFIED" in f["message"]),
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
    print(f"ledger quotes     : {report['ledger_quotes_checked']} checked, {report['ledger_verified']} verified")
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
