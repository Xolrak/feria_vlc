##########
# Script name: run_tests.ps1
# Description: Script para ejecutar las pruebas unitarias
# Version: 1.0
###########

Clear-Host

# Cambia el directorio actual al directorio del script
Set-Location -LiteralPath $PSScriptRoot

Write-Host "Ejecutando pruebas unitarias..." -ForegroundColor Cyan
python .\tests.py

Write-Host "`nPresione cualquier tecla para salir..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 