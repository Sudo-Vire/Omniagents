#!/usr/bin/env python3
"""Validate the skill's installed utility inventory."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from pathlib import PurePosixPath


UTILS_INDEX = Path("dependencies/utils/check_utils.txt")
UTILITY_CATEGORIES = ("agents", "skills", "tools")
SKILL_MARKERS = (
    Path("framework/orchestration/AGENT_INSTRUCTIONS.md"),
    Path("dependencies/installation/requirements.txt"),
)


def find_skill_root(start: Path) -> Path | None:
    """Find the nearest parent containing the framework and dependencies."""
    for candidate in (start, *start.parents):
        if all((candidate / marker).is_file() for marker in SKILL_MARKERS):
            return candidate
    return None


def _has_files(path: Path) -> bool:
    if path.is_file():
        return path.stat().st_size > 0
    return path.is_dir() and any(
        item.is_file() and item.stat().st_size > 0 for item in path.rglob("*")
    )


def _load_utility_index(index_path: Path) -> tuple[list[PurePosixPath], list[str]]:
    entries = []
    errors = []
    seen = set()
    try:
        lines = index_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        return [], [f"Cannot read {UTILS_INDEX.as_posix()}: {exc}"]

    for line_number, raw_line in enumerate(lines, start=1):
        entry_text = raw_line.strip()
        if not entry_text or entry_text.startswith("#"):
            continue
        entry = PurePosixPath(entry_text)
        if (
            "\\" in entry_text
            or entry.is_absolute()
            or len(entry.parts) < 2
            or entry.parts[0] not in UTILITY_CATEGORIES
            or any(part in ("", ".", "..") for part in entry.parts)
        ):
            errors.append(f"Invalid entry at line {line_number}: {entry_text}")
            continue
        if entry in seen:
            errors.append(f"Duplicate entry at line {line_number}: {entry_text}")
            continue
        seen.add(entry)
        entries.append(entry)
    return entries, errors


def _discover_utilities(
    utils_dir: Path, entries: list[PurePosixPath]
) -> set[PurePosixPath]:
    discovered = set()
    for category in UTILITY_CATEGORIES:
        category_dir = utils_dir / category
        if not category_dir.is_dir():
            continue
        for item in category_dir.iterdir():
            if _has_files(item):
                discovered.add(PurePosixPath(category, item.name))

    grouped_paths = {
        PurePosixPath(*entry.parts[:length])
        for entry in entries
        for length in range(2, len(entry.parts))
    }
    for group in grouped_paths:
        group_dir = utils_dir.joinpath(*group.parts)
        if not group_dir.is_dir():
            continue
        for item in group_dir.iterdir():
            if item.is_dir() and _has_files(item):
                discovered.add(group / item.name)
    return discovered


def check_dependency_assets(skill_root: Path) -> list[str]:
    """Return missing, empty, invalid, or unregistered utility inventory entries."""
    utils_dir = skill_root / "dependencies" / "utils"
    index_path = skill_root / UTILS_INDEX
    if not index_path.is_file():
        return [f"Missing inventory file: {UTILS_INDEX.as_posix()}"]

    entries, errors = _load_utility_index(index_path)
    checked_entries = set()
    for entry in entries:
        utility_path = utils_dir.joinpath(*entry.parts)
        try:
            utility_path.resolve().relative_to(utils_dir.resolve())
        except ValueError:
            errors.append(f"Path escapes utils directory: {entry.as_posix()}")
            continue
        checked_entries.add(entry)
        if not _has_files(utility_path):
            errors.append(f"Missing or empty utility: {entry.as_posix()}")

    for entry in sorted(_discover_utilities(utils_dir, entries) - checked_entries):
        is_grouped = any(
            listed.parts[: len(entry.parts)] == entry.parts
            for listed in checked_entries
        )
        if not is_grouped:
            errors.append(f"Utility not listed in check_utils.txt: {entry.as_posix()}")
    return errors


PLACEHOLDER_MARKER = "PLACEHOLDER.md"


def find_placeholders(skill_root: Path) -> list[str]:
    """Return inventoried utilities that only reserve their place."""
    utils_dir = skill_root / "dependencies" / "utils"
    return sorted(
        marker.parent.relative_to(utils_dir).as_posix()
        for marker in utils_dir.rglob(PLACEHOLDER_MARKER)
    )


def check_sequential_thinking(skill_root: Path) -> None:
    """Warn, and when interactive offer activation, if the MCP is not configured.

    Never changes the preflight result: the MCP is optional.
    """
    try:
        import check_mcp
    except ImportError:
        return
    check_mcp.run(
        skill_root,
        check_mcp.guess_project_dir(skill_root, Path.cwd()),
        interactive=sys.stdin.isatty() and sys.stdout.isatty(),
    )


def check_actualization(skill_root: Path) -> None:
    """Note, without failing, that tools cannot be added without the actualization module."""
    if not (skill_root / "framework" / "actualization" / "update_ecosystem.py").is_file():
        print(
            "NOTE: the actualization module (framework/actualization/) is not installed, so "
            "tools, agents and skills cannot be added. Download it with "
            "`python framework/orchestration/get_actualization.py` (asks first)."
        )


def check_python_version() -> None:
    """Verify Python version and availability."""
    if sys.version_info < (3, 8):
        print(
            f"ERROR: Python 3.8+ is required, but found Python {sys.version.split()[0]}. "
            "Please install Python 3.8 or higher before running Omniagents scripts.",
            file=sys.stderr,
        )
    else:
        print(f"Python check passed: Python {sys.version.split()[0]} is installed.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check downloaded agent, skill, and tool asset directories."
    )
    parser.add_argument(
        "--skill-root",
        type=Path,
        help="Skill root; by default, detect it from this script's location.",
    )
    parser.add_argument(
        "--skip-mcp-check",
        action="store_true",
        help="Do not check whether the Sequential Thinking MCP is configured.",
    )
    args = parser.parse_args(argv)

    skill_root = (
        args.skill_root.resolve()
        if args.skill_root
        else find_skill_root(Path(__file__).resolve().parent)
    )
    if skill_root is None:
        print(
            "ERROR: skill root not found; expected framework/orchestration/"
            "AGENT_INSTRUCTIONS.md and dependencies/installation/requirements.txt.",
            file=sys.stderr,
        )
        return 2

    check_python_version()

    errors = check_dependency_assets(skill_root)
    if errors:
        print("Utility inventory check failed:")
        for error in errors:
            print(f"  - {error}")
        print(
            "Update dependencies/utils/check_utils.txt for intended resources, "
            "or add the missing utility contents under dependencies/utils/. "
            "To restore utilities pinned in dependencies/utils/sources.json, run "
            "scripts/fetch_utils.py. This check does not install or download anything."
        )
        return 2

    print(f"All utilities listed in {UTILS_INDEX.as_posix()} are present and non-empty.")
    for placeholder in find_placeholders(skill_root):
        print(
            f"WARNING: {placeholder} is only a placeholder; its upstream content "
            f"is not downloaded (see {placeholder}/{PLACEHOLDER_MARKER})."
        )
    if not args.skip_mcp_check:
        check_sequential_thinking(skill_root)
    check_actualization(skill_root)
    print(
        "Next: continue with "
        f"{(skill_root / 'framework' / 'orchestration').as_posix()}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
