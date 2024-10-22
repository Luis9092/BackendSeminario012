import smtplib
from email.message import EmailMessage

def enviar_correo_contraseña(email_destino, contraseña, email_origen, contraseña_origen):
    # Crea el mensaje de correo
    mensaje = EmailMessage()
    mensaje['Subject'] = 'Tu contraseña para el login'
    mensaje['From'] = email_origen
    mensaje['To'] = email_destino
    mensaje.set_content(f'Tu contraseña para el login es: {contraseña}')

    # Configuración del servidor SMTP
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as servidor:
            servidor.login(email_origen, contraseña_origen)
            servidor.send_message(mensaje)
            print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Ejemplo de usojj
email_destino = 'jgodoym11@miumg.edu.gt'
contraseña = 'nxck wrvo rlgc vaeh'
email_origen = 'ferreteriagodoys@gmail.com'
contraseña_origen = 'nxck wrvo rlgc vaeh'

enviar_correo_contraseña(email_destino, contraseña, email_origen, contraseña_origen)