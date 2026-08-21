"""
Workflow boundary exceptions — fail closed, never silent (PR-4; workflow_spec
§11).

workflow_spec §11 [E]: *"Fail closed (PR-4): on missing authorization or unmet
precondition, a Workflow halts rather than proceeds; a step that cannot be
Traced is not completed."* Every error here exists to make that halt explicit
at the point of failure rather than letting a composition proceed partially.

`DirectCollaborationForbidden` is the boundary's most load-bearing error. INV-13
[E] states that *"no Agent Instance may collaborate directly with another Agent
Instance outside of a shared Workflow, Knowledge, or scoped Memory."* Freeze §6
records the forbidden direction as *"direct Instance↔Instance"*, and Freeze AD-9
names free agent-to-agent delegation a rejected anti-pattern. The primary
defence is structural — this package offers no type that can express such an
edge — and this exception is the second line, raised where a caller attempts
coordination that names no Workflow.

Deliberately ABSENT: no exception for an empty Workflow declaration. Domain
Model §7 invariant 15 [E] and ADR-0007 make zero declared Workflows *"a valid
architectural state"*. Raising on one would invent a minimum cardinality the
ratified model does not impose.

Dependencies: stdlib only (INV-12).
"""


class WorkflowError(Exception):
    """Base for every failure raised by the Workflow boundary."""


class InvalidWorkflow(WorkflowError, ValueError):
    """A Workflow contract is structurally invalid.

    Raised at construction, before the value can travel anywhere — structural
    fail-closed validation only, never domain logic and never authority
    evaluation (PR-3)."""


class InvalidWorkflowStep(WorkflowError, ValueError):
    """A composition step is structurally invalid.

    A step is an Agent-Instance action. A step naming no acting Agent Instance
    could produce no Trace, and INV-4 requires exactly one Trace per action —
    so such a step is rejected rather than admitted untraceable."""


class InvalidWorkflowComposition(WorkflowError, ValueError):
    """A composition is structurally invalid.

    Malformed, not empty: ordering, duplication, and membership are checked;
    a composition with no steps is a separate, valid state."""


class InvalidWorkflowDeclaration(WorkflowError, ValueError):
    """An Agent Definition's Workflow declaration is structurally invalid.

    Invalid means malformed — not empty. Domain Model §7 invariant 15 and
    ADR-0007 make an empty declaration a valid state."""


class UnresolvedWorkflow(WorkflowError, LookupError):
    """A declared Workflow could not be resolved.

    workflow_spec §11 [E]: the composition halts rather than proceeds. This
    boundary raises; it does not substitute a default, retry, or fall back."""


class DuplicateWorkflowDeclaration(WorkflowError, ValueError):
    """The same Workflow key was declared more than once by one Definition.

    A repeated key makes the declared set ambiguous, which fails closed rather
    than resolving to an arbitrary entry."""


class DirectCollaborationForbidden(WorkflowError, ValueError):
    """Coordination was attempted outside a Workflow (INV-13).

    INV-13 [E]: *"No Agent Instance may collaborate directly with another Agent
    Instance outside of a shared Workflow, Knowledge, or scoped Memory."*
    Workflow is the sole channel this boundary owns; Knowledge and scoped
    Memory are owned elsewhere and are not reachable from here."""


class InvalidWorkflowRealization(WorkflowError, ValueError):
    """Raised when a Workflow's Capability realization cannot be constructed
    accountably.

    Domain Model §4 [E] and Freeze §6 fix `Workflow realizes Capability`. Fail
    closed (PR-4): a malformed reference, a non-`CapabilityRef` entry, or a
    `capability_key` realized twice is refused rather than coerced. An **empty**
    realization is *not* an error — no canonical source states a cardinality for
    this edge, so none is imposed."""
