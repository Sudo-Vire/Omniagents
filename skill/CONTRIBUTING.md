# Contributing to Omniagents

Thank you for your interest in contributing! We welcome new agents, skills, tools, bug fixes and documentation improvements.

## Development workflow

1. **Fork** the repository and clone your fork.
2. **Create a branch** (see the branch naming rules in [PULL_REQUEST_INSTRUCTIONS.md](skill/framework/orchestration/instructions/others/PULL_REQUEST_INSTRUCTIONS.md)):
   ```bash
   git checkout -b feature/amazing-agent
   ```
3. **Make surgical changes** that follow the existing structure. Everything installable lives under `skill/`.
4. **Add resources through the updater** so the inventory stays consistent:
   ```bash
   python skill/framework/actualization/update_ecosystem.py
   ```
   Downloaded upstream resources must also be listed in `skill/dependencies/utils/sources.json` with a pinned commit.
5. **Validate**:
   ```bash
   python -B -m unittest discover -s skill/tests -p "test_*.py"
   python -B skill/scripts/check_dependencies.py
   ```
6. **Commit and push**, then open a Pull Request against `master`:
   ```bash
   git commit -m "feat(agents): add amazing new agent"
   git push origin feature/amazing-agent
   ```

`LICENSE`, `NOTICE`, `AUTHORS.md` and `CONTRIBUTING.md` exist twice on purpose: in the repository root so GitHub detects them, and in `skill/` so they travel with an installed skill. Edit the root copy and run `python scripts/sync_legal.py` to update the one in `skill/`; CI and a test fail if they differ.
