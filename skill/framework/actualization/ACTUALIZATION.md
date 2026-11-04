# Agentic Instructions: Ecosystem Update Workflow (`actualization/`)

When the user requests to add a new resource or update the Omniagents ecosystem, the AI assistant must follow this protocol from the portable skill package (the directory containing `SKILL.md`):

1. **Invoke the Updater Script**: Run `python framework/actualization/update_ecosystem.py` from the skill root. For cross-model sync, follow [MODEL_SYNC_INSTRUCTIONS.md](./MODEL_SYNC_INSTRUCTIONS.md).
2. **Interactive Prompts**:
   - Prompt the user for the resource type (Agent, Skill, Tool, Sub-rule, Framework, Plugin, MCP Server, Prompt).
   - Prompt for the precise name/identifier.
3. **Duplicate Check & Warning**:
   - Check if the resource already exists in `dependencies/utils/` or `framework/orchestration/instructions/`.
   - If it exists, warn the user and ask whether to update references or overwrite.
   - When adding an agent, skill, tool, or framework/plugin/prompt resource, register its relative path in `dependencies/utils/check_utils.txt`. The preflight will report it until resource files are actually present.
   - If the resource is downloaded from a GitHub repository, also pin it in `dependencies/utils/sources.json` (`owner/repo` plus a full 40-character commit SHA) so `scripts/fetch_utils.py` can restore it. `update_ecosystem.py` offers this step; vendored resources authored in this repo are not listed there.
   - For the Sequential Thinking MCP, use the existing `dependencies/utils/tools/mcp-sequential-thinking/README.md` to configure the target host; do not treat an inventory entry as proof of a running MCP connection.
4. **Registration & Catalog Sync**:
   - Register the resource in the matching catalogs under `framework/orchestration/instructions/` when applicable.
5. **Execution of Installation Script**:
   - Check whether a resource-specific installation script (`install.py`, `install.ps1`, `setup.py`) exists. Ask for explicit approval before running it or `python dependencies/installation/install.py`; installers may install packages, run code, or write `.env`.
6. **Git Commit & Push**:
   - Ask for explicit authorization before staging, committing, or pushing changes.
