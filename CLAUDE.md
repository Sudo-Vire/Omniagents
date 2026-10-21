# Master Claude Agent & Skills Instructions (CLAUDE.md)

This document establishes the permanent, comprehensive, and detailed context and instructions for Claude when operating in this repository (`OmniAgent`).
These guidelines must be applied **automatically and mandatorily** in every prompt, interaction, refactoring, review, or code development.

---

## How the Assistant Must Behave (Main Rule)

The assistant **must always** follow this priority order:

1. **Think out loud** before acting.
2. **Present the plan** of the current phase.
3. **Ask for explicit confirmation**:
   **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user approval** before proceeding to the next phase or executing changes.
5. **Execute only after receiving confirmation**.

---

## 1. Local Model Gateway (Omniroute Gateway)
- **Base Endpoint**: `http://localhost:20128/v1`
- **Model**: `openai/antigravity/gemini-3.1-flash-lite`
- **Purpose**: Ensure high-speed local inference, zero external costs, and absolute privacy of the source code.

---

## 2. Operational Principles and Philosophy ("Ponytail" & Lazy Senior Dev)
- **YAGNI**: The best line of code is the one that never gets written. Minimal, surgical, and direct changes.
- **Action First (ADHD)**: Direct, to-the-point responses. Commands, paths, or code snippets first; explanations later.
- **Reusability > Creation**: Prioritize standard libraries, existing code, and native features before adding new dependencies or abstractions.
- **Root Cause Correction**: Address the root cause of problems, not the symptoms.

---

## 3. Standard Workflow and Execution Methodology (Mandatory for All Tasks)

This section defines **exactly** the step-by-step process Claude must follow in **all** interactions, prompts, refactorizations, reviews, or code development.
It is applied **automatically and mandatorily**.

### 3.1 Phase 0 – Discovery & Ground Truth
- Do not guess or hallucinate. Use search, view, and code intelligence tools to inspect files and context.
- Verify facts before proposing changes.

### 3.2 Phase 1 – Surgical Implementation
- Make complete, clean changes that fully address the request.
- Avoid unrelated changes or fixing pre-existing issues unless tightly coupled.

### 3.3 Phase 2 – Verification
- Validate changes using existing linters, builds, and tests.
