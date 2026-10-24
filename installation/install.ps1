# Omniagents Advanced Prerequisite & Interactive PowerShell Installer
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "         Omniagents AI Ecosystem - Prerequisite & Setup Wizard      " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

# 1. Prerequisite Checks
Write-Host "`n--- Phase 1: Verifying System Prerequisites ---" -ForegroundColor Yellow

# Python check
$pyVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Error: Python is not installed or not in PATH. Please install Python >= 3.10." -ForegroundColor Red
    exit 1
}
Write-Host "    [OK] Python detected: $pyVersion" -ForegroundColor Green

# Git check
try {
    $gitVersion = git --version 2>&1
    Write-Host "    [OK] Git detected: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "    [!] Warning: Git is recommended for fetching repository updates." -ForegroundColor Yellow
}

# Rust / Cargo check
try {
    $cargoVersion = cargo --version 2>&1
    Write-Host "    [OK] Rust/Cargo detected: $cargoVersion" -ForegroundColor Green
} catch {
    Write-Host "    [!] Rust/Cargo is not detected on your system." -ForegroundColor Yellow
    Write-Host "        Some high-performance tools or extensions may require Rust." -ForegroundColor White
    Write-Host "        To install Rust (rustup):" -ForegroundColor White
    Write-Host "        - Run via winget: winget install Rustlang.Rustup" -ForegroundColor Cyan
    Write-Host "        - Or visit: https://rustup.rs/" -ForegroundColor Cyan
    
    $cont = Read-Host "`nWould you like to continue without Rust/Cargo? (Y/n)"
    if ($cont -eq 'n' -or $cont -eq 'N') {
        Write-Host "Aborting installation." -ForegroundColor Red
        exit 1
    }
}

# 2. Virtual Environment & Dependencies
Write-Host "`n--- Phase 2: Setting up Python Environment & Dependencies ---" -ForegroundColor Yellow
if (!(Test-Path ".venv")) {
    Write-Host "[+] Creating isolated virtual environment (.venv)..." -ForegroundColor Green
    python -m venv .venv
} else {
    Write-Host "[+] Virtual environment (.venv) already exists." -ForegroundColor Yellow
}

$pip = ".\.venv\Scripts\pip"
if (Test-Path "requirements.txt") {
    Write-Host "[+] Installing Python dependencies..." -ForegroundColor Green
    & $pip install --upgrade pip
    & $pip install -r requirements.txt
}

# 3. Omniroute Local Gateway Check
Write-Host "`n--- Phase 3: Checking Local AI Gateway (Omniroute) ---" -ForegroundColor Yellow
$gatewayActive = $false
try {
    $response = Invoke-RestMethod -Uri "http://localhost:20128/v1/models" -Headers @{ Authorization = "Bearer not-needed" } -TimeoutSec 2
    $gatewayActive = $true
    Write-Host "[+] Success: Omniroute gateway is running on http://localhost:20128/v1" -ForegroundColor Cyan
} catch {
    Write-Host "[!] Omniroute Gateway is NOT running on http://localhost:20128/v1." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "--- HOW TO OBTAIN & INSTALL OMNIROUTE ---" -ForegroundColor Cyan
    Write-Host "1. Omniroute provides local LLM routing for Omniagents agents." -ForegroundColor White
    Write-Host "2. Start your Omniroute service locally on port 20128." -ForegroundColor White
    Write-Host "3. Alternatively, configure custom API endpoints below." -ForegroundColor White
    Write-Host ""
    
    $choice = Read-Host "Would you like to configure custom API base URL now? (y/N)"
    if ($choice -eq 'y' -or $choice -eq 'Y') {
        $customBase = Read-Host "Enter API Base URL [default: http://localhost:20128/v1]"
        if ([string]::IsNullOrWhiteSpace($customBase)) { $customBase = "http://localhost:20128/v1" }
        $customKey = Read-Host "Enter API Key [default: not-needed]"
        if ([string]::IsNullOrWhiteSpace($customKey)) { $customKey = "not-needed" }

        $envContent = "OMNIROUTE_API_BASE=$customBase`nOPENAI_API_BASE=$customBase`nOPENAI_API_KEY=$customKey`n"
        Set-Content -Path ".env" -Value $envContent
        Write-Host "[+] Configuration saved to .env successfully." -ForegroundColor Green
    }
}

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "      Omniagents Ecosystem Installation & Setup Completed!          " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "1. Activate venv: .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "2. Explore agents: agents/" -ForegroundColor Yellow
Write-Host "3. Explore skills: skills/" -ForegroundColor Yellow
Write-Host "4. Run tools:      python tools/browser_agent.py" -ForegroundColor Yellow
