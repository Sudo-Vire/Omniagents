# OmniAgent — Universal AI Agent & Multi-Model Orchestration Ecosystem

**OmniAgent** is a production-grade operating system and framework for orchestrating advanced AI agents, micro-subagents, specialized security and knowledge graph skills, automation tools, and local/cloud LLM gateways (**Claude, Copilot, Gemini, OpenAI, and Omniroute**).

---

## 📂 Project Structure (4 Core Modules)

```text
OmniAgent/
├── installation/            # [Independent Module] Autonomous installers downloading tools from official sources
│   ├── install.py           # Python prerequisite & environment setup wizard
│   ├── install.ps1          # PowerShell setup wizard
│   ├── requirements.txt     # Official PyPI dependency manifest
│   ├── Makefile             # Shortcut commands
│   └── .env.example         # Environment variables template
├── pre-downloaded/          # [Independent Module] Standalone pre-downloaded ecosystem assets
│   ├── agents/              # Macro agents (agency-agents) & micro-subagents (claude-subagents)
│   ├── skills/              # Pre-downloaded skills (Strix, Graphify, Karpathy, UI/UX, Vercel, etc.)
│   └── tools/               # Automation scripts & MCP servers (mcp-sequential-thinking, etc.)
├── orchestration/           # [Independent Module] Multi-agent orchestration rules and model instructions
│   ├── instructions/        # Model-specific instructions (claude/, copilot/, gemini/sub-rules/, openai/sub-rules/, others/)
│   └── docs/                # Ecosystem guides & tooling validation
└── actualization/           # [Independent Module] AI-powered ecosystem updaters & cross-model synchronization
    ├── update_ecosystem.py  # Interactive assistant to add agents, tools, skills, or MCPs with AI-generated docs
    └── update_model_instructions.py # AI-verified cross-model instruction synchronizer
```

---

## 🧠 Orchestration Module (`orchestration/`)
Tailored multi-agent instruction frameworks optimized for each LLM runtime:
- **GitHub Copilot**: `orchestration/instructions/copilot/copilot-instructions.md`
- **Claude (Anthropic)**: `orchestration/instructions/claude/CLAUDE.md`
- **Google Gemini**: `orchestration/instructions/gemini/GEMINI.md` (with Context Caching & modular `sub-rules/`)
- **OpenAI / GPT**: `orchestration/instructions/openai/OPENAI.md` & `assistant-instructions.json` (with Assistants API support)

---

## 🔄 AI-Powered Ecosystem Updating & Actualization (`actualization/`)
OmniAgent includes autonomous tools to expand the ecosystem and synchronize instructions across models:
- **Add Resources**: Run `python actualization/update_ecosystem.py` to interactively add agents, MCP servers, skills, or sub-rules. The system uses the local Omniroute AI gateway to generate rich, context-aware integration documentation automatically.
- **Sync Instructions**: Run `python actualization/update_model_instructions.py` to verify and align multi-model instructions.

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
Licensed under the **Non-Commercial Software License Agreement** (Commercialization without explicit written permission from Sudo-Vire is strictly prohibited). See [LICENSE](LICENSE).
