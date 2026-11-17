"""LangSmith evaluation suite for Omniagents activation and agent routing."""

from __future__ import annotations

import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Tuple

_tests_dir = Path(__file__).resolve().parent
if str(_tests_dir) not in sys.path:
    sys.path.insert(0, str(_tests_dir))

from support import SKILL_DIR  # noqa: E402
from skill.framework.runtime.nodes import (
    decision_tree_node,
    dual_catalog_router_node,
)
from skill.framework.runtime.state import create_initial_state


def load_activation_cases(skill_dir: Path) -> List[Dict[str, Any]]:
    """Parse evaluation prompts and ground truth from activation-evaluation.md."""
    eval_file = skill_dir / "references" / "activation-evaluation.md"
    content = eval_file.read_text(encoding="utf-8")

    cases: List[Dict[str, Any]] = []

    # 1. Should use the skill -> complex
    should_section = content.split("## Should use the skill", 1)[1].split("\n## ", 1)[0]
    for m in re.finditer(r'^\d+\.\s*[“"](.+?)[”"]', should_section, re.MULTILINE):
        cases.append({
            "prompt": m.group(1).strip(),
            "expected_complexity": "complex",
            "category": "should_use",
        })

    # 2. Should not use the skill -> simple
    should_not_section = content.split("## Should not use the skill", 1)[1].split("\n## ", 1)[0]
    for m in re.finditer(r'^\d+\.\s*[“"](.+?)[”"]', should_not_section, re.MULTILINE):
        cases.append({
            "prompt": m.group(1).strip(),
            "expected_complexity": "simple",
            "category": "should_not_use",
        })

    return cases


def evaluate_decision_tree(cases: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Measure classification accuracy of decision_tree_node."""
    total = len(cases)
    correct = 0
    details = []

    for case in cases:
        state = create_initial_state(objective=case["prompt"])
        res = decision_tree_node(state)
        predicted = res.get("task_complexity")
        is_correct = (predicted == case["expected_complexity"])
        if is_correct:
            correct += 1
        details.append({
            "prompt": case["prompt"],
            "expected": case["expected_complexity"],
            "predicted": predicted,
            "correct": is_correct,
        })

    accuracy = (correct / total) if total > 0 else 0.0
    return {
        "total": total,
        "correct": correct,
        "accuracy": accuracy,
        "details": details,
    }


def evaluate_tactical_router() -> Dict[str, Any]:
    """Measure fidelity of tactical specialist selection based on tech stack."""
    test_stacks: List[Tuple[str, str, str]] = [
        ("package.json", "{}", "01-core-development/fullstack-developer.md"),
        ("requirements.txt", "fastapi>=0.100.0", "02-language-specialists/django-developer.md"),
        ("pyproject.toml", "[tool.poetry]", "02-language-specialists/django-developer.md"),
        ("unknown.txt", "plain content", "01-core-development/backend-architect.md"),
    ]

    total = len(test_stacks)
    correct = 0
    orig_cwd = os.getcwd()

    try:
        for filename, content, expected in test_stacks:
            with tempfile.TemporaryDirectory() as tmp_dir:
                try:
                    os.chdir(tmp_dir)
                    if filename != "unknown.txt":
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(content)
                    state = create_initial_state("Develop microservice backend")
                    res = dual_catalog_router_node(state)
                    if res.get("active_tactical_agent") == expected:
                        correct += 1
                finally:
                    os.chdir(orig_cwd)
    finally:
        os.chdir(orig_cwd)

    return {
        "total": total,
        "correct": correct,
        "accuracy": (correct / total) if total > 0 else 0.0,
    }


def run_langsmith_cloud_eval(cases: List[Dict[str, Any]]) -> bool:
    """Run evaluation via official LangSmith Client if configured."""
    api_key = os.getenv("LANGCHAIN_API_KEY")
    if not api_key:
        return False

    try:
        from langsmith import Client
        client = Client()
        dataset_name = "omniagents-activation-eval"
        if not client.has_dataset(dataset_name=dataset_name):
            dataset = client.create_dataset(
                dataset_name=dataset_name,
                description="Omniagents activation evaluation dataset",
            )
            for case in cases:
                client.create_example(
                    inputs={"objective": case["prompt"]},
                    outputs={"complexity": case["expected_complexity"]},
                    dataset_id=dataset.id,
                )
        print(f"[LangSmith] Synced dataset '{dataset_name}' to LangSmith Cloud.")
        return True
    except Exception as exc:
        print(f"[LangSmith] Cloud evaluation sync skipped: {exc}", file=sys.stderr)
        return False


class TestLangSmithEvaluation(unittest.TestCase):
    """Unittest runner for the evaluation suite."""

    def test_decision_tree_accuracy(self) -> None:
        cases = load_activation_cases(SKILL_DIR)
        self.assertGreaterEqual(len(cases), 6, "Expected at least 6 activation evaluation cases")
        metrics = evaluate_decision_tree(cases)
        self.assertGreaterEqual(
            metrics["accuracy"],
            0.85,
            f"Classification accuracy ({metrics['accuracy']:.2%}) fell below required 85% threshold.",
        )

    def test_tactical_specialist_fidelity(self) -> None:
        metrics = evaluate_tactical_router()
        self.assertEqual(
            metrics["accuracy"],
            1.0,
            f"Tactical router fidelity ({metrics['accuracy']:.2%}) must be 100%.",
        )


def main() -> int:
    print("=" * 65)
    print(" Omniagents LangSmith & Benchmark Evaluation Suite")
    print("=" * 65)

    cases = load_activation_cases(SKILL_DIR)
    print(f"Loaded {len(cases)} cases from {SKILL_DIR / 'references' / 'activation-evaluation.md'}\n")

    print("Running Decision Tree Classification Evaluation...")
    dt_metrics = evaluate_decision_tree(cases)
    print(f"  - Total cases : {dt_metrics['total']}")
    print(f"  - Correct     : {dt_metrics['correct']}")
    print(f"  - Accuracy    : {dt_metrics['accuracy']:.1%}\n")

    print("Running Tactical Router Stack Detection Evaluation...")
    tr_metrics = evaluate_tactical_router()
    print(f"  - Total stacks: {tr_metrics['total']}")
    print(f"  - Correct     : {tr_metrics['correct']}")
    print(f"  - Accuracy    : {tr_metrics['accuracy']:.1%}\n")

    run_langsmith_cloud_eval(cases)

    print("=" * 65)
    success = (dt_metrics["accuracy"] >= 0.85) and (tr_metrics["accuracy"] == 1.0)
    print(f"Evaluation Result: {'PASSED' if success else 'FAILED'}")
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
