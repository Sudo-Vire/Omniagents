# Orchestration Module (`framework/orchestration/`)

This module contains universal and model-specific orchestration instructions, rules, and configuration templates for OmniAgent, organized by LLM runtime under `instructions/`. These are declarative instructions; this repository does not include a callable multi-agent orchestration runtime.

---

## 📂 Subfolder Layout (`instructions/`)

Each model folder is **self-contained**: its files only link to files inside that same folder, so a host can load just its own folder. Shared policy lives in [AGENT_INSTRUCTIONS.md](./AGENT_INSTRUCTIONS.md), which points to each model's folder. Every folder also carries its own `PULL_REQUEST_INSTRUCTIONS.md` and architecture notes.

1. **Claude (`framework/orchestration/instructions/claude/`)**:
   - Contains the Claude master instructions (`CLAUDE.md`), `ARCHITECTURE.md` and `PULL_REQUEST_INSTRUCTIONS.md`.
2. **GitHub Copilot (`framework/orchestration/instructions/copilot/`)**:
   - Contains the definitive master rulebook (`copilot-instructions.md`), `PULL_REQUEST_INSTRUCTIONS.md` and the `docs/` modules it links.
3. **Google Gemini (`framework/orchestration/instructions/gemini/`)**:
   - Contains system configuration (`gemini-config.json`), master instructions (`GEMINI.md`), `sub-rules-ecosystem.md`, `docs/`, `sub-rules/` and `PULL_REQUEST_INSTRUCTIONS.md`.
4. **OpenAI / GPT (`framework/orchestration/instructions/openai/`)**:
   - Contains system instructions (`OPENAI.md`), the Assistant API payload (`assistant-instructions.json`), `docs/`, `sub-rules/` and `PULL_REQUEST_INSTRUCTIONS.md`.
5. **Others / Universal (`framework/orchestration/instructions/others/`)**:
   - Contains universal master instructions (`agents.md`), `ARCHITECTURE.md` and `PULL_REQUEST_INSTRUCTIONS.md` for any other LLM models (Llama, Mistral, Grok, etc.).

Paths inside the JSON configs are relative to the JSON file. The ecosystem updater (`framework/actualization/update_ecosystem.py`) appends integration blocks to the files of every model listed above.

## Using orchestration without the actualization module

`framework/orchestration/` works on its own. Adding a tool, agent or skill is the one thing that needs `framework/actualization/`. When that folder is missing, the instructions tell the agent to warn the user and offer [get_actualization.py](./get_actualization.py), a standalone script (standard library only) that downloads just that module after confirmation. `python get_actualization.py --check` reports whether it is present (exit `0`) or missing (exit `3`).

## Portable Agent Skill

The complete skill package is this directory's root (the folder containing `SKILL.md`). It checks that baseline downloaded assets under `dependencies/utils/` are present, then points the host agent to the appropriate instructions here. Copy the whole directory to a location supported by the intended host; no host-specific installation path is assumed.
