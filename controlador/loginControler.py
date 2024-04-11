from flask import Flask, render_template, request, redirect, url_for, session
from app import app, usuarios # Asegúrate de que 'usuarios' es correcto y accesible
import yagmail
import threading
import pymongo
import urllib.request
import urllib.parse
import json
# Asegúrate de que 'Usuario' es correcto y accesible

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    estado = False

    if request.method == 'POST':
        recaptcha_response = request.form['g-recaptcha-response']
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': '6LeKF7cpAAAAAOHzUiUFCEAIa6INCfBp2fttTTSm',
            'response': recaptcha_response
        }
        
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        if result['success']:
            correo = request.form['correo']
            password = request.form['password']
            usuario = usuarios.find_one({"correo": correo, "password": password})
            if usuario:
                email = yagmail.SMTP('juanesrondon50@gmail.com',open('password.txt').read(), encoding='UTF-8')
                asunto = "el usuario ingreso al sistema"
                mensaje = f"se informa que el usuario {usuario['correo']} ha ingresado al sistema"
                thread = threading.Thread(
                    target=email.send,
                    args=(['juanesrondon50@gmail.com', usuario['correo']], asunto, mensaje)
                )
                thread.start()
                session['usuario'] = correo  
                return redirect(url_for('listaProductos')) # Redirigir a la página de productos después de iniciar sesión
            else:
                mensaje = "Correo o contraseña incorrecto"
        else:
            mensaje = "Verificación de reCAPTCHA fallida"

    return render_template('login.html', mensaje=mensaje, estado=estado)
