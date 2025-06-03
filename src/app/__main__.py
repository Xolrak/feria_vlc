#!/usr/bin/env python3

"""
Script name: __main__.py
Author: Carlos Castañeda
Description: main de la app que gestiona los envios de correos
Version: 6.4
"""

import os
import sys
from typing import Dict, Tuple, List
from config import leer_credenciales, comprobar_credenciales
from database import (
    obtener_usuarios_sin_correo,
    marcar_correo_enviado,
    obtener_todos_los_usuarios,
    insertar_usuario
)
from mailer import enviar_correo
from utils import validar_correo

def cargar_configuracion() -> Tuple[Dict, str, str]:

    ruta_base = os.path.dirname(__file__)
    ruta_info = os.path.normpath(os.path.join(ruta_base, '..', 'credenciales.inf'))
    comprobar_credenciales(ruta_info)
    datos = leer_credenciales(ruta_info)
    
    db_config = {
        'host': datos.get('db_host'),
        'user': datos.get('db_user'),
        'password': datos.get('db_password'),
        'database': datos.get('db_nombre'),
        'port': int(datos.get('db_port', 3306))
    }
    
    return db_config, datos.get('email'), datos.get('app_password')

def cargar_html(nombre_archivo: str) -> str:

    ruta_base = os.path.dirname(__file__)
    ruta_html = os.path.join(ruta_base, '..', 'html', nombre_archivo)
    with open(ruta_html, 'r', encoding='utf-8') as f:
        return f.read()

def procesar_nuevo_usuario(db_config: Dict) -> None:

    print("\n=== Insertar nuevo usuario ===")
    
    # Solicitar y validar correo
    while True:
        correo = input("Correo electrónico: ").strip()
        if validar_correo(correo):
            break
        print("Error: Formato de correo electrónico inválido. Intente nuevamente.")

    # Solicitar y validar nombre
    nombre = input("Nombre: ").strip()
    while not nombre:
        print("Error: El nombre no puede estar vacío.")
        nombre = input("Nombre: ").strip()

    # Solicitar y validar primer apellido
    apellido1 = input("Primer apellido: ").strip()
    while not apellido1:
        print("Error: El primer apellido no puede estar vacío.")
        apellido1 = input("Primer apellido: ").strip()

    # Solicitar segundo apellido (opcional)
    apellido2 = input("Segundo apellido (opcional, presione Enter para omitir): ").strip() or None

    # Insertar usuario
    exito, resultado = insertar_usuario(db_config, correo, nombre, apellido1, apellido2)
    if exito:
        print(f"\nUsuario insertado correctamente con ID: {resultado}")
    else:
        print(f"\nError al insertar usuario: {resultado}")

def enviar_newsletter_comic(db_config: Dict, email: str, app_password: str) -> None:

    html = cargar_html("SalonComic.html")
    usuarios = obtener_todos_los_usuarios(db_config)
    print(f"Se enviarán correos del Salón del Cómic a {len(usuarios)} usuarios.")
    
    for id_usuario, correo, nombre in usuarios:
        try:
            enviar_correo(email, app_password, correo, nombre, html, 1)
            print(f"Correo enviado a {nombre} <{correo}>")
        except Exception as e:
            print(f"Error enviando correo a {correo}: {e}")

def enviar_sorteo_2ruedas(db_config: Dict, email: str, app_password: str, id_encuesta: int) -> None:

    html = cargar_html("2ruedas.html")
    usuarios = obtener_usuarios_sin_correo(db_config, id_encuesta)
    
    if not usuarios:
        print("No hay usuarios pendientes de recibir el correo de 2RUEDAS.")
        return
        
    print(f"Se enviarán correos de 2RUEDAS a {len(usuarios)} usuarios pendientes.")
    for id_usuario, correo, nombre in usuarios:
        try:
            enviar_correo(email, app_password, correo, nombre, html, 2)
            print(f"Correo enviado a {nombre} <{correo}>")
            marcar_correo_enviado(db_config, id_usuario, id_encuesta)
        except Exception as e:
            print(f"Error enviando correo a {correo}: {e}")

def mostrar_ayuda() -> None:
    """Muestra el mensaje de ayuda del programa."""
    print("Uso: python __main__.py <opcion>")
    print("Opciones:")
    print("  1 - Newsletter del Salón del Cómic (todos los usuarios)")
    print("  2 - Sorteo dos entradas para 2RUEDAS (solo usuarios pendientes)")
    print("  3 - Insertar nuevo usuario en la base de datos")

def main() -> None:
    """Función principal del programa."""
    if len(sys.argv) != 2 or sys.argv[1] not in ["1", "2", "3"]:
        mostrar_ayuda()
        sys.exit(1)

    opcion = sys.argv[1]
    db_config, email, app_password = cargar_configuracion()
    
    if opcion == "1":
        enviar_newsletter_comic(db_config, email, app_password)
    elif opcion == "2":
        enviar_sorteo_2ruedas(db_config, email, app_password, id_encuesta=1)
    elif opcion == "3":
        procesar_nuevo_usuario(db_config)
        return

if __name__ == "__main__":
    main()

