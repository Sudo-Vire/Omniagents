# Devian — AI Agentic Ecosystem & Tooling Guide

Welcome to the official documentation and reference guide for **Devian**, an advanced, open-source AI agentic ecosystem, local model gateway, security testing suite, and automation framework.

---

## 1. Architecture & Core Components

Devian is structured into modular components designed for high-performance software engineering, autonomous agents, and multi-model workflows:

### 🌐 Local Model Gateway (Omniroute)
- **Base Endpoint**: \http://localhost:20128/v1\
- **Default Model**: \openai/antigravity/gemini-3.1-flash-lite\
- **Purpose**: Unified local routing gateway for LLM inference across multiple providers and models.

### 🤖 Dual Agent Ecosystem (\gents/\)
- **Macro Agent Catalog (\gency-agents/\)**: Domain-specific autonomous agents covering engineering, security, data science, product management, and strategy.
- **Tactical Micro-Subagents (\claude-subagents/\)**: Specialized prompt-driven sub-agents for granular code modification, debugging, and review tasks.

### 🧠 Skills & Superpowers (\skills/\)
- **Andrej Karpathy Skills (\ndrej-karpathy-skills/\)**: Advanced development routines, workflow patterns, and coding practices.
- **Superpowers (\superpowers/\)**: Modular extension packs providing advanced reasoning, search, testing, and UI/UX capabilities.

### 🛠️ Tools & Automation Scripts (\	ools/\)
- **Browser Automation (\rowser_agent.py\)**: Headless browser automation and web interaction utilities.
- **Office Automation (\office.py\)**: Document processing and workspace utility scripts.

### 🛡️ Security, Knowledge Graphs & Quality
- **Autonomous Pentesting (Strix)**: Deep vulnerability analysis and proof-of-concept exploit generation.
- **Knowledge Graph (Graphify)**: Structural codebase mapping and context retrieval.
- **Linters & Formatters**: Ruff, Biome, and Git-Cliff for pristine code quality and changelog generation.

---

## 🚀 Quick Usage

1. **Clone the repository**:
   \\\ash
   git clone https://github.com/Sudo-Vire/Devian.git
   cd Devian
   \\\
2. **Explore Agents & Skills**:
   - Check agents under \gents/\ and skills under \skills/\.
   - Integrate with VS Code, Copilot SDK, or your preferred LLM runtime.
