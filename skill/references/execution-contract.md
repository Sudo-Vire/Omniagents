# Execution contract

This is a conversational contract for a procedural skill, not a validated API. The host agent must check the stated inputs and report the output fields; this repository does not enforce them in an orchestration runtime.

## Input

| Field | Type | Requirement and default | Validation |
|---|---|---|---|
| `objective` | String | Required; no default | Must be non-empty and describe the requested outcome |
| `context` | String | Optional; defaults to empty | Include only relevant, authorized repository context |
| `constraints` | List of strings | Optional; defaults to `[]` | State applicable scope, privacy, permission, and deadline limits |
| `acceptance_criteria` | List of strings | Optional; defaults to `[]` | Use measurable checks when available |

Ask for clarification only when missing information blocks safe or correct execution. Do not invent timeouts, budgets, or agent limits.

## Output

Return these fields in a concise structured summary:

| Field | Type | Requirement and default |
|---|---|---|
| `status` | String enum | Required; `completed`, `partial`, `blocked`, `failed`, or `cancelled` |
| `result` | String | Required; findings or delivered work, separating verified facts from agent claims |
| `errors` | List of `{code: string, message: string}` | Defaults to `[]`; never include secrets |
| `artifacts` | List of strings | Defaults to `[]`; include only existing paths or URLs |
| `warnings` | List of strings | Defaults to `[]`; include limitations and unverified or partial results |
| `metrics` | Object | Omit unless the host reports measured values |

This is a conversational response shape, not a JSON API. Example only; it is not an execution record:

```yaml
status: partial
result: "The available instructions identify relevant agents, but the repository has no callable orchestration runtime."
errors: []
artifacts: []
warnings:
  - "Delegation depends on native host tools and was not performed by this repository."
```

## Error codes

- `INVALID_INPUT`: the objective or constraints are insufficient or contradictory.
- `DEPENDENCY_MISSING`: a required downloaded asset group is absent or empty.
- `HOST_DELEGATION_UNAVAILABLE`: the host has no suitable agent-delegation tool.
- `AGENT_FAILED`: a delegated task failed; preserve useful partial output.
- `APPROVAL_REQUIRED`: an action needs authorization that has not been granted.
- `TIMEOUT_UNENFORCED`: a requested time limit cannot be applied by the host.

## Partial results

Use `partial` when some work is verified but a delegated task, test, or acceptance criterion remains incomplete. Use `blocked` when no safe next step is available without user input or a missing prerequisite. Do not convert errors into success-shaped output.
