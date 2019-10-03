# Programa de prueba de la conexion Python-Cassandra.

# Instalar el driver de Python para comunicarse con Cassandra con
# los siguientes pasos:
# 1. Abrir una terminal del sistema (la llamaremos CMD), situarse 
# en la carpeta C:/Python34/Scripts/
# 2. Ejecutar la siguiente instruccion:
#      pip install dse-driver==2.0.0 --user
# Ejecutar las instrucciones del siguiente archivo (el cual 
# sirve para crear la BD de prueba de la conexion 
# Python-Cassandra):
#    C2_CassandraPython_BDdePrueba.txt

# Colocar en C:/BDnR/Programas/Python al presente programa.
# En CMD situarse en la carpeta: C:/BDnR/Programas/Python.
# Ejecutar la instruccion: python C2_CassandraPythonPrueba.py
# (o c:\python34\python C2_CassandraPythonPrueba.py)
# Con lo anterior se ejecutara este programa.

# PROGRAMA:
# Biblioteca con los objetos de conexion Python-Cassandra.
from cassandra.cluster import Cluster

# Conexion a Cassandra.
cluster = Cluster()
session = cluster.connect('mykeyspace')

# Lee e imprime en terminal los datos de la BD.
rows = session.execute('SELECT * from users')
print()
print()
print('Los valores en la tabla son:')
for row in rows:
    print (row.user_id, row.fname, row.lname)

# Pide los datos para dar de alta en la BD a un nuevo usuario.
print('Alta de nuevo usuario:')
id = input('Escribe la clave: ')	
fname = input('Escribe el nombre: ')
lname = input('Escribe el apellido: ')

# Inserta en la BD al nuevo usuario.
session.execute("insert into users(user_id, fname, lname) values (%s, %s, %s)", (int(id), fname, lname) )

# Lee de nuevo los datos desde la BD para verificar que todo
# esta bien.
print()
rows = session.execute('SELECT * from users')
print('Los valores en la tabla son:')
for row in rows:
    print (row.user_id, row.fname, row.lname)



