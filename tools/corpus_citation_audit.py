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
DEFAULT_ROOTS = (
    "docs/architecture/platform-organization",
    # The reconstitution candidate and its audit
    # (`ACT-CC-CANONICAL-ARCHITECTURE-RECONSTITUTION-SUBMISSION-v1.0`).
    # A candidate for the architecture SSOT is exactly the document whose
    # pointers must resolve before anyone proposes ratifying it.
    "docs/architecture/candidates",
    # Added under `ACT-CC-…-AUTHORITY-EVIDENCE-RESOLUTION-GATE §5.1`. This root
    # holds the Governance Decision Register, the Founder Decisions, and the
    # execution record — **the documents that carry the most citations in the
    # repository, and the ones the citation checker could not see.**
    "docs/governance",
    # Added under `ACT-CC-P11-001` in the same change that created
    # `docs/architecture/p11/`. A new directory outside these roots is invisible
    # to this auditor — `VF-11`'s failure shape, *a guard that passes because it
    # cannot see the newest work*. Adding the root alongside the directory means
    # the blind spot never exists in a committed state.
    "docs/architecture/p11",
    # Added under `DP-01 §3 W3` in the same change that created
    # `docs/architecture/organization/delegations/`, for the reason stated
    # directly above. This root had **never been audited** — it holds the P10
    # Department, Capability and Agent Definition records, whose cross-references
    # are the evidence the ownership graph is built from. The blind spot was
    # older than the directory that exposed it.
    "docs/architecture/organization",
    # Added under `ACT-CC-P11-005 §23` in the same change that created
    # `tools/planning/`. The W2 surface carries its architectural citations in
    # docstrings, so it is a root in its own right.
    #
    # **Scoped deliberately to this package rather than to `tools/`.** Scanning
    # all of `tools/` surfaces five findings, every one of them the auditor
    # documenting its own citation grammar (`file.md`, `FILE.md`), the
    # `ILLUSTRATIVE` registry's own worked example, or the VF-11 regression
    # fixture that exists precisely *because* it must not resolve. Clearing them
    # would mean five exemptions added so the tool could read itself — which is
    # the pressure `NON_RESIDENT` is written to resist. The finding is recorded
    # in the W2 evidence package and left for a change that is about it.
    "tools/planning",
    # The W6 → W2 evidence path, added under `ACT-CC-P11-006 §26` in the same
    # change that created it. Named as a file for the reason given in
    # `_iter_markdown`.
    "tools/performance_evidence.py",
    # `ACT-CC-P11-007 §26`: added with the surface, not after it. Both modules
    # carry their governing citations in docstrings and nowhere else.
    "tools/escalation_register.py",
    "tools/planning_continuity.py",
    "tools/agent_instance_registry.py",
    "tools/w4_delegation.py",
    "tools/w4_execution.py",
)

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
#: Cited paths that name a source **outside this repository**. Each value must
#: name the governance record that establishes the non-residency — an entry is
#: never added to make an ERROR go away, only because a record already says the
#: source is external.
#:
#: The registry is consulted **only after resolution fails** (see ``audit``). A
#: path that resolves is checked normally no matter what is listed here, so a
#: generic key like ``setup.py`` can never silence a real, resolvable citation.
NON_RESIDENT = {
    "AIOS_CANONICAL_ARCHITECTURE.md": "NEVER resident — absent from full git history and from the archived corpus review's verified inventory; see SG-01, G-07",
    "AIOS_MASTER_PROGRAM_v1_0_LENGKAP.md": "Architect-supplied upload, outside the repository",
    # Supplied with `ACT-CC-P11-001` as the P11 Roadmap / PRD / Construction
    # Blueprint. Recorded non-resident rather than persisted into the repository:
    # `ACT-CC-P11-001 §5` forbids turning a supplied source copy into a canonical
    # artifact, and the document's own header states it is `Draft for Founder
    # Review / Authority Ratification Required Before Construction`.
    "AIOS_PHASE_11___AUTONOMOUS_ORGANIZATION.txt": "Founder-supplied upload, outside the repository — P11 Blueprint, Draft, ACT-CC-P11-001",
    "AIOS_COFOUNDER_DELEGATION_CHARTER_v1.0.txt": "supplied upload, outside the repository — ESC-C5-01; presence disclosed at ACT-CC-P6-070 §2.1",
    # The Graphify archive, external corpus at Intake (E-66). Verified present
    # in `graphify-8/graphify/` and recorded at VERIFICATION §49.
    "extract.py": "Graphify external archive (graphify-8/graphify/) — E-66, Intake",
    "llm.py": "Graphify external archive (graphify-8/graphify/) — E-66, Intake",
    "watch.py": "Graphify external archive (graphify-8/graphify/) — E-66, Intake",
    "requirements.txt": "Graphify external archive — E-66, Intake",
    "setup.py": "Graphify external archive — E-66, Intake",
    "factory.py": "Graphify external archive — E-66, Intake",
    # EAI-0001 reviewed the external repository `1jehuang/jcode` at a pinned
    # revision (GDR-0012 §3.12). Confirmed by direct search: this basename has
    # never existed anywhere in this repository's history, and `dd8755f7` is not
    # a commit here.
    "scripts/check_dependency_boundaries.py": "external repository `1jehuang/jcode` reviewed as EAI-0001 — GDR-0012",
}

