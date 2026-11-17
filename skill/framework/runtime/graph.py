"""LangGraph StateGraph assembly, conditional routing, checkpointing, and LangSmith observability."""

from __future__ import annotations

import os
from typing import Any, Callable, Dict, Literal, Optional

from .state import AgentState, create_initial_state
from .nodes import (
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

# Try importing real LangGraph components; provide compliant fallback if not installed.
try:
    from langgraph.graph import StateGraph, START, END
    from langgraph.checkpoint.memory import MemorySaver
    HAVE_LANGGRAPH = True
except ImportError:
    HAVE_LANGGRAPH = False
    START = "__start__"
    END = "__end__"

    class MemorySaver:
        """In-memory checkpointer fallback when langgraph is not installed."""
        def __init__(self) -> None:
            self.storage: dict[str, dict[str, Any]] = {}

        def get(self, config: dict[str, Any]) -> Optional[dict[str, Any]]:
            thread_id = config.get("configurable", {}).get("thread_id", "default")
            return self.storage.get(thread_id)

        def put(self, config: dict[str, Any], checkpoint: dict[str, Any]) -> None:
            thread_id = config.get("configurable", {}).get("thread_id", "default")
            self.storage[thread_id] = checkpoint

    class FallbackCompiledGraph:
        """Deterministic graph executor mimicking LangGraph execution loop."""
        def __init__(
            self,
            nodes: dict[str, Callable[..., Any]],
            edges: dict[str, str],
            conditional_edges: dict[str, tuple[Callable[..., Any], dict[str, str]]],
            checkpointer: Any = None,
        ) -> None:
            self.nodes = nodes
            self.edges = edges
            self.conditional_edges = conditional_edges
            self.checkpointer = checkpointer

        def invoke(self, state: AgentState, config: Optional[dict[str, Any]] = None) -> AgentState:
            current_state = dict(state)
            current_node = self.edges.get(START)

            visited_count = 0
            max_steps = 50

            while current_node and current_node != END and visited_count < max_steps:
                visited_count += 1
                node_func = self.nodes.get(current_node)
                if not node_func:
                    break

                # Execute node with defensive exception handling
                try:
                    patch = node_func(current_state, config)
                except Exception as exc:
                    patch = {
                        "status": "failed",
                        "errors": [{"code": "AGENT_FAILED", "message": f"Node {current_node} failed: {exc}"}],
                    }

                # Apply state patch honoring list concatenation (Annotated operator.add)
                if isinstance(patch, dict):
                    for k, v in patch.items():
                        if k in ("sequential_thoughts", "execution_artifacts", "errors", "warnings"):
                            existing = current_state.get(k) or []
                            current_state[k] = list(existing) + list(v)
                        else:
                            current_state[k] = v

                # Save checkpoint if configured
                if self.checkpointer and config:
                    try:
                        self.checkpointer.put(config, dict(current_state))
                    except Exception:
                        pass

                # Resolve next node
                if current_node in self.conditional_edges:
                    route_fn, path_map = self.conditional_edges[current_node]
                    route_key = route_fn(current_state)
                    next_node = path_map.get(route_key, END)
                else:
                    next_node = self.edges.get(current_node, END)

                current_node = next_node

            return current_state  # type: ignore

    class StateGraph:  # type: ignore
        """Fallback StateGraph builder conforming to LangGraph interface."""
        def __init__(self, state_schema: Any) -> None:
            self.state_schema = state_schema
            self.nodes: dict[str, Callable[..., Any]] = {}
            self.edges: dict[str, str] = {}
            self.conditional_edges: dict[str, tuple[Callable[..., Any], dict[str, str]]] = {}

        def add_node(self, name: str, action: Callable[..., Any]) -> None:
            self.nodes[name] = action

        def add_edge(self, start_key: str, end_key: str) -> None:
            self.edges[start_key] = end_key

        def add_conditional_edges(
            self,
            source: str,
            path: Callable[..., Any],
            path_map: dict[str, str],
        ) -> None:
            self.conditional_edges[source] = (path, path_map)

        def compile(self, checkpointer: Any = None) -> Any:
            return FallbackCompiledGraph(
                self.nodes,
                self.edges,
                self.conditional_edges,
                checkpointer=checkpointer,
            )


def configure_langsmith_tracing(project_name: str = "omniagents-orchestration") -> bool:
    """Configure LangSmith tracing environment variables if API credentials are present."""
    api_key = os.getenv("LANGCHAIN_API_KEY")
    if api_key:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ.setdefault("LANGCHAIN_PROJECT", project_name)
        if "LANGCHAIN_ENDPOINT" not in os.environ:
            os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        return True
    return False


def build_runnable_config(
    state: dict[str, Any],
    thread_id: str,
    extra_tags: Optional[list[str]] = None,
    extra_metadata: Optional[dict[str, Any]] = None,
    llm: Optional[Any] = None,
) -> dict[str, Any]:
    """Construct enriched RunnableConfig with metadata and tags for LangSmith observability."""
    complexity = state.get("task_complexity", "unknown")
    macro = state.get("active_macro_agent") or "none"
    retries = state.get("validation_retries", 0)

    tags = ["omniagents", f"complexity:{complexity}", f"macro:{macro}"]
    if extra_tags:
        tags.extend(extra_tags)

    metadata: dict[str, Any] = {
        "gateway": "omniroute",
        "retries": retries,
        "thread_id": thread_id,
    }
    if extra_metadata:
        metadata.update(extra_metadata)

    configurable: dict[str, Any] = {"thread_id": thread_id}
    if llm is not None:
        configurable["llm"] = llm

    return {
        "configurable": configurable,
        "tags": tags,
        "metadata": metadata,
    }


def create_orchestrator_graph(checkpointer: Any = None) -> Any:
    """Build and compile the modular Omniagents orchestration graph.

    Topological Flow:
        [START] -> [preflight_node]
            ├─(blocked)─> [END]
            └─(ok)──────> [decision_tree_node]
                            ├─(simple)─> [executor_node]
                            └─(complex)─> [sequential_thinking_node]
                                            -> [dual_catalog_router_node]
                                            -> [virtual_office_planner_node]
                                            -> [human_approval_gate]
                                                ├─(cancelled)─> [END]
                                                └─(approved)──> [executor_node]
                                                                  -> [validation_node]
                                                                      ├─(retry < 3)──> [executor_node]
                                                                      ├─(partial)────> [END]
                                                                      └─(completed)──> [END]
    """
    workflow = StateGraph(AgentState)

    # Register Nodes
    workflow.add_node("preflight_node", preflight_node)
    workflow.add_node("decision_tree_node", decision_tree_node)
    workflow.add_node("sequential_thinking_node", sequential_thinking_node)
    workflow.add_node("dual_catalog_router_node", dual_catalog_router_node)
    workflow.add_node("virtual_office_planner_node", virtual_office_planner_node)
    workflow.add_node("human_approval_gate", human_approval_gate)
    workflow.add_node("executor_node", executor_node)
    workflow.add_node("validation_node", validation_node)

    # Register Edges & Conditional Transitions
    workflow.add_edge(START, "preflight_node")

    workflow.add_conditional_edges(
        "preflight_node",
        route_preflight,
        {
            "blocked": END,
            "ok": "decision_tree_node",
        },
    )

    workflow.add_conditional_edges(
        "decision_tree_node",
        route_decision_tree,
        {
            "simple": "executor_node",
            "complex": "sequential_thinking_node",
        },
    )

    workflow.add_edge("sequential_thinking_node", "dual_catalog_router_node")
    workflow.add_edge("dual_catalog_router_node", "virtual_office_planner_node")
    workflow.add_edge("virtual_office_planner_node", "human_approval_gate")

    workflow.add_conditional_edges(
        "human_approval_gate",
        route_human_approval,
        {
            "approved": "executor_node",
            "cancelled": END,
        },
    )

    workflow.add_edge("executor_node", "validation_node")

    workflow.add_conditional_edges(
        "validation_node",
        route_validation,
        {
            "retry": "executor_node",
            "partial": END,
            "completed": END,
        },
    )

    if checkpointer is None:
        checkpointer = MemorySaver()

    return workflow.compile(checkpointer=checkpointer)


def run_orchestration(
    input_data: dict[str, Any],
    thread_id: str = "session-001",
    checkpointer: Any = None,
    llm: Optional[Any] = None,
) -> dict[str, Any]:
    """Execute the Omniagents LangGraph orchestration workflow.

    Conforms strictly to the execution contract:
    Returns status, result, errors, artifacts, warnings.
    """
    configure_langsmith_tracing()

    objective = input_data.get("objective", "")
    context = input_data.get("context", "")
    constraints = input_data.get("constraints", [])
    acceptance_criteria = input_data.get("acceptance_criteria", [])

    initial_state = create_initial_state(
        objective=objective,
        context=context,
        constraints=constraints,
        acceptance_criteria=acceptance_criteria,
    )

    # If caller provided initial state overrides (e.g. human_approved=True or simulated tests)
    for key in ("human_approved", "validation_results", "task_complexity"):
        if key in input_data:
            initial_state[key] = input_data[key]

    config = build_runnable_config(
        initial_state,
        thread_id=thread_id,
        llm=llm,
    )

    app = create_orchestrator_graph(checkpointer=checkpointer)
    final_state = app.invoke(initial_state, config=config)

    # Format return dictionary strictly complying with execution-contract.md
    return {
        "status": final_state.get("status", "partial"),
        "result": final_state.get("result", ""),
        "errors": final_state.get("errors", []),
        "artifacts": final_state.get("execution_artifacts", []),
        "warnings": final_state.get("warnings", []),
        "state": final_state,
    }
