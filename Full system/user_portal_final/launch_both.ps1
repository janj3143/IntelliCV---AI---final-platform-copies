# Launch Both Versions for Comparison
# IntelliCV A/B Testing - Professional Pro vs Simple Start

Write-Host "=" * 60 -ForegroundColor Magenta
Write-Host "    IntelliCV A/B Testing - Two Versions Comparison" -ForegroundColor Magenta
Write-Host "=" * 60 -ForegroundColor Magenta
Write-Host ""

Write-Host "Starting Professional Pro (Port 8501)..." -ForegroundColor Green
Write-Host "Features: 4 Pricing Plans, AI Validation, Mentorship Model" -ForegroundColor Cyan
Write-Host "URL: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""

# Start Professional Pro in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\user_portal_final\pages_pro'; streamlit run 00_Landing.py --server.port 8501"

Start-Sleep 3

Write-Host "Starting Simple Start (Port 8502)..." -ForegroundColor Blue
Write-Host "Features: 3 Pricing Plans, Basic Analysis, Quick Setup" -ForegroundColor Cyan
Write-Host "URL: http://localhost:8502" -ForegroundColor Yellow
Write-Host ""

# Start Simple Start in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\user_portal_final\pages_simple'; streamlit run 00_Landing.py --server.port 8502"

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Magenta
Write-Host "Both versions are now running!" -ForegroundColor Green
Write-Host "Professional Pro: http://localhost:8501" -ForegroundColor Yellow
Write-Host "Simple Start:     http://localhost:8502" -ForegroundColor Yellow
Write-Host "=" * 60 -ForegroundColor Magenta
Write-Host ""
Write-Host "Test both versions and choose which works best for your users!" -ForegroundColor White
Write-Host "Press any key to close this launcher..." -ForegroundColor Gray

# Wait for user input
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")