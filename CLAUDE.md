# CLAUDE.md — Master Claude Agent & Skills Instructions

This document establishes the permanent, comprehensive, and detailed instructions for Claude when working in this repository (`OmniAgent`).
Claude must apply these guidelines automatically and mandatorily in every prompt, interaction, refactoring, review, or code development.

---

## Behavioral Rules & Workflow

1. **Think out loud** before acting.
2. **Present the plan** of the current phase.
3. **Ask for explicit confirmation**:
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user approval** before proceeding.
5. **Execute only after receiving confirmation**.

---

## 1. Local Model Gateway (Omniroute Gateway)
- **Base Endpoint**: `http://localhost:20128/v1`
- **Model**: `openai/antigravity/gemini-3.1-flash-lite`
- **Purpose**: High-speed local inference, zero external costs, and privacy.

---

## 2. Operational Principles ("Ponytail" & Lazy Senior Dev)
- **YAGNI**: Minimal, surgical, and direct changes.
- **Action First**: Direct, to-the-point responses.
- **Reusability over Creation**: Prioritize existing code and stdlib.
