# Importar las siguientes
# flask              - Crea una aplicación Web
# flask_cors         - Permite acceder a cada una de las rutas de la app  
# flask_sqlalchemy   - Para trabajar con la base de datos
# flask_marshmallow  - Para poder hacer conversión de datos 

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# CREAR LA APP
app = Flask(__name__)

# PERMITIR EL ACCESO DEL FRONTEND A LA RUTAS DE LAS APP
CORS(app)

# CONFIGURACIÓN A LA BASE DE DATOS                   //USER:PASSWORD@LOCALHOST/NOMBRE DB
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:@localhost/reservacanchas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 

# PERMITE MANIPULAR LA BASE DE DATOS DE LA APP
db = SQLAlchemy(app)
ma = Marshmallow(app)   # Convierte Objetos a Json y viceversa

# DEFINIR LA CLASE PRODUCTO (ESTRUCTURA DE LA TABLA DE UNA BASE DE DATOS)
#class Socios(db.Model):      # Esta clase representa a la tabla.
# class Socios(db.Model):     # Esta clase representa a la tabla.
#     nroSocio = db.Column(db.Integer, primary_key=True)
#     nombre = db.Column(db.String(100))
#     telefono = db.Column(db.Integer)
       
#     def __init__(self, nombre, telefono):  # Definimos el Constructor
#         self.nombre = nombre
#         self.telefono = telefono
       
# class Canchas(db.Model):      # Esta clase representa a la tabla.
#     id_cancha = db.Column(db.Integer, primary_key=True)
#     nombreCancha = db.Column(db.String(20))
        
#     def __init__(self, nombreCancha):  # Definimos el Constructor
#         self.nombreCancha = nombreCancha
        
class Reserva(db.Model):      # Esta clase representa a la tabla.
    id = db.Column(db.Integer, primary_key=True)
    nrosocio = db.Column(db.Integer)
    nombre = db.Column(db.String(50))
    horario = db.Column(db.Date)
    deporte = db.Column(db.String(10))
        
    def __init__(self, nrosocio, nombre, horario, deporte):  # Definimos el Constructor
        self.nrosocio = nrosocio
        self.nombre = nombre
        self.horario = horario
        self.deporte = deporte
        

# CÓDIGO QUE CREARÁ TODAS LAS TABLAS
with app.app_context():
    db.create_all()


# CLASE QUE PERMITIRÁ ACCEDER A LOS MÉTODOS DE CONVERSIÓN DE DATOS -  7
# class SociosSchema(ma.Schema):
#     class Meta:
#         fields = ("nroSocio", "nombre", "telefono")
# class CanchasSchema(ma.Schema):
#     class Meta:
#         fields = ("id_cancha", "nombreCancha")
class ReservasSchema(ma.Schema):
    class Meta:
        fields = ("id", "nrosocio", "nombre", "horario", "deporte")


# CREAR DOS OBJETOS
# socio_schema = SociosSchema()   #Trae una línea de la tabla
# socios_schema = SociosSchema(many=True)  #Trae varias líneas de la tabla

# cancha_schema = CanchasSchema()
# canchas_schema = CanchasSchema(many=True)

rango_schema = ReservasSchema()
rangos_schema = ReservasSchema(many=True)

# CREAR RUTAS (ENDPOINT)
# '/productos' ENDPOINT PARA RECIBIR DATOS: POST
# '/productos' ENDPOINT PARA MOSTRAR TODAS LAS reservas DISPONIBLES EN LA BASE DE DATOS: GET
# '/productos/<id>' ENDPOINT PARA MOSTRAR UNA reserva POR ID: GET
# '/productos/<id>' ENDPOINT PARA BORRAR UNA reserva POR ID: DELETE
# '/productos/<id>' ENDPOINT PARA MODIFICAR UNA reserva POR ID: PUT

# ENDPOINT/RUTA "reservas" para mostrar todas las reservas
# DISPONIBLES EN LA BASE DE DATOS:
@app.route("/reservas", methods=['GET'])
def get_reservas(): 
    # El metodo query.all() lo hereda de db.Model 
    # Permite obtener todos los datos de la tabla Producto
    # CONSULTAR (GET) TODA LA INFO EN LA TABLA RESERVA
    all_reservas = Reserva.query.all()
    
    return rangos_schema.jsonify(all_reservas)


# RUTA CREAR UN NUEVO REGISTRO EN LA TABLA, que vienen de un json
@app.route("/reservas", methods=['POST'])
def create_reserva(): 

    # request.json contiene el json que envió el cliente 
    # Para insertar registro en la tabla de la base de datos 
    # Se usará la clase Reserva(tabla) pasándole cada dato recibido.    
    # RECIBEN LOS DATOS
    nrosocio = request.json[nrosocio]
    nombre = request.json[nombre]
    horario = request[horario]
    deporte = request[deporte]

    # INSERTAR EN DB
    # Para agregar los cambios a la db con db.session.add(objeto) 
    # Para guardar los cambios a la db con db.session.commit()
    new_reserva = Reserva(nrosocio, nombre, horario, deporte)
    db.session.add(new_reserva)
    db.session.commit()
    # Retornar los datos guardados en formato JSON 
    # Para ello, usar el objeto reserva_schema para que convierta con 
    # jsonify los datos recién ingresados que son objetos a JSON
    return rango_schema.jsonify(new_reserva)
    
# MOSTRAR un registro de RESERVA POR ID
@app.route('/reservas/<id>',methods=['GET'])
def get_reserva(id):
    # Consultar por id, a la clase Reserva.
    # Se hace una consulta (query) para obtener (get) un registro por id
    reserva = Reserva.query.get(id)

   # Retorna el JSON de una reserva recibida como parámetro
   # Para ello, usar el objeto reserva_schema para que convierta con                   # jsonify los datos recién ingresados que son objetos a JSON  
    return rango_schema.jsonify(reserva)   


# BORRAR RESERVA
@app.route('/reservas/<id>', methods=['DELETE'])
def delete_reserva(id):
    # Consultar por id, a la clase Reserva.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    reserva = Reserva.query.get(id)
    
    # A partir de db y la sesión establecida con la base de datos borrar 
    # el producto.
    # Se guardan lo cambios con commit
    db.session.delete(reserva)
    db.session.commit()

# ENDPOINT PARA MODIFICAR UNA RESERVA POR ID
@app.route('/reservas/<id>', methods=['PUT'])
def update_reserva(id):
    # Consultar por id, a la clase Reserva.
    #  Se hace una consulta (query) para obtener (get) un registro por id
    reserva=Reserva.query.get(id)
 
    #  Recibir los datos a modificar
    nrosocio = request.json[nrosocio]
    nombre = request.json[nombre]
    horario = request[horario]
    deporte = request[deporte]

    # Del objeto resultante de la consulta modificar los valores  
    Reserva.nrosocio=nrosocio
    Reserva.nombre=nombre
    Reserva.horario=horario
    Reserva.deporte=deporte
    #  Guardar los cambios
    db.session.commit()
   # Para ello, usar el objeto reserva_schema para que convierta
   # con jsonify el dato recién eliminado que son objetos a JSON  
    return rango_schema.jsonify(Reserva)


# BLOQUE PRINCIPAL
if __name__== "__main__":
    app.run(debug=True)