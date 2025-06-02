##########
# Script name: launch.ps1
# Description: Este script ejecuta en cadena todo lo necesario para
#              ejecutar la app de envio de mails usando Windows
# Version: 1.0
###########

Clear-Host

# Cambia el directorio actual al directorio del script
Set-Location -LiteralPath $PSScriptRoot
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
    
    # La opcion 1 envia correos y marca a la lista de remitentes como ya enviados en la bbdd
    # La opcion 2 envia los correos independientemente de si ya se les habían enviado correos
    [int]$opcion = 2
    python .\__main__.py $opcion
    Write-Host "Correos enviados" -ForegroundColor Green
}

function main {

    Comprobar-Archivos
    Comprobar-ExistenciaMjml
    Convertir-MjmlAHtml
    Ejecutar-App
}

main