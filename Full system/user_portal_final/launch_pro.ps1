# Launch Professional Pro Version
# IntelliCV Professional Pro - Full Feature Set
# Port: 8501

Write-Host "Starting IntelliCV Professional Pro..." -ForegroundColor Green
Write-Host "Features: 4 Pricing Plans, AI Validation, Mentorship Model" -ForegroundColor Cyan
Write-Host "URL: http://localhost:8501" -ForegroundColor Yellow
Write-Host ""

Set-Location "c:\IntelliCV-AI\IntelliCV\SANDBOX\BACKEND-ADMIN-REORIENTATION\user_portal_final\pages_pro"

# Launch Streamlit
streamlit run 00_Landing.py --server.port 8501