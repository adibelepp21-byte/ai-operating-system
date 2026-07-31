"""
Knowledge retrieval experiment.

Tests whether retrieval over already-existing governance documents
provides operational value for an Agent Instance's "consumes Knowledge"
relationship (Domain Model §4), without creating any Knowledge entity,
storage convention, or promotion pipeline — retrieval only, read-only,
nothing cached to disk.

Two interfaces exist for this experiment, deliberately:

  - `search()` — the original naive linear substring scan (kept as the
    baseline this phase's index-backed adapter is measured against).
  - `KnowledgeRetrievalAdapter.retrieve()` — the upgraded interface this
    phase's directive required: document loader + text index +
    structured `EvidenceReference` output (file, line, heading context),
    ranked by query-term overlap.

Neither asserts a Knowledge Framework or attempts to model Knowledge's
real governed lifecycle (durable, revised/superseded via review — Domain
Model §6); both only test whether *finding* relevant governance text is
itself useful.
"""

import re
from dataclasses import dataclass
from pathlib import Path

from .index import WORD_RE, TextIndex
from .loader import CORPUS_ROOT, DocumentLoader

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_ROOT = REPO_ROOT / "docs"


@dataclass(frozen=True)
class RetrievalHit:
    file: Path
    line_number: int
    line_text: str


def search(query, root=DOCS_ROOT, max_hits=20):
    """Naive baseline: case-insensitive substring scan across every .md
    file under root, line by line. No ranking, no index."""
    hits = []
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    for f in sorted(root.rglob("*.md")):
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for i, line in enumerate(text.splitlines(), start=1):
            if pattern.search(line):
                hits.append(RetrievalHit(file=f, line_number=i, line_text=line.strip()))
                if len(hits) >= max_hits:
                    return hits
    return hits


@dataclass(frozen=True)
class EvidenceReference:
    """The retrieval interface's structured output: a citable pointer
    into the corpus, not just a raw line."""
    file: Path
    line_number: int
    line_text: str
    heading_context: str
    score: int


class KnowledgeRetrievalAdapter:
    """document loader + text index + retrieval interface +
    evidence-reference output — the four components this phase's
    directive asked for, assembled as one adapter."""

    def __init__(self, root=CORPUS_ROOT):
        self.loader = DocumentLoader(root)
        self.documents = self.loader.load_all()
        self.index = TextIndex(self.documents)

    def retrieve(self, query, max_hits=10):
        words = WORD_RE.findall(query.lower())
        if not words:
            return ()

        scores = {}
        for word in words:
            for location in self.index.lookup(word):
                scores[location] = scores.get(location, 0) + 1

        ranked = sorted(scores.items(), key=lambda kv: -kv[1])[:max_hits]
        results = []
        for (path, line_no), score in ranked:
            doc = self.documents[path]
            results.append(EvidenceReference(
                file=path,
                line_number=line_no,
                line_text=doc.lines[line_no - 1].strip(),
                heading_context=doc.line_headings[line_no - 1] or "(no heading)",
                score=score,
            ))
        return tuple(results)
