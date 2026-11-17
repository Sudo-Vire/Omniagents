"""Unit and integration tests for the Omniagents LangGraph runtime."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

_tests_dir = Path(__file__).resolve().parent
if str(_tests_dir) not in sys.path:
    sys.path.insert(0, str(_tests_dir))

from support import SKILL_DIR  # noqa: E402

try:
    from skill.framework.runtime.state import AgentState, create_initial_state
    from skill.framework.runtime import nodes
    from skill.framework.runtime.nodes import (
        TaskClassification,
        preflight_node,
        route_preflight,
        decision_tree_node,
        route_decision_tree,
        sequential_thinking_node,
        dual_catalog_router_node,
        virtual_office_planner_node,
        human_approval_gate,
        route_human_approval,
        executor_node,
        validation_node,
        route_validation,
    )
    from skill.framework.runtime.graph import (
        build_runnable_config,
        create_orchestrator_graph,
        run_orchestration,
    )
except ImportError:
    from framework.runtime.state import AgentState, create_initial_state
    from framework.runtime import nodes
    from framework.runtime.nodes import (
        TaskClassification,
        preflight_node,
        route_preflight,
        decision_tree_node,
        route_decision_tree,
        sequential_thinking_node,
        dual_catalog_router_node,
        virtual_office_planner_node,
        human_approval_gate,
        route_human_approval,
        executor_node,
        validation_node,
        route_validation,
    )
    from framework.runtime.graph import (
        build_runnable_config,
        create_orchestrator_graph,
        run_orchestration,
    )


class FakeStructuredModel:
    """Mock structured LLM model for unit testing without live network."""

    def __init__(self, output: TaskClassification) -> None:
        self.output = output

    def invoke(self, *args, **kwargs) -> TaskClassification:
        return self.output


class FakeChatModel:
    """Fake chat model adhering to LangChain ChatModel interface."""

    def __init__(self, structured_output: TaskClassification) -> None:
        self.structured_output = structured_output

    def with_structured_output(self, schema):
        return FakeStructuredModel(self.structured_output)

    def invoke(self, *args, **kwargs) -> str:
        return "Fake model response"


class TestRuntimeGraph(unittest.TestCase):
    """Test suite covering the deterministic LangGraph orchestration workflow."""

    def test_initial_state_defaults(self) -> None:
        state = create_initial_state("Implement auth module", context="Repo context")
        self.assertEqual(state["objective"], "Implement auth module")
        self.assertEqual(state["context"], "Repo context")
        self.assertEqual(state["constraints"], [])
        self.assertEqual(state["acceptance_criteria"], [])
        self.assertEqual(state["task_complexity"], "simple")
        self.assertEqual(state["sequential_thoughts"], [])
        self.assertEqual(state["execution_artifacts"], [])
        self.assertEqual(state["validation_retries"], 0)
        self.assertEqual(state["status"], "partial")

    def test_preflight_node_success_and_blocked(self) -> None:
        # 1. Success case
        state = create_initial_state("Standard task")
        with patch.object(nodes, "preflight_check", return_value={"success": True}):
            res = preflight_node(state)
            self.assertEqual(res["status"], "partial")
            state["status"] = res["status"]
            self.assertEqual(route_preflight(state), "ok")

        # 2. Blocked case (missing dependencies)
        with patch.object(
            nodes,
            "preflight_check",
            return_value={"success": False, "errors": ["Missing agents/agency-agents"]},
        ):
            res = preflight_node(state)
            self.assertEqual(res["status"], "blocked")
            self.assertTrue(len(res["errors"]) > 0)
            self.assertEqual(res["errors"][0]["code"], "DEPENDENCY_MISSING")
            state["status"] = res["status"]
            self.assertEqual(route_preflight(state), "blocked")

    def test_decision_tree_complexity_heuristic(self) -> None:
        # Simple task
        state_simple = create_initial_state("Fix this one spelling mistake in the README.")
        res_simple = decision_tree_node(state_simple)
        self.assertEqual(res_simple["task_complexity"], "simple")
        state_simple["task_complexity"] = res_simple["task_complexity"]
        self.assertEqual(route_decision_tree(state_simple), "simple")

        # Complex task
        state_complex = create_initial_state("Coordinate independent architecture and test-plan reviews")
        res_complex = decision_tree_node(state_complex)
        self.assertEqual(res_complex["task_complexity"], "complex")
        state_complex["task_complexity"] = res_complex["task_complexity"]
        self.assertEqual(route_decision_tree(state_complex), "complex")

    def test_decision_tree_with_fake_llm(self) -> None:
        fake_llm = FakeChatModel(TaskClassification(complexity="complex", reasoning="Multi-agent requirements"))
        state = create_initial_state("Refactor payment processing")
        config = {"configurable": {"llm": fake_llm}}

        res = decision_tree_node(state, config=config)
        self.assertEqual(res["task_complexity"], "complex")

    def test_sequential_thinking_node(self) -> None:
        state = create_initial_state("Design database migrations", constraints=["Zero downtime"])
        res = sequential_thinking_node(state)
        thoughts = res["sequential_thoughts"]
        self.assertGreaterEqual(len(thoughts), 3)
        self.assertTrue(any("Hypothesis" in t for t in thoughts))
        self.assertTrue(any("Zero downtime" in t for t in thoughts))

    def test_dual_catalog_router_node(self) -> None:
        # Test UI-focused task
        state_ui = create_initial_state("Redesign frontend accessibility and css layout")
        res_ui = dual_catalog_router_node(state_ui)
        self.assertEqual(res_ui["active_macro_agent"], "design/design-ui-designer.md")

        # Test Security-focused task
        state_sec = create_initial_state("Perform security audit and pentest with strix")
        res_sec = dual_catalog_router_node(state_sec)
        self.assertEqual(res_sec["active_macro_agent"], "engineering/engineering-identity-access-engineer.md")

        # Test Stack detection
        with tempfile.TemporaryDirectory() as tmp_dir:
            orig_cwd = os.getcwd()
            try:
                os.chdir(tmp_dir)
                # Test Node/Package.json stack
                with open("package.json", "w", encoding="utf-8") as f:
                    f.write("{}")
                res = dual_catalog_router_node(state_ui)
                self.assertEqual(res["active_tactical_agent"], "01-core-development/fullstack-developer.md")

                os.remove("package.json")
                # Test Python/Requirements.txt stack
                with open("requirements.txt", "w", encoding="utf-8") as f:
                    f.write("django>=4.0")
                res = dual_catalog_router_node(state_ui)
                self.assertEqual(res["active_tactical_agent"], "02-language-specialists/django-developer.md")
            finally:
                os.chdir(orig_cwd)

    def test_virtual_office_planner_node(self) -> None:
        state = create_initial_state("Refactor identity and access management")
        state["active_macro_agent"] = "engineering/engineering-identity-access-engineer.md"
        state["active_tactical_agent"] = "01-core-development/backend-architect.md"
        state["sequential_thoughts"] = ["Hypothesis 1: OAuth2 flow upgrade"]

        res = virtual_office_planner_node(state)
        self.assertIn("Virtual Office Plan", res["office_plan"])
        self.assertIn("OAuth2 flow upgrade", res["office_plan"])

    def test_human_approval_gate_approved_and_cancelled(self) -> None:
        # Pre-approved
        state_approved = create_initial_state("Task A")
        state_approved["human_approved"] = True
        res_approved = human_approval_gate(state_approved)
        self.assertTrue(res_approved["human_approved"])
        self.assertEqual(route_human_approval(state_approved), "approved")

        # User rejected / cancelled
        state_rejected = create_initial_state("Task B")
        with patch.object(nodes, "interrupt", return_value=False):
            res_rejected = human_approval_gate(state_rejected)
            self.assertFalse(res_rejected["human_approved"])
            self.assertEqual(res_rejected["status"], "cancelled")
            self.assertEqual(route_human_approval(res_rejected), "cancelled")

    def test_validation_retry_loop_and_max_limit(self) -> None:
        state = create_initial_state("Task with lint errors")

        # Retries 0 -> 1 (retry)
        state["validation_retries"] = 0
        state["validation_results"] = {"simulate_error": True}
        res_1 = validation_node(state)
        self.assertEqual(res_1["validation_retries"], 1)
        self.assertTrue(len(res_1["warnings"]) > 0)
        state["validation_retries"] = 1
        self.assertEqual(route_validation(state), "retry")

        # Retries 1 -> 2 (retry)
        state["validation_retries"] = 1
        res_2 = validation_node(state)
        self.assertEqual(res_2["validation_retries"], 2)

        # Retries 2 -> 3 (retry)
        state["validation_retries"] = 2
        res_3 = validation_node(state)
        self.assertEqual(res_3["validation_retries"], 3)

        # Persistent failure at retry 3 -> status="partial", routes to END
        state["validation_retries"] = 3
        res_final = validation_node(state)
        self.assertEqual(res_final["status"], "partial")
        self.assertIn("Persistent validation failures after 3 retries", res_final["warnings"][0])
        state["status"] = "partial"
        self.assertEqual(route_validation(state), "partial")

    def test_validation_clean_completion(self) -> None:
        state = create_initial_state("Clean task")
        with patch.object(nodes, "run_python_linter", return_value={"success": True, "executed": True}), \
             patch.object(nodes, "run_js_linter", return_value={"success": True, "executed": True}):
            res = validation_node(state)
            self.assertEqual(res["status"], "completed")
            self.assertIn("Successfully orchestrated task", res["result"])
            state["status"] = res["status"]
            self.assertEqual(route_validation(state), "completed")

    def test_build_runnable_config_observability(self) -> None:
        state = create_initial_state("Observable task")
        state["task_complexity"] = "complex"
        state["active_macro_agent"] = "engineering/engineering-software-architect.md"
        state["validation_retries"] = 2

        config = build_runnable_config(state, thread_id="thread-test-123")
        self.assertIn("omniagents", config["tags"])
        self.assertIn("complexity:complex", config["tags"])
        self.assertIn("macro:engineering/engineering-software-architect.md", config["tags"])
        self.assertEqual(config["metadata"]["thread_id"], "thread-test-123")
        self.assertEqual(config["metadata"]["retries"], 2)
        self.assertEqual(config["metadata"]["gateway"], "omniroute")

    def test_full_orchestration_simple_flow(self) -> None:
        input_data = {
            "objective": "Fix this one spelling mistake in the README.",
            "context": "README.md line 12",
        }
        output = run_orchestration(input_data=input_data, thread_id="test-simple")
        self.assertEqual(output["status"], "completed")
        self.assertEqual(output["state"]["task_complexity"], "simple")
        self.assertIn("Successfully orchestrated task", output["result"])

    def test_full_orchestration_complex_flow(self) -> None:
        input_data = {
            "objective": "Coordinate independent architecture and security reviews for new API",
            "context": "API v2 design",
            "human_approved": True,
        }
        output = run_orchestration(input_data=input_data, thread_id="test-complex")
        self.assertEqual(output["status"], "completed")
        self.assertEqual(output["state"]["task_complexity"], "complex")
        self.assertIsNotNone(output["state"]["active_macro_agent"])
        self.assertIsNotNone(output["state"]["office_plan"])

    def test_activation_evaluation_dataset(self) -> None:
        from eval_langsmith import load_activation_cases, evaluate_decision_tree
        cases = load_activation_cases(SKILL_DIR)
        metrics = evaluate_decision_tree(cases)
        self.assertGreaterEqual(metrics["accuracy"], 0.85)


if __name__ == "__main__":
    unittest.main()
