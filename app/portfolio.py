from flask import (Blueprint, render_template,
                   request, redirect, url_for, current_app)

import sendgrid
from sendgrid.helpers.mail import *


bp = Blueprint('portfolio', __name__, url_prefix='/')


@bp.route('/', methods=['GET'])
def index():
    return render_template('portfolio/index.html')


@bp.route('/mail', methods=['GET', 'POST'])
def mail():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    mensaje = request.form.get('mensaje')

    if request.method == 'POST':
        enviar_mail(nombre, email, mensaje)
        return render_template('portfolio/enviar_mail.html')
        
    return redirect(url_for('portfolio.index'))


def enviar_mail(nombre, email, mensaje):
    mi_email = 'g.astudilloc1@gmail.com'
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_KEY'])
    
    from_email = Email(mi_email)
    to_email = To(mi_email, substitutions={
        "-name-": nombre,
        "-email-": email,
        "-message-": mensaje,
    })

    html_content = """
    <p>Hola Germán, tienes un nuevo correo desde tu portafolio:</p>
    <p>Nombre: -name-</p>
    <p>Email: -email-</p>
    <p>Mensaje: -message-</p>
    """

    mail = Mail(mi_email, to_email, "Nuevo contacto desde portafolio", html_content=html_content)
    response = sg.client.mail.send.post(request_body=mail.get())