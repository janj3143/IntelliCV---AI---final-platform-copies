# Simple Start Portal Launcher - Clean Version
# Avoids directory flipping issues

$PythonPath = "C:\IntelliCV-AI\IntelliCV\env310\python.exe"
$PortalDir = "C:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\user_portal_final\pages_simple"
$Port = 8504

Write-Host "⚡ IntelliCV Simple Start Portal" -ForegroundColor Blue
Write-Host "===============================" -ForegroundColor Blue

# Verify paths
if (-not (Test-Path $PythonPath)) {
    Write-Host "❌ Python not found: $PythonPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path $PortalDir)) {
    Write-Host "❌ Portal directory not found: $PortalDir" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

$WelcomeFile = Join-Path $PortalDir "00_Welcome.py"
if (-not (Test-Path $WelcomeFile)) {
    Write-Host "❌ Welcome file not found: $WelcomeFile" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Python found: $PythonPath" -ForegroundColor Green
Write-Host "✅ Portal directory: $PortalDir" -ForegroundColor Green
Write-Host "✅ Welcome file: $WelcomeFile" -ForegroundColor Green
Write-Host ""

# Change to portal directory BEFORE running Streamlit
Write-Host "📁 Changing to portal directory..." -ForegroundColor Yellow
Set-Location $PortalDir

Write-Host "📍 Current directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host "🚀 Starting Simple Start Portal on port $Port..." -ForegroundColor Blue
Write-Host "🌐 URL: http://localhost:$Port" -ForegroundColor Cyan
Write-Host ""
Write-Host "💰 Features: Streamlined pricing display" -ForegroundColor White
Write-Host "🛡️ Security: Simplified 2FA options" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the portal" -ForegroundColor Red
Write-Host ""

# Run Streamlit with the correct working directory
& $PythonPath -m streamlit run "00_Welcome.py" --server.port $Port

Write-Host ""
Write-Host "Portal stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"