"""
In-memory text index for the Knowledge retrieval experiment.

A genuine inverted index (word -> [(file, line_number), ...]), built
once per process from documents already loaded by loader.py. Not
persisted, not incremental, no ranking beyond query-term overlap count —
deliberately the simplest structure that still qualifies as indexing
rather than a linear scan, so the experiment can measure whether
indexing is worth its cost over the naive substring search this
experiment started with.
"""

import re
from collections import defaultdict

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9\-]*")


class TextIndex:
    def __init__(self, documents: dict):
        self._index = defaultdict(list)
        self._build(documents)

    def _build(self, documents):
        for path, doc in documents.items():
            for line_no, line in enumerate(doc.lines, start=1):
                for word in WORD_RE.findall(line.lower()):
                    self._index[word].append((path, line_no))

    def lookup(self, word):
        return self._index.get(word.lower(), [])

    @property
    def vocabulary_size(self):
        return len(self._index)
