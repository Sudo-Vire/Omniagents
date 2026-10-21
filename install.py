#!/usr/bin/env python3
"""
Devian Autonomous Ecosystem & Gateway Installer
Guides the user through setting up Devian, installing Python dependencies,
detecting or guiding the setup of Omniroute (local LLM gateway), and configuring environment variables.
"""

import os
import sys
import subprocess
import urllib.request
import json
import time

def run_command(cmd):
    print(f"-> Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[!] Warning: Command failed with exit code {result.returncode}")
    return result.returncode == 0

def check_gateway():
    gateway_url = "http://localhost:20128/v1/models"
    try:
        req = urllib.request.Request(gateway_url, headers={"Authorization": "Bearer not-needed"})
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status == 200
    except Exception:
        return false

def main():
    print("================================================================")
    print("         Devian Advanced AI Ecosystem - Setup & Installer       ")
    print("================================================================")

    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    # 1. Python version check
    if sys.version_info < (3, 10):
        print("[!] Error: Python 3.10 or higher is required.")
        sys.exit(1)
    print(f"[+] Python version verified: {sys.version.split()[0]}")

    # 2. Virtual environment setup
    venv_dir = os.path.join(root_dir, ".venv")
    if not os.path.exists(venv_dir):
        print("[+] Creating isolated virtual environment (.venv)...")
        run_command(f"{sys.executable} -m venv .venv")
    else:
        print("[+] Virtual environment (.venv) already exists.")

    if os.name == "nt":
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
    else:
        pip_path = os.path.join(venv_dir, "bin", "pip")

    # 3. Install core dependencies
    if os.path.exists("requirements.txt"):
        print("[+] Installing Python dependencies for agents, tools, and workflows...")
        run_command(f'"{pip_path}" install --upgrade pip')
        run_command(f'"{pip_path}" install -r requirements.txt')
    else:
        print("[!] requirements.txt not found. Skipping dependency installation.")

    # 4. Omniroute / Local LLM Gateway check & interactive guidance
    print("\n----------------------------------------------------------------")
    print("[+] Checking Local AI Gateway (Omniroute)...")
    gateway_active = check_gateway()

    if gateway_active:
        print("[+] Success: Omniroute gateway is running and reachable on http://localhost:20128/v1")
    else:
        print("[!] Omniroute Gateway is NOT currently running or installed on http://localhost:20128/v1.")
        print("\n--- HOW TO OBTAIN & INSTALL OMNIROUTE ---")
        print("1. Omniroute provides local LLM routing for Devian agents.")
        print("2. If you have Omniroute installed locally, start its service:")
        print("   - Run your Omniroute server binary or docker container on port 20128.")
        print("3. If you need to install Omniroute or configure another provider:")
        print("   - Set your environment variables (e.g., OMNIROUTE_API_BASE or OPENAI_API_BASE).")
        print("----------------------------------------------------------------\n")

        choice = input("Would you like to configure custom gateway / API settings now? (y/N): ").strip().lower()
        if choice == 'y':
            custom_base = input("Enter API Base URL [default: http://localhost:20128/v1]: ").strip()
            if not custom_base:
                custom_base = "http://localhost:20128/v1"
            
            custom_key = input("Enter API Key [default: not-needed]: ").strip()
            if not custom_key:
                custom_key = "not-needed"

            # Save configuration to .env
            env_content = f"OMNIROUTE_API_BASE={custom_base}\nOPENAI_API_BASE={custom_base}\nOPENAI_API_KEY={custom_key}\n"
            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)
            print("[+] Configuration saved to .env successfully.")

    # 5. Summary & Instructions
    print("\n================================================================")
    print("      Devian Ecosystem Installation & Setup Completed!          ")
    print("================================================================")
    print("Next Steps:")
    if os.name == "nt":
        print("1. Activate virtual environment: .\\.venv\\Scripts\\Activate.ps1")
    else:
        print("1. Activate virtual environment: source .venv/bin/activate")
    print("2. Explore agents in:            agents/")
    print("3. Explore skills in:            skills/")
    print("4. Run automation tools:         python tools/browser_agent.py")
    print("================================================================")

if __name__ == "__main__":
    main()
