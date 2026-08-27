"""
Behavioural evidence for the stored-record decoding seam (ACT-CC-P6-048).

Evidences what decoding *does*: the Infrastructure conformance suite continues
to evidence what the boundary *is*, and is unmodified by this Act.

Scope A — decoding a well-formed record.
Scope B — fail-closed rejection (PR-4).
Scope C — determinism and order preservation (Blueprint §26).
Scope D — reading through an injected facility.
Scope E — the seam carries representation only, never meaning.
"""

import json
import tempfile
import unittest
from pathlib import Path

from native_core.core.infrastructure import (
    LocalAppendOnlyStorage,
    RecordDecodeError,
    decode_record,
    decode_records,
    read_records,
)

PARTITION = "definition-catalog"


def _encoded(**fields) -> bytes:
    return json.dumps(fields, sort_keys=True).encode("utf-8")


class _Store:
    """A provisioned append-only store in a temporary directory."""

    def __enter__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.storage = LocalAppendOnlyStorage(Path(self._tmp.name))
        self.storage.provision()
        return self.storage

    def __exit__(self, *exc):
        self._tmp.cleanup()
        return False


# --------------------------------------------------------------------------
# Scope A — decoding
# --------------------------------------------------------------------------


class TestDecoding(unittest.TestCase):
    def test_a_json_object_decodes_to_a_mapping(self):
        self.assertEqual({"runtime_key": "rt.a"}, decode_record(_encoded(runtime_key="rt.a")))

    def test_nested_and_unicode_content_survives(self):
        raw = _encoded(runtime_key="rt.é", definition_names=["Agent Ω", "B"])
        self.assertEqual(["Agent Ω", "B"], decode_record(raw)["definition_names"])

    def test_a_bytearray_decodes(self):
        self.assertEqual({"a": 1}, decode_record(bytearray(b'{"a": 1}')))

    def test_many_records_decode_in_order(self):
        raws = [_encoded(n=i) for i in range(5)]
        self.assertEqual([0, 1, 2, 3, 4], [r["n"] for r in decode_records(raws)])


# --------------------------------------------------------------------------
# Scope B — fail closed (PR-4)
# --------------------------------------------------------------------------


class TestFailsClosed(unittest.TestCase):
    def test_invalid_json_raises(self):
        with self.assertRaises(RecordDecodeError):
            decode_record(b"{not json")

    def test_invalid_utf8_raises(self):
        with self.assertRaises(RecordDecodeError):
            decode_record(b"\xff\xfe{}")

    def test_a_non_object_is_not_a_record(self):
        for raw in (b"[1, 2]", b'"text"', b"7", b"null", b"true"):
            with self.assertRaises(RecordDecodeError):
                decode_record(raw)

    def test_a_non_bytes_input_raises(self):
        for value in ("{}", {"a": 1}, None, 7):
            with self.assertRaises(RecordDecodeError):
                decode_record(value)

    def test_a_bad_record_halts_the_sequence_rather_than_being_skipped(self):
        """A partial catalog would answer questions it cannot support."""
        raws = [_encoded(n=0), b"{broken", _encoded(n=2)]
        produced = []
        with self.assertRaises(RecordDecodeError):
            for record in decode_records(raws):
                produced.append(record)
        self.assertEqual([{"n": 0}], produced)

    def test_reading_requires_a_real_facility(self):
        for value in (None, "storage", object()):
            with self.assertRaises(RecordDecodeError):
                read_records(value, PARTITION)

    def test_reading_requires_a_partition_name(self):
        with _Store() as storage:
            for name in ("", "   ", None, 7):
                with self.assertRaises(RecordDecodeError):
                    read_records(storage, name)


# --------------------------------------------------------------------------
# Scope C — determinism (Blueprint §26)
# --------------------------------------------------------------------------


class TestDeterminism(unittest.TestCase):
    def test_the_same_bytes_always_decode_identically(self):
        raw = _encoded(runtime_key="rt.a", definition_names=["X"])
        self.assertEqual([decode_record(raw)] * 20, [decode_record(raw) for _ in range(20)])

    def test_append_order_is_preserved_on_read(self):
        with _Store() as storage:
            for i in range(4):
                storage.append(PARTITION, _encoded(n=i))
            self.assertEqual([0, 1, 2, 3], [r["n"] for r in read_records(storage, PARTITION)])

    def test_repeated_reads_agree(self):
        with _Store() as storage:
            storage.append(PARTITION, _encoded(n=1))
            first = list(read_records(storage, PARTITION))
            self.assertEqual(first, list(read_records(storage, PARTITION)))


# --------------------------------------------------------------------------
# Scope D — reading through the facility
# --------------------------------------------------------------------------


class TestReadsThroughTheFacility(unittest.TestCase):
    def test_records_written_to_a_partition_are_read_back(self):
        with _Store() as storage:
            storage.append(PARTITION, _encoded(runtime_key="rt.a", definition_names=["A"]))
            self.assertEqual(
                [{"runtime_key": "rt.a", "definition_names": ["A"]}],
                list(read_records(storage, PARTITION)),
            )

    def test_an_empty_partition_yields_nothing(self):
        with _Store() as storage:
            self.assertEqual([], list(read_records(storage, PARTITION)))

    def test_reading_retains_no_state_and_releases_nothing(self):
        with _Store() as storage:
            storage.append(PARTITION, _encoded(n=1))
            list(read_records(storage, PARTITION))
            self.assertTrue(storage.is_ready)


# --------------------------------------------------------------------------
# Scope E — representation only, never meaning
# --------------------------------------------------------------------------


class TestCarriesRepresentationOnly(unittest.TestCase):
    def test_no_schema_is_imposed(self):
        """Field vocabulary belongs to the consuming boundary, not here."""
        self.assertEqual({"anything": [1, {"nested": True}]}, decode_record(_encoded(anything=[1, {"nested": True}])))

    def test_an_empty_object_is_a_valid_record(self):
        self.assertEqual({}, decode_record(b"{}"))

    def test_the_seam_knows_no_entity(self):
        source = (Path(__file__).resolve().parent.parent / "records.py").read_text()
        for word in ("Agent", "Definition", "Runtime", "Capability", "Workflow"):
            self.assertNotIn(f"import {word}", source)


if __name__ == "__main__":
    unittest.main()
