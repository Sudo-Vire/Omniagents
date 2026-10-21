#!/usr/bin/env python3
"""
Devian Autonomous Installer & Setup Script
Sets up the environment, virtual environment, installs dependencies,
verifies the local LLM gateway, and initializes the AI ecosystem.
"""

import os
import sys
import subprocess
import urllib.request
import json

def run_command(cmd):
    print(f"-> Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Warning: Command failed with exit code {result.returncode}")
    return result.returncode == 0

def main():
    print("==================================================")
    print("      Devian Autonomous Ecosystem Installer       ")
    print("==================================================")

    root_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(root_dir)

    # 1. Check Python version
    if sys.version_info < (3, 10):
        print("Error: Python 3.10 or higher is required.")
        sys.exit(1)
    print(f"[+] Python version: {sys.version.split()[0]}")

    # 2. Create virtual environment
    venv_dir = os.path.join(root_dir, ".venv")
    if not os.path.exists(venv_dir):
        print("[+] Creating virtual environment (.venv)...")
        run_command(f"{sys.executable} -m venv .venv")
    else:
        print("[+] Virtual environment already exists.")

    # Determine pip path in venv
    if os.name == "nt":
        pip_path = os.path.join(venv_dir, "Scripts", "pip")
        python_path = os.path.join(venv_dir, "Scripts", "python")
    else:
        pip_path = os.path.join(venv_dir, "bin", "pip")
        python_path = os.path.join(venv_dir, "bin", "python")

    # 3. Upgrade pip & install requirements
    if os.path.exists("requirements.txt"):
        print("[+] Installing dependencies from requirements.txt...")
        run_command(f'"{pip_path}" install --upgrade pip')
        run_command(f'"{pip_path}" install -r requirements.txt')
    else:
        print("[-] requirements.txt not found.")

    # 4. Verify Local LLM Gateway (Omniroute)
    gateway_url = "http://localhost:20128/v1/models"
    print(f"[+] Checking local AI gateway at {gateway_url}...")
    try:
        req = urllib.request.Request(gateway_url, headers={"Authorization": "Bearer not-needed"})
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                print("[+] Local AI Gateway (Omniroute) is active and reachable!")
            else:
                print(f"[!] Gateway responded with status {response.status}")
    except Exception as e:
        print(f"[!] Warning: Could not connect to local AI gateway ({e}).")
        print("    Make sure Omniroute gateway is running on http://localhost:20128/v1 if using local inference.")

    print("==================================================")
    print("      Devian Installation Completed Successfully! ")
    print("==================================================")
    print("To run browser agent: .venv\\Scripts\\python tools/browser_agent.py")
    print("To run office agent:  .venv\\Scripts\\python tools/office.py")
    print("==================================================")

if __name__ == "__main__":
    main()
