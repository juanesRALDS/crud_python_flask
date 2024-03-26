#app.py

from flask import Flask
import pymongo
import os


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/img'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)


