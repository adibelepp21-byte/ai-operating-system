"""
Document loader for the Knowledge retrieval experiment.

Loads and caches every .md file under docs/architecture (the current
corpus this phase asked the experiment to use), keeping each line
alongside the nearest preceding Markdown heading, so retrieval can
report heading context, not just a bare line number. In-memory only —
nothing is persisted to disk, and nothing here defines a Knowledge
entity, storage convention, or promotion path.
"""

from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CORPUS_ROOT = REPO_ROOT / "docs" / "architecture"


@dataclass(frozen=True)
class LoadedDocument:
    path: Path
    lines: tuple
    line_headings: tuple  # parallel to lines: nearest preceding heading, or None


class DocumentLoader:
    def __init__(self, root=CORPUS_ROOT):
        self.root = root
        self._cache = None

    def load_all(self):
        if self._cache is None:
            documents = {}
            for f in sorted(self.root.rglob("*.md")):
                try:
                    text = f.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                lines = text.splitlines()
                headings = []
                current = None
                for line in lines:
                    if line.strip().startswith("#"):
                        current = line.strip()
                    headings.append(current)
                documents[f] = LoadedDocument(path=f, lines=tuple(lines), line_headings=tuple(headings))
            self._cache = documents
        return self._cache
