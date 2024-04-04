from mongoengine import Document, ReferenceField, StringField, IntField, EmailField

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
categoria = Categoria(nombre="prueba_0123")
#categoria.save()

#remplaza los datos para insetar nuevos documentos  
user = Usuario(usuario="djfdñfdañfj", password="12fdfa3455", nombres="ussddmklfer", correo="userkldalfndaSena@sena.edu.co")
#user.save()

user = Usuario.objects(usuario="juanesRA", password="12345").first()

consulta_product = Producto.objects()

print(user)