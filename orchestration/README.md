# Orchestration Module (`orchestration/`)

This module houses all universal and model-specific orchestration instructions, rules, and configuration templates for OmniAgent, organized by LLM runtime under `instructions/`.

---

## 📂 Subfolder Layout (`instructions/`)

1. **Claude (`instructions/claude/`)**:
   - Points to root `CLAUDE.md`.
2. **GitHub Copilot (`instructions/copilot/`)**:
   - Contains the definitive master rulebook (`copilot-instructions.md`).
3. **Google Gemini (`instructions/gemini/`)**:
   - Contains system configuration (`gemini-config.json`) and master instructions (`GEMINI.md`).
4. **OpenAI / GPT (`instructions/openai/`)**:
   - Contains system instructions (`OPENAI.md`) and Assistant API payload (`assistant-instructions.json`).
5. **Others / Universal (`instructions/others/`)**:
   - Contains universal master instructions (`agents.md`) for any other LLM models (Llama, Mistral, Grok, etc.).


