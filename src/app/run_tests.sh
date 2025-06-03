#!/bin/bash

##########
# Script name: run_tests.sh
# Description: Script para ejecutar las pruebas unitarias
# Version: 1.1
###########

clear

# Verificar y activar el entorno virtual
VENV_PATH="./venv"
if [ ! -d "$VENV_PATH" ]; then
    echo -e "\e[31mError: No se encontró el entorno virtual. Ejecute primero launch.sh para crearlo.\e[0m"
    exit 1
fi

source "$VENV_PATH/bin/activate"

echo -e "\e[36mEjecutando pruebas unitarias...\e[0m"
python tests.py

echo -e "\nPresione Enter para salir..."
read 