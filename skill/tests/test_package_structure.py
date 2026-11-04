from __future__ import annotations

import importlib.util
import json
import re
import tempfile
import unittest
from pathlib import Path

from support import SKILL_DIR  # noqa: E402
from check_dependencies import (  # noqa: E402
    find_skill_root,
)
import update_ecosystem  # noqa: E402
import update_model_instructions  # noqa: E402


class PackageStructureTests(unittest.TestCase):
    def test_macro_agent_text_references_exist(self) -> None:
        agents = SKILL_DIR / "dependencies" / "utils" / "agents" / "agency-agents"
        pattern = re.compile(r"`([a-z0-9-]+/[A-Za-z0-9_.-]+\.md)`")
        missing = []
        checked = 0
        for doc in (SKILL_DIR / "framework").rglob("*.md"):
            for line in doc.read_text(encoding="utf-8").splitlines():
                if "Macro Agent" not in line:
                    continue
                for ref in pattern.findall(line):
                    checked += 1
                    if not (agents / ref).is_file():
                        missing.append(f"{doc.name}: {ref}")
        self.assertGreater(checked, 0)
        self.assertEqual([], missing)

    def test_third_party_doc_covers_every_utility_with_license(self) -> None:
        utils = SKILL_DIR / "dependencies" / "utils"
        doc = (utils / "THIRD_PARTY.md").read_text(encoding="utf-8")
        for key in ("agents/agency-agents", "skills/graphify", "skills/gsd",
                    "skills/ui-ux-pro-max", "skills/ciberseguridad",
                    "skills/grill-me", "skills/find-skills", "skills/superpowers"):
            self.assertIn(f"`{key}", doc)
        for key in ("skills/graphify", "skills/ciberseguridad"):
            self.assertTrue((utils / key / "LICENSE").is_file(), key)

    def test_skill_frontmatter_is_valid_for_installation(self) -> None:
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", skill_text, re.DOTALL)
        self.assertIsNotNone(match)
        frontmatter = match.group(1)
        name_match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", frontmatter, re.MULTILINE)
        description_match = re.search(
            r"^description:\s*(.+)$", frontmatter, re.MULTILINE
        )
        compatibility_match = re.search(
            r"^compatibility:\s*(.+)$", frontmatter, re.MULTILINE
        )
        self.assertIsNotNone(name_match)
        self.assertIsNotNone(description_match)
        self.assertIsNotNone(compatibility_match)
        self.assertEqual(name_match.group(1), "omniagents-orchestration")
        self.assertLessEqual(len(name_match.group(1)), 64)
        self.assertTrue(name_match.group(1)[0].isalnum())
        self.assertTrue(name_match.group(1)[-1].isalnum())
        self.assertNotIn("--", name_match.group(1))
        self.assertLessEqual(len(description_match.group(1)), 1024)
        self.assertLessEqual(len(compatibility_match.group(1)), 500)

    def test_skill_instructions_do_not_require_a_specific_host(self) -> None:
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Any host that can load Agent Skills", skill_text)
        self.assertIn("optional templates for VS Code and Claude Code", skill_text)
        self.assertIn("native host agent tools", skill_text)

    def test_docs_do_not_hardcode_repository_paths(self) -> None:
        pattern = re.compile(r"skill/(dependencies|framework|scripts|references)")
        offenders = [
            str(path.relative_to(SKILL_DIR))
            for path in list((SKILL_DIR / "framework").rglob("*.md"))
            + [SKILL_DIR / "SKILL.md", *(SKILL_DIR / "references").glob("*.md")]
            if pattern.search(path.read_text(encoding="utf-8", errors="ignore"))
        ]
        self.assertEqual(offenders, [])

    def test_model_instruction_folders_are_self_contained(self) -> None:
        instructions = SKILL_DIR / "framework" / "orchestration" / "instructions"
        for model_dir in (p for p in instructions.iterdir() if p.is_dir()):
            for md in model_dir.rglob("*.md"):
                text = md.read_text(encoding="utf-8", errors="ignore")
                targets = re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", text)
                targets += re.findall(r"^\s*- @([\w./\-]+)", text, re.MULTILINE)
                for target in targets:
                    if target.startswith(("http", "#")) or target == "absolute_path":
                        continue
                    resolved = (md.parent / target.split("#")[0]).resolve()
                    if "<" in target or not target.split("#")[0]:
                        continue
                    candidate = resolved if resolved.exists() else (model_dir / target).resolve()
                    self.assertTrue(candidate.exists(), f"{md.relative_to(SKILL_DIR)} -> {target}")
                    self.assertTrue(
                        str(candidate).startswith(str(model_dir.resolve())),
                        f"{md.relative_to(SKILL_DIR)} leaves its model folder: {target}",
                    )
            for config in model_dir.glob("*.json"):
                for cached in json.loads(config.read_text(encoding="utf-8-sig")).get(
                    "context_caching", {}
                ).get("cached_files", []):
                    self.assertTrue((model_dir / cached).is_file(), f"{config.name} -> {cached}")

    def test_sync_legal_script_detects_and_fixes_differences(self) -> None:
        script = SKILL_DIR.parent / "scripts" / "sync_legal.py"
        if not script.is_file():
            self.skipTest("repository-level script not present in an installed skill")
        spec = importlib.util.spec_from_file_location("sync_legal", script)
        sync_legal = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sync_legal)
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "skill").mkdir()
            for name in sync_legal.FILES:
                (root / name).write_text(f"{name}\n", encoding="utf-8")
            self.assertEqual(len(sync_legal.out_of_sync(root)), 4)
            self.assertEqual(sorted(sync_legal.sync(root)), sorted(sync_legal.FILES))
            self.assertEqual(sync_legal.out_of_sync(root), [])
            (root / "LICENSE").write_text("changed\n", encoding="utf-8")
            self.assertEqual(len(sync_legal.out_of_sync(root)), 1)

    def test_legal_files_travel_with_the_skill_and_match_the_repository_root(self) -> None:
        for name in ("LICENSE", "NOTICE", "AUTHORS.md", "CONTRIBUTING.md"):
            inside = SKILL_DIR / name
            self.assertTrue(inside.is_file(), name)
            root_copy = SKILL_DIR.parent / name
            # The root copy only exists in the repository checkout, not in an installed skill.
            if (SKILL_DIR.parent / ".git").exists() or root_copy.exists():
                self.assertTrue(root_copy.is_file(), f"{name} missing in repository root")
                self.assertEqual(
                    inside.read_bytes().replace(b"\r\n", b"\n"),
                    root_copy.read_bytes().replace(b"\r\n", b"\n"),
                    f"{name} differs between skill/ and the repository root",
                )

    def test_referenced_markdown_files_exist(self) -> None:
        skill_text = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", skill_text):
            if target.startswith(("https://", "http://", "#")):
                continue
            self.assertTrue((SKILL_DIR / target).is_file(), target)

    def test_preflight_finds_the_portable_skill_root(self) -> None:
        self.assertEqual(find_skill_root(SKILL_DIR / "scripts"), SKILL_DIR)

    def test_actualization_scripts_use_packaged_paths(self) -> None:
        self.assertEqual(
            Path(update_ecosystem.UTILS_DIR),
            SKILL_DIR / "dependencies" / "utils",
        )
        self.assertEqual(
            Path(update_ecosystem.INSTALLATION_DIR),
            SKILL_DIR / "dependencies" / "installation",
        )
        expected_instructions = (
            SKILL_DIR / "framework" / "orchestration" / "instructions"
        )
        self.assertEqual(
            Path(update_ecosystem.INSTRUCTIONS_DIR), expected_instructions
        )
        self.assertEqual(
            Path(update_model_instructions.INSTRUCTIONS_DIR), expected_instructions
        )

    def test_activation_evaluation_has_required_case_counts(self) -> None:
        evaluation = (
            SKILL_DIR / "references" / "activation-evaluation.md"
        ).read_text(encoding="utf-8")
        for heading, expected_count in (
            ("## Should use the skill", 3),
            ("## Should not use the skill", 3),
            ("## Ambiguous", 2),
        ):
            section = evaluation.split(heading, maxsplit=1)[1].split(
                "\n## ", maxsplit=1
            )[0]
            self.assertEqual(
                len(re.findall(r"^\d+\.", section, re.MULTILINE)), expected_count
            )


if __name__ == "__main__":
    unittest.main()
