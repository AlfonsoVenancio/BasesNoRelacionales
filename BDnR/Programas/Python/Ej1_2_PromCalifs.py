# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 13:33:42 2019

@author: psdist
"""

import random

#Genera las califs.
n=5
califs=[]
for i in range(n):
  c= float(random.randint(5,10))
  califs.append(c)
print(califs)

#Porcentajes.
p=[0.1, 0.2, 0.23, 0.3, 0.17]
print(p)

#Calcula el promedio ponderado.
prom= 0
for i in range(n):
  prom += califs[i] * p[i]

print("Promedio (con decimales):" + str(prom))
