# Devian — AI Agentic Ecosystem & Tooling Guide

Welcome to the official documentation and reference guide for **Devian**, an advanced, open-source AI agentic ecosystem, local model gateway, security testing suite, and automation framework.

---

## 1. Architecture & Core Components

Devian is structured into modular components designed for high-performance software engineering, autonomous agents, and multi-model workflows:

### 🌐 Local Model Gateway (Omniroute)
- **Base Endpoint**: `http://localhost:20128/v1`
- **Default Model**: `openai/antigravity/gemini-3.1-flash-lite`
- **Purpose**: Unified local routing gateway for LLM inference across multiple providers and models. *Note: If Omniroute is not yet downloaded or running, the autonomous installer will guide you through setup and configuration.*

### 🤖 Dual Agent Ecosystem (`agents/`)
- **Macro Agent Catalog (`agency-agents/`)**: Domain-specific autonomous agents covering engineering, security, data science, product management, and strategy.
- **Tactical Micro-Subagents (`claude-subagents/`)**: Specialized prompt-driven sub-agents for granular code modification, debugging, and review tasks.

### 🧠 Skills & Superpowers (`skills/`)
- **Andrej Karpathy Skills (`andrej-karpathy-skills/`)**: Advanced development routines, workflow patterns, and coding practices.
- **Superpowers (`superpowers/`)**: Modular extension packs providing advanced reasoning, search, testing, and UI/UX capabilities.

### 🛠️ Tools & Automation Scripts (`tools/`)
- **Browser Automation (`browser_agent.py`)**: Headless browser automation and web interaction utilities.
- **Office Automation (`office.py`)**: Document processing and workspace utility scripts.

### 🛡️ Security, Knowledge Graphs & Quality
- **Autonomous Pentesting (Strix)**: Deep vulnerability analysis and proof-of-concept exploit generation.
- **Knowledge Graph (Graphify)**: Structural codebase mapping and context retrieval.
- **Linters & Formatters**: Ruff, Biome, and Git-Cliff for pristine code quality and changelog generation.

---

## ⚙️ Prerequisites & Autonomous Installation

To run Devian and download all ecosystem elements, tools, and internal dependencies autonomously:

### System Requirements
- **Python**: Version 3.10 or higher.
- **Git**: For cloning and fetching repository updates.
- **Local LLM Gateway (Omniroute)**: Optional initially — the interactive installer will check for it and guide you if it needs to be installed or configured.

### Autonomous Installation Commands
Run the interactive setup wizard via command:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sudo-Vire/Devian.git
   cd Devian
   ```

2. **Run Interactive Installer**:
   - **Cross-Platform (Python)**:
     ```bash
     python install.py
     ```
   - **Windows (PowerShell)**:
     ```powershell
     .\install.ps1
     ```
