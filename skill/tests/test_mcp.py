from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from support import MCP_ADAPTERS, SKILL_DIR  # noqa: E402
import check_mcp  # noqa: E402


class McpTests(unittest.TestCase):
    def test_workspace_mcp_config_registers_sequential_thinking(self) -> None:
        config_path = MCP_ADAPTERS / "vscode.mcp.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        server = config["servers"]["sequential-thinking"]
        self.assertEqual(server["type"], "stdio")
        self.assertEqual(server["command"], "npx")
        self.assertEqual(
            server["args"],
            ["-y", "@modelcontextprotocol/server-sequential-thinking@2.0.0"],
        )

    def test_claude_code_mcp_config_registers_sequential_thinking(self) -> None:
        config_path = MCP_ADAPTERS / "mcpServers.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        server = config["mcpServers"]["sequential-thinking"]
        self.assertEqual(server["type"], "stdio")
        self.assertEqual(server["command"], "npx")
        self.assertEqual(
            server["args"],
            ["-y", "@modelcontextprotocol/server-sequential-thinking@2.0.0"],
        )

    def test_sequential_thinking_mcp_is_registered_and_documented(self) -> None:
        inventory = (
            SKILL_DIR / "dependencies" / "utils" / "check_utils.txt"
        ).read_text(encoding="utf-8")
        integration = (
            SKILL_DIR
            / "dependencies"
            / "utils"
            / "tools"
            / "mcp-sequential-thinking"
            / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn("tools/mcp-sequential-thinking", inventory)
        self.assertIn(
            "@modelcontextprotocol/server-sequential-thinking@2.0.0",
            integration,
        )
        self.assertIn("sequentialthinking", integration)
        self.assertIn("does not prove that the host connected", integration)

        for relative_path in (
            Path("framework/orchestration/AGENT_INSTRUCTIONS.md"),
            Path("framework/orchestration/instructions/copilot/docs/TOOLING_AND_VALIDATION.md"),
            Path("framework/orchestration/instructions/gemini/docs/TOOLING_AND_VALIDATION.md"),
            Path("framework/orchestration/instructions/openai/docs/TOOLING_AND_VALIDATION.md"),
        ):
            instructions = (SKILL_DIR / relative_path).read_text(encoding="utf-8")
            self.assertIn("sequentialthinking", instructions, str(relative_path))

    def _run_mcp(self, project: Path, answers: list[str], **kwargs) -> tuple[int, str]:
        output: list[str] = []
        with (
            patch.object(check_mcp, "config_candidates", lambda p: [("VS Code (workspace)", p / ".vscode" / "mcp.json")]),
            patch.object(check_mcp, "check_node", lambda: (True, "Node.js v24.0.0")),
            patch.object(check_mcp, "probe_server", lambda: (True, "ok")),
            patch.dict(os.environ, {check_mcp.SKIP_ENV: ""}),
        ):
            code = check_mcp.run(
                SKILL_DIR, project, ask=lambda _prompt: answers.pop(0),
                out=output.append, **kwargs,
            )
        self.assertEqual(answers, [])
        return code, "\n".join(output)

    def test_mcp_check_warns_without_prompting_when_not_interactive(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, text = self._run_mcp(Path(tmp), [])
            self.assertEqual(code, 0)
            self.assertIn("AVISO", text)
            self.assertFalse((Path(tmp) / ".vscode").exists())

    def test_mcp_check_manual_choice_writes_report_without_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            report = project / "report.md"
            code, text = self._run_mcp(project, ["1", "1"], interactive=True, report_file=report)
            self.assertEqual(code, 0)
            self.assertIn("activar manualmente", text)
            self.assertIn("Pasos para VS Code", report.read_text(encoding="utf-8"))
            self.assertFalse((project / ".vscode").exists())

    def test_mcp_check_auto_choice_merges_config_after_confirmation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            config = project / ".vscode" / "mcp.json"
            config.parent.mkdir()
            config.write_text('{"servers": {"other": {"command": "x"}}}', encoding="utf-8")
            code, text = self._run_mcp(project, ["2", "1", "s", "n"], interactive=True)
            servers = json.loads(config.read_text(encoding="utf-8"))["servers"]
            self.assertEqual(code, 0)
            self.assertIn("other", servers)
            self.assertEqual(servers["sequential-thinking"]["args"][-1], check_mcp.PACKAGE)
            self.assertTrue(config.with_name("mcp.json.omniagents.bak").is_file())
            self.assertIn("[Hecho por el script]", text)

    def test_mcp_check_auto_choice_declined_changes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            code, text = self._run_mcp(project, ["2", "1", "n"], interactive=True)
            self.assertFalse((project / ".vscode").exists())
            self.assertIn("Cancelado", text)

    def test_mcp_check_skip_choice_reports_and_changes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            code, text = self._run_mcp(Path(tmp), ["3"], interactive=True)
            self.assertIn("no activar", text)
            self.assertFalse((Path(tmp) / ".vscode").exists())

    def test_mcp_check_detects_existing_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            config = project / ".vscode" / "mcp.json"
            config.parent.mkdir()
            config.write_text('{"servers": {"sequential-thinking": {}}}', encoding="utf-8")
            code, text = self._run_mcp(project, [], interactive=True)
            self.assertEqual(code, 0)
            self.assertNotIn("AVISO", text)
            self.assertIn("configuración encontrada", text)

    def test_mcp_merge_refuses_unsafe_files_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mcp.json"
            path.write_text('{ // comment\n "servers": {} }', encoding="utf-8")
            with self.assertRaises(ValueError):
                check_mcp.merge_server_config(path, "servers", {})
            path.write_text("{}", encoding="utf-8")
            self.assertTrue(check_mcp.merge_server_config(path, "servers", {"command": "npx"}))
            self.assertFalse(check_mcp.merge_server_config(path, "servers", {"command": "npx"}))

    def test_mcp_project_dir_guess_uses_install_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp).resolve()
            skill = project / ".claude" / "skills" / "omniagents-orchestration"
            skill.mkdir(parents=True)
            self.assertEqual(check_mcp.guess_project_dir(skill, skill / "scripts"), project)
            self.assertEqual(check_mcp.guess_project_dir(skill, project), project)

    def test_mcp_templates_match_script_package(self) -> None:
        for name in ("vscode.mcp.json", "mcpServers.json"):
            text = (MCP_ADAPTERS / name).read_text(encoding="utf-8")
            self.assertIn(check_mcp.PACKAGE, text)


if __name__ == "__main__":
    unittest.main()
