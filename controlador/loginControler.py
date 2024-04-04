from flask import Flask, render_template, request, redirect, url_for, session
from app import app, usuarios 
import yagmail
import threading
import pymongo

"""
@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    estado =False

    if request.method == 'POST':
        correo = request.form['correo']
        password = request.form['password']
        usuario = usuarios.find_one({"correo": correo, "password": password})
        if usuario:
            email = yagmail.SMTP('juanesrondon50@gmail.com', 'wkje zjqc zujh ffka', encoding='UTF-8')
            asunto="el usuario ingreso al sistema"
            mensaje=f"se informa que el usuario {usuario ['correo']} ha ingresado al sistema"
            email.send(to=['juanesrondon50@gmail.com', usuario['correo']], subject=asunto, contents= mensaje)
            session['usuario'] = correo  
            return redirect(url_for('listaProductos'))  # Redirigir a la página de productos después de iniciar sesión
        else:
            mensaje = "Correo o contraseña incorrecto"
    return render_template('login.html', mensaje=mensaje, estado=estado)

#otra forma de hacer que hace que la aplicacion no se quede cargando mientras se envia el codigo
"""

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    estado = False

    try: 
        def enviarCorreo(email, destinatarios, asunto, mensaje):
            email.send(to=destinatarios, subject=asunto, contents=mensaje)

        if request.method == 'POST':
            correo = request.form['correo']
            password = request.form['password']
            usuario = usuarios.find_one({"correo": correo, "password": password})
            if usuario:
                email = yagmail.SMTP('juanesrondon50@gmail.com', 'wkje zjqc zujh ffka', encoding='UTF-8')
                asunto = "el usuario ingreso al sistema"
                mensaje = f"se informa que el usuario {usuario ['correo']} ha ingresado al sistema"
                thread = threading.Thread(
                    target=enviarCorreo,
                    args=(email, ['juanesrondon50@gmail.com', usuario['correo']], asunto, mensaje)
                )
                thread.start()
                session['usuarios'] = correo  
                return redirect(url_for('listaProductos'))  # Redirigir a la página de productos después de iniciar sesión
            else:
                mensaje = "Correo o contraseña incorrecto"     
    except pymongo.errors.PyMongoError as error:
        mensaje=error

    return render_template('login.html', mensaje=mensaje, estado=estado)
