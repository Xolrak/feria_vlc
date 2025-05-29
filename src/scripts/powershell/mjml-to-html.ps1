# Rutas de las carpetas
$mjmlFolder = "..\..\mjml"
$htmlFolder = "..\..\html"

# comprobación de carpeta de destino
if (!(Test-Path $htmlFolder)) {
    New-Item -ItemType Directory -Path $htmlFolder | Out-Null
}

# se listan los .mjml
Get-ChildItem -Path $mjmlFolder -Filter *.mjml | ForEach-Object {
    $mjmlFile = $_.FullName
    $fileNameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
    $htmlFile = Join-Path $htmlFolder "$fileNameWithoutExt.html"

    # se convierte el archivo a .html, conservando el nombre
    Write-Host "Convirtiendo $($_.Name) a HTML..." -ForegroundColor Cyan
    mjml $mjmlFile -o $htmlFile
}
