# Master OpenAI GPT Agent & Skills Instructions (OPENAI.md)

This document establishes the permanent instructions for OpenAI GPT models (GPT-4o, o1, o3-mini, Custom GPTs, and Assistants API) operating within OmniAgent.

---

## 🤖 How OpenAI Models Ingest Instructions
1. **API / Developer Message**: Passed as the `developer` or `system` role in Chat Completions.
2. **Assistants API**: Uploaded as instructions or parsed via `assistant-instructions.json`.
3. **Custom GPTs**: Pasted directly into the "Instructions" configuration box.

---

## Core Guidelines & Operational Philosophy
- **YAGNI & Lazy Senior Dev / Ponytail**: Minimal, surgical, fact-grounded changes.
- **Action First**: Concise code and command delivery.
- **Gateway**: Connected to local Omniroute gateway at `http://localhost:20128/v1`.
- **Pre-Downloaded Ecosystem**: Access skills in `pre-downloaded/skills/` and tools in `pre-downloaded/tools/`.
