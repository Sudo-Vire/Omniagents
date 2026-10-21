# Devian Autonomous PowerShell Installer
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "      Devian Autonomous Ecosystem Installer       " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

# 1. Create virtual environment
if (!(Test-Path ".venv")) {
    Write-Host "[+] Creating virtual environment (.venv)..." -ForegroundColor Green
    python -m venv .venv
} else {
    Write-Host "[+] Virtual environment already exists." -ForegroundColor Yellow
}

# 2. Upgrade pip and install requirements
$pip = ".\.venv\Scripts\pip"
$python = ".\.venv\Scripts\python"

if (Test-Path "requirements.txt") {
    Write-Host "[+] Installing dependencies from requirements.txt..." -ForegroundColor Green
    & $pip install --upgrade pip
    & $pip install -r requirements.txt
}

# 3. Check gateway
Write-Host "[+] Verifying local AI Gateway (Omniroute)..." -ForegroundColor Green
try {
    $response = Invoke-RestMethod -Uri "http://localhost:20128/v1/models" -Headers @{ Authorization = "Bearer not-needed" } -TimeoutSec 3
    Write-Host "[+] Local AI Gateway is active!" -ForegroundColor Cyan
} catch {
    Write-Host "[!] Warning: Local AI gateway not reachable on http://localhost:20128/v1." -ForegroundColor Yellow
}

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "      Devian Installation Completed Successfully! " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Activate venv: .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "Run tool:      python tools/browser_agent.py" -ForegroundColor Yellow
