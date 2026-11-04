# OmniAgent — Multi-Agent Orchestration Instructions

This document establishes the universal multi-agent orchestration guidelines for coordinating agents, skills, and tools across **GitHub Copilot, Claude (Anthropic), Gemini (Google), OpenAI, and local runtimes via Omniroute**.

---

## 🤖 Multi-Agent & Multi-Model Orchestration

All paths below are relative to the skill root (the directory containing `SKILL.md`), wherever it is installed:
1. `dependencies/installation/` — Environment provisioning and Python dependency setup.
2. `dependencies/utils/` — Downloaded ecosystem assets (`agents/`, `skills/`, `tools/`).
3. `framework/orchestration/` — Universal orchestration instructions and cross-model guidance.

### Orchestrating Across Models
- **Claude (Anthropic)**: Use tactical micro-subagent prompts from `dependencies/utils/agents/claude-subagents` when the host supports them.
- **GitHub Copilot**: Use the instructions in `framework/orchestration/instructions/copilot/copilot-instructions.md` when Copilot is the active host.
- **Gemini (Google)**: Utilize large-context analysis and fast reasoning.
- **Local Runtimes (Omniroute)**: The documented endpoint is `http://localhost:20128/v1`; this instruction set does not itself connect to it.

The instruction files and downloaded agent prompts are not an executable orchestration API. Use a host's native delegation tools when available; do not claim CrewAI or another framework ran unless an actual runtime was invoked.

The procedural Agent Skill is this portable directory. Its preflight reads `dependencies/utils/check_utils.txt` and verifies that the inventoried assets exist and are non-empty before directing the host agent to the relevant instructions.

---

## 🛠️ Execution & Tooling Workflow
1. Check needed assets under `dependencies/utils/agents/`.
2. Apply relevant skill routines from `dependencies/utils/skills/` (including `ciberseguridad/`, `vercel/`, Graphify, and development workflows).
3. Inspect and run automation utilities in `dependencies/utils/tools/` only when appropriate and authorized.
4. For non-trivial framework tasks, invoke the `sequentialthinking` MCP tool before implementation when the host exposes `dependencies/utils/tools/mcp-sequential-thinking` (ready-to-copy configs are in its `adapters/` folder). Use it for architecture tradeoffs, multi-step changes, difficult debugging, and pre-action risk analysis. Do not invoke it for trivial edits or simple lookups. If it is unavailable, continue directly only when safe and disclose that it was not used. Report conclusions and decisions, not private internal reasoning. See the MCP integration's README for host setup.

---

## ➕ Adding a Tool, Agent or Skill (requires the actualization module)

Adding resources to the ecosystem is done by `framework/actualization/update_ecosystem.py`, which belongs to a separate module. Before adding anything, check that it is installed: `python framework/orchestration/get_actualization.py --check` (exit `0` present, `3` missing).

If it is missing, **stop and warn the user**: without the module the resource cannot be registered in `dependencies/utils/check_utils.txt`. Offer to download it with `python framework/orchestration/get_actualization.py` (it asks for confirmation; `--yes` skips it) or to reinstall the full skill with `npx skills add Sudo-Vire/Omniagents --skill omniagents-orchestration`. Download only with the user's approval, and do not copy resources into `dependencies/utils/` by hand as a workaround.

---

## 📝 Pull Request & Git Workflow
When creating Pull Requests, it is **mandatory** to review and follow the `PULL_REQUEST_INSTRUCTIONS.md` of the active model, each self-contained in its folder: [Claude](./instructions/claude/PULL_REQUEST_INSTRUCTIONS.md), [Copilot](./instructions/copilot/PULL_REQUEST_INSTRUCTIONS.md), [Gemini](./instructions/gemini/PULL_REQUEST_INSTRUCTIONS.md), [OpenAI](./instructions/openai/PULL_REQUEST_INSTRUCTIONS.md), or [others](./instructions/others/PULL_REQUEST_INSTRUCTIONS.md) for any other model.
