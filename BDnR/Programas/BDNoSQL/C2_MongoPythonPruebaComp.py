
#Conexion al servidor de mongo.
from pymongo import MongoClient as Connection
connection = Connection('localhost',27017)

#Conexion a la BD.
db = connection.ejemplo

#Obtencion e impresion de los datos de prueba.
coll = db.emp
for doc in coll.find():
	print(doc)

#Alta de un nuevo departamento.
claveDep = int(input('Escribe la clave del depto.: '))
nombreDep = input('Escribe el nombre del depto.: ')

#Lo guarda en la BD.
u= {"depId": claveDep, "nomDep": nombre Dep, "emps":""};
db.emp.save(u);

#Obtencion e impresion de los datos de prueba.
coll = db.emp
for doc in coll.find():
	print(doc)

