
#! coding: latin-1

# Lee datos desde un archivo, los multiplica por 2 y
# los escribe en otro archivo.

# Apertura del archivo.
flec= open('datos.txt','r')
fesc= open('resultados.txt','w')

cad="a"	# Para forzar la entrada al ciclo.
while len(cad)>0:
# Lectura desde archivo (se lee como cadena):
  cad = flec.readline()
  if len(cad)>0:	    # Al llegar a EOF, regresa una cadena vacía.
    arre = cad.split(',')	# Para separar cada número.
    
    fesc.write('Los números multiplicados por 2 son: \n')
    for num in arre:
      num2= int(num) * 2
      salida= str(num2)+'\n'
      fesc.write(salida)

# Cierra archivos.
flec.close()
fesc.close()
print('Terminé lectura y escritura de archivo')
