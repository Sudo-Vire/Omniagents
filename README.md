# Omniagents

Omniagents is a host-neutral Agent Skill (`skill/`) that orchestrates agents, skills and tools. It works from any install location and does not require VS Code, Claude or any specific editor. Delegation uses the native tools of whichever agent host loads it.

## Clean install

This branch (`master-no-dependencies`) ships the skill **without the third-party agents and skills** (about 1,300 files). Their folders under `skill/dependencies/utils/` contain only a `PLACEHOLDER.md` (plus the upstream `LICENSE` when there is one), and they are downloaded on demand with `fetch_utils.py`:

- `sources.json`: 9 utilities pinned to a commit.
- `sources_not_pinned.json`: 18 utilities that follow an upstream branch (`agency-agents`, `graphify`, `gsd`, `ui-ux-pro-max`, the five other Vercel skills, the nine Strix security skills). `graphify` and `gsd` are copied from their repositories into `utils` with a path map, not installed with their own installers. Unpinned downloads can differ from what Omniagents was tested with.

Everything is installed in one step with `python <skill-root>/scripts/fetch_utils.py` (see [Install](#install)).

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
│   │       ├── sources.json    # Pinned upstream repositories for downloaded utilities
│   │       └── sources_not_pinned.json  # Upstream branches (not pinned)
│   ├── references/             # Execution contract, configuration, troubleshooting
│   ├── scripts/                # check_dependencies.py, check_mcp.py, fetch_utils.py
│   └── tests/                  # Package tests
├── .github/workflows/          # ci.yml (tests, preflight, npx install test), verify-sources.yml
├── scripts/sync_legal.py       # Keeps the legal files identical in the root and in skill/
├── AUTHORS.md, CONTRIBUTING.md, LICENSE, NOTICE   # Same files as in skill/ (GitHub detects these)
└── README.md
```

## Install

> **Looking for the version with every utility included?** The [`master`](https://github.com/Sudo-Vire/Omniagents/tree/master) branch ships all third-party agents and skills already downloaded, so it is the more stable option. However, it may not cover new third-party agents or features added upstream after it was last updated; those are only picked up here when you run `fetch_utils.py`.

Without cloning, using the [`skills` CLI](https://github.com/vercel-labs/skills) (Node.js 22.20+):

```bash
# This branch (the CLI accepts a GitHub URL with a branch)
npx skills add https://github.com/Sudo-Vire/Omniagents/tree/master-no-dependencies

# For all your projects, one agent, no prompts, real copies instead of symlinks
npx skills add https://github.com/Sudo-Vire/Omniagents/tree/master-no-dependencies -g -a claude-code --copy -y
```

The CLI installs the complete `skill/` folder, but the third-party utilities are only placeholders until you run `fetch_utils.py` once after installing. Update with `npx skills update`. Set `DISABLE_TELEMETRY=1` to opt out of the CLI's anonymous telemetry.

Alternatively, clone this branch (`git clone --branch master-no-dependencies https://github.com/Sudo-Vire/Omniagents.git`; the `master` branch includes all utilities).

Copy the whole `skill/` folder to the skill location your host uses, keeping its structure. If the host requires the directory name to match `name` in `SKILL.md`, name it `omniagents-orchestration` (Claude Code: `.claude/skills/omniagents-orchestration/` in a project or `~/.claude/skills/omniagents-orchestration/` for user scope). Do not copy local runtime folders such as `dependencies/installation/.venv/` or Python caches.

Then, from any directory:

```text
python <skill-root>/scripts/check_dependencies.py
```

If a utility is missing or only a placeholder, restore it from its upstream source:

```text
python <skill-root>/scripts/fetch_utils.py
```

This downloads every utility in `skill/dependencies/utils/sources.json` (9, pinned to commits) and `sources_not_pinned.json` (18, following the upstream branch) into `skill/dependencies/utils/`. Until a utility is restored, its folder holds only a `PLACEHOLDER.md` and the preflight warns about it. The script uses only the Python standard library and never executes downloaded content. Use `--force` to re-download, or name specific utilities (for example `skills/grill-me`) to fetch only those.

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
