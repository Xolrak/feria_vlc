#!/bin/bash

##########
# Script name: launch.sh
# Description: Este script ejecuta en cadena todo lo necesario para
#              ejecutar la app de envio de mails usando Linux
# Version: 1.2
###########

clear

set -e  # Si algo falla, para el script

mostrar_menu() {
    echo -e "\n\e[36m=== Menú de Envío de Correos ===\e[0m"
    echo "1. Enviar Newsletter del Salón del Cómic (todos los usuarios)"
    echo "2. Enviar Sorteo 2RUEDAS (solo usuarios pendientes)"
    echo "3. Insertar nuevo usuario en la base de datos"
    echo "Q. Salir"
    echo -e "\e[36m================================\e[0m\n"
}

# Verificación de archivo de credenciales
if [ ! -f ../credenciales.inf ]; then
    echo -e "\e[31mError: No se encontró el archivo '../credenciales.inf'.\e[0m"
    echo -e "\e[31mAsegúrate de que existe antes de continuar.\e[0m"
    exit 1
fi

convertir_mjml_a_html() {
    local mjmlFolder="../mjml"
    local htmlFolder="../html"

    # Comprobar que mjml está instalado
    if ! command -v mjml >/dev/null 2>&1; then
        echo -e "\e[31mError: mjml no está instalado o no está en el PATH. Instálalo y vuelve a intentarlo.\e[0m"
        exit 1
    fi

    # Crear carpeta html si no existe
    if [ ! -d "$htmlFolder" ]; then
        mkdir -p "$htmlFolder"
    fi

    # Convertir cada archivo .mjml a .html
    for mjmlFile in "$mjmlFolder"/*.mjml; do
        [ -e "$mjmlFile" ] || continue
        local finalName=$(basename "$mjmlFile" .mjml)
        local htmlFile="$htmlFolder/$finalName.html"

        echo -e "\e[36mConvirtiendo $(basename "$mjmlFile") a HTML...\e[0m"
        mjml "$mjmlFile" -o "$htmlFile"
    done
}

echo -e "\e[33mIniciando conversión de MJML a HTML...\e[0m"
convertir_mjml_a_html

echo -e "\e[33mPreparando entorno virtual...\e[0m"

# Crear y activar entorno virtual si no existe
VENV_PATH="./venv"
if [ ! -d "$VENV_PATH" ]; then
    echo -e "\e[36mCreando nuevo entorno virtual...\e[0m"
    python3 -m venv "$VENV_PATH"
fi

source "$VENV_PATH/bin/activate"

# Instalar dependencias si es necesario
if [ ! -f "$VENV_PATH/installed" ]; then
    echo -e "\e[36mInstalando dependencias...\e[0m"
    pip install mysql-connector-python
    touch "$VENV_PATH/installed"
fi

while true; do
    mostrar_menu
    read -p "Seleccione una opción: " opcion
    
    case ${opcion^^} in
        1)
            echo -e "\e[33mEnviando Newsletter del Salón del Cómic...\e[0m"
            python __main__.py 1
            echo -e "\e[32mProceso completado!\e[0m"
            break
            ;;
        2)
            echo -e "\e[33mEnviando correos de sorteo 2RUEDAS...\e[0m"
            python __main__.py 2
            echo -e "\e[32mProceso completado!\e[0m"
            break
            ;;
        3)
            echo -e "\e[33mIniciando inserción de nuevo usuario...\e[0m"
            python __main__.py 3
            echo -e "\e[32mProceso completado!\e[0m"
            break
            ;;
        Q)
            echo -e "\e[31mSaliendo...\e[0m"
            exit 0
            ;;
        *)
            echo -e "\e[31mOpción no válida\e[0m"
            ;;
    esac
done