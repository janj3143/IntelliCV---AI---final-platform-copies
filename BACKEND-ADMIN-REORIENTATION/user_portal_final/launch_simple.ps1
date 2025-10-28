# Launch Simple Start Version
# IntelliCV Simple Start - Streamlined Experience
# Port: 8502

Write-Host "Starting IntelliCV Simple Start..." -ForegroundColor Green
Write-Host "Features: 3 Pricing Plans, Basic Analysis, Quick Setup" -ForegroundColor Cyan
Write-Host "URL: http://localhost:8502" -ForegroundColor Yellow
Write-Host ""

Set-Location "c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\user_portal_final\pages_simple"

# Launch Streamlit
streamlit run 00_Landing.py --server.port 8502