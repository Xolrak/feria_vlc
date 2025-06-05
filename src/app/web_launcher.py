from flask import Flask, render_template, redirect, url_for, flash, request
import os
import subprocess
from pathlib import Path
from typing import Dict, Tuple

from config import leer_credenciales, comprobar_credenciales
from database import (
    obtener_usuarios_sin_correo,
    marcar_correo_enviado,
    obtener_todos_los_usuarios,
    insertar_usuario
)
from mailer import enviar_correo
from utils import validar_correo

app = Flask(__name__)
app.secret_key = os.urandom(24)

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

def check_mjml():
    try:
        # En Windows, el comando mjml puede estar en diferentes ubicaciones
        if os.name == 'nt':  # Windows
            try:
                # Intentar con npm global
                subprocess.run(['npm', 'list', '-g', 'mjml'], capture_output=True, check=True)
                return
            except:
                # Intentar con npm local
                try:
                    subprocess.run(['npm', 'list', 'mjml'], capture_output=True, check=True)
                    return
                except:
                    pass
            
            # Si llegamos aquí, intentar directamente con mjml
            subprocess.run(['mjml', '--version'], capture_output=True, shell=True, check=True)
        else:  # Linux/Mac
            result = subprocess.run(['which', 'mjml'], capture_output=True, text=True)
            if result.returncode != 0:
                # Intentar encontrar mjml en node_modules
                ruta_base = os.path.dirname(os.path.abspath(__file__))
                node_mjml = os.path.join(ruta_base, 'node_modules', '.bin', 'mjml')
                if not os.path.exists(node_mjml):
                    raise RuntimeError("MJML no encontrado. Instálalo con: npm install -g mjml")
    except Exception as e:
        print(f"Error al verificar MJML: {str(e)}")
        raise RuntimeError("MJML no está instalado. Instálalo con: npm install -g mjml")

def convert_mjml_to_html():
    try:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        mjml_folder = os.path.normpath(os.path.join(ruta_base, '..', 'mjml'))
        html_folder = os.path.normpath(os.path.join(ruta_base, '..', 'html'))
        
        if not os.path.exists(mjml_folder):
            raise RuntimeError(f"Carpeta MJML no encontrada en: {mjml_folder}")
            
        os.makedirs(html_folder, exist_ok=True)
        
        for mjml_file in Path(mjml_folder).glob("*.mjml"):
            html_file = os.path.join(html_folder, f"{mjml_file.stem}.html")
            try:
                if os.name == 'nt':  # Windows
                    cmd = f'mjml "{mjml_file.absolute()}" -o "{html_file}"'
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                else:
                    # En Linux, primero intentar con mjml global
                    try:
                        result = subprocess.run(
                            ['mjml', str(mjml_file.absolute()), '-o', html_file],
                            capture_output=True,
                            text=True
                        )
                    except FileNotFoundError:
                        # Si falla, intentar con mjml local
                        node_mjml = os.path.join(ruta_base, 'node_modules', '.bin', 'mjml')
                        if os.path.exists(node_mjml):
                            result = subprocess.run(
                                [node_mjml, str(mjml_file.absolute()), '-o', html_file],
                                capture_output=True,
                                text=True
                            )
                        else:
                            raise RuntimeError("No se encontró MJML ni global ni localmente")
                
                if result.returncode != 0:
                    raise RuntimeError(f"Error de MJML: {result.stderr}")
                    
                print(f"Convertido: {mjml_file.name} -> {os.path.basename(html_file)}")
            except Exception as e:
                print(f"Error al convertir {mjml_file.name}: {str(e)}")
                raise RuntimeError(f"Error al convertir {mjml_file.name}: {str(e)}")
    except Exception as e:
        print(f"Error en la conversión MJML: {str(e)}")
        raise RuntimeError(f"Error al convertir archivos MJML a HTML: {str(e)}")

@app.route('/')
def index():
    try:
        db_config, _, _ = cargar_configuracion()
        check_mjml()
        convert_mjml_to_html()
        return render_template('index.html')
    except Exception as e:
        flash(str(e), 'error')
        return render_template('error.html', error=str(e))

@app.route('/execute/<int:option>')
def execute_option(option):
    try:
        db_config, email, app_password = cargar_configuracion()
        
        if option == 1:
            # Newsletter del Salón del Cómic
            html = cargar_html("SalonComic.html")
            usuarios = obtener_todos_los_usuarios(db_config)
            for id_usuario, correo, nombre in usuarios:
                try:
                    enviar_correo(email, app_password, correo, nombre, html, 1)
                    flash(f'Correo enviado a {nombre} <{correo}>', 'success')
                except Exception as e:
                    flash(f'Error enviando correo a {correo}: {str(e)}', 'error')
                    
        elif option == 2:
            # Sorteo 2RUEDAS
            html = cargar_html("2ruedas.html")
            usuarios = obtener_usuarios_sin_correo(db_config, 1)  # id_encuesta = 1
            if not usuarios:
                flash('No hay usuarios pendientes de recibir el correo de 2RUEDAS.', 'info')
            else:
                for id_usuario, correo, nombre in usuarios:
                    try:
                        enviar_correo(email, app_password, correo, nombre, html, 2)
                        marcar_correo_enviado(db_config, id_usuario, 1)
                        flash(f'Correo enviado a {nombre} <{correo}>', 'success')
                    except Exception as e:
                        flash(f'Error enviando correo a {correo}: {str(e)}', 'error')
                        
        elif option == 3:
            # Redirigir al formulario de nuevo usuario
            return redirect(url_for('nuevo_usuario_form'))
            
    except Exception as e:
        flash(str(e), 'error')
        
    return redirect(url_for('index'))

@app.route('/nuevo_usuario', methods=['GET', 'POST'])
def nuevo_usuario_form():
    if request.method == 'POST':
        correo = request.form.get('correo', '').strip()
        nombre = request.form.get('nombre', '').strip()
        apellido1 = request.form.get('apellido1', '').strip()
        apellido2 = request.form.get('apellido2', '').strip() or None
        
        if not validar_correo(correo):
            flash('Error: Formato de correo electrónico inválido.', 'error')
            return redirect(url_for('nuevo_usuario_form'))
            
        if not nombre or not apellido1:
            flash('Error: El nombre y primer apellido son obligatorios.', 'error')
            return redirect(url_for('nuevo_usuario_form'))
            
        try:
            db_config, _, _ = cargar_configuracion()
            exito, resultado = insertar_usuario(db_config, correo, nombre, apellido1, apellido2)
            if exito:
                flash(f'Usuario insertado correctamente con ID: {resultado}', 'success')
                return redirect(url_for('index'))
            else:
                flash(f'Error al insertar usuario: {resultado}', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            
        return redirect(url_for('nuevo_usuario_form'))
        
    return render_template('nuevo_usuario.html')

if __name__ == '__main__':
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print("\n=== Servidor Web de Feria VLC ===")
    print(f"Servidor iniciado en:")
    print(f"- Local (esta máquina): http://localhost:5000")
    print(f"- Red local (otras máquinas): http://{local_ip}:5000")
    print("CTRL+C para detener el servidor")
    print("================================\n")
    
    # Configurar el servidor para escuchar en todas las interfaces
    app.run(
        host='0.0.0.0',  # Escuchar en todas las interfaces
        port=5000,
        debug=False,  # Deshabilitar modo debug en producción
        threaded=True  # Permitir múltiples conexiones simultáneas
    ) 