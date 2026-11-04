from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import tempfile
import unittest
from pathlib import Path

from support import SKILL_DIR  # noqa: E402
from check_dependencies import (  # noqa: E402
    UTILS_INDEX,
    check_dependency_assets,
    find_placeholders,
    main,
)


class PreflightTests(unittest.TestCase):
    def test_preflight_warns_about_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            marker = Path(tmp) / "dependencies/utils/agents/x/PLACEHOLDER.md"
            marker.parent.mkdir(parents=True)
            marker.write_text("stub", encoding="utf-8")
            self.assertEqual(find_placeholders(Path(tmp)), ["agents/x"])

    def test_dependency_check_reports_missing_utility(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            (root / UTILS_INDEX).parent.mkdir(parents=True)
            (root / UTILS_INDEX).write_text(
                "agents/missing-agent\n", encoding="utf-8"
            )
            errors = check_dependency_assets(root)
            self.assertEqual(errors, ["Missing or empty utility: agents/missing-agent"])

    def test_dependency_check_reports_missing_inventory_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            self.assertEqual(
                check_dependency_assets(Path(temp_dir)),
                ["Missing inventory file: dependencies/utils/check_utils.txt"],
            )

    def test_dependency_check_accepts_complete_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_root = Path(temp_dir)
            utils_dir = skill_root / "dependencies" / "utils"
            for entry in (
                "agents/agent-one",
                "skills/vercel/skill-one",
                "skills/ciberseguridad/skill-two",
                "tools/tool.py",
            ):
                utility = utils_dir / Path(entry)
                utility.parent.mkdir(parents=True, exist_ok=True)
                if utility.suffix:
                    utility.write_text("present", encoding="utf-8")
                else:
                    utility.mkdir()
                    (utility / "README.md").write_text("present", encoding="utf-8")
            (utils_dir / "check_utils.txt").write_text(
                "agents/agent-one\n"
                "skills/vercel/skill-one\n"
                "skills/ciberseguridad/skill-two\n"
                "tools/tool.py\n",
                encoding="utf-8",
            )

            self.assertEqual(check_dependency_assets(skill_root), [])

    def test_dependency_check_detects_unlisted_resource_in_group(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_root = Path(temp_dir)
            utils_dir = skill_root / "dependencies" / "utils"
            group = utils_dir / "skills" / "vercel"
            for name in ("listed-skill", "unlisted-skill"):
                skill = group / name
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text("content", encoding="utf-8")
            (utils_dir / "check_utils.txt").write_text(
                "skills/vercel/listed-skill\n", encoding="utf-8"
            )

            self.assertEqual(
                check_dependency_assets(skill_root),
                [
                    "Utility not listed in check_utils.txt: "
                    "skills/vercel/unlisted-skill"
                ],
            )

    def test_dependency_check_rejects_unlisted_utility(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_root = Path(temp_dir)
            utils_dir = skill_root / "dependencies" / "utils"
            (utils_dir / "check_utils.txt").parent.mkdir(parents=True)
            (utils_dir / "check_utils.txt").write_text("", encoding="utf-8")
            unlisted = utils_dir / "tools" / "new-tool"
            unlisted.mkdir(parents=True)
            (unlisted / "tool.py").write_text("pass", encoding="utf-8")

            self.assertEqual(
                check_dependency_assets(skill_root),
                ["Utility not listed in check_utils.txt: tools/new-tool"],
            )

    def test_dependency_check_rejects_invalid_inventory_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_root = Path(temp_dir)
            index = skill_root / UTILS_INDEX
            index.parent.mkdir(parents=True)
            index.write_text("../outside\n", encoding="utf-8")

            self.assertEqual(
                check_dependency_assets(skill_root),
                ["Invalid entry at line 1: ../outside"],
            )

    def test_dependency_check_rejects_duplicate_inventory_entries(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_root = Path(temp_dir)
            utils_dir = skill_root / "dependencies" / "utils"
            utility = utils_dir / "tools" / "tool.py"
            utility.parent.mkdir(parents=True)
            utility.write_text("pass\n", encoding="utf-8")
            (utils_dir / "check_utils.txt").write_text(
                "tools/tool.py\ntools/tool.py\n", encoding="utf-8"
            )

            self.assertEqual(
                check_dependency_assets(skill_root),
                ["Duplicate entry at line 2: tools/tool.py"],
            )

    def test_dependency_check_validates_real_utils_inventory(self) -> None:
        self.assertEqual(check_dependency_assets(SKILL_DIR), [])

    def test_cli_reports_missing_inventory_resources(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            index = root / UTILS_INDEX
            index.parent.mkdir(parents=True)
            index.write_text("tools/missing-tool\n", encoding="utf-8")
            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(["--skill-root", str(root)])

            self.assertEqual(exit_code, 2)
            self.assertIn("tools/missing-tool", output.getvalue())

    def test_cli_routes_complete_assets_to_framework(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_root = Path(temp_dir)
            utils_dir = skill_root / "dependencies" / "utils"
            utility = utils_dir / "skills" / "sample"
            utility.mkdir(parents=True)
            (utility / "SKILL.md").write_text("sample", encoding="utf-8")
            (utils_dir / "check_utils.txt").write_text(
                "skills/sample\n", encoding="utf-8"
            )

            output = StringIO()
            with redirect_stdout(output):
                exit_code = main(["--skill-root", str(skill_root)])

            self.assertEqual(exit_code, 0)
            self.assertIn("framework/orchestration", output.getvalue())


if __name__ == "__main__":
    unittest.main()
