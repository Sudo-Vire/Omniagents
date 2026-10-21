# Gemini Orchestration Instructions (Google Gemini / API)

This document defines the custom orchestration rules created by **Sudo-Vire** for running OmniAgent workflows using Google Gemini models.

---

## ⚡ Behavior & Execution Guidelines for Gemini

1. **Large-Context Analysis**:
   - Leverage Gemini's large context window to ingest entire repositories, agency-agents, and pre-downloaded skills in a single pass.
2. **Precision & Completeness**:
   - Make precise, surgical changes. Avoid regressions.
3. **Action-First & Concise**:
   - Suppress unnecessary preamble; provide immediate actionable code and commands.
4. **Tool Utilization**:
   - Reference pre-downloaded tools in `pre-downloaded/tools/` and skills in `pre-downloaded/skills/`.
