@echo off
echo ========================================
echo   Demarrage du serveur E-Commerce
echo ========================================
echo.

cd /d "%~dp0"
call env\Scripts\activate.bat

echo [INFO] Environnement virtuel active
echo [INFO] Lancement du serveur Django...
echo.

python manage.py runserver

pause

