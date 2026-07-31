"""
Skill boundary exceptions — fail closed, never silent (PR-4; skill_spec §11).

skill_spec §11 [E]: *"Fail closed (PR-4): a Skill that cannot be resolved/used
causes the invoking action to halt accountably, not to proceed silently."*
Every error here exists to make that halt explicit at the point of failure.

Deliberately ABSENT: no exception for an empty Skill declaration. Domain Model
§7 invariant 15 [E] states that *"an empty Skill declaration ... represent[s] a
valid architectural state"*, and ADR-0007 resolved the question. Zero declared
Skills is correct, not an error, and raising on it would invent a minimum
cardinality the ratified model does not impose.

Dependencies: stdlib only (INV-12).
"""


class SkillError(Exception):
    """Base for every failure raised by the Skill boundary."""


class InvalidSkill(SkillError, ValueError):
    """A Skill contract is structurally invalid.

    Raised at construction, before the value can travel anywhere — structural
    fail-closed validation only, never domain logic and never authority
    evaluation (PR-3)."""


class InvalidSkillDeclaration(SkillError, ValueError):
    """An Agent Definition's Skill declaration is structurally invalid.

    Invalid means malformed — not empty. Domain Model §7 invariant 15 makes an
    empty declaration a valid state."""


class UnresolvedSkill(SkillError, LookupError):
    """A declared Skill could not be resolved.

    skill_spec §11 [E]: the invoking action halts accountably rather than
    proceeding silently. This boundary raises; it does not substitute a
    default, retry, or fall back."""


class DuplicateSkillDeclaration(SkillError, ValueError):
    """The same Skill key was declared more than once by one Agent Definition.

    A declaration set names each Skill at most once; a repeated key makes the
    declared set ambiguous, which fails closed rather than resolving to an
    arbitrary entry."""
