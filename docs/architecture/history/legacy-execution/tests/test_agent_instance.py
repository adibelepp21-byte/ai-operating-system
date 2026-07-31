"""
Dedicated unit tests for execution/agent_instance.py.

Foundation Test Coverage Hardening phase.

Run with:
    python3 -m unittest discover -s execution/tests
"""

import sys
import unittest
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from execution import agent_instance


@dataclass(frozen=True)
class _FakeAgentDefinition:
    name: str = "Fake Agent"
    version: str = "1.0"


@dataclass(frozen=True)
class _FakeRuntime:
    canonical_key: str = "runtime.fake"


class SpawnTest(unittest.TestCase):
    def test_spawn_copies_definition_and_runtime_identity(self):
        instance = agent_instance.spawn(_FakeAgentDefinition(), _FakeRuntime())
        self.assertEqual(instance.agent_definition_name, "Fake Agent")
        self.assertEqual(instance.agent_definition_version, "1.0")
        self.assertEqual(instance.runtime_key, "runtime.fake")

    def test_spawn_status_starts_as_spawned(self):
        instance = agent_instance.spawn(_FakeAgentDefinition(), _FakeRuntime())
        self.assertEqual(instance.status, "spawned")

    def test_spawn_generates_unique_instance_ids(self):
        i1 = agent_instance.spawn(_FakeAgentDefinition(), _FakeRuntime())
        i2 = agent_instance.spawn(_FakeAgentDefinition(), _FakeRuntime())
        self.assertNotEqual(i1.instance_id, i2.instance_id)
        self.assertTrue(i1.instance_id.startswith("instance-"))


class LifecycleTest(unittest.TestCase):
    def test_activate_transitions_to_active(self):
        instance = agent_instance.spawn(_FakeAgentDefinition(), _FakeRuntime())
        instance.activate()
        self.assertEqual(instance.status, "active")

    def test_terminate_transitions_to_terminated(self):
        instance = agent_instance.spawn(_FakeAgentDefinition(), _FakeRuntime())
        instance.activate()
        instance.terminate()
        self.assertEqual(instance.status, "terminated")

    def test_terminate_without_activate_still_works(self):
        instance = agent_instance.spawn(_FakeAgentDefinition(), _FakeRuntime())
        instance.terminate()
        self.assertEqual(instance.status, "terminated")

    def test_spawned_at_is_a_real_timestamp(self):
        import time
        before = time.time()
        instance = agent_instance.spawn(_FakeAgentDefinition(), _FakeRuntime())
        after = time.time()
        self.assertTrue(before <= instance.spawned_at <= after)


if __name__ == "__main__":
    unittest.main()
