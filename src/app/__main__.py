#!/usr/bin/env python3

"""
Script name: __main__.py
Author: Carlos Castañeda
Description: main de la app que gestiona los envios de correos
Version: 4.0
"""

import os
from config import leer_credenciales, comprobar_credenciales
from database import obtener_usuarios_sin_correo, marcar_correo_enviado, obtener_todos_los_usuarios
from mailer import enviar_correo

def mostrar_menu():
    print("\n--- MENÚ ---")
    print("1. Enviar correos SOLO a usuarios que aún no lo han recibido (HTML 1)")
    print("2. Enviar correos a TODOS los usuarios (HTML 2, sin comprobar)")
    print("3. Salir")

def cargar_html(nombre_archivo):
    ruta_base = os.path.dirname(__file__)
    ruta_html = os.path.join(ruta_base, '..', 'html', nombre_archivo)
    with open(ruta_html, 'r', encoding='utf-8') as f:
        return f.read()

def main():
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

    # Aquí defines los HTMLs por separado
    archivo_html_opcion_1 = "SalonComic.html"
    archivo_html_opcion_2 = "SalonComic.html"

    html_opcion_1 = cargar_html(archivo_html_opcion_1)
    html_opcion_2 = cargar_html(archivo_html_opcion_2)

    while True:
        mostrar_menu()
        opcion = input("Elige una opción (1-3): ").strip()

        if opcion == "1":
            usuarios = obtener_usuarios_sin_correo(db_config, id_encuesta)
            if not usuarios:
                print("No hay usuarios pendientes de recibir el correo.")
            else:
                print(f"Se enviarán correos a {len(usuarios)} usuarios (con filtro).")
                for id_usuario, correo, nombre in usuarios:
                    try:
                        enviar_correo(EMAIL, APP_PASSWORD, correo, nombre, html_opcion_1)
                        print(f"Correo enviado a {nombre} <{correo}>")
                        marcar_correo_enviado(db_config, id_usuario, id_encuesta)
                    except Exception as e:
                        print(f"Error enviando correo a {correo}: {e}")

        elif opcion == "2":
            usuarios = obtener_todos_los_usuarios(db_config)
            print(f"Se enviarán correos a {len(usuarios)} usuarios (sin filtro).")
            for id_usuario, correo, nombre in usuarios:
                try:
                    enviar_correo(EMAIL, APP_PASSWORD, correo, nombre, html_opcion_2)
                    print(f"Correo enviado a {nombre} <{correo}>")
                except Exception as e:
                    print(f"Error enviando correo a {correo}: {e}")

        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, prueba otra vez.")

if __name__ == "__main__":
    main()
