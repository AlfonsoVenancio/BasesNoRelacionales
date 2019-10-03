# -*- coding: utf-8 -*-
"""
Ej. 1.2: Listas básico.

"""

import random

#Genera la lista de califs. de manera aleatoria.
#Se guardan como float, con un decimal que puede ser distinto de 0.
califs = [round(random.uniform(6, 10),1) for i in range(0,5)]
print("Califs.: ",califs)

porcentajes = [.1,.2,.23,.3,.17]

prom = [c*p for c,p in zip(califs, porcentajes)]

result = round(sum(prom),1)

print("Promedio (redondeado): ",result)
