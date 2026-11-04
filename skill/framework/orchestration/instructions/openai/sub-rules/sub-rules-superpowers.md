# Superpowers, Karpathy Skills, Browser-Use & Graphify (Modular Subfile)

## 1. Superpowers (`superpowers`) Framework & SDLC Methodology
- **Location**: `superpowers`
- **Purpose**: Agentic skills framework and software development methodology for structured flows of brainstorming, TDD, systematic debugging, plan writing/execution, and subagent-guided development.
- **Key Skills**: `brainstorming`, `test-driven-development`, `systematic-debugging`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `verification-before-completion`.

## 2. Andrej Karpathy Skills (`multica-ai/andrej-karpathy-skills`)
- **Location**: `multica-ai/andrej-karpathy-skills`
- **Purpose**: Behavioral guidelines and coding rules based on Andrej Karpathy's observations:
  1. **Think Before Coding**: Don't assume. Don't hide confusion. Surface tradeoffs.
  2. **Simplicity First**: Minimum code that solves the problem. Nothing speculative.
  3. **Surgical Changes**: Touch only what you must. Clean up only your own mess.
  4. **Goal-Driven Execution**: Define success criteria. Loop until verified.

## 3. Browser-Use & E2E Autonomous Browser Testing Integration
- **Tool**: **Browser-Use** (`browser-use/browser-use`)
- **Purpose**: AI-driven browser automation for autonomous End-to-End (E2E) testing, graphical interface verification, complex user flows and real-time validation.
- **Mandatory Verification Policy**: Every UI change must be verified autonomously using Browser-Use (or integrated Playwright/MCP tools) before finishing any workflow.

## 4. Architectural Knowledge Graph (Graphify)
For any question about architecture, file relationships, dependencies or component explanation:
- **When to use**: When questions of the type *"how do I..."*, *"where is..."*, *"what does..."* or *"explain architecture"* are asked.
- **Tool**: `graphify query "<question>"` or review `graphify-out/GRAPH_REPORT.md` and `graphify-out/wiki/index.md`.

## 5. Linters and Formatters (Ruff & Biome)
- **Python**: **Ruff** (`ruff check` and `ruff format`)
- **JavaScript / TypeScript / Web**: **Biome** (`biome check`)
- **When to use**: Always when code writing is finished before declaring a task completed.
