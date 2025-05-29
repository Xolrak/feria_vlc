#!/usr/bin/env python3

"""
Script name: EnviarCorreos.py
Author: Carlos Castañeda
Description: Script que automatiza el envío de templates .html por correo
Version: 2.0
"""

import smtplib
import sys
import os
import mysql.connector
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
        sys.exit(1)
    else:
        print(f"Archivo de credenciales encontrado en: {ruta}")

def obtener_usuarios_sin_correo(db_config, id_encuesta):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    query = """
        SELECT u.id_usuario, u.correo_electronico, u.nombre 
        FROM Usuarios u
        JOIN Hacen h ON u.id_usuario = h.id_usuario
        WHERE h.id_encuesta = %s AND h.correo_enviado = FALSE
    """
    cursor.execute(query, (id_encuesta,))
    resultados = cursor.fetchall()

    cursor.close()
    cnx.close()

    return resultados

def marcar_correo_enviado(db_config, id_usuario, id_encuesta):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    update = """
        UPDATE Hacen
        SET correo_enviado = TRUE
        WHERE id_usuario = %s AND id_encuesta = %s
    """
    cursor.execute(update, (id_usuario, id_encuesta))
    cnx.commit()

    cursor.close()
    cnx.close()

# ---------------- CONFIGURACIÓN ------------------

# Ruta del script actual
ruta_base = os.path.dirname(__file__)

# Leer credenciales
ruta_info = os.path.join(ruta_base, '..', 'credenciales.inf')
ruta_info = os.path.normpath(ruta_info)
comprobar_credenciales(ruta_info)
datos = leer_credenciales(ruta_info)

EMAIL = datos.get('email')
APP_PASSWORD = datos.get('app_password')

# Datos para la BBDD
db_config = {
    'host': datos.get('db_host'),
    'user': datos.get('db_user'),
    'password': datos.get('db_password'),
    'database': datos.get('db_nombre'),
    'port': int(datos.get('db_port', 3306))  # por si acaso no lo ponen en el .inf
}


# ID de la encuesta
id_encuesta = 1

# Nombre del archivo HTML
nombre_archivo = input("Escribe el nombre del archivo que quieres enviar: ")
ruta_html = os.path.join(ruta_base, '..', 'html', nombre_archivo)

with open(ruta_html, 'r', encoding='utf-8') as f:
    html_content = f.read()

# ---------------- ENVÍO DE CORREOS ------------------

usuarios = obtener_usuarios_sin_correo(db_config, id_encuesta)

if not usuarios:
    print("No hay usuarios pendientes de recibir el correo. ¡Todo en orden, socio!")
else:
    print(f"Se enviarán correos a {len(usuarios)} usuarios.")

    for id_usuario, correo, nombre in usuarios:
        html_personalizado = html_content.replace('{{nombre}}', nombre)

        mensaje = MIMEMultipart('alternative')
        mensaje['Subject'] = 'Correo HTML'
        mensaje['From'] = EMAIL
        mensaje['To'] = correo
        mensaje.attach(MIMEText(html_personalizado, 'html'))

        try:
            with smtplib.SMTP('smtp.office365.com', 587) as servidor:
                servidor.starttls()
                servidor.login(EMAIL, APP_PASSWORD)
                servidor.send_message(mensaje)
            print(f"Correo enviado a {nombre} <{correo}>")
            marcar_correo_enviado(db_config, id_usuario, id_encuesta)
        except Exception as e:
            print(f"Error enviando correo a {correo}: {e}")
