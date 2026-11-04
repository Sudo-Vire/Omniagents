# Omniagents

Omniagents is a host-neutral Agent Skill (`skill/`) that orchestrates agents, skills and tools. It works from any install location and does not require VS Code, Claude or any specific editor. Delegation uses the native tools of whichever agent host loads it.

> **Clean install without dependencies.** This branch (`master`) includes the third-party agents and skills already downloaded under `skill/dependencies/utils/` (about 1,300 files). The [`master-no-dependencies`](https://github.com/Sudo-Vire/Omniagents/tree/master-no-dependencies) branch is the same skill without them: those folders only hold a `PLACEHOLDER.md`, and `scripts/fetch_utils.py` downloads them into `utils/` on demand. To install it:
>
> ```bash
> npx skills add https://github.com/Sudo-Vire/Omniagents/tree/master-no-dependencies --skill omniagents-orchestration
> python <skill-root>/scripts/fetch_utils.py
> ```

## Repository layout

```text
.
├── skill/                      # The installable package (copy this whole folder)
│   ├── SKILL.md                # Entry point and procedure
│   ├── AUTHORS.md, CONTRIBUTING.md, LICENSE, NOTICE   # Copies that travel with the skill
│   ├── framework/
│   │   ├── orchestration/      # Per-model instructions (claude, copilot, gemini, openai, others)
│   │   └── actualization/      # Ecosystem and model-sync update tooling
│   ├── dependencies/
│   │   ├── installation/       # Optional Python environment setup
│   │   └── utils/              # Agents, skills, tools, inventory and upstream sources
│   │       ├── check_utils.txt # Inventory verified by the preflight
│   │       └── sources.json    # Pinned upstream repositories for downloaded utilities
│   ├── references/             # Execution contract, configuration, troubleshooting
│   ├── scripts/                # check_dependencies.py, check_mcp.py, fetch_utils.py
│   └── tests/                  # Package tests
├── .github/workflows/          # ci.yml (tests, preflight, npx install test), verify-sources.yml
├── scripts/sync_legal.py       # Keeps the legal files identical in the root and in skill/
├── AUTHORS.md, CONTRIBUTING.md, LICENSE, NOTICE   # Same files as in skill/ (GitHub detects these)
└── README.md
```

## Install

Without cloning, using the [`skills` CLI](https://github.com/vercel-labs/skills) (Node.js 22.20+):

```bash
# Current project; the CLI asks which agents to install to
npx skills add Sudo-Vire/Omniagents 

# For all your projects, one agent, no prompts, real copies instead of symlinks
npx skills add Sudo-Vire/Omniagents -g -a claude-code --copy -y
```

The CLI installs the complete `skill/` folder, including `dependencies/utils/`. Update with `npx skills update`. Set `DISABLE_TELEMETRY=1` to opt out of the CLI's anonymous telemetry.

Alternatively, everything is versioned in this repository, so cloning or downloading it also includes all utilities:

```text
git clone https://github.com/Sudo-Vire/Omniagents.git
```

Copy the whole `skill/` folder to the skill location your host uses, keeping its structure. If the host requires the directory name to match `name` in `SKILL.md`, name it `omniagents-orchestration` (Claude Code: `.claude/skills/omniagents-orchestration/` in a project or `~/.claude/skills/omniagents-orchestration/` for user scope). Do not copy local runtime folders such as `dependencies/installation/.venv/` or Python caches.

Then, from any directory:

```text
python <skill-root>/scripts/check_dependencies.py
```

If a downloaded utility is missing (for example, a partial copy), restore it from its pinned upstream source:

```text
python <skill-root>/scripts/fetch_utils.py
```

This downloads `agents/claude-subagents` ([VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)) and `skills/superpowers` ([obra/superpowers](https://github.com/obra/superpowers)) at the commits pinned in `skill/dependencies/utils/sources.json`. It uses only the Python standard library and never executes downloaded content. Use `--force` to re-download.

### Sequential Thinking MCP (optional)

Copy the template for your host from `skill/dependencies/utils/tools/mcp-sequential-thinking/adapters/` and follow the [MCP setup guide](skill/dependencies/utils/tools/mcp-sequential-thinking/README.md). No configuration file can start or approve an MCP server; the host does that, and the tool must appear in the host before it is considered active.

## Validate

Run with Python 3.10 or later:

```text
python -B -m unittest discover -s skill/tests -p "test_*.py" -v
python -B skill/scripts/check_dependencies.py
```

The preflight is read-only. It does not install or download anything.

## Optional dependency setup

The installer is not required by the preflight. It installs packages and may write `.env`, so inspect it first and run it from its directory:

```text
cd skill/dependencies/installation
python install.py
```

## License

See [AUTHORS.md](AUTHORS.md), [NOTICE](NOTICE) and [LICENSE](LICENSE). Third-party utilities keep their own licenses inside their folders.
