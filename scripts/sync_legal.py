#!/usr/bin/env python3
"""Keep the legal files in the repository root and in skill/ identical.

The repository root copies are the source of truth (GitHub detects the license
there). skill/ carries copies so they travel with an installed skill.

    python scripts/sync_legal.py           # copy root -> skill/
    python scripts/sync_legal.py --check   # exit 1 if any pair differs or is missing
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

FILES = ("LICENSE", "NOTICE", "AUTHORS.md", "CONTRIBUTING.md")
REPO_ROOT = Path(__file__).resolve().parent.parent


def _normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n")


def out_of_sync(root: Path = REPO_ROOT) -> list[str]:
    problems = []
    for name in FILES:
        source, copy = root / name, root / "skill" / name
        if not source.is_file():
            problems.append(f"{name}: missing in the repository root")
        elif not copy.is_file():
            problems.append(f"{name}: missing in skill/")
        elif _normalized(source) != _normalized(copy):
            problems.append(f"{name}: differs between the root and skill/")
    return problems


def sync(root: Path = REPO_ROOT) -> list[str]:
    copied = []
    for name in FILES:
        source, copy = root / name, root / "skill" / name
        if not source.is_file():
            raise FileNotFoundError(f"{name} is missing in the repository root")
        if not copy.is_file() or _normalized(source) != _normalized(copy):
            copy.write_bytes(_normalized(source))
            copied.append(name)
    return copied


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="only report differences")
    args = parser.parse_args(argv)

    if args.check:
        problems = out_of_sync()
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        if problems:
            print("Run: python scripts/sync_legal.py", file=sys.stderr)
        else:
            print("OK: legal files are identical in the root and in skill/.")
        return 1 if problems else 0

    try:
        copied = sync()
    except FileNotFoundError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Copied: " + ", ".join(copied) if copied else "Already in sync.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
