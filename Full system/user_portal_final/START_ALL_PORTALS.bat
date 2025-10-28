@echo off
echo ========================================
echo IntelliCV-AI Portal Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python not found! Please install Python first.
    echo.
    echo Option 1: Install from Microsoft Store
    echo   - Open Microsoft Store
    echo   - Search for "Python 3.11" or "Python 3.12"
    echo   - Click Install
    echo.
    echo Option 2: Install from python.org
    echo   - Go to https://python.org/downloads
    echo   - Download Python 3.11 or 3.12
    echo   - Run installer and check "Add Python to PATH"
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

echo Python found! Installing Streamlit...
pip install streamlit
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install Streamlit. Please check your internet connection.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting IntelliCV-AI Portals
echo ========================================
echo.
echo Portal URLs will be:
echo - Professional Pro:    http://localhost:8503
echo - Simple Start:        http://localhost:8504  
echo - Backup Recovered:    http://localhost:8508
echo.
echo Press Ctrl+C in any terminal to stop a portal
echo.

REM Start portals in separate command windows
echo Starting Professional Pro Portal (Port 8503)...
start "IntelliCV Professional Pro" cmd /k "cd /d "%~dp0pages_pro" && streamlit run 00_Welcome.py --server.port 8503"

timeout /t 3 /nobreak >nul

echo Starting Simple Start Portal (Port 8504)...
start "IntelliCV Simple Start" cmd /k "cd /d "%~dp0pages_simple" && streamlit run 00_Welcome.py --server.port 8504"

timeout /t 3 /nobreak >nul

echo Starting Backup Recovered Portal (Port 8508)...
start "IntelliCV Backup Recovered" cmd /k "cd /d "%~dp0pages_backup_recovered" && streamlit run 00_Welcome.py --server.port 8508"

echo.
echo ========================================
echo All portals are starting up!
echo ========================================
echo.
echo Wait 10-15 seconds for the portals to fully load, then visit:
echo.
echo 🏆 Professional Pro:    http://localhost:8503
echo ⚡ Simple Start:        http://localhost:8504  
echo 🚀 Backup Recovered:    http://localhost:8508
echo.
echo Each portal will open in a separate command window.
echo To stop a portal, close its command window or press Ctrl+C.
echo.
pause