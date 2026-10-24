# Master Copilot Router & Execution Rules

This repository uses a Hyper-Modular AI Context architecture. You must follow these root principles automatically in every prompt, refactoring, or code development.

## 🚨 CRITICAL BEHAVIOR (Main Rule)
You must ALWAYS execute tasks following this strict communication order:
1. **Think out loud** inside your reasoning process before responding.
2. **Present the current phase plan** to the user.
3. **Ask explicitly**: "Is this correct or would you like to make any changes?"
4. **Wait** for explicit user approval before executing ANY code or moving to the next phase.

---

## 🗺️ Context Map & Modular Documentation
When executing a task, you must index and read the specialized file corresponding to your current domain:

- **Core Architecture & Tech Stack:** Refer to [@ARCHITECTURE.md](./docs/ARCHITECTURE.md)
- **SDLC & Execution Workflow:** Refer to [@SDLC_WORKFLOW.md](./docs/SDLC_WORKFLOW.md)
- **Operational Philosophy:** Refer to [@PHILOSOPHY.md](./docs/PHILOSOPHY.md)
- **Agent Catalogs (`agency-agents` & `claude-subagents`):** Refer to [@AGENTS_CATALOG.md](./docs/AGENTS_CATALOG.md)
- **Local Model Gateway & Endpoints:** Refer to [@GATEWAY.md](./docs/GATEWAY.md)
- **Git Standards & Versioning:** Refer to [@GIT_AND_VERSIONING.md](./docs/GIT_AND_VERSIONING.md)
- **Tooling, Testing & Validation (Browser-Use, Ruff, Biome):** Refer to [@TOOLING_AND_VALIDATION.md](./docs/TOOLING_AND_VALIDATION.md)

---

## ⚡ Simplified Flow (For Minor Tasks Only)
If a task is classified as **Simple** (under 10 lines, obvious bugfix, or direct query):
1. Propose the minimal surgical change (YAGNI).
2. Apply linters: `ruff check/format` (Python) or `biome check` (JS/TS).
3. Commit with Conventional Commits.
