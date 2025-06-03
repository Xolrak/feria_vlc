"""
Script name: mailer.py
Author: Carlos Castañeda
Description: funcion para enviar los html
Version: 1.1
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(email, app_password, correo_destino, nombre_destino, html_content, opcion):

    html_personalizado = html_content.replace('{{nombre}}', nombre_destino)

    if opcion == 1:
        asunto = '¡Novedades del Salón del Cómic!'
    elif opcion == 2:
        asunto = '¡Sorteo de entradas para MotoGP!'
    else:
        asunto = 'Correo sin asunto definido'

    mensaje = MIMEMultipart('alternative')
    mensaje['Subject'] = asunto
    mensaje['From'] = email
    mensaje['To'] = correo_destino
    mensaje.attach(MIMEText(html_personalizado, 'html'))

    with smtplib.SMTP('smtp.office365.com', 587) as servidor:
        servidor.starttls()
        servidor.login(email, app_password)
        servidor.send_message(mensaje)
