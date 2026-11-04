#!/usr/bin/env python3
"""Download upstream utilities listed in dependencies/utils/sources.json
(pinned to commit SHAs) and sources_not_pinned.json (following a branch).

Standard library only. Utilities that already have real content are skipped
unless --force is given. Archives are extracted without executing anything.
A source may set `path` (extract one upstream folder at the root) or `map`
({upstream path: destination}) when the upstream layout differs from the one
used under dependencies/utils/.
"""

from __future__ import annotations

import argparse
import io
import json
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

PLACEHOLDER_MARKER = "PLACEHOLDER.md"
SOURCES = Path("dependencies/utils/sources.json")
SOURCES_NOT_PINNED = Path("dependencies/utils/sources_not_pinned.json")
ARCHIVE_URL = "https://codeload.github.com/{repo}/zip/{ref}"


def find_skill_root(start: Path) -> Path | None:
    for candidate in (start, *start.parents):
        if (candidate / SOURCES).is_file():
            return candidate
    return None


def load_sources(skill_root: Path) -> dict[str, dict]:
    """Merge pinned (sources.json) and unpinned (sources_not_pinned.json) sources."""
    sources: dict[str, dict] = {}
    for path, unpinned in ((SOURCES, False), (SOURCES_NOT_PINNED, True)):
        file = skill_root / path
        if not file.is_file():
            continue
        for key, value in json.loads(file.read_text(encoding="utf-8")).items():
            if not key.startswith("_"):
                sources[key] = {**value, "unpinned": unpinned}
    return sources


def is_installed(path: Path) -> bool:
    if not path.is_dir():
        return False
    files = [
        p for p in path.rglob("*")
        if p.is_file() and p.name not in (PLACEHOLDER_MARKER, "LICENSE")
    ]
    return any(p.stat().st_size > 0 for p in files)


def safe_extract(
    archive: zipfile.ZipFile,
    target: Path,
    subpath: str = "",
    mapping: dict[str, str] | None = None,
) -> int:
    """Extract an archive, dropping its top-level folder and rejecting escapes.

    With subpath, only that folder of the repository is extracted, at the target root.
    With mapping ({upstream path: destination relative to target}), each upstream file
    or folder is placed at its destination and everything else is skipped.
    """
    count = 0
    target = target.resolve()
    prefix = PurePosixPath(subpath).parts if subpath else ()
    rules = [
        (PurePosixPath(src).parts, PurePosixPath(dst).parts)
        for src, dst in (mapping or {}).items()
    ]
    for info in archive.infolist():
        parts = PurePosixPath(info.filename).parts[1:]
        if not parts or info.is_dir():
            continue
        if any(part in ("..", "") for part in parts) or PurePosixPath(*parts).is_absolute():
            raise ValueError(f"Unsafe path in archive: {info.filename}")
        if rules:
            for src, dst in rules:
                if parts[: len(src)] == src:
                    parts = (*dst, *parts[len(src):])
                    break
            else:
                continue
        elif prefix:
            if parts[: len(prefix)] != prefix or len(parts) == len(prefix):
                continue
            parts = parts[len(prefix):]
        destination = target.joinpath(*parts).resolve()
        destination.relative_to(target)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(info) as source, open(destination, "wb") as out:
            shutil.copyfileobj(source, out)
        count += 1
    return count


def fetch(skill_root: Path, key: str, source: dict, force: bool) -> bool:
    target = skill_root / "dependencies" / "utils" / Path(*PurePosixPath(key).parts)
    if is_installed(target) and not force:
        print(f"OK      {key}: already downloaded")
        return True
    url = ARCHIVE_URL.format(repo=source["repo"], ref=source["ref"])
    note = " (unpinned: follows the upstream branch)" if source.get("unpinned") else ""
    print(f"FETCH   {key}: {url}{note}")
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read()
    except OSError as exc:
        print(f"ERROR   {key}: download failed ({exc})", file=sys.stderr)
        return False

    with tempfile.TemporaryDirectory() as tmp:
        staged = Path(tmp) / "staged"
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            count = safe_extract(archive, staged, source.get("path", ""), source.get("map"))
        if count == 0:
            print(f"ERROR   {key}: archive was empty", file=sys.stderr)
            return False
        # The upstream LICENSE often lives at the repository root, outside a subpath.
        local_license = target / "LICENSE"
        kept_license = local_license.read_bytes() if local_license.is_file() else None
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(staged, target)
        if kept_license is not None and not (target / "LICENSE").exists():
            (target / "LICENSE").write_bytes(kept_license)
    print(f"DONE    {key}: {count} files from {source['repo']}@{source['ref'][:12]}")
    return True


def verify(key: str, source: dict) -> bool:
    """Check that the pinned archive is still downloadable, without downloading it."""
    url = ARCHIVE_URL.format(repo=source["repo"], ref=source["ref"])
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            print(f"OK      {key}: {source['repo']}@{source['ref'][:12]} ({response.status})")
        return True
    except OSError as exc:
        print(f"ERROR   {key}: pinned archive unavailable ({exc})", file=sys.stderr)
        return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", type=Path)
    parser.add_argument("--force", action="store_true", help="re-download existing utilities")
    parser.add_argument("--verify", action="store_true", help="only check that the pinned archives still exist (no download)")
    parser.add_argument("only", nargs="*", help="limit to these utility keys")
    args = parser.parse_args(argv)

    skill_root = args.skill_root.resolve() if args.skill_root else find_skill_root(Path(__file__).resolve().parent)
    if skill_root is None:
        print("ERROR: skill root not found (missing dependencies/utils/sources.json).", file=sys.stderr)
        return 2

    sources = load_sources(skill_root)
    selected = {k: v for k, v in sources.items() if not args.only or k in args.only}
    if args.verify:
        return 0 if all([verify(key, value) for key, value in selected.items()]) else 1
    results = [fetch(skill_root, key, value, args.force) for key, value in selected.items()]
    return 0 if all(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
