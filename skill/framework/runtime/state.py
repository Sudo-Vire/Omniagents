"""AgentState definition with reducers for LangGraph runtime."""

from __future__ import annotations

import operator
from typing import Annotated, Any, Literal, Optional, TypedDict


class AgentState(TypedDict):
    # Entradas conforme a skill/references/execution-contract.md
    objective: str
    context: str
    constraints: list[str]
    acceptance_criteria: list[str]

    # Metadatos de orquestación interna
    task_complexity: Literal["simple", "complex"]
    sequential_thoughts: Annotated[list[str], operator.add]
    active_macro_agent: Optional[str]
    active_tactical_agent: Optional[str]
    office_plan: Optional[str]

    # Human-in-the-Loop y ejecución
    human_approved: bool
    execution_artifacts: Annotated[list[str], operator.add]

    # Validación y control de ciclos
    validation_results: dict[str, Any]
    validation_retries: int  # Contador para evitar bucles infinitos (máximo 3)

    # Salidas según el contrato de ejecución
    status: Literal["completed", "partial", "blocked", "failed", "cancelled"]
    result: str
    errors: Annotated[list[dict[str, str]], operator.add]
    warnings: Annotated[list[str], operator.add]


def create_initial_state(
    objective: str,
    context: str = "",
    constraints: list[str] | None = None,
    acceptance_criteria: list[str] | None = None,
) -> AgentState:
    """Create a fully-initialized AgentState dictionary with contract defaults."""
    return {
        "objective": objective,
        "context": context,
        "constraints": list(constraints) if constraints else [],
        "acceptance_criteria": list(acceptance_criteria) if acceptance_criteria else [],
        "task_complexity": "simple",
        "sequential_thoughts": [],
        "active_macro_agent": None,
        "active_tactical_agent": None,
        "office_plan": None,
        "human_approved": False,
        "execution_artifacts": [],
        "validation_results": {},
        "validation_retries": 0,
        "status": "partial",
        "result": "",
        "errors": [],
        "warnings": [],
    }
