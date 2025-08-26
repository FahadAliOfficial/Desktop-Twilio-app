# PowerShell script to run Twilio Calling Dashboard
# Run this script to start the application with proper environment setup

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Twilio Calling Dashboard" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion detected" -ForegroundColor Green
} catch {
    Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies if needed
if ((Test-Path "requirements.txt") -and (-not (Test-Path ".install_done"))) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        New-Item -Path ".install_done" -ItemType File -Force | Out-Null
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
    Write-Host "Please run setup.py first or copy .env.template to .env" -ForegroundColor Yellow
    Write-Host ""
    $choice = Read-Host "Continue anyway? (y/N)"
    if ($choice -ne "y" -and $choice -ne "Y") {
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit 1
    }
}

# Run the application
Write-Host "Starting Twilio Calling Dashboard..." -ForegroundColor Green
Write-Host ""

try {
    python main.py
} catch {
    Write-Host "❌ Application failed to start" -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
}

# Keep window open if there was an error
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Application exited with an error" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}