#: Routes that **illustrate a convention** rather than point at a file, keyed by
#: ``(source path, cited token)``.
#:
#: A naming-convention section that says *a Capability named "X" is recorded at
#: ``capabilities/x.md``* is describing a rule with a worked example. The example
#: names nothing real **by design** — the sentence beside it names a Department
#: "Architecture", which is equally hypothetical and equally absent.
#:
#: Same discipline as ``NON_RESIDENT``: consulted **only after resolution
#: fails**, so an entry can never mask a citation that resolves; keyed by source
#: as well as token, so it exempts one illustration rather than a filename
#: everywhere; and **never added to make an ERROR go away** — only because the
#: cited text is demonstrably an example rather than a pointer. A test asserts
#: every entry still fails to resolve, so an entry that becomes real is caught
#: instead of silently exempting a live file.
ILLUSTRATIVE = {
    ("docs/architecture/organization/README.md",
     "capabilities/governance-artifact-maintenance.md"):
        'worked example in the "Naming Convention" section — the Capability '
        '"Governance Artifact Maintenance" does not exist and is not claimed to; '
        "the same sentence invents a Department named \"Architecture\"",
}

#: A cited route carrying a literal placeholder is a **template**, not a pointer.
#: `docs/architecture/adr/decisions/ADR-NNNN.md` is the ADR naming convention,
#: not a file anyone expects to exist.
PLACEHOLDER = re.compile(r"(?:NNNN|XXXX|<[^>]+>|\{[^}]+\})")

# Basenames too generic for a bare citation to identify anything. The corpus
# cites these fully elsewhere; a bare mention is prose, not a pointer.
GENERIC = {"__init__.py", "README.md"}


