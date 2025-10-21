@echo off
REM IntelliCV-AI Main Application Launcher
REM =====================================
REM Launches the consolidated main.py application
REM Clean Welcome -> Login/Registration -> Profile -> CV upload flow

echo ===============================================
echo   🚀 IntelliCV-AI - Intelligent Career Platform
echo ===============================================
echo.
echo Starting main application with admin AI integration...
echo.

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ Error: main.py not found
    echo Please ensure you're in the correct directory
    echo Expected file: main.py
    pause
    exit /b 1
)

echo ✅ Found main.py - launching application...
echo.
echo 🌐 Opening in browser: http://localhost:8501
echo.
echo 📋 User Flow:
echo    1. Welcome page (professional entry)
echo    2. Login/Registration options  
echo    3. Profile setup and payment
echo    4. Dashboard with admin AI integration
echo    5. Resume upload with enhanced analysis
echo.
echo 🧠 Features Available:
echo    • 6-System AI Coordination (NLP + Bayesian + LLM + Neural + Expert + Statistical)
echo    • Enhanced Job Title Engine (422 lines LinkedIn integration)
echo    • Real AI Data Connector (3,418+ JSON sources)
echo    • Bidirectional Admin Integration
echo.
echo ⚡ Press Ctrl+C to stop the application
echo ===============================================
echo.

REM Launch Streamlit with main.py
streamlit run main.py --server.port=8501 --server.address=localhost

echo.
echo Application stopped.
pause