@echo off
echo ========================================
echo   Dashboard COVID-19 & Mpox
echo ========================================
echo.
echo Lancement du dashboard...
echo.
cd /d "%~dp0"
cd scripts
python dashboard_final.py
pause 