# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 14:12:25 2019

Ej. 1.3: manejo de tuplas.
@author: psdist
"""

#Función "tipo Java"
def tuplaPares(t):
  resp=[]
  for i in range(0, len(t), 2):
    resp.append(t[i])
  return tuple(resp)

#Función usando tuplas.
def tuplaPares2(t):
  resp=()
  for i in range(0, len(t), 2):
    resp += (t[i],)
  return resp

#Función al estilo python
def tuplaPares3(t):
  return t[::2]

#Uso.
tupla= ('Yo', 'mi', 'a', 'prueba', 'tupla')
print("Tupla:",tupla)
#print("Resultado:", tuplaPares(tupla))
#print("Resultado:", tuplaPares2(tupla))
print("Resultado:", tuplaPares3(tupla))










