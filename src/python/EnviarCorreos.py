#!/usr/bin/env python3

"""
Script name: EnviarCorreos.py
Author: Carlos Castañeda
Description: Script que automatiza el envío de templates .html por correo
Version: 1.0
"""

import smtplib
import sys
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def leer_credenciales(ruta):
    credenciales = {}
    with open(ruta, 'r') as f:
        for linea in f:
            if '=' in linea:
                clave, valor = linea.strip().split('=', 1)
                credenciales[clave.strip()] = valor.strip()
    return credenciales

def comprobar_credenciales(ruta):
    if not os.path.exists(ruta):
        print(f"No se ha encontrado el archivo de credenciales en: {ruta}")
        sys.exit(1)  # Si no se encuentra el archivo, se para el programa
    else:
        print(f"Archivo de credenciales encontrado en: {ruta}")

# Ruta del script actual
ruta_base = os.path.dirname(__file__)

# Leer credenciales
ruta_info = os.path.join(ruta_base, '..', 'credenciales.inf')
ruta_info = os.path.normpath(ruta_info)
comprobar_credenciales(ruta_info)
datos = leer_credenciales(ruta_info)

EMAIL = datos.get('email')
APP_PASSWORD = datos.get('app_password')

nombre_archivo = input("Escribe el nombre del archivo que quieres enviar: ")

# Ruta del archivo HTML
ruta_html = os.path.join(ruta_base, '..', 'html', nombre_archivo)

with open(ruta_html, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Reemplaza {{nombre}} por el nombre personalizado
nombre_personalizado = "nombre"
html_personalizado = html_content.replace('{{nombre}}', nombre_personalizado)

# Preparacion del correo
mensaje = MIMEMultipart('alternative')
mensaje['Subject'] = 'Correo HTML'
mensaje['From'] = EMAIL
mensaje['To'] = 'mail@mail.com'
mensaje.attach(MIMEText(html_personalizado, 'html'))

# Envio
with smtplib.SMTP('smtp.office365.com', 587) as servidor:
    servidor.starttls()
    servidor.login(EMAIL, APP_PASSWORD)
    servidor.send_message(mensaje)

print("¡Correo enviado!")