"""
Script name: config.py
Author: Carlos Castañeda
Description: funciones para el uso de credenciales ..\credenciales.inf
"""

import os
import sys

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
