#!/usr/bin/env python3

"""
Script name: __main__.py
Author: Carlos Castañeda
Description: main de la app que gestiona los envios de correos
Version: 3.0
"""

import os
from config import leer_credenciales, comprobar_credenciales
from database import obtener_usuarios_sin_correo, marcar_correo_enviado
from mailer import enviar_correo

# Ruta base
ruta_base = os.path.dirname(__file__)
ruta_info = os.path.normpath(os.path.join(ruta_base, '..', 'credenciales.inf'))
comprobar_credenciales(ruta_info)
datos = leer_credenciales(ruta_info)

EMAIL = datos.get('email')
APP_PASSWORD = datos.get('app_password')

db_config = {
    'host': datos.get('db_host'),
    'user': datos.get('db_user'),
    'password': datos.get('db_password'),
    'database': datos.get('db_nombre'),
    'port': int(datos.get('db_port', 3306))
}

id_encuesta = 1

nombre_archivo = input("Escribe el nombre del archivo que quieres enviar: ")
ruta_html = os.path.join(ruta_base, '..', 'html', nombre_archivo)

with open(ruta_html, 'r', encoding='utf-8') as f:
    html_content = f.read()

usuarios = obtener_usuarios_sin_correo(db_config, id_encuesta)

if not usuarios:
    print("No hay usuarios pendientes de recibir el correo.")
else:
    print(f"Se enviarán correos a {len(usuarios)} usuarios.")

    for id_usuario, correo, nombre in usuarios:
        try:
            enviar_correo(EMAIL, APP_PASSWORD, correo, nombre, html_content)
            print(f"Correo enviado a {nombre} <{correo}>")
            marcar_correo_enviado(db_config, id_usuario, id_encuesta)
        except Exception as e:
            print(f"Error enviando correo a {correo}: {e}")
