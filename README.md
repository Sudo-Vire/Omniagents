# Devian — Advanced AI Agentic Ecosystem & Tooling

Devian is an open-source, modular framework and ecosystem for advanced AI agents, micro-subagents, specialized skills, autonomous workflows, and local model gateway tooling.


---

## ⚙️ Makefile & Quick Commands

If you have `make` installed, you can use convenient shortcuts:
- `make install` - Run the autonomous installer
- `make lint`    - Verify syntax and lint code
- `make clean`   - Clean caches and build artifacts

---

## 📁 Repository Structure

```text
Devian/
├── agents/                  # Specialized AI agents & sub-agents
│   ├── agency-agents/       # Macro agent catalog (domain-specific agents)
│   └── claude-subagents/    # Tactical micro-subagents
├── skills/                  # Reusable agent skills & superpowers
│   ├── andrej-karpathy-skills/
│   └── superpowers/
├── tools/                   # Execution scripts & utilities (browser automation, office tools, etc.)
│   ├── browser_agent.py
│   └── office.py
└── docs/                    # Ecosystem guides and architectural documentation
    └── ECOSYSTEM_GUIDE.md
```

---

## 🛠️ Prerequisites & System Requirements

- **Python**: Version 3.10 or higher.
- **Local Model Gateway (Omniroute)**: Running at `http://localhost:20128/v1` (optional if using cloud/other providers).
- **Git**: For cloning and fetching repository updates.

---

## 🚀 Installation & Autonomous Setup

You can install Devian and download all ecosystem elements, tools, and dependencies fully autonomously using the provided installation scripts:

### Option 1: Python Installer (Cross-Platform)
```bash
python install.py
```

### Option 2: PowerShell Installer (Windows)
```powershell
.\install.ps1
```

### Manual Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sudo-Vire/Devian.git
   cd Devian
   ```
2. **Create virtual environment & install dependencies**:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux:
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```

---

## 📄 License & Contributing

Contributions are welcome! Please open issues or pull requests for enhancements, new agents, or additional skills.

