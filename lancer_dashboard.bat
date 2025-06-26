@echo off
echo ========================================
echo   Dashboard COVID-19 & Mpox
echo ========================================
echo.
echo Installation et lancement automatique...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou pas dans le PATH
    echo Installez Python depuis https://python.org
    pause
    exit /b 1
)

REM Installer les dépendances
echo Installation des dependances...
pip install -r backend/requirements_dashboard.txt

REM Lancer le dashboard
echo.
echo Lancement du dashboard...
cd backend
python launch_dashboard.py

pause 