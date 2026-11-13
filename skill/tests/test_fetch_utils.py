from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from support import SKILL_DIR  # noqa: E402


class FetchUtilsTests(unittest.TestCase):
    def test_sources_are_either_downloaded_or_have_a_placeholder(self) -> None:
        utils_dir = SKILL_DIR / "dependencies/utils"
        pinned = json.loads((utils_dir / "sources.json").read_text(encoding="utf-8"))
        unpinned = json.loads((utils_dir / "sources_not_pinned.json").read_text(encoding="utf-8"))
        inventory = (utils_dir / "check_utils.txt").read_text(encoding="utf-8").split()
        pinned = {k: v for k, v in pinned.items() if not k.startswith("_")}
        unpinned = {k: v for k, v in unpinned.items() if not k.startswith("_")}
        self.assertEqual(set(), set(pinned) & set(unpinned))
        for key, source in pinned.items():
            self.assertRegex(source["ref"], r"^[0-9a-f]{40}$", key)
        for key, source in unpinned.items():
            self.assertIn("repo", source, key)
            self.assertTrue(
                "map" in source or "path" in source or key == "agents/agency-agents", key
            )
            self.assertIn("ref", source, key)
            self.assertNotRegex(source["ref"], r"^[0-9a-f]{40}$", key)
        for key in {**pinned, **unpinned}:
            self.assertIn(key, inventory)
            target = utils_dir / key
            content = [
                p for p in target.rglob("*")
                if p.is_file() and p.name not in ("LICENSE", "PLACEHOLDER.md")
            ]
            placeholder = target / "PLACEHOLDER.md"
            if content:
                self.assertFalse(placeholder.exists(), f"{key} is downloaded but still has a placeholder")
            else:
                self.assertTrue(placeholder.is_file(), f"{key} has neither content nor a placeholder")
                self.assertIn(f"fetch_utils.py {key}", placeholder.read_text(encoding="utf-8"), key)

    def test_every_agent_and_skill_in_the_inventory_has_a_source(self) -> None:
        utils_dir = SKILL_DIR / "dependencies/utils"
        known = set()
        for name in ("sources.json", "sources_not_pinned.json"):
            known |= {k for k in json.loads((utils_dir / name).read_text(encoding="utf-8")) if not k.startswith("_")}
        for key in (utils_dir / "check_utils.txt").read_text(encoding="utf-8").split():
            if key.startswith(("agents/", "skills/")):
                self.assertIn(key, known, f"{key} has no entry in sources.json or sources_not_pinned.json")

    def test_fetch_utils_rejects_unsafe_archives_and_strips_root(self) -> None:
        import io
        import zipfile

        import fetch_utils

        def build(names: list[str]) -> zipfile.ZipFile:
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w") as archive:
                for name in names:
                    archive.writestr(name, "x")
            return zipfile.ZipFile(io.BytesIO(buffer.getvalue()))

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "out"
            self.assertEqual(fetch_utils.safe_extract(build(["repo-sha/a/b.md"]), target), 1)
            self.assertTrue((target / "a" / "b.md").is_file())
            with self.assertRaises(ValueError):
                fetch_utils.safe_extract(build(["repo-sha/../evil.md"]), target)

    def test_safe_extract_map_places_files_and_folders_and_skips_the_rest(self) -> None:
        import io
        import zipfile

        import fetch_utils

        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as archive:
            for name in ("r/pkg/skill.md", "r/pkg/refs/a.md", "r/pkg/other/b.md", "r/LICENSE", "r/README.md"):
                archive.writestr(name, "x")
        mapping = {"pkg/skill.md": "SKILL.md", "pkg/refs": "references", "LICENSE": "LICENSE"}
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "out"
            count = fetch_utils.safe_extract(zipfile.ZipFile(io.BytesIO(buffer.getvalue())), target, mapping=mapping)
            self.assertEqual(3, count)
            found = sorted(p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file())
            self.assertEqual(["LICENSE", "SKILL.md", "references/a.md"], found)


if __name__ == "__main__":
    unittest.main()
