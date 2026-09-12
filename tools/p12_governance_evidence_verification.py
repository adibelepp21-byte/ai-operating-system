"""P12-W6 — governance evidence verification (`§19` scope: `GOVERNANCE`).

`§26` requires governance evidence to establish nine elements:

```text
decision body · authority · effective date · scope · status · provenance
affected surfaces · current state · verification
```

and closes: *"Register entries are records of decisions, not substitutes for
decision authority."*

**Measured against instrument bodies, not against a dataclass.** A field on a
parser proves the parser could read an element; only the corpus shows whether
any instrument states it. The two diverge here in both directions: the parser
carries fields the corpus rarely fills, and the corpus carries labels the parser
has no field for.

**Coverage is reported per element as a count, never as a boolean.** `§26` says
governance evidence *must establish* these — an element that one instrument in
385 states is not established by the corpus, and a yes/no would report it
identically to one that all 385 state.

**What is measured is machine-readable establishment, and the distinction
matters.** An instrument may establish its authority in prose and state no
`Authority:` label, and this module will not count it. That is deliberate and it
is the point: `§26` exists so governance evidence can be *used*, and every
resident consumer of it — the index, the register, the derived views, this suite
— reads labels. An element stated only in prose is established for a human
reader and absent for every consumer. **It is not an overclaim to be avoided by
softening the result; it is the result, provided the module says which of the
two it measured.** It does, here and in every emitted detail line.

An element with **no resident label at all** is `ABSENT`. It is not a failure of
this module, and it is not closed by inventing a label.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]

ESTABLISHED = "ESTABLISHED"
PARTIAL = "PARTIAL"
ABSENT = "ABSENT"

#: An element is `ESTABLISHED` only when most of the corpus states it. Below
#: this it is `PARTIAL`: present, but not something a reader may rely on finding.
#: Declared as data so the threshold is visible and can be argued with, rather
#: than buried in a comparison.
ESTABLISHED_FRACTION = 0.5

#: `§26`'s nine, in its order.
GOVERNANCE_ELEMENTS: Tuple[str, ...] = (
    "decision body", "authority", "effective date", "scope", "status",
    "provenance", "affected surfaces", "current state", "verification",
)

#: The labels a resident instrument actually uses for each element, read from
#: the corpus rather than assumed. An empty tuple is a claim that no resident
#: label carries this element, and it is checked by the `ABSENT` control.
ELEMENT_LABELS: Dict[str, Tuple[str, ...]] = {
    "decision body": ("Decided by", "Decided By", "Issued by", "Issued By",
                      "Decision Owner", "Approved by", "Approved By",
                      "Recorded by", "Executed by", "Proposer", "Executor"),
    "authority": ("Authority", "Execution Authority", "Decision Authority",
                  "Ratification Authority", "Authority posture",
                  "Prepared under", "Executed under", "Recorded under"),
    "effective date": ("Date", "Date recorded", "Date Recorded",
                       "Date issued", "Date Issued", "Effective",
                       "Established"),
    "scope": ("Scope", "Subject", "Corpus item"),
    "status": ("Status",),
    "provenance": (),          # structural: see `_provenance_coverage`
    "affected surfaces": (),   # no resident label
    "current state": ("Decision", "Decision State", "Determination",
                      "Ratification Authorization", "Result", "VERDICT"),
    "verification": (),        # no resident label
}

_LABEL_LINE = re.compile(r"^[-*]?\s*\**([A-Z][A-Za-z /()-]{2,40})\**\s*:\s*(.+)$")

#: How far into a document a metadata label may appear. Instruments carry their
#: header block at the top; scanning the whole body would count a sentence in a
#: later section that happens to look like a label.
_HEADER_LINES = 80


@dataclass(frozen=True)
class ElementCoverage:
    element: str
    status: str
    instruments: int
    population: int
    labels_seen: Tuple[str, ...]
    detail: str


def instruments() -> Tuple[Tuple[Path, str], ...]:
    """Every resident governance instrument, with its body."""
    from tools.governance_index import tracked_markdown, is_governance_record
    found = []
    for path in tracked_markdown(REPO_ROOT):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        if is_governance_record(text):
            found.append((path, text))
    return tuple(found)


def _labels_of(text: str) -> Tuple[str, ...]:
    seen = set()
    for line in text.split("\n")[:_HEADER_LINES]:
        match = _LABEL_LINE.match(line.strip())
        if match and match.group(2).strip():
            seen.add(match.group(1).strip())
    return tuple(sorted(seen))


def _provenance_coverage(population: int) -> ElementCoverage:
    """Provenance is structural, not a label.

    Every indexed instrument carries `source_path` and `source_hash` — where it
    was read from and what its bytes were. That is provenance of the record,
    established for the whole population by construction rather than by any
    instrument choosing to state it.
    """
    return ElementCoverage(
        "provenance", ESTABLISHED, population, population,
        ("source_path", "source_hash"),
        "structural: every indexed instrument carries its path and content hash")


def coverage(population=None) -> Tuple[ElementCoverage, ...]:
    docs = instruments() if population is None else population
    total = len(docs)
    per_doc = [(_labels_of(text)) for _, text in docs]

    results = []
    for element in GOVERNANCE_ELEMENTS:
        if element == "provenance":
            results.append(_provenance_coverage(total))
            continue
        labels = ELEMENT_LABELS[element]
        if not labels:
            results.append(ElementCoverage(
                element, ABSENT, 0, total, (),
                "no resident instrument label carries this element"))
            continue
        seen = set()
        count = 0
        for found in per_doc:
            matched = [label for label in labels if label in found]
            if matched:
                count += 1
                seen.update(matched)
        if count == 0:
            status = ABSENT
            detail = (f"{len(labels)} label(s) are searched for and none "
                      "appears in any instrument header")
        elif total and count / total >= ESTABLISHED_FRACTION:
            status = ESTABLISHED
            detail = f"{count}/{total} instruments carry a label for it"
        else:
            status = PARTIAL
            detail = (f"{count}/{total} carry a label; the rest state it in "
                      "prose or not at all")
        results.append(ElementCoverage(element, status, count, total,
                                       tuple(sorted(seen)), detail))
    return tuple(results)


def by_population() -> dict:
    """The same measurement over the whole corpus and over Founder acts alone.

    Reported because the denominator is arguable and the result must not depend
    on my choice of it. The narrower population is **worse**, not better, which
    rules out the obvious objection — that the wide population is diluted by
    documents that are not decision instruments. Founder acts state fewer
    labelled elements than the corpus average, because they state them in prose.
    """
    docs = instruments()
    acts = tuple((path, text) for path, text in docs
                 if "docs/governance/acts/" in path.as_posix())
    return {
        "corpus": {r.element: (r.status, r.instruments, r.population)
                   for r in coverage(population=docs)},
        "founder_acts": {r.element: (r.status, r.instruments, r.population)
                         for r in coverage(population=acts)},
    }


def summary() -> dict:
    results = coverage()
    return {
        "elements": len(results),
        "population": results[0].population if results else 0,
        "established": sum(1 for r in results if r.status == ESTABLISHED),
        "partial": sum(1 for r in results if r.status == PARTIAL),
        "absent": sum(1 for r in results if r.status == ABSENT),
        "absent_elements": tuple(r.element for r in results
                                 if r.status == ABSENT),
        "partial_elements": tuple(r.element for r in results
                                  if r.status == PARTIAL),
    }


def main(argv=None) -> int:
    for result in coverage():
        print(f"{result.element:<18} {result.status:<12} "
              f"{result.instruments:>4}/{result.population:<5} "
              f"{result.detail[:56]}")
    print()
    print("summary:", summary())
    print()
    print("An element one instrument in hundreds states is not established by")
    print("the corpus. A boolean would report it identically to one all state.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
