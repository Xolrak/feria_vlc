"""
Script name: utils.py
Author: Carlos Castañeda
Description: Funciones de utilidad para la aplicación
Version: 1.0
"""

import re

def validar_correo(correo):

    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo) is not None 