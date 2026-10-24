# Agentic Instructions: Ecosystem Update Workflow (`actualization/`)

When the user requests to add a new resource or update the Omniagents ecosystem, the AI assistant must follow this protocol:

1. **Invoke the Updater Script**: Run `python actualization/update_ecosystem.py`.
2. **Interactive Prompts**:
   - Prompt the user for the resource type (Agent, Skill, Tool, Sub-rule, Framework, Plugin, MCP Server, Prompt).
   - Prompt for the precise name/identifier.
3. **Duplicate Check & Warning**:
   - Check if the resource already exists in `pre-downloaded/` or `orchestration/instructions/`.
   - If it exists, warn the user and ask whether to update references or overwrite.
4. **Registration & Catalog Sync**:
   - Automatically register the resource in `AGENTS_CATALOG.md` across Gemini, OpenAI, and Copilot.
5. **Execution of Installation Script**:
   - Check if an installation script (`install.py`, `install.ps1`, `setup.py`) exists for the resource or trigger `python installation/install.py` to ensure dependencies and prerequisites are fully provisioned.
6. **Git Commit & Push**:
   - Stage changes, commit using Conventional Commits with the Co-authored-by trailer, and push to `origin master`.
