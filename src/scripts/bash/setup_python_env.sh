#!/bin/bash

set -e  # Rompe si algo falla

# Ruta del entorno virtual dentro del proyecto
VENV_DIR="/home/ubuntu/feria_vlc/src/scripts/bash/venv"

echo "Verificando entorno virtual..."

# Verifica si python3.12 está disponible
if ! command -v python3.12 >/dev/null 2>&1; then
    echo "python3.12 no está instalado. Instálalo antes con pyenv o apt."
    exit 1
fi

# Instala el paquete venv si no está
if ! dpkg -s python3.12-venv >/dev/null 2>&1; then
    echo "Instalando python3.12-venv..."
    sudo apt update
    sudo apt install -y python3.12-venv
fi

# Crea entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando entorno virtual en $VENV_DIR..."
    python3.12 -m venv "$VENV_DIR"
else
    echo "Entorno virtual ya existe."
fi

# Activa entorno virtual
echo "Activando entorno virtual..."
source "$VENV_DIR/bin/activate"

# Actualizar pip
pip install --upgrade pip

# Instalar mysql-connector-python si no está
if ! pip show mysql-connector-python >/dev/null 2>&1; then
    echo "Instalando mysql-connector-python..."
    pip install mysql-connector-python
else
    echo "mysql-connector-python ya está instalado."
fi

# Instalar dependencias de sistema para mysqlclient
echo "Instalando dependencias para mysqlclient..."
sudo apt install -y default-libmysqlclient-dev build-essential pkg-config

# Instalar mysqlclient si no está
if ! pip show mysqlclient >/dev/null 2>&1; then
    echo "Instalando mysqlclient..."
    pip install mysqlclient
else
    echo "mysqlclient ya está instalado."
fi
