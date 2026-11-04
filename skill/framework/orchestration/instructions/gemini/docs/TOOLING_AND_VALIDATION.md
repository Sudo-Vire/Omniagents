# Tooling, Testing & Validation

## 1. Superpowers Framework (`superpowers`)
- Structured flows for brainstorming, TDD, systematic debugging, plan writing/execution.
- Key skills: `brainstorming`, `test-driven-development`, `systematic-debugging`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `verification-before-completion`.

## 2. Andrej Karpathy Skills (`multica-ai/andrej-karpathy-skills`)
- Think before coding (surface tradeoffs).
- Simplicity first (minimum code).
- Surgical changes (touch only what you must).
- Goal-driven execution (loop until verified).

## 3. Browser-Use & E2E Testing
- AI-driven browser automation for autonomous End-to-End testing and UI verification.
- Mandatory verification policy for all UI changes.

## 4. Linters & Formatters (Ruff & Biome)
- Python: **Ruff** (`ruff check`, `ruff format`)
- JS/TS/Web: **Biome** (`biome check`)
- Run before declaring any task completed.

## 5. Model Context Protocol (MCP) & Sequential Thinking
- **Tool / MCP Server**: Official `@modelcontextprotocol/server-sequential-thinking` integration, tracked at `dependencies/utils/tools/mcp-sequential-thinking/`.
- **Purpose**: Dynamic, step-by-step reasoning and problem breakdown for complex software architecture, debugging, and multi-step algorithmic planning.
- **Setup**: Follow the host-specific instructions in the integration README. The host must expose the `sequentialthinking` tool; a registry entry by itself does not connect an MCP server. Node.js 24+ and npm access are required for its pinned `npx` launcher.
- **Usage Policy**: For non-trivial framework tasks, invoke `sequentialthinking` before implementation when the host exposes it. Use it for architecture tradeoffs, multi-step changes, difficult debugging, or pre-action risk analysis. Skip trivial edits and lookups. If unavailable, work directly only when safe and disclose the limitation. Report conclusions and decisions, not private internal reasoning.
