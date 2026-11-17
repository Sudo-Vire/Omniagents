"""Runtime tools for preflight checks, linting, code modifications, and UI verification."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Optional

try:
    from langchain_core.tools import tool
except ImportError:
    def tool(*dargs: Any, **dkwargs: Any) -> Callable[..., Any]:
        """Fallback tool decorator when langchain_core is not installed."""
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            func.name = getattr(func, "__name__", "anonymous_tool")
            func.description = getattr(func, "__doc__", "") or ""
            return func
        if len(dargs) == 1 and callable(dargs[0]):
            return decorator(dargs[0])
        return decorator


def _find_skill_root(start: Optional[Path] = None) -> Optional[Path]:
    """Find the nearest directory containing the skill markers."""
    if start is None:
        start = Path(__file__).resolve().parent
    markers = (
        Path("framework/orchestration/AGENT_INSTRUCTIONS.md"),
        Path("dependencies/installation/requirements.txt"),
    )
    for candidate in (start, *start.parents):
        if all((candidate / m).is_file() for m in markers):
            return candidate
    return None


@tool
def preflight_check(skill_root: Optional[str] = None) -> dict[str, Any]:
    """Run programmatically the preflight dependency inventory checks.

    Validates that utilities listed in dependencies/utils/check_utils.txt are present.
    """
    root_path = Path(skill_root).resolve() if skill_root else _find_skill_root()
    if root_path is None:
        return {
            "success": False,
            "errors": ["Skill root not found: framework/orchestration/AGENT_INSTRUCTIONS.md missing."],
            "placeholders": [],
            "skill_root": None,
        }

    scripts_dir = root_path / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    try:
        from check_dependencies import check_dependency_assets, find_placeholders
        errors = check_dependency_assets(root_path)
        placeholders = find_placeholders(root_path)
        return {
            "success": len(errors) == 0,
            "errors": errors,
            "placeholders": placeholders,
            "skill_root": str(root_path),
        }
    except Exception as exc:
        return {
            "success": False,
            "errors": [f"Preflight check execution failed: {exc}"],
            "placeholders": [],
            "skill_root": str(root_path),
        }


@tool
def run_python_linter(target_dir: str = ".") -> dict[str, Any]:
    """Run ruff check and ruff format --check defensively on the target path."""
    results: dict[str, Any] = {
        "executed": False,
        "success": True,
        "linter": "ruff",
        "errors": [],
        "warnings": [],
        "output": "",
    }
    
    # Check if ruff is executable
    try:
        check_proc = subprocess.run(
            ["ruff", "check", target_dir],
            capture_output=True,
            text=True,
            timeout=30,
        )
        format_proc = subprocess.run(
            ["ruff", "format", "--check", target_dir],
            capture_output=True,
            text=True,
            timeout=30,
        )
        results["executed"] = True
        combined_output = (check_proc.stdout + "\n" + check_proc.stderr + "\n" +
                           format_proc.stdout + "\n" + format_proc.stderr).strip()
        results["output"] = combined_output
        if check_proc.returncode != 0 or format_proc.returncode != 0:
            results["success"] = False
            results["errors"].append(combined_output or "Ruff linter/formatter reported issues.")
    except FileNotFoundError:
        results["executed"] = False
        results["warnings"].append("ruff is not installed on this system; linting skipped.")
    except subprocess.TimeoutExpired:
        results["executed"] = True
        results["success"] = False
        results["errors"].append("ruff check timed out after 30 seconds.")
    except Exception as exc:
        results["executed"] = True
        results["success"] = False
        results["errors"].append(f"Unexpected error running ruff: {exc}")

    return results


@tool
def run_js_linter(target_dir: str = ".") -> dict[str, Any]:
    """Run biome check defensively on the target path."""
    results: dict[str, Any] = {
        "executed": False,
        "success": True,
        "linter": "biome",
        "errors": [],
        "warnings": [],
        "output": "",
    }

    try:
        proc = subprocess.run(
            ["biome", "check", target_dir],
            capture_output=True,
            text=True,
            timeout=30,
        )
        results["executed"] = True
        combined_output = (proc.stdout + "\n" + proc.stderr).strip()
        results["output"] = combined_output
        if proc.returncode != 0:
            results["success"] = False
            results["errors"].append(combined_output or "Biome linter reported issues.")
    except FileNotFoundError:
        results["executed"] = False
        results["warnings"].append("biome is not installed on this system; linting skipped.")
    except subprocess.TimeoutExpired:
        results["executed"] = True
        results["success"] = False
        results["errors"].append("biome check timed out after 30 seconds.")
    except Exception as exc:
        results["executed"] = True
        results["success"] = False
        results["errors"].append(f"Unexpected error running biome: {exc}")

    return results


@tool
def run_browser_verification(task: str = "Verify UI elements and visual structure") -> dict[str, Any]:
    """Execute headless verification using browser_agent.py if available."""
    root_path = _find_skill_root()
    if root_path is None:
        return {"executed": False, "success": True, "warning": "Skill root not found for browser_agent."}

    agent_script = root_path / "dependencies" / "utils" / "tools" / "browser_agent.py"
    if not agent_script.is_file():
        return {
            "executed": False,
            "success": True,
            "warning": f"browser_agent.py not found at {agent_script}",
        }

    try:
        import browser_use  # noqa: F401
    except ImportError:
        return {
            "executed": False,
            "success": True,
            "warning": "browser-use package is not installed; UI verification skipped.",
        }

    try:
        proc = subprocess.run(
            [sys.executable, str(agent_script), task],
            capture_output=True,
            text=True,
            timeout=45,
        )
        return {
            "executed": True,
            "success": proc.returncode == 0,
            "output": (proc.stdout + "\n" + proc.stderr).strip(),
        }
    except subprocess.TimeoutExpired:
        return {
            "executed": True,
            "success": False,
            "errors": ["browser_agent verification timed out after 45s."],
        }
    except Exception as exc:
        return {
            "executed": False,
            "success": False,
            "errors": [f"Failed to execute browser_agent: {exc}"],
        }


@tool
def safe_file_edit(file_path: str, content: str) -> dict[str, Any]:
    """Safely create or update a file on disk."""
    try:
        target = Path(file_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return {"success": True, "path": str(target), "bytes_written": len(content)}
    except Exception as exc:
        return {"success": False, "path": file_path, "error": str(exc)}


@tool
def run_aider_headless(instruction: str, files: list[str] | None = None) -> dict[str, Any]:
    """Delegate to Aider in headless non-destructive mode if installed."""
    results: dict[str, Any] = {
        "executed": False,
        "success": True,
        "output": "",
        "warnings": [],
    }
    cmd = ["aider", "--message", instruction, "--yes-always", "--no-git"]
    if files:
        cmd.extend(files)

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        results["executed"] = True
        results["output"] = (proc.stdout + "\n" + proc.stderr).strip()
        results["success"] = proc.returncode == 0
    except FileNotFoundError:
        results["executed"] = False
        results["warnings"].append("Aider is not installed on system; direct editor used.")
    except Exception as exc:
        results["executed"] = False
        results["warnings"].append(f"Aider execution error: {exc}")

    return results
