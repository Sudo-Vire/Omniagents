# Claude Orchestration Instructions (Claude Code / Anthropic API)

This document defines the custom orchestration rules created by **Sudo-Vire** for running OmniAgent workflows using Anthropic Claude models (Claude 3.5 Sonnet, Claude Opus, Claude Code CLI).

---

## 🧠 Behavior & Execution Guidelines for Claude

1. **Structured Reasoning & Planning**:
   - Before editing files or executing commands, present a clear, step-by-step plan.
   - Follow the "Ponytail" / Lazy Senior Dev philosophy: minimal code, maximum reusability, YAGNI.
2. **Action-First Output (ADHD-friendly)**:
   - Lead with the next action (command, path, snippet).
   - Number multi-step work clearly.
   - End with one concrete next step doable in under 2 minutes.
3. **Integration with Pre-Downloaded Ecosystem**:
   - Utilize micro-subagents from `pre-downloaded/agents/claude-subagents/`.
   - Apply systematic debugging and workflow routines from `pre-downloaded/skills/`.
4. **Local Gateway Connection**:
   - Connect to local Omniroute gateway at `http://localhost:20128/v1` when required.
