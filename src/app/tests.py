#!/usr/bin/env python3

"""
Script name: tests.py
Author: Carlos Castañeda
Description: Tests unitarios para la aplicación de envío de correos
Version: 1.2
"""

import unittest
import os
from config import leer_credenciales, comprobar_credenciales
from database import insertar_usuario, obtener_todos_los_usuarios, eliminar_usuario
from mailer import enviar_correo
from utils import validar_correo
import random
import string

class TestFeriaApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configuración inicial que se ejecuta una vez antes de todas las pruebas
        ruta_base = os.path.dirname(__file__)
        ruta_info = os.path.normpath(os.path.join(ruta_base, '..', 'credenciales.inf'))
        comprobar_credenciales(ruta_info)
        datos = leer_credenciales(ruta_info)
        
        cls.db_config = {
            'host': datos.get('db_host'),
            'user': datos.get('db_user'),
            'password': datos.get('db_password'),
            'database': datos.get('db_nombre'),
            'port': int(datos.get('db_port', 3306))
        }
        
        cls.EMAIL = datos.get('email')
        cls.APP_PASSWORD = datos.get('app_password')
        
        # Lista para almacenar los IDs de usuarios creados durante las pruebas
        cls.usuarios_prueba = []

    @classmethod
    def tearDownClass(cls):
        # Limpieza final: eliminar todos los usuarios de prueba
        for id_usuario in cls.usuarios_prueba:
            eliminar_usuario(cls.db_config, id_usuario=id_usuario)
        print(f"\nLimpieza: {len(cls.usuarios_prueba)} usuarios de prueba eliminados")

    def generar_correo_aleatorio(self):
        # Genera un correo aleatorio para pruebas
        letras = string.ascii_lowercase
        nombre = ''.join(random.choice(letras) for i in range(8))
        return f"test_{nombre}@test.com"

    def test_1_insertar_usuario_nuevo(self):
        """Test de inserción de un nuevo usuario"""
        correo = self.generar_correo_aleatorio()
        nombre = "Test"
        apellido1 = "Usuario"
        apellido2 = "Prueba"
        
        exito, resultado = insertar_usuario(self.db_config, correo, nombre, apellido1, apellido2)
        self.assertTrue(exito, f"Error al insertar usuario: {resultado}")
        self.assertIsInstance(resultado, int, "El ID devuelto no es un número")
        
        # Guardar el ID para limpieza posterior
        if exito:
            self.usuarios_prueba.append(resultado)
            
        print(f"\nTest 1: Usuario insertado correctamente con ID {resultado}")

    def test_2_insertar_usuario_duplicado(self):
        """Test de inserción de un usuario con correo duplicado"""
        correo = self.generar_correo_aleatorio()
        nombre = "Test"
        apellido1 = "Usuario"
        
        # Primera inserción
        exito1, resultado = insertar_usuario(self.db_config, correo, nombre, apellido1)
        self.assertTrue(exito1, "Error en la primera inserción")
        
        # Guardar el ID para limpieza posterior
        if exito1:
            self.usuarios_prueba.append(resultado)
        
        # Intento de inserción duplicada
        exito2, mensaje = insertar_usuario(self.db_config, correo, nombre, apellido1)
        self.assertFalse(exito2, "La inserción duplicada no debería ser exitosa")
        self.assertEqual(mensaje, "El correo electrónico ya existe en la base de datos")
        print("\nTest 2: Detección de correo duplicado correcta")

    def test_3_obtener_usuarios(self):
        """Test de obtención de usuarios"""
        usuarios = obtener_todos_los_usuarios(self.db_config)
        self.assertIsInstance(usuarios, list, "El resultado debe ser una lista")
        self.assertTrue(len(usuarios) > 0, "La base de datos debe contener al menos un usuario")
        print(f"\nTest 3: Se encontraron {len(usuarios)} usuarios en la base de datos")

    def test_4_validar_formato_correo(self):
        """Test de validación de formato de correo"""
        correos_validos = [
            "test@example.com",
            "user.name@domain.com",
            "user+label@domain.co.uk"
        ]
        
        correos_invalidos = [
            "test@",
            "@domain.com",
            "test.domain.com",
            "test@domain",
            ""
        ]
        
        for correo in correos_validos:
            self.assertTrue(validar_correo(correo), f"El correo {correo} debería ser válido")
            
        for correo in correos_invalidos:
            self.assertFalse(validar_correo(correo), f"El correo {correo} debería ser inválido")
            
        print("\nTest 4: Validación de formato de correos correcta")

if __name__ == '__main__':
    print("\n=== Iniciando pruebas de la aplicación ===\n")
    unittest.main(verbosity=2) 