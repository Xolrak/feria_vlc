#!/bin/bash

# Script para lanzar el servidor web de Feria VLC
# Versión: 1.3

# Obtener el directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Colores para los mensajes
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python3 no está instalado${NC}"
    exit 1
fi

# Verificar que existe el entorno virtual
VENV_PATH="${SCRIPT_DIR}/venv"
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}Error: El entorno virtual no existe. Ejecuta primero 'src/scripts/setup_python_env.sh'${NC}"
    exit 1
fi

# Activar entorno virtual
echo -e "${YELLOW}Activando entorno virtual...${NC}"
source "$VENV_PATH/bin/activate"

# Obtener la IP local
if command -v ip &> /dev/null; then
    IP=$(ip addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d/ -f1 | head -n1)
else
    IP=$(ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | head -n1)
fi

# Cambiar al directorio del script
cd "$SCRIPT_DIR"

# Limpiar pantalla
clear

echo -e "${CYAN}=== Servidor Web de Feria VLC ===${NC}"
echo "Accede al servidor desde:"
echo "- Esta máquina: http://localhost:5000"
echo "- Otras máquinas en la red: http://${IP}:5000"
echo "CTRL+C para detener el servidor"
echo -e "${CYAN}===============================${NC}"

# Iniciar el servidor web
python web_launcher.py 