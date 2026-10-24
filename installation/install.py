#!/usr/bin/env python3
"""
Omniagents Advanced Ecosystem & Prerequisite Installer
Verifies system prerequisites (Python, Git, Rust/Cargo), sets up virtual environment,
installs dependencies, checks/guides Omniroute setup, and configures environment variables.
"""

import os
import sys
import subprocess
import shutil
import urllib.request

def run_command(cmd):
    print(f"-> Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[!] Warning: Command failed with exit code {result.returncode}")
    return result.returncode == 0

def check_tool(name, check_cmd):
    print(f"[+] Checking prerequisite: {name}...")
    if shutil.which(name) or subprocess.run(check_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
        print(f"    [OK] {name} is installed.")
        return True
    else:
        print(f"    [!] {name} is NOT found.")
        return False

def check_gateway():
    gateway_url = "http://localhost:20128/v1/models"
    try:
        req = urllib.request.Request(gateway_url, headers={"Authorization": "Bearer not-needed"})
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except Exception:
        return False

def main():
    print("================================================================")
    print("         Omniagents AI Ecosystem - Prerequisite & Setup Wizard      ")
    print("================================================================")

    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    # 1. Prerequisite Checks: Python, Git, Rust/Cargo
    print("\n--- Phase 1: Verifying System Prerequisites ---")
    
    # Python check
    if sys.version_info < (3, 10):
        print("[!] Error: Python 3.10 or higher is required. Please install Python from https://www.python.org/")
        sys.exit(1)
    print(f"    [OK] Python version: {sys.version.split()[0]}")

    # Git check
    has_git = check_tool("git", "git --version")
    if not has_git:
        print("[!] Warning: Git is recommended for fetching and updating ecosystem components.")
        print("    Download Git from: https://git-scm.com/")

    # Rust / Cargo check (needed for compiling certain high-performance ecosystem packages)
    has_rust = check_tool("cargo", "cargo --version")
    if not has_rust:
        print("\n[!] Rust / Cargo is not detected on your system.")
        print("    Some ecosystem tools or packages may require Rust to compile.")
        print("    To install Rust (rustup):")
        print("    - Windows: Visit https://rustup.rs/ or run: winget install Rustlang.Rustup")
        print("    - macOS/Linux: curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh")
        
        choice = input("\nWould you like to continue without Rust/Cargo? (Y/n): ").strip().lower()
        if choice == 'n':
            print("Aborting installation. Please install Rust and re-run.")
            sys.exit(1)

    # 2. Virtual Environment & Dependencies
    print("\n--- Phase 2: Setting up Python Environment & Dependencies ---")
    venv_dir = os.path.join(root_dir, ".venv")
    if not os.path.exists(venv_dir):
        print("[+] Creating isolated virtual environment (.venv)...")
        run_command(f"{sys.executable} -m venv .venv")
    else:
        print("[+] Virtual environment (.venv) already exists.")

    pip_path = os.path.join(venv_dir, "Scripts", "pip") if os.name == "nt" else os.path.join(venv_dir, "bin", "pip")

    if os.path.exists("requirements.txt"):
        print("[+] Installing Python dependencies for agents, tools, and workflows...")
        run_command(f'"{pip_path}" install --upgrade pip')
        run_command(f'"{pip_path}" install -r requirements.txt')

    # 3. Omniroute / Local LLM Gateway Check & Guidance
    print("\n--- Phase 3: Checking Local AI Gateway (Omniroute) ---")
    gateway_active = check_gateway()

    if gateway_active:
        print("[+] Success: Omniroute gateway is running on http://localhost:20128/v1")
    else:
        print("[!] Omniroute Gateway is NOT running or installed on http://localhost:20128/v1.")
        print("\n    How to obtain & set up Omniroute:")
        print("    1. Omniroute provides local LLM routing for Omniagents agents.")
        print("    2. Start your Omniroute service on port 20128.")
        print("    3. Or configure custom API base endpoints below.")
        
        choice = input("\nWould you like to configure custom API base URL now? (y/N): ").strip().lower()
        if choice == 'y':
            custom_base = input("Enter API Base URL [default: http://localhost:20128/v1]: ").strip() or "http://localhost:20128/v1"
            custom_key = input("Enter API Key [default: not-needed]: ").strip() or "not-needed"
            
            env_content = f"OMNIROUTE_API_BASE={custom_base}\nOPENAI_API_BASE={custom_base}\nOPENAI_API_KEY={custom_key}\n"
            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)
            print("[+] Configuration saved to .env successfully.")

    # 4. Summary
    print("\n================================================================")
    print("      Omniagents Ecosystem Installation & Setup Completed!          ")
    print("================================================================")
    if os.name == "nt":
        print("1. Activate venv: .\\.venv\\Scripts\\Activate.ps1")
    else:
        print("1. Activate venv: source .venv/bin/activate")
    print("2. Explore agents: agents/")
    print("3. Explore skills: skills/")
    print("4. Run tools:      python tools/browser_agent.py")
    print("================================================================")

if __name__ == "__main__":
    main()
