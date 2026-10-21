# Gemini Orchestration Instructions & System Config

Google Gemini models do not read a local `gemini.md` file by default. Instead, Gemini ingests system instructions via API payloads, CLI configuration flags, or structured JSON configuration files such as **`gemini-config.json`**.

---

## ⚡ How to Configure Gemini for OmniAgent

1. **System Prompt Injection**: Pass the system instruction defined in `gemini-config.json` into the Gemini API client or CLI system prompt parameter.
2. **Execution Rules**:
   - Leverage Gemini's large-context window for repository-wide analysis.
   - Follow the Lazy Senior Dev / Ponytail principle: minimal, surgical changes.
   - Access pre-downloaded skills (`pre-downloaded/skills/`) and tools (`pre-downloaded/tools/`).
