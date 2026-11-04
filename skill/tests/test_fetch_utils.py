from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from support import SKILL_DIR  # noqa: E402


class FetchUtilsTests(unittest.TestCase):
    def test_pinned_sources_are_installed_and_not_placeholders(self) -> None:
        sources = json.loads(
            (SKILL_DIR / "dependencies/utils/sources.json").read_text(encoding="utf-8")
        )
        inventory = (SKILL_DIR / "dependencies/utils/check_utils.txt").read_text(
            encoding="utf-8"
        ).split()
        for key, source in sources.items():
            if key.startswith("_"):
                continue
            self.assertRegex(source["ref"], r"^[0-9a-f]{40}$", key)
            self.assertIn(key, inventory)
            target = SKILL_DIR / "dependencies/utils" / key
            self.assertFalse((target / "PLACEHOLDER.md").exists(), key)
            self.assertTrue(any(p.is_file() and p.name != "LICENSE" for p in target.rglob("*")), key)

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


if __name__ == "__main__":
    unittest.main()
