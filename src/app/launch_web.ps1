# Script para lanzar el servidor web de Feria VLC
# Versión: 1.0

# Comprobar si se está ejecutando como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "AVISO: No se está ejecutando como administrador. Algunas funciones del firewall podrían no estar disponibles." -ForegroundColor Yellow
}

# Verificar Python y dependencias
try {
    python -c "import flask" 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Flask no está instalado. Instalando..." -ForegroundColor Yellow
        pip install -r requirements.txt
    }
} catch {
    Write-Host "Error: Python no está instalado o no está en el PATH" -ForegroundColor Red
    exit 1
}

# Obtener la IP local
$ip = (Get-NetIPAddress | Where-Object { $_.AddressFamily -eq 'IPv4' -and $_.PrefixOrigin -eq 'Dhcp' }).IPAddress
if (-not $ip) {
    $ip = (Get-NetIPAddress | Where-Object { $_.AddressFamily -eq 'IPv4' -and $_.InterfaceAlias -notlike '*Loopback*' })[0].IPAddress
}

# Intentar configurar el firewall si se ejecuta como administrador
if ($isAdmin) {
    $ruleName = "Feria VLC Web Server"
    $ruleExists = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

    if (-not $ruleExists) {
        Write-Host "Configurando regla de firewall..." -ForegroundColor Yellow
        New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5000
    }
}

Clear-Host
Write-Host "=== Servidor Web de Feria VLC ===" -ForegroundColor Cyan
Write-Host "Accede al servidor desde:"
Write-Host "- Esta máquina: http://localhost:5000"
Write-Host "- Otras máquinas en la red: http://${ip}:5000"
Write-Host "CTRL+C para detener el servidor"
Write-Host "===============================" -ForegroundColor Cyan

# Iniciar el servidor web
python web_launcher.py 