# Devian Autonomous & Interactive PowerShell Installer
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "         Devian Advanced AI Ecosystem - Setup & Installer       " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

# 1. Create virtual environment
if (!(Test-Path ".venv")) {
    Write-Host "[+] Creating isolated virtual environment (.venv)..." -ForegroundColor Green
    python -m venv .venv
} else {
    Write-Host "[+] Virtual environment (.venv) already exists." -ForegroundColor Yellow
}

$pip = ".\.venv\Scripts\pip"
$python = ".\.venv\Scripts\python"

# 2. Install requirements
if (Test-Path "requirements.txt") {
    Write-Host "[+] Installing Python dependencies for agents, tools, and workflows..." -ForegroundColor Green
    & $pip install --upgrade pip
    & $pip install -r requirements.txt
}

# 3. Check Omniroute Local Gateway
Write-Host "[+] Verifying Local AI Gateway (Omniroute)..." -ForegroundColor Green
$gatewayActive = $false
try {
    $response = Invoke-RestMethod -Uri "http://localhost:20128/v1/models" -Headers @{ Authorization = "Bearer not-needed" } -TimeoutSec 2
    $gatewayActive = $true
    Write-Host "[+] Success: Omniroute gateway is running on http://localhost:20128/v1" -ForegroundColor Cyan
} catch {
    Write-Host "[!] Omniroute Gateway is NOT currently running on http://localhost:20128/v1." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "--- HOW TO OBTAIN & INSTALL OMNIROUTE ---" -ForegroundColor Cyan
    Write-Host "1. Omniroute provides local LLM routing for Devian agents." -ForegroundColor White
    Write-Host "2. Start your Omniroute gateway service locally on port 20128." -ForegroundColor White
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
Write-Host "      Devian Ecosystem Installation & Setup Completed!          " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "1. Activate venv: .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "2. Explore agents: agents/" -ForegroundColor Yellow
Write-Host "3. Explore skills: skills/" -ForegroundColor Yellow
Write-Host "4. Run tools:      python tools/browser_agent.py" -ForegroundColor Yellow
