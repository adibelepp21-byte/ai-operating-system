# Bounded Exception Register

**Status:** Mechanism established, **applied to nothing.**
**Authority:** ADR-0009 (Approved) · MB-01 Stage 1 (P7-I48) · Stage 2 implementation (P7-I52)

---

## Purpose

AIOS conformance is fail-closed: a gate passes or it fails. Before this
mechanism, the corpus could express only two states for a known defect —
**zero**, or **one frozen exception** carried by a single
`unittest.expectedFailure` marker.

A marker asserts that a test fails. It does not assert *why*, *where*, or
*how widely*. If a second instance of the same defect appeared, the marker
would still be satisfied and the suite would still report green. The
tolerance is unbounded in extent while appearing bounded in form.

This mechanism supplies the missing third state: **these specific sites, and
no others.**

## Validation scope

Only the roots a register explicitly declares in its `scan_scope`. **A
register that declares no scope scans nothing and passes vacuously.** There
is no implicit scan of the repository, and none of `native_core/`.

## Assumptions

- Exception sites are discoverable by static analysis of Python source.
- A site's enclosing qualified name, and its ordinal within that scope, are
  stable under edits made elsewhere in the same file.
- An identifier is *resolvable* when it appears as a literal token in its
  governance register file.

## False-positive risk

Low for detection — matching is AST-based, not textual. Identity, however,
is deliberately strict: a site that changes scope, or whose ordinal shifts
because a sibling was added or reordered, is reported **both** as an absent
registration and as an unregistered site. That is intended. A structural
reorder is observable architectural change, and re-authorization is the
correct response (P7-I52 §7).

## Operational value

Converts an unbounded tolerance into an enumerated one, and makes the
difference between a defect that *moved* and a defect that was *fixed*
mechanically visible.

## Severity model

**Always failure.** There is no warning level. Ambiguity resolves to failure
in every case.

---

## Identity model

An exception site is identified by a four-tuple:

```
(relative module path, enclosing qualified name, exception class name,
 ordinal within enclosing scope)
```

**The line number is navigational metadata and is not part of identity.**
Line numbers churn on any edit above a site, which would make the register
unusable within a day.

| Event | Consequence |
|---|---|
| Edit above a site | Identity unchanged; only the recorded line drifts |
| Site moves to another function or module | Old identity absent **and** new identity unregistered — both fail |
| Site disappears | Registered identity absent — fails |
| Sibling site added or reordered | Ordinals shift; affected identities fail |
| Two identical registrations | Duplicate identity — fails |

## Fail-closed behaviour

| # | Condition | Result |
|---|---|---|
| 1 | Unregistered site inside declared scope | `UNREGISTERED_SITE` |
| 2 | Registered site exists, in scope, provenance resolves | **the only passing case** |
| 3 | Registered site no longer exists | `ABSENT_REGISTERED_SITE` |
| 4 | One identity registered more than once | `DUPLICATE_IDENTITY` |
| 5 | Register unparseable, or any field unknown or missing | `MALFORMED_REGISTER` |
| 6 | Entry outside every declared scan scope | `UNAUTHORIZED_EXPANSION` |
| 7 | Finding, decision, or authorizing act does not resolve | `UNRESOLVED_PROVENANCE` |

Case 6 is what makes the bound real: an entry that no declared scope covers
can never be checked against reality, so it could tolerate anything. The
verifier fails on it rather than ignoring it.

## Growth and authorization model

**The register cannot expand itself.** The verifier is read-only by
construction: the package exposes no serializer, and there is no `--update`,
`--fix`, `--accept`, or auto-registration of any kind. The loop
`code → verifier → register` cannot close.

Every entry must name three things, and all three must resolve:

- **`finding_id`** — must appear in the Finding Register.
- **`governance_decision_id`** — must appear in the Governance Decision Register.
- **`authorizing_act`** — must name a directive.

This is structural, not procedural: an entry cannot be added before the
governance record that admits it exists, because the verifier resolves the
reference and fails when it does not resolve.

**The register may shrink freely.** Removing an entry because the underlying
defect was repaired needs no governance act beyond the one that repaired it.
Growth is the direction that is gated.

## How an authorized registration would eventually be introduced

1. A finding is recorded in the Finding Register.
2. An Architect act admits it as a bounded exception, recorded in the
   Governance Decision Register.
3. A Maintenance Baseline authorizes the edit, naming the exact paths.
4. The entry is written by hand under that authorization, carrying the
   finding, the decision, and the authorizing act.
5. The scan scope covering it is declared in the same register.

No step in that sequence is performed by this tooling. Step 4 is a human
edit under an authorization; the verifier only checks the result.

---

## Scope of this baseline — read this before assuming applicability

**MB-01 establishes the mechanism. It applies it to nothing.**

- The shipped `register.json` is **empty**: no entries, no scan scope.
- **P7-F-2 is not registered.** Its five `KnowledgeError` sites remain
  exactly as they are, and its `expectedFailure` marker is untouched.
- **Baseline 04A is not modified**, and was explicitly out of MB-01's scope.
- The empty register **is not authorization for any future entry.** It is an
  empty instrument. Every entry that is ever added will require its own
  governance chain, as set out above.

Applying the mechanism to the Knowledge sites would be a separate act —
**MB-02** — which is not authorized and has not been opened. It would
require explicit authorization to modify frozen Baseline 04A under
GDR-0010 Ruling 3.

---

## Files

| Path | Deliverable | Contents |
|---|---|---|
| `register.py` | D-1 | Register format and strict read-only loading |
| `register.json` | D-2 | The register instance — **empty** |
| `identity.py` | D-3 | Identity model and AST site discovery |
| `provenance.py` | D-3 | Provenance resolution against governance registers |
| `verifier.py` | D-3 | The fail-closed verifier |
| `tests/` | D-4 | 26 tests, standard library only, synthetic fixtures |
| `README.md` | D-5 | This document |

## Running

```
python3 -m tools.bounded_exception
python3 -m unittest discover -s tools/bounded_exception/tests -t .
```

The verifier takes no arguments and writes nothing.
