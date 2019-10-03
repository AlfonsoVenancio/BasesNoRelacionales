# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 19:31:48 2018

@author: flopezg
"""

x = int(input("Introduce un número: "))
if x < 0:
	x = 0
	print('Negativo cambiado a cero')
elif x == 0:
	print('Cero')
elif x == 1:
	print('Uno')
else:	
	print("Más")

