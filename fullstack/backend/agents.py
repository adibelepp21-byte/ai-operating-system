"""Agent Instance registration through the application (FS-DP-07 **A2**).

```text
User → Create Agent → Backend → AIOS Agent Capability → Persist → Result
        (console / API)   (route)   (AgentDefinition, AgentInstance)   (store)
```

**What A2 is, and what it is not.** `FS-DP-07` defines A2 as *instance
registration only*: an operator holding the scope `aios.agent.register`
registers an Agent **Instance** of an **existing** governed Definition through
the canonical contracts. Definitions stay governed documents (owned by exactly
one Platform Division); the application reads them and never writes one. A3,
the Agent Factory, is not built here. Selected by the delegated decision
`ACT-008-DG-01` (Register `§101`) under `ACT-CC-POST-P13-AIOS-FULL-STACK-008`
`§7.2`, which is also the authority instrument the package required
(`FS-DP-07` `R2.5`): it extends the registration that `FD-P11-001 §7` allowed
for P11-W4 to the application. `tools/agent_instance_registry.py` belongs to
that earlier, scoped authority and is **not** imported or reused.

**The canonical mechanism.** The identity is `native_core`'s `AgentInstance`
(INV-3: exactly one Definition), built from the `AgentDefinition` contract
parsed from the governed document. Both are immutable data contracts with no
behaviour. The organizational facts the contract deliberately omits (who
registered it, on whose authority, what it may use, its lifecycle) live in an
application record beside it, in the append-only partition `fullstack-agents`.

**`AGENT INSTANCE ≠ AUTHORITY`.** A registration grants nothing: the record
says so (`grants_authority: false`) and no method here answers whether an
instance may do anything. The permitted capabilities are bounded by the
Definition's implemented ones and never exceed them.

**Append-only.** A registration is never edited or deleted. Two concurrent
requests for one key can both pass the uniqueness check; the **first record in
append order is the registration** and the other request is refused (409) after
the fact. The refused record stays in the partition, inert, because nothing in
the store is deleted; reads ignore it.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from native_core.core.agent.definition import AgentDefinition, InvalidAgentDefinition
from native_core.core.agent.instance import AgentInstance, InvalidAgentInstance
from native_core.core.infrastructure import StorageFacility

AGENTS_PARTITION = "fullstack-agents"
#: The registration record format; successor formats are read beside it (FS-04 `§4`).
AGENT_FORMAT = "fullstack.agent-instance/1"
INSTANCE_KEY = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")
ORGANIZATION = Path("docs/architecture/organization")
REGISTERED = "REGISTERED"

#: Why the application may register instances at all. Fixed in code, so a
#: request cannot name its own authority.
AUTHORITY = {"instrument": "ACT-CC-POST-P13-AIOS-FULL-STACK-008", "section": "7.2",
             "decision": "ACT-008-DG-01", "package": "FS-DP-07", "option": "A2"}


class InvalidAgentRequest(ValueError):
    """The registration request is malformed or names something that does not exist."""


class DuplicateInstance(RuntimeError):
    """An instance with this identity is already registered."""


_LINK_TEXT = re.compile(r"\[`([a-z0-9.\-]+)`\]")
_CAPABILITY_LINK = re.compile(r"\]\(\.\./capabilities/([a-z0-9\-]+)\.md\)")


def _section(text: str, heading: str) -> str:
    match = re.search(rf"(?ms)^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text)
    return match.group(1) if match else ""


def _definition_from(path: Path) -> Optional[Tuple[AgentDefinition, str]]:
    """One governed document → (contract, status), or None if it cannot be read
    as a complete Definition. An unreadable document is simply not registrable."""
    text = path.read_text(encoding="utf-8")
    version = re.search(r"(?m)^- \*\*Version:\*\*\s*(.+?)\s*$", text)
    status = re.search(r"(?m)^- \*\*Status:\*\*\s*(.+?)\s*$", text)
    capabilities = tuple(dict.fromkeys(_CAPABILITY_LINK.findall(_section(text, "Implemented Capability"))))
    if not (version and status and capabilities and INSTANCE_KEY.match(path.stem)):
        return None
    skills = tuple(dict.fromkeys(k for k in _LINK_TEXT.findall(_section(text, "Permitted Skills"))
                                 if k.startswith("skill.")))
    workflows = tuple(dict.fromkeys(k for k in _LINK_TEXT.findall(_section(text, "Permitted Workflows"))
                                    if k.startswith("workflow.")))
    try:
        definition = AgentDefinition(
            agent_definition_key=path.stem, agent_definition_version=version.group(1),
            owning_department_key=path.parents[1].name, implemented_capabilities=capabilities,
            specified_skills=skills, specified_workflows=workflows)
    except InvalidAgentDefinition:
        return None
    return definition, status.group(1)


class GovernedDefinitions:
    """The Agent Definitions that exist as governed documents. Read-only: the
    application never authors, edits or retires one (that is A3, not built)."""

    def __init__(self, repo_root: Path):
        self._root = Path(repo_root) / ORGANIZATION

    def active(self) -> Dict[str, AgentDefinition]:
        found: Dict[str, AgentDefinition] = {}
        for path in sorted(self._root.glob("*/agent-definitions/*.md")):
            read = _definition_from(path)
            if read is not None and read[1].lower().startswith("active"):
                found[read[0].agent_definition_key] = read[0]
        return found

    def describe(self) -> List[dict]:
        return [{"definition": d.agent_definition_key, "version": d.agent_definition_version,
                 "owning_department": d.owning_department_key,
                 "implemented_capabilities": list(d.implemented_capabilities),
                 "specified_skills": list(d.specified_skills),
                 "specified_workflows": list(d.specified_workflows)}
                for d in self.active().values()]


@dataclass(frozen=True)
class RegistrationRequest:
    definition: str
    instance_key: str
    capabilities: Tuple[str, ...]


def parse_request(body: dict) -> RegistrationRequest:
    unknown = set(body) - {"definition", "instance_key", "capabilities"}
    if unknown:
        raise InvalidAgentRequest(f"unknown field(s): {sorted(unknown)}")
    definition, key, capabilities = (body.get("definition"), body.get("instance_key"),
                                     body.get("capabilities"))
    if not isinstance(definition, str) or not definition:
        raise InvalidAgentRequest("definition must name an existing governed Agent Definition")
    if not isinstance(key, str) or not INSTANCE_KEY.match(key):
        raise InvalidAgentRequest("instance_key must be 3-64 characters: lower-case letters, "
                                  "digits and hyphens, starting with a letter or digit")
    if (not isinstance(capabilities, list) or not capabilities
            or not all(isinstance(c, str) and c for c in capabilities)):
        raise InvalidAgentRequest("capabilities must be a non-empty list of capability keys "
                                  "the Definition implements")
    if len(set(capabilities)) != len(capabilities):
        raise InvalidAgentRequest("a capability is named more than once")
    return RegistrationRequest(definition, key, tuple(capabilities))


class AgentRegistry:
    """Registrations over the shared store. Holds no state of its own."""

    def __init__(self, storage: StorageFacility, definitions: GovernedDefinitions,
                 runtime_id: Optional[str] = None,
                 clock=lambda: datetime.now(timezone.utc)):
        self._storage, self._definitions = storage, definitions
        self._runtime_id, self._clock = runtime_id, clock

    # -- reads ----------------------------------------------------------------

    def _records(self) -> List[Tuple[bytes, dict]]:
        """First record per instance key, in append order. A later record for
        the same key is an inert refused duplicate and is skipped."""
        seen, out = set(), []
        for raw in self._storage.read(AGENTS_PARTITION):
            record = json.loads(raw.decode("utf-8"))
            if record.get("instance_key") in seen:
                continue
            seen.add(record.get("instance_key"))
            out.append((raw, record))
        return out

    def instances(self) -> List[dict]:
        return [record for _, record in self._records()]

    def instance(self, key: str) -> Optional[dict]:
        return next((r for r in self.instances() if r["instance_key"] == key), None)

    # -- the one write ----------------------------------------------------------

    def register(self, request: RegistrationRequest, subject: str) -> dict:
        definition = self._definitions.active().get(request.definition)
        if definition is None:
            raise InvalidAgentRequest(
                f"no active governed Agent Definition {request.definition!r}; the application "
                "registers Instances of existing Definitions and never creates a Definition")
        outside = [c for c in request.capabilities if c not in definition.implemented_capabilities]
        if outside:
            raise InvalidAgentRequest(
                f"capabilities not implemented by {definition.agent_definition_key!r}: "
                f"{outside}; an Instance never exceeds its Definition")
        if self.instance(request.instance_key) is not None:
            raise DuplicateInstance(f"instance {request.instance_key!r} is already registered")
        try:
            identity = AgentInstance(agent_instance=request.instance_key,
                                     agent_definition=definition)   # INV-3
        except InvalidAgentInstance as error:
            raise InvalidAgentRequest(str(error)) from error
        record = {
            "format": AGENT_FORMAT,
            "instance_key": identity.agent_instance,
            "definition": {"key": definition.agent_definition_key,
                           "version": definition.agent_definition_version,
                           "owning_department": definition.owning_department_key},
            "implemented_capabilities": list(definition.implemented_capabilities),
            "permitted_capabilities": list(request.capabilities),
            "created_by": subject, "accountable_to": subject,
            "authority": dict(AUTHORITY),
            "lifecycle": REGISTERED,
            "grants_authority": False,
            "registered_at": self._clock().isoformat(timespec="milliseconds"),
            "runtime_id": self._runtime_id,
        }
        raw = json.dumps(record, sort_keys=True, separators=(",", ":")).encode("utf-8")
        self._storage.append(AGENTS_PARTITION, raw)
        first = next((r for r in self._storage.read(AGENTS_PARTITION)
                      if json.loads(r.decode("utf-8")).get("instance_key") == request.instance_key),
                     None)
        if first != raw:        # a concurrent request registered this key first
            raise DuplicateInstance(f"instance {request.instance_key!r} is already registered")
        return record
