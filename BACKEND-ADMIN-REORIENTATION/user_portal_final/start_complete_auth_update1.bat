@echo off
echo 🚀 IntelliCV-AI Complete Authentication System
echo ============================================
echo.
echo Starting complete authentication system with:
echo - 2FA (Two-Factor Authentication)
echo - SMS Verification  
echo - Email Confirmation
echo - Terms & Conditions
echo - Pricing with Marketing Consent
echo - Highly Visible Logo Background
echo.
echo Will be available at: http://localhost:8506
echo.

cd /d "c:\IntelliCV"

REM Try different Python executables
if exist "env310\Scripts\python.exe" (
    echo Using virtual environment Python...
    env310\Scripts\python.exe -m streamlit run "SANDBOX\user_portal_final\enhanced_app_complete_auth_update1.py" --server.port 8506
) else if exist "python.exe" (
    echo Using local Python executable...
    python.exe -m streamlit run "SANDBOX\user_portal_final\enhanced_app_complete_auth_update1.py" --server.port 8506
) else (
    echo Trying system Python...
    python -m streamlit run "SANDBOX\user_portal_final\enhanced_app_complete_auth_update1.py" --server.port 8506
)

pause