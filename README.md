# OmniAgent — Universal AI Agent & Multi-Model Orchestration Ecosystem

**OmniAgent** is an open-source, production-grade operating system and framework for orchestrating advanced AI agents, micro-subagents, specialized security and knowledge graph skills, automation tools, and local/cloud LLM gateways (**Claude, Copilot, Gemini, OpenAI, and Omniroute**).

---

## 📂 Project Structure (3 Independent Core Modules)

```text
OmniAgent/
├── CLAUDE.md                # Native instruction file for Claude (Anthropic)
├── installation/            # [Independent Module] Autonomous installers downloading tools from official sources
│   ├── install.py           # Python prerequisite & environment setup wizard
│   ├── install.ps1          # PowerShell setup wizard
│   ├── requirements.txt     # Official PyPI dependency manifest
│   ├── Makefile             # Shortcut commands
│   └── .env.example         # Environment variables template
├── pre-downloaded/          # [Independent Module] Standalone pre-downloaded ecosystem assets
│   ├── agents/              # Macro agents (agency-agents) & micro-subagents (claude-subagents)
│   ├── skills/              # Pre-downloaded skills (Strix, Graphify, Karpathy, UI/UX, Vercel, etc.)
│   └── tools/               # Automation scripts (browser_agent.py, office.py)
└── orchestration/           # [Independent Module] Multi-agent orchestration rules and model instructions
    ├── instructions/        # Model-specific instructions (claude/, copilot/, gemini/, openai/, others/)
    └── docs/                # Ecosystem guides
```

---


---

## 🧠 Orchestration Module (`orchestration/`)
Created by **Sudo-Vire**, the orchestration module contains custom multi-agent instruction frameworks tailored for specific LLM runtimes:
- **GitHub Copilot**: `orchestration/agents/copilot-instructions.md`
- **Claude (Anthropic)**: `orchestration/agents/claude-instructions.md`
- **Gemini (Google)**: `orchestration/agents/gemini-instructions.md`

## 🌐 Multi-Agent & Multi-Model Orchestration

OmniAgent provides unified orchestration across leading AI models and assistants:
- **GitHub Copilot** (VS Code / Copilot SDK)
- **Claude** (Anthropic Claude Code & Desktop)
- **Gemini** (Google Gemini CLI & API)
- **Omniroute / Local Gateways** (`http://localhost:20128/v1`)

---

## ⚙️ Autonomous Installation

### System Requirements
- **Python**: Version 3.10 or higher.
- **Git**: For repository updates.
- **Rust / Cargo**: Recommended for high-performance extensions.

### Installation Commands
```bash
git clone https://github.com/Sudo-Vire/Omniagents.git OmniAgent
cd OmniAgent/installation

# Cross-platform Python installer
python install.py

# Or Windows PowerShell installer
.\install.ps1
```

---

## 📜 Authorship & Copyright Attribution

Please refer to [AUTHORS.md](AUTHORS.md) and [NOTICE](NOTICE) for explicit copyright attribution to upstream creators for Strix, Graphify, Agency Agents, Claude Subagents, and Andrej Karpathy Skills.

---

## 📄 License
Licensed under the [MIT License](LICENSE).
