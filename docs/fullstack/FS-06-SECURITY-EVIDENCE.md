# FS-06 — Security & Authority Integration: Evidence

| Field | Value |
|---|---|
| **Stage** | FS-06 Security & Authority Integration (Act `§17`) |
| **Code** | `fullstack/backend/security.py`; the request sequence in `api.py`; `docs_tool.py` |
| **Tests** | `fullstack/tests/test_security.py` (17) |
| **Reserved** | the authentication mechanism and identity: **FS-DP-02**, Architect-reserved (D2) |

## The two flows of Act `§17`

```text
User → Identity → Authentication → Authorization → Capability → AIOS
         └─ FS-DP-02 ─┘   └─ scope rule ─┘   └─ Tool governance, Workflow lifecycle
User → Role → Permission → Policy → Action → Audit
        └ principal's scopes ┘ └ route scope ┘ └ audit ledger
```

- **Identity and Authentication** stop at a port. The shipped
  implementation, `NoAuthenticator`, authenticates nobody.
- **Authorization** is one rule, `authorize(principal, scope)`, applied to
  every route. Unknown scope names fail closed.
- **Capability** stays in AIOS. A Tool is reached only by a Workflow step,
  through `ToolInvocationGovernance`; no route invokes a Tool.
- **Audit** records every protected decision, allowed or refused.

## Verification

| Control | Evidence |
|---|---|
| Production posture: every protected route answers 401; nothing runs | `test_every_protected_route_answers_401` |
| Missing or wrong credential = nobody | `test_no_credential_or_a_wrong_one_is_nobody` |
| Observer reads, cannot act or audit | `test_the_observer_can_read_but_not_act_or_audit` |
| Least privilege: a run-only principal cannot read | `test_least_privilege_a_run_only_principal_cannot_read` |
| A failing authenticator fails closed | `test_a_failing_authenticator_authenticates_nobody` |
| Unknown scope refused; unknown scope cannot be granted | `test_the_rule_fails_closed_on_an_unknown_scope` |
| Every decision audited, with no header or credential | `Audit` |
| No credential in any record, response or shipped file | `Secrets` (NC-10) |
| Security headers on every response | `test_api_responses_carry_the_security_headers` |
| Tool confined to `docs/`: traversal, absolute, hidden, symlink escape, wrong suffix, oversize, non-UTF-8 all refused | `ToolConfinement` |
| Frontend is not the authority | browser check *"an observer cannot run a workflow even with the UI bypassed"* |

## Exit determination (`§17`)

| Criterion | Result |
|---|---|
| Authentication verified | **BLOCKED (FS-DP-02).** The fail-closed posture is verified; no mechanism exists to verify |
| Authorization verified | met |
| Least-privilege boundaries verified | met |
| Secrets not exposed | met |
| Audit evidence exists | met |
| Unauthorized actions are rejected | met |
| Security tests pass | 17 / 17 |
| Security-sensitive failure modes tested | met: broken authenticator, stopped Runtime, corrupt record, internal error |

**FS-06: EXIT MET except authentication, which is Architect-reserved
(FS-DP-02).** Act `§28`: *"unrelated authorized work shall continue"*.
FS-07 proceeds, and its evidence says which authenticator it used.
