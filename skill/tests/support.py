"""Shared paths for the skill tests; importing it makes the skill scripts importable."""

from __future__ import annotations

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
MCP_ADAPTERS = (
    SKILL_DIR / "dependencies" / "utils" / "tools" / "mcp-sequential-thinking" / "adapters"
)

for _path in (
    SKILL_DIR / "scripts",
    SKILL_DIR / "framework" / "actualization",
    SKILL_DIR / "framework" / "orchestration",
):
    if str(_path) not in sys.path:
        sys.path.append(str(_path))
