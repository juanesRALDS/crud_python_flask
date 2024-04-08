#por favor descargar esta version de flask: Flask==2.2.5, fue la que me funciono en este proyecto para la libreria de mongoEngine

from mongoengine import Document, ReferenceField, StringField, IntField, EmailField
from bson import ObjectId


# Crear clase que representa la colección usuario en la base de datos
class Usuario(Document):
    usuario = StringField(max_length=50, required=True, unique=True) # campo nombre del usuario
    password = StringField(max_length=50)
    nombres = StringField(max_length=50)
    correo = EmailField(required=True, unique=True)
    meta = {'collection': 'USUARIOS'} # Especificar el nombre de la colección que va usar, (quitar para que genere una  nueva coleccion a apartir  de la  clase)

# Crear clase que representa la colección categorias en la base de datos
class Categoria(Document):
    nombre = StringField(max_length=50, unique=True)
    meta = {'collection': 'CATEGORIAS'} # Especificar el nombre de la colección

# Crear la clase que representa la colección producto en la base de datos
class Producto(Document):
    codigo = IntField(unique=True)
    nombre = StringField(max_length=50)
    precio = IntField()
    Categoria = ReferenceField(Categoria)
    meta = {'collection': 'PRODUCTOS'}  # Especificar el nombre de la colección que va usar, (quitar para que genere una  nueva coleccion a apartir  de la  clase)

# Ahora, cuando crees y guardes un documento de la clase Categoria, se insertará en la colección "CATEGORIAS",  remplaza los datos para añadir nuevas colecciones
#categoria = Categoria(nombre="ropa")
#categoria.save()

#remplaza los datos para insetar nuevos documentos  
#user = Usuario(usuario="djfdñfdañfj", password="12fdfa3455", nombres="ussddmklfer", correo="userkldalfndaSena@sena.edu.co")
#producto_doc = Producto()
#user.save()

#user = Usuario.objects(usuario="juanesRA", password="12345").first()

#consulta_product = Producto.objects()

#actualizar un docummento
#Producto.objects(codigo=13).update_one(set__precio=9329832

#eliminacion de un documento
#obj = Categoria.objects(id=ObjectId('660f2035fc8ba45fa737aedd')).first()

"""
# Verifica si el objeto existe antes de intentar eliminarlo
#if obj:
    obj.delete()
else:
    print("El documento con el ID especificado no se encontró.")
"""