def _tracked_files() -> set:
    """Paths git tracks, as repo-relative POSIX strings.

    Used to decide whether an *untracked* file sits in a protected area. It is
    NOT itself the scope guard — see ``_is_readable`` for why that distinction
    matters.
    """
    try:
        out = subprocess.run(
            ["git", "ls-files", "-z"], cwd=str(REPO_ROOT),
            capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return set()
    return {p for p in out.split("\0") if p}


# Areas whose UNTRACKED contents this programme may not read at all.
# ``docs/program/`` holds thirteen untracked protected packages that governance
# forbids staging, committing, modifying, relocating, renaming, deleting,
# persisting, normalizing, inspecting for commit convenience, or using as
# implicit authority. Its *tracked* contents are ordinary repository records.
PROTECTED_UNTRACKED_PREFIXES = ("docs/program/",)


def _is_readable(path: Path, tracked: set) -> bool:
    """Whether the audit may read this file.

    Containment is keyed on **path policy**, not on tracked status.

    ``VF-10`` added a guard that scanned tracked files only. That contained the
    protected packages — but it used "tracked" as a *proxy* for "not protected",
    and the proxy fails **open** in the direction that matters most: every file
    this programme writes is untracked until it is staged, so a newly authored
    artifact was silently skipped and its citations never checked. A probe
    carrying a deliberately broken citation reported ``0 errors`` while
    untracked and ``1 error`` once staged (``VF-11``).

    **A verifier that silently ignores the newest work reports the safety of the
    previous state as though it were the safety of the current one.**

    So: untracked files under a protected prefix are refused; everything else in
    the audit root is read, tracked or not.
    """
    rel = path.relative_to(REPO_ROOT).as_posix()
    if rel in tracked:
        return True
    return not rel.startswith(PROTECTED_UNTRACKED_PREFIXES)


def _iter_markdown(root: Path):
    tracked = _tracked_files()
    if not tracked:
        raise SystemExit(
            "refusing to scan: could not determine tracked files, so protected "
            "untracked paths cannot be identified (see _is_readable)."
        )
    # Python is scanned as well as Markdown. `ACT-CC-P11-005 §23` requires the
    # roots to cover *"all repository surfaces that materially participate"* in
    # the work being verified, and W2's decisive citations — `DP-01 §3 W2`,
    # `DP-03 §8.4`, `DP-04 §8.2` — live in module docstrings, not in any
    # document. Scanning only Markdown made every one of them invisible.
    # A root may name a single file. Directory roots are the norm, but a module
    # that materially participates in P11 while sitting in a directory whose
    # other contents are out of scope has no directory of its own to name —
    # `tools/performance_evidence.py` is exactly that. Without this, the choice
    # would be between leaving its citations unaudited and adopting all of
    # `tools/`, whose five self-referential findings are documented above.
    candidates = ([root] if root.is_file()
                  else list(root.rglob("*.md")) + list(root.rglob("*.py")))
    for path in sorted(candidates):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if not _is_readable(path, tracked):
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


#: Some frozen Volume 1 bodies carry headings with **no ``#`` marker at all** —
#: ``4. Capability Ownership Matrix`` alone on its line. ``B3.md`` uses this
#: form for all eleven of its sections, and ``A1.md`` switches to it partway
#: through the same file, after a ``⸻`` rule.
#:
#: Accepting bare numbered lines unconditionally would confirm ordinary list
#: items as sections: **92 of 172** bodies under ``docs/architecture`` contain
#: restarting ``N.`` runs. So the form is accepted only when the line is
#: surrounded by blank lines, opens with a capital, and carries no sentence
#: punctuation. Measured against the same corpus: **45** files match, and in
#: every one the numbers are strictly increasing — the restart signature of a
#: list never appears. The strictness costs recall, never precision: a heading
#: this misses stays a WARN, which already means *unconfirmed, not disproved*.
BARE_HEADING = re.compile(r"^(\d+)\.\s+[A-Z][^.!?]*$")


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
    return _has_bare_heading(text.split("\n"), number)


def _has_bare_heading(lines: list[str], number: str) -> bool:
    """The unmarked convention, accepted only under the guard described above."""
    for index, line in enumerate(lines):
        match = BARE_HEADING.match(line)
        if match is None or match.group(1) != number:
            continue
        before = lines[index - 1].strip() if index else ""
        after = lines[index + 1].strip() if index + 1 < len(lines) else ""
        if before == "" and after == "":
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
                        # Resolution failed. Only now may the registries speak —
                        # so an entry can never mask a citation that resolves.
                        if (rel, cited) in ILLUSTRATIVE:
                            findings.append({
                                "severity": "INFO", "source": f"{rel}:{lineno}",
                                "citation": cited,
                                "message": f"ILLUSTRATIVE — {ILLUSTRATIVE[(rel, cited)]}",
                            })
                        elif cited in NON_RESIDENT:
                            findings.append({
                                "severity": "INFO", "source": f"{rel}:{lineno}",
                                "citation": cited,
                                "message": f"NON-RESIDENT by record — {NON_RESIDENT[cited]}",
                            })
                        elif PLACEHOLDER.search(cited):
                            findings.append({
                                "severity": "INFO", "source": f"{rel}:{lineno}",
                                "citation": cited,
                                "message": "TEMPLATE ROUTE — carries a literal placeholder; not a pointer to a file",
                            })
                        else:
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
