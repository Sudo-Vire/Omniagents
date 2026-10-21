# OmniAgent-OS Universal Agent & Multi-Model Instructions

This document establishes the universal orchestration guidelines for AI agents across **Claude (Anthropic), GitHub Copilot, Gemini (Google), OpenAI, and local runtimes via Omniroute**.

---

## 🌐 Multi-Model / Multi-Agent Compatibility

OmniAgent-OS is designed to operate seamlessly across different AI runtimes:
- **GitHub Copilot / VS Code**: Native SDK and editor integration.
- **Claude (Anthropic)**: Advanced reasoning and system prompt orchestration.
- **Gemini (Google)**: Large-context analysis and fast inference.
- **Local Runtimes (Omniroute)**: High-speed local gateway at `http://localhost:20128/v1`.

---

## 🎯 Core Behavioral Rules

1. **Precision & surgical changes**: Make complete, clean changes without unrequested abstractions.
2. **Multi-agent tool invocation**: Use agents (`agency-agents`, `claude-subagents`) and skills (`skills/`) according to task requirements.
3. **Fact-grounded reasoning**: Verify code, tests, and dependencies before concluding.
4. **Clear confirmation**: Always confirm with the user before executing destructive or complex architectural changes.
