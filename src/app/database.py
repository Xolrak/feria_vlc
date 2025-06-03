"""
Script name: database.py
Author: Carlos Castañeda
Description: funciones para interactuar con la base de datos
Version: 1.2
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

def insertar_usuario(db_config, correo, nombre, apellido1, apellido2=None):

    cnx = None
    cursor = None
    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Verificar si el correo ya existe
        query_check = "SELECT id_usuario FROM Usuarios WHERE correo_electronico = %s"
        cursor.execute(query_check, (correo,))
        if cursor.fetchone():
            return False, "El correo electrónico ya existe en la base de datos"

        # Insertar nuevo usuario
        if apellido2:
            query = """
                INSERT INTO Usuarios (correo_electronico, nombre, apellido_1, apellido_2)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (correo, nombre, apellido1, apellido2))
        else:
            query = """
                INSERT INTO Usuarios (correo_electronico, nombre, apellido_1)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (correo, nombre, apellido1))

        # Obtener el ID del usuario insertado
        id_usuario = cursor.lastrowid

        # Insertar en la tabla Hacen para la encuesta activa
        query_hacen = """
            INSERT INTO Hacen (id_usuario, id_encuesta, realizada, correo_enviado)
            VALUES (%s, %s, FALSE, FALSE)
        """
        cursor.execute(query_hacen, (id_usuario, 1))  # 1 es el ID de la encuesta activa

        # Confirmar transacción
        cnx.commit()
        return True, id_usuario

    except mysql.connector.Error as err:
        if cnx:
            cnx.rollback()
        return False, f"Error de base de datos: {err}"
    except Exception as e:
        if cnx:
            cnx.rollback()
        return False, f"Error: {str(e)}"
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()

def eliminar_usuario(db_config, id_usuario=None, correo=None):

    try:
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        if id_usuario:
            query = "DELETE FROM Usuarios WHERE id_usuario = %s"
            cursor.execute(query, (id_usuario,))
        elif correo:
            query = "DELETE FROM Usuarios WHERE correo_electronico = %s"
            cursor.execute(query, (correo,))
        else:
            return False, "Se debe proporcionar un ID o correo electrónico"

        cnx.commit()
        filas_afectadas = cursor.rowcount
        cursor.close()
        cnx.close()

        if filas_afectadas > 0:
            return True, f"Usuario eliminado correctamente"
        else:
            return False, "No se encontró el usuario"

    except mysql.connector.Error as err:
        return False, f"Error de base de datos: {err}"
    except Exception as e:
        return False, f"Error: {str(e)}"
