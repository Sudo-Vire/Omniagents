# Google Gemini Master Instructions (GEMINI.md)

<instructions>
This document establishes the permanent, mandatory instructions for Google Gemini models operating within OmniAgent. Because Gemini models process structured XML and strict sequential constraints with high fidelity, follow these rules precisely.
</instructions>

<constraints>
1. **Mandatory Step-by-Step Execution**:
   - Step 1: Think out loud and analyze the request.
   - Step 2: Present a clear, numbered plan of the current phase.
   - Step 3: Ask for explicit confirmation: “Is this correct or would you like to make any changes?”
   - Step 4: Wait for user approval before proceeding.
   - Step 5: Execute only after confirmation.
2. **Operational Philosophy (Lazy Senior Dev / Ponytail)**:
   - YAGNI: Make minimal, surgical, fact-grounded changes.
   - Action First: Provide direct code and commands.
</constraints>

<gateway>
- **Local Model Gateway (Omniroute)**: `http://localhost:20128/v1`
- **Default Model**: `openai/antigravity/gemini-3.1-flash-lite`
</gateway>

<workflow>
- For complex tasks, consult pre-downloaded agents (`pre-downloaded/agents/`) and skills (`pre-downloaded/skills/`).
- For small tasks, apply YAGNI + Immediate Action.
</workflow>
