"""Tests for `tools.governance_delegation_register`.

The property under test is that an append-only register is read with its
supersession marks applied. A superseded entry keeps its original
`| **Status** | **ACTIVE** |` row, so a reader that trusts that row reports a
superseded delegation as in force.
"""

import tempfile
import unittest
from pathlib import Path

from tools import governance_delegation_register as reg
from tools import p12_self_model as model

_SYNTHETIC = """# Register

## 3. Register Entries

### DEL-A-OLD-001 — Old delegation

| Field | Value |
|---|---|
| **Delegation ID** | `DEL-A-OLD-001` |
| **Delegated Role** | Old office |
| **Scope** | old scope |
| **Status** | **ACTIVE** |

### 3.1 Scope

Body text that is not a field.

### DEL-B-DORMANT-001 — Dormant delegation

| Field | Value |
|---|---|
| **Delegate** | Old office |
| **Status** | **ACTIVE — DORMANT UNTIL INVOKED** |

## 12. Later Append

### DEL-C-NEW-001 — New delegation

| Field | Value |
|---|---|
| **Delegated Role** | New office |
| **Status** | **ACTIVE** |

#### Supersession mark — `DEL-A-OLD-001`

| Field | Value |
|---|---|
| **Status from 2026-01-01** | **SUPERSEDED** by `DEL-C-NEW-001` |

#### Activation record — `ACT-X-A`

| Field | Value |
|---|---|
| **Status** | **REVOKED** |
"""


def _write(text: str) -> Path:
    directory = Path(tempfile.mkdtemp())
    path = directory / "register.md"
    path.write_text(text, encoding="utf-8")
    return path


class ResidentRegister(unittest.TestCase):
    """What the committed register states after the V2 registration."""

    def setUp(self):
        self.by_id = {d.identifier: d for d in reg.read_register()}

    def test_v2_delegation_is_in_force(self):
        self.assertTrue(self.by_id["DEL-CFV2-CEO-001"].in_force)

    def test_v1_delegation_is_superseded_by_v2_despite_its_own_status_row(self):
        v1 = self.by_id["DEL-T4.4-CF-001"]
        self.assertEqual(v1.declared_status, "ACTIVE")
        self.assertEqual(v1.effective_status, "SUPERSEDED")
        self.assertEqual(v1.superseded_by, ("DEL-CFV2-CEO-001",))
        self.assertFalse(v1.in_force)

    def test_dormant_delegation_stays_in_force_and_dormant(self):
        dormant = self.by_id["DEL-F03-015-P7I99-001"]
        self.assertTrue(dormant.in_force)
        self.assertIn("DORMANT", dormant.effective_status)

    def test_exactly_one_co_founder_delegation_defines_the_role(self):
        roles = [d for d in reg.in_force()
                 if d.role.startswith("AIOS Co-Founder + Delegated CEO")]
        self.assertEqual([d.identifier for d in roles], ["DEL-CFV2-CEO-001"])


class SyntheticRegister(unittest.TestCase):

    def setUp(self):
        self.by_id = {d.identifier: d
                      for d in reg.read_register(_write(_SYNTHETIC))}

    def test_every_entry_is_read(self):
        self.assertEqual(set(self.by_id),
                         {"DEL-A-OLD-001", "DEL-B-DORMANT-001", "DEL-C-NEW-001"})

    def test_mark_applies_to_its_target_only(self):
        self.assertEqual(self.by_id["DEL-A-OLD-001"].effective_status, "SUPERSEDED")
        self.assertEqual(self.by_id["DEL-C-NEW-001"].effective_status, "ACTIVE")

    def test_later_status_rows_do_not_leak_into_an_entry(self):
        """The activation record's REVOKED row sits after DEL-C-NEW-001 and must
        not be read as that entry's status."""
        self.assertEqual(self.by_id["DEL-C-NEW-001"].declared_status, "ACTIVE")

    def test_body_subheading_does_not_end_field_reading_early(self):
        self.assertEqual(self.by_id["DEL-A-OLD-001"].scope, "old scope")

    def test_delegate_field_is_accepted_as_role(self):
        self.assertEqual(self.by_id["DEL-B-DORMANT-001"].role, "Old office")

    def test_without_a_mark_the_declared_status_governs(self):
        text = _SYNTHETIC.split("#### Supersession mark")[0]
        by_id = {d.identifier: d for d in reg.read_register(_write(text))}
        self.assertTrue(by_id["DEL-A-OLD-001"].in_force)


class FailsClosed(unittest.TestCase):

    def test_missing_register_raises_rather_than_reporting_nothing_in_force(self):
        with self.assertRaises(reg.DelegationRegisterUnreadable):
            reg.read_register(Path(tempfile.mkdtemp()) / "absent.md")

    def test_self_model_reports_unresolved_for_an_empty_root(self):
        answer = model.authority(Path(tempfile.mkdtemp()))
        self.assertFalse(answer.value["operative_delegation"]["resolved"])
        self.assertEqual(answer.value["operative_delegation"]["in_force"], [])


class SelfModelUsesTheRegister(unittest.TestCase):

    def test_authority_answer_names_the_v2_delegation(self):
        answer = model.authority()
        operative = answer.value["operative_delegation"]
        self.assertTrue(operative["resolved"])
        self.assertIn("DEL-CFV2-CEO-001",
                      [d["identifier"] for d in operative["in_force"]])
        self.assertIn("DEL-T4.4-CF-001",
                      [d["identifier"] for d in operative["superseded"]])

    def test_the_answer_grants_nothing(self):
        self.assertIsNone(model.authority().value["self_model_authority"])


if __name__ == "__main__":
    unittest.main()
