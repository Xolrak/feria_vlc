#!/bin/bash

##########
# Script name: main.sh
# Description: Este script ejecuta en cadena todo lo necesario para
#              enviar los mails
# Version: 1.0
###########

convertir_mjml_a_html() {
    local mjmlFolder="../mjml"
    local htmlFolder="../html"

    # Comprobación de carpeta de destino
    if [ ! -d "$htmlFolder" ]; then
        mkdir -p "$htmlFolder"
    fi

    # Listar archivos .mjml y convertirlos a .html
    for mjmlFile in "$mjmlFolder"/*.mjml; do
        # Comprobar si hay archivos mjml
        [ -e "$mjmlFile" ] || continue

        finalName=$(basename "$mjmlFile" .mjml)
        htmlFile="$htmlFolder/$finalName.html"

        echo -e "\e[36mConvirtiendo $(basename "$mjmlFile") a HTML...\e[0m"
        mjml "$mjmlFile" -o "$htmlFile"
    done
}

# Ejecutar la función de conversión
convertir_mjml_a_html

# Ejecutar el script de Python para enviar correos
echo -e "\e[33mLanzando el script de envío de correos...\e[0m"
python3 ./EnviarCorreos.py
