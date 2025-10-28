@echo off
echo Starting IntelliCV Simple Start Portal...
echo Port: 8504
echo URL: http://localhost:8504
echo.
cd /d "%~dp0pages_simple"
streamlit run 00_Welcome.py --server.port 8504
pause