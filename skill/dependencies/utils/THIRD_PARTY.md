# Third-party content

Everything under `dependencies/utils/` comes from the upstream projects below and keeps its own license. The repository's own license covers only the original Omniagents work (see `LICENSE` and `NOTICE` in the repository root).

"Content check" records what was compared against the upstream default branch on 2026-11-04. It is a spot check of each skill's `SKILL.md` (and of `LICENSE` for `agency-agents`), not a byte-for-byte comparison of every file. "Differs" means the local copy is not identical to upstream today (a different version or local changes); local modifications have not been itemized.

| Utility (relative to `dependencies/utils/`) | Upstream | License | License evidence | Content check |
|---|---|---|---|---|
| `agents/agency-agents` | [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) | MIT | `LICENSE` in the folder, identical to upstream | Only `LICENSE` compared |
| `agents/claude-subagents` | [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | MIT | `LICENSE` in the folder | Downloaded at a pinned commit (`sources.json`) |
| `skills/superpowers` | [obra/superpowers](https://github.com/obra/superpowers) | MIT | `LICENSE` in the folder | Downloaded at a pinned commit (`sources.json`) |
| `skills/andrej-karpathy-skills` | [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) | MIT (declared in the skill's `license:` frontmatter; upstream has no `LICENSE` file) | Skill frontmatter | `karpathy-guidelines/SKILL.md` identical |
| `skills/find-skills` | [vercel-labs/skills](https://github.com/vercel-labs/skills) (`skills/find-skills`) | MIT | `LICENSE` in the folder | `SKILL.md` identical |
| `skills/grill-me` | [mattpocock/skills](https://github.com/mattpocock/skills) (`skills/productivity/grill-me`) | MIT | `LICENSE` in the folder | `SKILL.md` identical |
| `skills/graphify` | [safishamsi/graphify](https://github.com/safishamsi/graphify) | Apache-2.0 | `LICENSE` in the folder | `SKILL.md` differs from upstream `graphify/skill.md` (not itemized) |
| `skills/gsd` | [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done) | MIT | `LICENSE` in the folder | Upstream location of the files not identified; origin inferred from the folder and its `author: GSD Project` metadata |
| `skills/ui-ux-pro-max` | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | MIT | `LICENSE` in the folder | `SKILL.md` differs from upstream (not itemized) |
| `skills/vercel/*` (7 skills) | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | MIT (stated in its README "License" section; upstream has no `LICENSE` file) | Upstream README | `vercel-cli-with-tokens`, `vercel-composition-patterns`, `vercel-react-best-practices`, `vercel-react-native-skills` identical; `deploy-to-vercel` and `vercel-react-view-transitions` differ; `vercel-optimize` not compared |
| `skills/web-design-guidelines`, `skills/writing-guidelines` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | MIT (same note as above) | Upstream README | `SKILL.md` identical |
| `skills/ciberseguridad/*` | [usestrix/strix](https://github.com/usestrix/strix) | Apache-2.0 | `LICENSE` in the folder | `application-security-testing/SKILL.md` identical; others not compared |
| `tools/mcp-sequential-thinking` | Configuration templates only. The server is the npm package [`@modelcontextprotocol/server-sequential-thinking`](https://www.npmjs.com/package/@modelcontextprotocol/server-sequential-thinking) from [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | MIT, with a transition to Apache-2.0 (see the upstream `LICENSE`) | Not vendored; npm installs it on first launch | n/a |

## Rules for changes

- Add a row here when you add a utility, and keep the upstream `LICENSE` inside its folder when the upstream has one.
- Utilities pinned in `sources.json` (everything marked "pinned" below) are still committed, so installing works offline; the pin lets `fetch_utils.py` restore or refresh them and `fetch_utils.py --verify` (also run weekly in CI) confirm the commit still exists. Utilities that differ from upstream, and `agents/agency-agents` (used by the framework), are deliberately not pinned.
- Do not add a utility whose license does not allow redistribution; pin it in `sources.json` instead so users download it themselves.
- Apache-2.0 content: keep the `LICENSE` and any upstream notices, and mark modified files as changed.
