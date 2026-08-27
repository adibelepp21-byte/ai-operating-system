"""
End-to-end evidence for the Definition decoding seam (ACT-CC-P6-048).

Evidences the whole path the Act set out to close:

    stored bytes ─→ Infrastructure decoding ─→ Runtime DefinitionCatalog ─→ host

Each half is evidenced in its own boundary's suite; this suite evidences that
they meet. Ownership stays split across the seam: Infrastructure answers *"what
did the store hold?"*, Runtime answers *"what does it mean?"* — the decoder
imposes no field vocabulary, and the catalog validates every field itself.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from native_core.core.infrastructure import LocalAppendOnlyStorage, read_records
from native_core.core.runtime.discovery import (
    DefinitionCatalog,
    MalformedDeclaration,
    UndeclaredDefinition,
)

PARTITION = "definition-catalog"
BATCH = "runtime.batch-governance-review-substrate"
TEXTUAL = "runtime.textual-reasoning-execution-substrate"
INTEGRITY = "Governance Artifact Integrity Agent"


def _declaration(runtime_key, definition_names) -> bytes:
    return json.dumps(
        {"runtime_key": runtime_key, "definition_names": list(definition_names)},
        sort_keys=True,
    ).encode("utf-8")


class _Catalogued:
    """A store holding a governed catalog of host declarations."""

    def __init__(self, *records: bytes):
        self._records = records

    def __enter__(self):
        self._tmp = tempfile.TemporaryDirectory()
        storage = LocalAppendOnlyStorage(Path(self._tmp.name))
        storage.provision()
        for record in self._records:
            storage.append(PARTITION, record)
        self.storage = storage
        return storage

    def __exit__(self, *exc):
        self._tmp.cleanup()
        return False


def _catalog(storage) -> DefinitionCatalog:
    return DefinitionCatalog.from_records(read_records(storage, PARTITION))


class TestTheSeamCarriesStoredDataIntoDiscovery(unittest.TestCase):
    def test_a_stored_catalog_resolves_a_definition_name_to_a_host(self):
        with _Catalogued(
            _declaration(TEXTUAL, [INTEGRITY, "Reasoning Agent"]),
            _declaration(BATCH, [INTEGRITY]),
        ) as storage:
            self.assertEqual(BATCH, _catalog(storage).resolve(INTEGRITY).runtime_key)

    def test_a_selector_binds_the_named_stored_host(self):
        with _Catalogued(
            _declaration(TEXTUAL, [INTEGRITY]), _declaration(BATCH, [INTEGRITY])
        ) as storage:
            resolved = _catalog(storage).resolve(INTEGRITY, selector=TEXTUAL)
            self.assertEqual(TEXTUAL, resolved.runtime_key)

    def test_every_stored_declaration_reaches_the_catalog(self):
        with _Catalogued(
            _declaration(TEXTUAL, [INTEGRITY]),
            _declaration(BATCH, ["Other Agent"]),
        ) as storage:
            self.assertEqual(
                [BATCH, TEXTUAL],
                [d.runtime_key for d in _catalog(storage).declarations],
            )

    def test_resolution_is_stable_across_rebuilds_from_the_same_store(self):
        with _Catalogued(_declaration(BATCH, [INTEGRITY])) as storage:
            self.assertEqual(
                {_catalog(storage).resolve(INTEGRITY).runtime_key for _ in range(10)},
                {BATCH},
            )

    def test_stored_write_order_does_not_change_resolution(self):
        forward = (_declaration(TEXTUAL, [INTEGRITY]), _declaration(BATCH, [INTEGRITY]))
        with _Catalogued(*forward) as storage:
            first = _catalog(storage).resolve(INTEGRITY).runtime_key
        with _Catalogued(*reversed(forward)) as storage:
            self.assertEqual(first, _catalog(storage).resolve(INTEGRITY).runtime_key)


class TestTheSeamFailsClosed(unittest.TestCase):
    def test_an_unstored_definition_does_not_resolve(self):
        with _Catalogued(_declaration(BATCH, [INTEGRITY])) as storage:
            with self.assertRaises(UndeclaredDefinition):
                _catalog(storage).resolve("No Such Agent")

    def test_an_empty_store_resolves_nothing(self):
        with _Catalogued() as storage:
            with self.assertRaises(UndeclaredDefinition):
                _catalog(storage).resolve(INTEGRITY)

    def test_a_stored_record_missing_a_field_halts_construction(self):
        with _Catalogued(json.dumps({"runtime_key": BATCH}).encode("utf-8")) as storage:
            with self.assertRaises(MalformedDeclaration):
                _catalog(storage)

    def test_a_stored_record_with_a_wrong_shape_halts_construction(self):
        record = json.dumps(
            {"runtime_key": BATCH, "definition_names": INTEGRITY}
        ).encode("utf-8")
        with _Catalogued(record) as storage:
            with self.assertRaises(MalformedDeclaration):
                _catalog(storage)

    def test_a_duplicated_stored_host_halts_construction(self):
        with _Catalogued(
            _declaration(BATCH, [INTEGRITY]), _declaration(BATCH, ["Other"])
        ) as storage:
            with self.assertRaises(MalformedDeclaration):
                _catalog(storage)

    def test_the_decoder_imposes_no_vocabulary_the_catalog_enforces_it(self):
        """Ownership stays split: decoding accepts the record, the catalog rejects it."""
        record = json.dumps({"unrelated": "field"}).encode("utf-8")
        with _Catalogued(record) as storage:
            self.assertEqual([{"unrelated": "field"}], list(read_records(storage, PARTITION)))
            with self.assertRaises(MalformedDeclaration):
                _catalog(storage)


class TestTheSeamIntroducesNoAgentDependency(unittest.TestCase):
    def test_the_whole_path_loads_no_agent_module(self):
        """The acyclic graph survives the seam, measured in a fresh interpreter."""
        program = (
            "import sys, json, tempfile;"
            "from pathlib import Path;"
            "from native_core.core.infrastructure import LocalAppendOnlyStorage, read_records;"
            "from native_core.core.runtime.discovery import DefinitionCatalog;"
            "d = tempfile.mkdtemp();"
            "s = LocalAppendOnlyStorage(Path(d));"
            "s.provision();"
            f"s.append({PARTITION!r}, json.dumps({{'runtime_key': {BATCH!r},"
            f" 'definition_names': [{INTEGRITY!r}]}}).encode('utf-8'));"
            f"c = DefinitionCatalog.from_records(read_records(s, {PARTITION!r}));"
            f"assert c.resolve({INTEGRITY!r}).runtime_key == {BATCH!r};"
            "print('AGENT_MODULES=' + repr([m for m in sys.modules if 'core.agent' in m]))"
        )
        result = subprocess.run(
            [sys.executable, "-c", program],
            capture_output=True,
            text=True,
            cwd=str(Path(__file__).resolve().parents[4]),
        )
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("AGENT_MODULES=[]", result.stdout)


if __name__ == "__main__":
    unittest.main()
