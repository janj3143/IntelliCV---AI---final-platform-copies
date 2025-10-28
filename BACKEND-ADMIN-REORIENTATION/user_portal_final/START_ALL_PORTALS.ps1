# IntelliCV-AI Portal Launcher (PowerShell)
# Run all three portals simultaneously

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "IntelliCV-AI Portal Launcher" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if Python is installed
function Test-Python {
    try {
        $pythonVersion = python --version 2>$null
        if ($pythonVersion) {
            Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
            return $true
        }
    }
    catch {
        Write-Host "❌ Python not found!" -ForegroundColor Red
        return $false
    }
    return $false
}

# Function to install Streamlit
function Install-Streamlit {
    Write-Host "📦 Installing Streamlit..." -ForegroundColor Yellow
    try {
        pip install streamlit
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Streamlit installed successfully!" -ForegroundColor Green
            return $true
        }
        else {
            Write-Host "❌ Failed to install Streamlit" -ForegroundColor Red
            return $false
        }
    }
    catch {
        Write-Host "❌ Error installing Streamlit: $_" -ForegroundColor Red
        return $false
    }
}

# Function to start a portal
function Start-Portal {
    param(
        [string]$Name,
        [string]$Path,
        [int]$Port,
        [string]$Color
    )
    
    Write-Host "🚀 Starting $Name on port $Port..." -ForegroundColor $Color
    
    $fullPath = Join-Path $PSScriptRoot $Path
    if (Test-Path $fullPath) {
        # Start in new PowerShell window
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$fullPath'; streamlit run 00_Welcome.py --server.port $Port" -WindowStyle Normal
        Start-Sleep 2
    }
    else {
        Write-Host "❌ Directory not found: $fullPath" -ForegroundColor Red
    }
}

# Check Python installation
if (-not (Test-Python)) {
    Write-Host ""
    Write-Host "🐍 Python Installation Required:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Option 1: Microsoft Store" -ForegroundColor White
    Write-Host "  - Open Microsoft Store" -ForegroundColor Gray
    Write-Host "  - Search for 'Python 3.11' or 'Python 3.12'" -ForegroundColor Gray
    Write-Host "  - Click Install" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 2: Python.org" -ForegroundColor White
    Write-Host "  - Go to https://python.org/downloads" -ForegroundColor Gray
    Write-Host "  - Download Python 3.11 or 3.12" -ForegroundColor Gray
    Write-Host "  - Run installer and check 'Add Python to PATH'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "After installing Python, run this script again." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Install Streamlit
if (-not (Install-Streamlit)) {
    Write-Host "Failed to install Streamlit. Please check your internet connection." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting All IntelliCV-AI Portals" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Portal URLs:" -ForegroundColor White
Write-Host "🏆 Professional Pro:    http://localhost:8503" -ForegroundColor Magenta
Write-Host "⚡ Simple Start:        http://localhost:8504" -ForegroundColor Blue
Write-Host "🚀 Backup Recovered:    http://localhost:8508" -ForegroundColor Green
Write-Host ""

# Start all portals
Start-Portal "Professional Pro" "pages_pro" 8503 "Magenta"
Start-Portal "Simple Start" "pages_simple" 8504 "Blue"
Start-Portal "Backup Recovered" "pages_backup_recovered" 8508 "Green"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All Portals Started!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏰ Wait 10-15 seconds for portals to fully load, then visit:" -ForegroundColor Yellow
Write-Host ""
Write-Host "🏆 Professional Pro:    http://localhost:8503" -ForegroundColor Magenta
Write-Host "⚡ Simple Start:        http://localhost:8504" -ForegroundColor Blue  
Write-Host "🚀 Backup Recovered:    http://localhost:8508" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Features to test:" -ForegroundColor White
Write-Host "   - New pricing: Free, $15.99, $149.99, $299.99" -ForegroundColor Gray
Write-Host "   - 2FA security options" -ForegroundColor Gray
Write-Host "   - Different user experiences" -ForegroundColor Gray
Write-Host "   - Admin AI integration (Backup Recovered)" -ForegroundColor Gray
Write-Host ""
Write-Host "🛑 To stop a portal: Close its PowerShell window or press Ctrl+C" -ForegroundColor Red
Write-Host ""

Read-Host "Press Enter to exit this launcher (portals will continue running)"