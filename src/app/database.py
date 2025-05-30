"""
Script name: database.py
Author: Carlos Castañeda
Description: funciones para interactuar con la base de datos
"""

import mysql.connector

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

def obtener_todos_los_usuarios(db_config):
    import mysql.connector
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario, correo_electronico, nombre FROM Usuarios;")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios
