# Script PowerShell pour demarrer le serveur E-Commerce

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Demarrage du serveur E-Commerce" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Aller dans le repertoire du script
Set-Location $PSScriptRoot

# Activer l'environnement virtuel
Write-Host "[INFO] Activation de l'environnement virtuel..." -ForegroundColor Yellow
& ".\env\Scripts\Activate.ps1"

Write-Host "[INFO] Lancement du serveur Django..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Site web : http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "Administration : http://127.0.0.1:8000/admin/" -ForegroundColor Green
Write-Host ""
Write-Host "Comptes de test :" -ForegroundColor Cyan
Write-Host "  Admin : admin / admin123" -ForegroundColor White
Write-Host "  Vendeur : vendeur1 / vendeur123" -ForegroundColor White
Write-Host "  Client : client1 / client123" -ForegroundColor White
Write-Host ""
Write-Host "Appuyez sur Ctrl+C pour arreter le serveur" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver

