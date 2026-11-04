from __future__ import annotations

import io
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from support import SKILL_DIR  # noqa: E402
import check_dependencies  # noqa: E402
import check_mcp  # noqa: E402
import get_actualization  # noqa: E402

MODEL_MASTER_FILES = (
    "claude/CLAUDE.md",
    "copilot/copilot-instructions.md",
    "gemini/GEMINI.md",
    "openai/OPENAI.md",
    "others/agents.md",
)


def _repo_zip(files: dict[str, bytes]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for name, data in files.items():
            archive.writestr(f"Omniagents-master/{name}", data)
    return buffer.getvalue()


class ActualizationModuleTests(unittest.TestCase):
    def test_every_model_tells_the_agent_to_check_the_module_before_adding_tools(self) -> None:
        instructions = SKILL_DIR / "framework" / "orchestration" / "instructions"
        paths = [instructions / name for name in MODEL_MASTER_FILES]
        paths.append(SKILL_DIR / "framework" / "orchestration" / "AGENT_INSTRUCTIONS.md")
        for path in paths:
            text = path.read_text(encoding="utf-8")
            self.assertIn("get_actualization.py", text, path.name)
            self.assertIn("--check", text, path.name)

    def test_check_reports_missing_and_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "actualization"
            with patch.object(get_actualization, "TARGET", target):
                self.assertFalse(get_actualization.is_present(target))
                self.assertEqual(get_actualization.main(["--check"]), 3)
                target.mkdir()
                (target / "update_ecosystem.py").write_text("", encoding="utf-8")
                self.assertEqual(get_actualization.main(["--check"]), 0)

    def test_download_extracts_only_the_actualization_folder(self) -> None:
        archive = _repo_zip({
            "skill/framework/actualization/update_ecosystem.py": b"print('ok')",
            "skill/framework/actualization/README.md": b"readme",
            "skill/framework/orchestration/README.md": b"not needed",
            "README.md": b"root",
        })
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "framework" / "actualization"
            response = SimpleNamespace(read=lambda: archive, __enter__=None)
            opener = patch.object(get_actualization.urllib.request, "urlopen")
            with opener as urlopen:
                urlopen.return_value.__enter__.return_value = response
                self.assertEqual(get_actualization.download("v1", target), 2)
            self.assertEqual(
                sorted(p.name for p in target.iterdir()), ["README.md", "update_ecosystem.py"]
            )

    def test_download_rejects_an_archive_without_the_module(self) -> None:
        archive = _repo_zip({"README.md": b"root"})
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "actualization"
            response = SimpleNamespace(read=lambda: archive)
            with patch.object(get_actualization.urllib.request, "urlopen") as urlopen:
                urlopen.return_value.__enter__.return_value = response
                with self.assertRaises(ValueError):
                    get_actualization.download("master", target)
            self.assertFalse(target.exists())

    def test_extract_rejects_path_traversal(self) -> None:
        archive = zipfile.ZipFile(io.BytesIO(_repo_zip({
            "skill/framework/actualization/../../../evil.py": b"x",
        })))
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                get_actualization.extract(archive, Path(tmp) / "actualization")

    def test_non_interactive_run_without_yes_does_not_download(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "actualization"
            with patch.object(get_actualization, "TARGET", target), patch.object(
                get_actualization, "download"
            ) as download:
                self.assertEqual(get_actualization.main([]), 3)
                download.assert_not_called()

    def test_preflight_notes_a_missing_module_without_failing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with patch("builtins.print") as printed:
                check_dependencies.check_actualization(Path(tmp))
            self.assertIn("get_actualization.py", printed.call_args.args[0])
            with patch("builtins.print") as printed:
                check_dependencies.check_actualization(SKILL_DIR)
            printed.assert_not_called()


class HostCliStatusTests(unittest.TestCase):
    def _status(self, stdout: str, returncode: int = 0) -> list[tuple[str, str, str]]:
        completed = SimpleNamespace(stdout=stdout, stderr="", returncode=returncode)

        def which(name: str) -> str | None:
            return "claude.exe" if name == "claude" else None

        with patch.object(check_mcp.shutil, "which", which), patch.object(
            check_mcp.subprocess, "run", return_value=completed
        ):
            return check_mcp.host_cli_status()

    def test_connected_server(self) -> None:
        result = self._status("sequential-thinking: npx -y pkg - ✓ Connected\n")
        self.assertEqual(result[0][:2], ("claude", "connected"))

    def test_failed_server(self) -> None:
        result = self._status("sequential-thinking: npx -y pkg - ✗ Failed to connect\n")
        self.assertEqual(result[0][1], "not-connected")

    def test_server_not_listed(self) -> None:
        result = self._status("other: x - ✓ Connected\n")
        self.assertEqual(result[0][1], "not-listed")

    def test_cli_that_cannot_run(self) -> None:
        with patch.object(check_mcp.shutil, "which", lambda name: "claude.exe" if name == "claude" else None), patch.object(
            check_mcp.subprocess, "run", side_effect=OSError("incompatible")
        ):
            self.assertEqual(check_mcp.host_cli_status()[0][1], "error")

    def test_host_check_without_any_cli(self) -> None:
        with patch.object(check_mcp.shutil, "which", return_value=None):
            self.assertEqual(check_mcp.host_check(lambda _line: None), 2)


if __name__ == "__main__":
    unittest.main()
