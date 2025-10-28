@echo off
echo Starting IntelliCV Professional Pro Portal...
echo Port: 8503
echo URL: http://localhost:8503
echo.
cd /d "%~dp0pages_pro"
streamlit run 00_Welcome.py --server.port 8503
pause