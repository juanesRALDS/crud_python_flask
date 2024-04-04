#app.py

from flask import Flask
import pymongo
import os
from flask_mongoengine import MongoEngine

app = Flask(__name__)
#claves secretas para manejo  de sesiones en flask
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = './static/img'

app.config['MONGODB_SETTINGS'] = [{
    "db": "GESTIONPRODUCTOS",
    "host": "localhost",
    "port": 27017
}]
db = MongoEngine(app)
APP_SECRET_KEY = os.urandom(20)

miConexion = pymongo.MongoClient('mongodb://localhost:27017/')
baseDatos = miConexion['GESTIONPRODUCTOS']

productos = baseDatos['PRODUCTOS']
categorias = baseDatos['CATEGORIAS']
usuarios = baseDatos['USUARIOS']

todo= productos.find()
print(todo)

#user = usuarios.find_one({"usuario": "juanesRA"})

#print(user["correo"]) 

from controlador.productosControler import *
from controlador.categoriasControler import *
from controlador.loginControler import *
from controlador.model import *


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)


