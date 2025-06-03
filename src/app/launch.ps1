##########
# Script name: launch.ps1
# Description: Este script ejecuta en cadena todo lo necesario para
#              ejecutar la app de envio de mails usando Windows
# Version: 1.2
###########

Clear-Host

# Cambia el directorio actual al directorio del script
Set-Location -LiteralPath $PSScriptRoot

function Mostrar-Menu {
    Write-Host "`n=== Menú de Envío de Correos ===" -ForegroundColor Cyan
    Write-Host "1. Enviar Newsletter del Salón del Cómic (todos los usuarios)"
    Write-Host "2. Enviar Sorteo 2RUEDAS (solo usuarios pendientes)"
    Write-Host "3. Insertar nuevo usuario en la base de datos"
    Write-Host "Q. Salir"
    Write-Host "================================`n" -ForegroundColor Cyan
}

function Comprobar-Archivos {

    [string]$credenciales = "../credenciales.inf"
    [string]$envDocker = "../docker/.env"
    [bool]$falta_credenciales = $false
    [bool]$falta_envDocker = $false

    if (-not (Test-Path -Path $credenciales)) {
        Write-Host "El archivo (../credenciales.inf) no existe." -ForegroundColor Red
        $falta_credenciales = $true
    }
    if (-not (Test-Path -Path $envDocker)) {
        Write-Host "El archivo (../docker/.env) no existe." -ForegroundColor Red
        $falta_envDocker = $true
    }
    if ($falta_credenciales || $falta_envDocker) {
        exit 1
    }
}
function Comprobar-ExistenciaMjml {
    
    try {
        Get-Command mjml -ErrorAction Stop | Out-Null
    }
    catch {
        Write-Host "Error: mjml no está instalado o no está en el PATH. Instálalo." -ForegroundColor Red
        exit 1 
    }
    
}
function Convertir-MjmlAHtml {
    
    $CarpetaMjml = "../mjml/"
    $CarpetaHtml = "../html/"

    # comprobación de carpeta de destino (../html/)
    if (-not (Test-Path $CarpetaHtml)) {
        New-Item -ItemType Directory -Path $CarpetaHtml | Out-Null
    }

    # se listan los .mjml
    Get-ChildItem -Path $CarpetaMjml -Filter *.mjml | ForEach-Object {
        $ArchivoMjml = $_.FullName
        $ArchivoMjmlSinExt = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
        $ArchivoHtml = Join-Path $CarpetaHtml "$ArchivoMjmlSinExt.html"

        # se convierte el archivo a .html, conservando el nombre
        Write-Host "Convirtiendo $($_.Name) a HTML..." -ForegroundColor Cyan
        mjml $ArchivoMjml -o $ArchivoHtml
    }
}
function Ejecutar-App {
    Mostrar-Menu
    $opcion = Read-Host "Seleccione una opción"
    
    switch ($opcion.ToUpper()) {
        "1" {
            Write-Host "Enviando Newsletter del Salón del Cómic..." -ForegroundColor Yellow
            python .\__main__.py 1
            Write-Host "Proceso completado" -ForegroundColor Green
        }
        "2" {
            Write-Host "Enviando correos de sorteo 2RUEDAS..." -ForegroundColor Yellow
            python .\__main__.py 2
            Write-Host "Proceso completado" -ForegroundColor Green
        }
        "3" {
            Write-Host "Iniciando inserción de nuevo usuario..." -ForegroundColor Yellow
            python .\__main__.py 3
            Write-Host "Proceso completado" -ForegroundColor Green
        }
        "Q" {
            Write-Host "Saliendo..." -ForegroundColor Red
            exit 0
        }
        default {
            Write-Host "Opción no válida" -ForegroundColor Red
            exit 1
        }
    }
}

function main {

    Comprobar-Archivos
    Comprobar-ExistenciaMjml
    Convertir-MjmlAHtml
    Ejecutar-App
}

main