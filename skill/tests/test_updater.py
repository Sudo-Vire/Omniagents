from __future__ import annotations

from contextlib import redirect_stdout
from io import BytesIO, StringIO, TextIOWrapper
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


from check_dependencies import (  # noqa: E402
    check_dependency_assets,
    main,
)
import update_ecosystem  # noqa: E402


class UpdaterTests(unittest.TestCase):
    def test_register_source_validates_and_is_idempotent(self) -> None:
        sha = "a" * 40
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sources.json"
            path.write_text("{}", encoding="utf-8")
            self.assertTrue(update_ecosystem.register_source("skills", "demo", "o/r", sha, "MIT", path))
            self.assertFalse(update_ecosystem.register_source("skills", "demo", "o/r", sha, "MIT", path))
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["skills/demo"]["ref"], sha)
            for bad in (("skills", "demo", "bad", sha), ("skills", "demo", "o/r", "main"), ("x", "demo", "o/r", sha)):
                with self.assertRaises(ValueError):
                    update_ecosystem.register_source(*bad, sources_path=path)

    def test_updater_registers_new_tool_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            index_path = Path(temp_dir) / "check_utils.txt"
            index_path.write_text("# utility inventory\n", encoding="utf-8")

            self.assertTrue(
                update_ecosystem.register_utility("tools", "new-tool", index_path)
            )
            self.assertFalse(
                update_ecosystem.register_utility("tools", "new-tool", index_path)
            )
            self.assertEqual(
                index_path.read_text(encoding="utf-8"),
                "# utility inventory\ntools/new-tool\n",
            )

    def test_updater_rejects_unsafe_resource_names(self) -> None:
        with self.assertRaises(ValueError):
            update_ecosystem.register_utility(
                "tools", "../outside", Path("unused-index.txt")
            )

    def test_updater_requires_approval_before_running_installer(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            installer = Path(temp_dir) / "install.py"
            installer.write_text("pass\n", encoding="utf-8")
            with (
                patch("builtins.input", return_value="n"),
                patch.object(update_ecosystem.subprocess, "run") as run,
            ):
                update_ecosystem.run_installation_script(temp_dir)

            run.assert_not_called()

    def test_updater_does_not_run_general_installer_for_host_configured_tool(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output = StringIO()
            with (
                redirect_stdout(output),
                patch.object(update_ecosystem.subprocess, "run") as run,
            ):
                update_ecosystem.run_installation_script(temp_dir)

            run.assert_not_called()
            self.assertIn("Configura la herramienta en el host", output.getvalue())

    def test_updater_registers_tool_when_added_interactively(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skill_root = Path(temp_dir)
            utils_dir = skill_root / "dependencies" / "utils"
            index_path = utils_dir / "check_utils.txt"
            stdout_buffer = BytesIO()
            windows_stdout = TextIOWrapper(stdout_buffer, encoding="cp1252")
            with (
                redirect_stdout(windows_stdout),
                patch.object(update_ecosystem, "UTILS_DIR", str(utils_dir)),
                patch.object(update_ecosystem, "UTILS_INDEX_PATH", str(index_path)),
                patch.object(update_ecosystem, "SKILL_ROOT", str(skill_root)),
                patch.object(update_ecosystem, "integrate_into_instructions"),
                patch.object(update_ecosystem, "run_installation_script"),
                patch.object(update_ecosystem, "SOURCES_PATH", str(utils_dir / "sources.json")),
                patch("builtins.input", side_effect=["3", "new-tool", ""]),
            ):
                update_ecosystem.main()
            windows_stdout.flush()
            output = stdout_buffer.getvalue().decode("cp1252")

            self.assertIn("OK: El Herramienta/MCP 'new-tool'", output)
            self.assertTrue((utils_dir / "tools" / "new-tool").is_dir())
            self.assertEqual(
                index_path.read_text(encoding="utf-8"),
                "tools/new-tool\n",
            )
            self.assertEqual(
                check_dependency_assets(skill_root),
                ["Missing or empty utility: tools/new-tool"],
            )
            (utils_dir / "tools" / "new-tool" / "tool.py").write_text(
                "pass\n", encoding="utf-8"
            )
            self.assertEqual(check_dependency_assets(skill_root), [])


if __name__ == "__main__":
    unittest.main()
