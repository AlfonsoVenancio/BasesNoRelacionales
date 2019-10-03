# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 13:19:05 2019

Ej. 1.5: devuelve como diccionario las palabras que aparecen dentro de una
cadena dada como parámetro, junto con sus ocurrencias.

@author: psdist
"""
def palabras(cad):
  #Separa cada palabra y las entrega en una lista.
  lista= cad.split()
  print(lista)
  
  #Recorre la lista, construye el diccionario y cuenta cada palabra.
  dic= {}
  for palabra in lista:
    if palabra in dic.keys():
      dic[palabra] += 1
    else:
      dic[palabra] = 1
  
  return dic
    
#Prog. principal.
cad= input("Dame la cadena:")
dic= palabras(cad)
print("resul.:",dic)


