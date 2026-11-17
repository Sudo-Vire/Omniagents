"""CLI entry point for running the Omniagents LangGraph runtime."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Ensure package importability when executed directly as a script
_CURRENT = Path(__file__).resolve()
_REPO_ROOT = _CURRENT.parents[3]
_SKILL_ROOT = _CURRENT.parents[2]
for _candidate in (_REPO_ROOT, _SKILL_ROOT):
    if str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))

try:
    from skill.framework.runtime.graph import run_orchestration
except ImportError:
    from framework.runtime.graph import run_orchestration


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Execute the Omniagents autonomous and observable LangGraph runtime.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--objective",
        required=True,
        help="Primary task objective to orchestrate.",
    )
    parser.add_argument(
        "--thread-id",
        default="session-001",
        help="Session/thread identifier for checkpointing and LangSmith tracing.",
    )
    parser.add_argument(
        "--context",
        default="",
        help="Relevant repository or architectural context.",
    )
    parser.add_argument(
        "--constraints",
        nargs="*",
        default=[],
        help="Scope, privacy, permission, or deadline limits.",
    )
    parser.add_argument(
        "--acceptance-criteria",
        nargs="*",
        default=[],
        help="Measurable acceptance criteria for the outcome.",
    )
    parser.add_argument(
        "--approve",
        action="store_true",
        help="Pre-approve the execution plan at the human approval gate.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output the execution result as structured JSON.",
    )

    args = parser.parse_args(argv)

    print("=" * 60)
    print(" Omniagents Autonomous Runtime (LangGraph + LangSmith)")
    print("=" * 60)
    print(f"Objective : {args.objective}")
    print(f"Thread ID : {args.thread_id}")
    if args.context:
        print(f"Context   : {args.context}")
    print("-" * 60)

    input_data = {
        "objective": args.objective,
        "context": args.context,
        "constraints": args.constraints,
        "acceptance_criteria": args.acceptance_criteria,
        "human_approved": args.approve,
    }

    try:
        output = run_orchestration(input_data=input_data, thread_id=args.thread_id)
    except Exception as exc:
        print(f"\n[FATAL ERROR] Runtime execution halted: {exc}", file=sys.stderr)
        return 1

    if args.json:
        # Exclude non-serializable objects from state if needed
        clean_output = {
            "status": output.get("status"),
            "result": output.get("result"),
            "errors": output.get("errors"),
            "artifacts": output.get("artifacts"),
            "warnings": output.get("warnings"),
        }
        print(json.dumps(clean_output, indent=2, ensure_ascii=False))
        return 0 if output.get("status") == "completed" else 2

    print(f"Status    : {output.get('status')}")
    print(f"Result    : {output.get('result')}")
    if output.get("artifacts"):
        print(f"Artifacts : {', '.join(output['artifacts'])}")
    if output.get("warnings"):
        print("Warnings  :")
        for w in output["warnings"]:
            print(f"  - {w}")
    if output.get("errors"):
        print("Errors    :")
        for e in output["errors"]:
            print(f"  - [{e.get('code')}]: {e.get('message')}")
    print("=" * 60)

    return 0 if output.get("status") in ("completed", "partial") else 2


if __name__ == "__main__":
    sys.exit(main())
