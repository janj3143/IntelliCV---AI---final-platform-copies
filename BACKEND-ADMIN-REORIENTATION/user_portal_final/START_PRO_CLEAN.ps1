# Professional Pro Portal Launcher - Clean Version
# Avoids directory flipping issues

$PythonPath = "C:\IntelliCV-AI\IntelliCV\env310\python.exe"
$PortalDir = "C:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\user_portal_final\pages_pro"
$Port = 8503

Write-Host "🏆 IntelliCV Professional Pro Portal" -ForegroundColor Magenta
Write-Host "=====================================" -ForegroundColor Magenta

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
Write-Host "🚀 Starting Professional Pro Portal on port $Port..." -ForegroundColor Magenta
Write-Host "🌐 URL: http://localhost:$Port" -ForegroundColor Cyan
Write-Host ""
Write-Host "💰 Features: Updated pricing ($15.99 monthly, $149.99 annual, $299.99 enterprise)" -ForegroundColor White
Write-Host "🛡️ Security: 2FA authentication options" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the portal" -ForegroundColor Red
Write-Host ""

# Run Streamlit with the correct working directory
& $PythonPath -m streamlit run "00_Welcome.py" --server.port $Port

Write-Host ""
Write-Host "Portal stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"