@echo off
echo Starting IntelliCV Backup Recovered Portal...
echo Port: 8508
echo URL: http://localhost:8508
echo.
cd /d "%~dp0pages_backup_recovered"
streamlit run 00_Welcome.py --server.port 8508
pause