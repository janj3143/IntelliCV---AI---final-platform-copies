# Backup Recovered Portal Launcher - Clean Version
# Advanced admin AI integration portal

$PythonPath = "C:\IntelliCV-AI\IntelliCV\env310\python.exe"
$PortalDir = "C:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\user_portal_final\pages_backup_recovered"
$Port = 8508

Write-Host "🔥 IntelliCV Backup Recovered Portal (Admin AI Enhanced)" -ForegroundColor Red
Write-Host "========================================================" -ForegroundColor Red

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
Write-Host "🚀 Starting Backup Recovered Portal on port $Port..." -ForegroundColor Red
Write-Host "🌐 URL: http://localhost:$Port" -ForegroundColor Cyan
Write-Host ""
Write-Host "💰 Features: Complete pricing with Enterprise $299.99" -ForegroundColor White
Write-Host "🛡️ Security: Full 2FA with QR codes" -ForegroundColor White
Write-Host "🤖 AI: Advanced admin AI integration" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the portal" -ForegroundColor Red
Write-Host ""

# Run Streamlit with the correct working directory
& $PythonPath -m streamlit run "00_Welcome.py" --server.port $Port

Write-Host ""
Write-Host "Portal stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"