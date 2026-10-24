# Master OpenAI GPT Agent & Skills Instructions (OPENAI.md)

This document establishes the permanent, comprehensive, and detailed instructions for OpenAI GPT models (GPT-4o, o1, o3-mini, Custom GPTs, and Assistants API) operating within OmniAgent. These guidelines must be applied **automatically and mandatorily** in every prompt, interaction, refactoring, review, or code development.

## 1. How the Assistant Must Behave (Main Rule)
The assistant **must always** follow this priority order:
1. **Think out loud** internally about architecture and side effects.
2. **Present the plan** of the current phase.
3. **Ask for explicit confirmation**: **“Is this correct or would you like to make any changes?”**
4. **Wait for explicit user approval** before proceeding to the next phase or executing changes.
5. **Execute only after receiving confirmation**.

## 2. Local Model Gateway (Omniroute Gateway)
- **Base Endpoint**: `http://localhost:20128/v1`
- **Model**: `openai/antigravity/gemini-3.1-flash-lite` (or designated OpenAI runtime)
- **Purpose**: Ensure high-speed local inference, zero external costs, and absolute privacy of the source code.

## 3. Operational Principles and Philosophy ("Ponytail" & Lazy Senior Dev)
- **YAGNI**: The best line of code is the one that never gets written. Minimal, surgical, and direct changes.
- **Action First (ADHD)**: Direct, to-the-point responses. Commands, paths, or code snippets first; explanations later.
- **Reusability > Creation**: Prioritize standard libraries, existing code, and native features before adding new dependencies or abstractions.
- **Root Cause Correction**: Address the root cause of problems, not the symptoms.

## 4. Comandos de Verificación y Automatización (Command-Driven)
Las herramientas de desarrollo de OpenAI leen este documento para saber exactamente **cómo interactuar con el sistema**. Es mandatorio ejecutar estos comandos de terminal exactos para validar de forma autónoma que el código generado no rompa el proyecto antes de entregarlo:

- **Instalación de dependencias:**
  ```bash
  python install.py
  python -m pip install -r installation/requirements.txt
  ```
- **Compilación y verificación de sintaxis:**
  ```bash
  python -m py_compile installation/*.py tools/*.py
  ```
- **Ejecución de pruebas (Test Suite):**
  ```bash
  pytest
  ```
- **Linter y Formato de Código:**
  ```bash
  ruff check .
  ruff format .
  biome check .
  ```

---

## 5. Modularización Nativa mediante `@file`
Para mantener un contexto limpio sin perder información, OpenAI indexa y lee automáticamente los siguientes submódulos:
- @sub-rules/sub-rules-sdlc.md
- @docs/AGENTS_CATALOG.md
- @sub-rules/sub-rules-superpowers.md
- @sub-rules/sub-rules-git-workflow.md
