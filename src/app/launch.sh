#!/bin/bash

##########
# Script name: main.sh
# Description: Este script ejecuta en cadena todo lo necesario para
#              enviar los mails
# Version: 1.0
###########

clear

set -e  # Si algo falla, para el script

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

echo -e "\e[33mPreparando entorno virtual y lanzando script de envío de correos...\e[0m"

VENV_PATH="/home/ubuntu/feria_vlc/src/scripts/bash/venv/bin/activate"
if [ ! -f "$VENV_PATH" ]; then
    echo -e "\e[31mError: No se encontró el entorno virtual en $VENV_PATH. Crea el venv primero.\e[0m"
    exit 1
fi

source "$VENV_PATH"

python __main__.py 2

echo -e "\e[32mCorreos enviados!\e[0m"