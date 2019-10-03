# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""
def func(cad):
    res=cad[0]
    resaux=[]
    m=0
    for i in range(1,len(cad)):
        if cad[i-1]<=cad[i]:
            res=res+cad[i] 
        else:
            resaux.append(res)
            res=cad[i]
    resaux.append(res)
    for j in range(len(resaux)):
        if len(resaux[j])>len(resaux[m]):
            m=j
    return resaux[m]

def lectura(archivo):
    with open(archivo) as lineas:
        lista=lineas.readlines()
    fesc=open('Resultado.txt','w')
    for word in lista:
       fesc.write(word + ' ')
       fesc.write(func(word) + '\n \n')
       
      
        
lectura('ArchivoDatos.txt')
    

