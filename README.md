# OmniAgent-OS — Universal AI Agent & Multi-Model Orchestration Ecosystem

**OmniAgent-OS** is an open-source, production-grade operating system and framework for orchestrating advanced AI agents, micro-subagents, specialized security and knowledge graph skills, automation tools, and local/cloud LLM gateways (**Claude, Copilot, Gemini, OpenAI, and Omniroute**).

---

## 📁 Repository Structure

```text
OmniAgent-OS/
├── agents/                  # Specialized AI agents & sub-agents
│   ├── agency-agents/       # Macro agent catalog (domain-specific agents)
│   └── claude-subagents/    # Tactical micro-subagents
├── skills/                  # Reusable agent skills & superpowers (Strix, Graphify, Karpathy, UI/UX, etc.)
│   ├── strix/
│   ├── graphify/
│   ├── andrej-karpathy-skills/
│   └── superpowers/
├── tools/                   # Execution scripts & utilities (browser automation, office tools, etc.)
│   ├── browser_agent.py
│   └── office.py
└── docs/                    # Ecosystem guides and architectural documentation
    └── ECOSYSTEM_GUIDE.md
```

---

## 🌐 Multi-Model & Multi-Agent Compatibility

OmniAgent-OS is built to run across leading AI assistants and model providers:
- **GitHub Copilot** (VS Code / Copilot SDK)
- **Claude** (Anthropic Claude Code & Desktop)
- **Gemini** (Google Gemini CLI & API)
- **Omniroute / Local Gateways** (`http://localhost:20128/v1`)

---

## ⚙️ Prerequisites & Autonomous Installation

### System Requirements
- **Python**: Version 3.10 or higher.
- **Git**: For cloning and fetching repository updates.
- **Rust / Cargo**: Recommended for high-performance extensions.

### Installation Commands
```bash
git clone https://github.com/Sudo-Vire/Devian.git OmniAgent-OS
cd OmniAgent-OS

# Cross-platform Python installer
python install.py

# Or Windows PowerShell installer
.\install.ps1
```

---

## 📜 Authorship & Credits

Please refer to [AUTHORS.md](AUTHORS.md) and [NOTICE](NOTICE) for explicit attribution to upstream creators and open-source contributors for Strix, Graphify, Agency Agents, Claude Subagents, and Andrej Karpathy Skills.

---

## 📄 License
Licensed under the [MIT License](LICENSE).
