# productosControler.py

import os
from bson.objectid import ObjectId
import pymongo
from PIL import Image
from io import BytesIO
import base64
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from app import app, productos, categorias, usuarios 
from bson.objectid import ObjectId


@app.route('/buscarProductoPorCodigo/<codigo>', methods=['GET'])
def buscarProductoPorCodigo(codigo):
    try:
        producto = productos.find_one({'codigo': int(codigo)})
        if producto:
            # Renderizar una plantilla específica para el producto encontrado
            return render_template('producto_detalle.html', producto=producto)
        else:
            return jsonify({"mensaje": "Producto no encontrado"}), 404
    except Exception as e:
        return jsonify({"mensaje": str(e)}), 500


@app.route('/eliminarProducto/<producto_id>', methods=['POST'])
def eliminarProducto(producto_id):
    try:
        resultado = productos.delete_one({'_id': ObjectId(producto_id)})
        if resultado.deleted_count == 1:
            return jsonify({"mensaje": "Producto eliminado correctamente"}), 200
        else:
            return jsonify({"mensaje": "No se pudo eliminar el producto"}), 400
    except Exception as e:
        return jsonify({"mensaje": str(e)}), 500

@app.route("/listaProductos", methods=['GET'])
def listaProductos():
    codigo = request.args.get('codigo')
    if codigo:
        # Redirigir al usuario a la búsqueda por código
        return redirect(url_for('buscarProductoPorCodigo', codigo=codigo))
    else:
        # Mostrar todos los productos
        listaProductos = productos.find()
        listaCategorias = categorias.find()
        listaP = []
        for p in listaProductos:
            categoria = categorias.find_one({'_id': p.get('categorias', None)})
            if categoria:
                p['categoria'] = categoria['nombre']
            else:
                p['categoria'] = "Sin categoría"
            listaP.append(p)
        return render_template("listaProductos.html", productos=listaP, listaCategorias=listaCategorias)


@app.route('/vistaAgregarProducto', methods=['GET'])
def AgregarProducto():
    categorias_from_db = categorias.find()
    return render_template('Form.html', categorias=categorias_from_db)

@app.route('/agregarProducto', methods=['POST'])
def agregarProducto():
    mensaje = None
    estado = False
    try:
        codigo = int(request.form['codigo'])
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        idCategoria = ObjectId(request.form['cdCategoria'])
        foto = request.files['fileFoto']
        
        if foto and allowed_file(foto.filename): # Asegúrate de tener una función allowed_file que verifique el tipo de archivo
            producto = {
                'codigo': codigo,
                'nombre': nombre,
                'precio': precio,
                'categoria': idCategoria
            }
            resultado = productos.insert_one(producto)
            if (resultado.acknowledged):
                idProducto = resultado.inserted_id
                nombreFotos = f'{idProducto}.jpg'
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFotos))
                mensaje = 'Producto Agregado Correctamente'
                estado = True
            else:
                mensaje = 'Problema Al Agregar El Producto'
        else:
            mensaje = 'Archivo no subido o tipo de archivo no permitido'
    except pymongo.errors.PyMongoError as error:  
        mensaje = str(error)
        flash((mensaje, estado))
    return redirect(url_for('listaProductos'))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/editarProducto/<producto_id>', methods=['GET', 'POST'])
def editarProducto(producto_id):
    if request.method == 'POST':
        # Procesar la actualización del producto
        codigo = int(request.form['codigo'])
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        idCategoria = ObjectId(request.form['categorias'])
        foto = request.files['fileFoto']
        
        producto = {
            'codigo': codigo,
            'nombre': nombre,
            'precio': precio,
            'categorias': idCategoria
        }
        
        resultado = productos.update_one({'_id': ObjectId(producto_id)}, {"$set": producto})
        if resultado.acknowledged:
            if foto and allowed_file(foto.filename):
                nombreFoto = f"{producto_id}.jpg"
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFoto))
            flash('Producto actualizado correctamente.')
            return redirect(url_for('listaProductos'))
        else:
            flash('No se pudo actualizar el producto.')
            return redirect(url_for('editarProducto', producto_id=producto_id))
    else:
        # Mostrar el formulario de edición
        producto = productos.find_one({'_id': ObjectId(producto_id)})
        categorias_from_db = categorias.find()
        return render_template('formEditar.html', producto=producto, categorias=categorias_from_db)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





""" def consultarProducto(codigo):
    try:
        consulta = {"codigo": codigo}
        producto = productos.find_one(consulta)
        if (producto is not None):
            return True
        else:
            return False
    except pymongo.error as error:
        print(error)
        return False """

"""
@app.route('/agregarProductoJson', methods=['POST'])
def agregarProductoJson():
    estado = False
    mensaje = None
    try:
        datos = request.json
        producto = datos.get('producto')
        fotoBase64 = datos.get('foto')["foto"]
        producto = {
            'codigo': int(producto["codigo"]),
            'nombre': producto["nombre"],
            'precio': int(producto["precio"]),
            'categoria': ObjectId(producto["categoria"])
        }
        resultado = productos.insert_one(producto)
        if resultado.acknowledged:
            rutaImagen = f"{os.path.join(app.config['UPLOAD_FOLDER'])}/{resultado.inserted_id}.jpg"
            fotoBase64 = fotoBase64[fotoBase64.index(',') + 1]
            fotoDecodificada = base64.b64decode(fotoBase64)
            imagen = Image.open(BytesIO(fotoDecodificada))
            imagenJpg = imagen.convert('RGB')
            imagen.save(rutaImagen)
            estado = True
            mensaje = 'Producto Agregado'
        else:
            mensaje = 'Problemas al Agregar'
    except pymongo.errors.PyMongoError as error:
        mensaje = str(error)
    retorno = {"estado": estado, "mensaje": mensaje}
    return jsonify(retorno)
"""

""" @app.route("/consultar/<codigo>", methods=["GET"])
def consultarPorCodigo(codigo):
    estado=False
    mensaje=None
    producto=None

    try:
        datosConsulta={'codigo':int(codigo)}
        producto=producto.find_one(datosConsulta)
        if (producto):
            estado=True
    except pymongo.errors as error:
        mensaje=error
    listaCategorias = categorias.find()
    return render_template("formEditar.html", producto=producto, categorias=listaCategorias)
"""
"""
@app.route("/editar", methods=["POST"])
def editar():
    estado=False
    mensaje=None
    try:
        codigo = int(request.form['codigo'])
        nombre = request.form['nombre']
        precio = int(request.form['precio'])
        idCategoria = ObjectId(request.form['categorias'])
        foto = request.files['fileFoto'] 
        idProducto=request.form['idProducto']
        producto = {
            'codigo': codigo,
            'nombre': nombre,
            'precio': precio,
            'categoria': idCategoria
        }

        resultado = productos.update_one({'_id':idProducto},{"$set": producto})
        #acknowledged que indica si el servidor de MongoDB confirmó que recibió y procesó la operación de escritura.
        if (resultado.acknowledged):
            listaCategorias = categorias.find()

            if(foto):
                nombreFoto=f"{idProducto}.jpg"
                foto.save(os.path.join(app.config['UPLOAD_FOLDER'], nombreFoto))
            mensaje="actualizado"
        else:
            mensaje="problemas al actualizar"

    except pymongo.errors as error:
        mensaje=error
    return render_template("form.html", producto=producto, categorias=listaCategorias, estado=estado, mensaje=mensaje) 

"""

