# Orchestration Module (`orchestration/`)

This module houses all universal and model-specific orchestration instructions, rules, and configuration templates for OmniAgent.

---

## 🧠 Model-Specific Instruction Mechanisms

Different LLM runners and assistants expect configuration and system instructions in different ways:

1. **Anthropic Claude (Claude Code / Claude Desktop)**:
   - Natively reads **`CLAUDE.md`** at the project root.
   - Reference: `orchestration/agents/claude-instructions.md` points to root `CLAUDE.md`.

2. **GitHub Copilot (VS Code / Copilot SDK)**:
   - Reads **`.github/copilot-instructions.md`** or repository instructions.
   - Reference: `orchestration/agents/copilot-instructions.md` (the definitive master rulebook).

3. **Google Gemini (Gemini CLI / API / Vertex)**:
   - Uses system instructions, API payloads, or configuration files such as **`orchestration/agents/gemini-config.json`**.
   - Reference: `orchestration/agents/gemini-instructions.md`.

4. **OpenAI / GPT (API / Custom Clients)**:
   - Uses system prompt messages configured via **`orchestration/agents/openai-instructions.md`**.
