@echo off
echo ========================================
echo   Dashboard COVID-19 & Mpox
echo ========================================
echo.
echo Lancement du dashboard...
echo.
cd /d "%~dp0"
python launch_dashboard.py
pause 