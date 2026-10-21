# OmniAgent — Multi-Agent Orchestration Instructions

This document establishes the universal multi-agent orchestration guidelines for coordinating agents, skills, and tools across **GitHub Copilot, Claude (Anthropic), Gemini (Google), OpenAI, and local runtimes via Omniroute**.

---

## 🤖 Multi-Agent & Multi-Model Orchestration

OmniAgent separates core components into three distinct modules:
1. `installation/` — Autonomous setup, environment provisioning, and dependency resolution.
2. `pre-downloaded/` — Pre-downloaded ecosystem assets (`agents/`, `skills/`, `tools/`).
3. `orchestration/` — Universal orchestration instructions and cross-model guidance.

### Orchestrating Across Models
- **Claude (Anthropic)**: Use tactical micro-subagents (`pre-downloaded/agents/claude-subagents`) and reasoning rules for complex code refactoring.
- **GitHub Copilot**: Leverage Copilot SDK / VS Code assistant instructions (`orchestration/copilot-instructions.md`) for editor-native workflows.
- **Gemini (Google)**: Utilize large-context analysis and fast reasoning.
- **Local Runtimes (Omniroute)**: Connect via `http://localhost:20128/v1` for zero-cost, private inference.

---

## 🛠️ Execution & Tooling Workflow
1. Load pre-downloaded agent prompts from `pre-downloaded/agents/`.
2. Apply skill routines from `pre-downloaded/skills/` (including Strix security scans, Graphify graph generation, and Karpathy dev routines).
3. Execute automation utilities in `pre-downloaded/tools/`.
