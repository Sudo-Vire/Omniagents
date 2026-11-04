# Troubleshooting

| Condition | Response |
|---|---|
| Dependency check cannot find the skill directory | Run the check from the skill root or pass `--skill-root <path>`. Do not guess a different path. |
| An asset group is missing or empty | Report `DEPENDENCY_MISSING`; inspect `dependencies/installation/` and ask before installing or downloading anything. The installer does not fetch asset collections. If the utility is pinned in `dependencies/utils/sources.json`, offer `python <skill-root>/scripts/fetch_utils.py` (add `--force` to redownload); run it only with approval. |
| `fetch_utils.py` fails | Check network access to `codeload.github.com`, that the `ref` in `sources.json` is a full commit SHA, and that the target folder is writable. A utility that is not in `sources.json` is vendored and must be restored from the repository, not downloaded. |
| The exact requested agent or skill is absent | Do not substitute an unrelated prompt. Report the missing resource and continue directly only if safe and useful. |
| The host has no delegation tool | Report `HOST_DELEGATION_UNAVAILABLE`; use one agent directly if that can satisfy the request, or ask how to proceed. |
| A delegated agent fails | Preserve verified partial output, report `AGENT_FAILED`, and do not retry an action with external side effects unless it is safe and authorized. |
| A requested timeout or budget cannot be enforced | Report `TIMEOUT_UNENFORCED`; treat the limit as guidance, not a guarantee. |
| The local gateway is offline | This skill does not require the gateway. Do not start or configure it unless requested. |
| The Sequential Thinking MCP is reported as not configured | Ask the user whether to activate it manually, automatically, or not at all (`python <skill-root>/scripts/check_mcp.py`). Without it, continue directly when safe and disclose that `sequentialthinking` was not used. |
| A request would install, publish, commit, push, or modify an external system | Stop and obtain the required user authorization. |

Report whether the issue blocked all work or only left a partial result. Do not claim that a test, agent, or integration ran when it did not.
