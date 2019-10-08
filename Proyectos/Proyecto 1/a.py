import pymongo
import json
import yaml
import datetime
import matplotlib.pyplot as pyplot

config = yaml.load(open("config.yaml",'r'), Loader=yaml.Loader)

def init_conexion():
    cliente = pymongo.MongoClient(config['Mongo']['Direccion'])
    base = cliente[config['Mongo']['Base']]
    coleccionAcciones = base[config['Mongo']['ColeccionAcciones']]
    coleccionDividendos = base[config['Mongo']['ColeccionDividendos']]
    return {"Cliente":cliente, "Base": base, "Acciones":coleccionAcciones, "Dividendos": coleccionDividendos}

def inserta_documentos(nombre_coleccion, path_documentos):
    conexion = init_conexion()
    documentos = open(path_documentos,'r').read().split("\n")
    coleccion = conexion[nombre_coleccion]
    for documentoJSON in documentos:
        documento = json.loads(documentoJSON)
        documento["Fecha"] = datetime.datetime.strptime(documento["Fecha"],"%Y-%M-%d")
        coleccion.insert_one(documento)
    print(len(documentos),"insertados a la coleccion",nombre_coleccion)

def consulta_general(nombre_coleccion, parametros_filtrado, parametros_impresion, sort_field = None, descending = False):
    conexion = init_conexion()
    coleccion = conexion[nombre_coleccion]
    result = coleccion.find(parametros_filtrado, parametros_impresion)
    if sort_field is not None:
        return result.sort(sort_field, -1 if descending else 1)
    return result

def precio_promedio_accion(id_accion, inicio_periodo, fin_periodo):
    acumulado = 0.0
    dias = 0
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id" : id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id":0, "CostoAccion" : 1, "Fecha" : 1 }
    documentos = consulta_general("Acciones", filtrado, impresion)
    for documento in documentos:
        acumulado += documento["CostoAccion"]
        dias += 1
    return acumulado/dias

def precio_max_accion(id_accion, inicio_periodo, fin_periodo): 
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id" : id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id":0, "CostoAccion" : 1, "Fecha" : 1 }
    documentos = consulta_general("Acciones", filtrado, impresion, "CostoAccion", True)
    return documentos.next()["CostoAccion"]

def precio_min_accion(id_accion, inicio_periodo, fin_periodo): 
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id" : id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id":0, "CostoAccion" : 1, "Fecha" : 1 }
    documentos = consulta_general("Acciones", filtrado, impresion, "CostoAccion")
    return documentos.next()["CostoAccion"]

def mejor_accion_empresa(nombre_empresa, fecha):
    fecha_accion = datetime.datetime.strptime(fecha, "%Y-%M-%d")
    filtrado = {"Empresa" : nombre_empresa, "Fecha":fecha_accion}
    impresion = {"_id":0}
    documentos = consulta_general("Acciones", filtrado, impresion, "CostoAccion", True)
    return documentos.next()

def pago_total_dividendo(id_accion, inicio_periodo, fin_periodo):
    acumulado = 0.0
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id" : id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id":0, "Pago" : 1}
    documentos = consulta_general("Dividendos", filtrado, impresion)
    for documento in documentos:
        acumulado += documento["Pago"]
    return acumulado

def prepara_documentos(documentos, llave_agrupamiento):
    diccionario = {}
    for documento in documentos:
        valor_llave = documento[llave_agrupamiento]
        if valor_llave not in diccionario:
            diccionario[valor_llave] = {}
        for llave, valor in documento.items():
            if llave != llave_agrupamiento:
                if llave not in diccionario[valor_llave]:
                    diccionario[valor_llave][llave] = []
                else:
                    diccionario[valor_llave][llave].append(valor)
    return diccionario

def grafica_costo_acciones():
    filtrado = {}
    impresion = {"_id": 0, "Id": 1, "CostoAccion": 1}
    documentos = consulta_general("Acciones", filtrado, impresion)
    diccionario_valores = prepara_documentos(documentos, "Id")
    pyplot.figure()
    pyplot.title("Costo de la accion")
    pyplot.xlabel("Días")
    pyplot.ylabel("Costo de la acción")
    for accion, valores_accion in diccionario_valores.items():
        for valores in valores_accion.values():
            pyplot.plot(valores, label = accion)
    pyplot.legend()
    pyplot.show()

def grafica_costo_accion(id_accion, inicio_periodo, fin_periodo):
    fecha_inicio = datetime.datetime.strptime(inicio_periodo, "%Y-%M-%d")
    fecha_fin = datetime.datetime.strptime(fin_periodo, "%Y-%M-%d")
    filtrado = {"Id": id_accion, "Fecha":{"$gte":fecha_inicio, "$lt":fecha_fin}}
    impresion = {"_id": 0, "Id": 1, "CostoAccion": 1}
    documentos = consulta_general("Acciones", filtrado, impresion)
    diccionario_valores = prepara_documentos(documentos, "Id")
    pyplot.figure()
    pyplot.title("Costo de la accion")
    pyplot.xlabel("Días")
    pyplot.ylabel("Costo de la acción")
    for accion, valores_accion in diccionario_valores.items():
        for valores in valores_accion.values():
            pyplot.plot(valores, label = accion)
    pyplot.legend()
    pyplot.show()

def grafica_pago_dividendos(ids_acciones, inicio_periodo, fin_periodo):
    pagos = []
    for id_accion in ids_acciones:
        pagos.append(pago_total_dividendo(id_accion, inicio_periodo, fin_periodo))
    pyplot.figure()
    pyplot.title("Pago total de dividendos")
    pyplot.xlabel("Acciones")
    pyplot.ylabel("Pago total de dividendos en el periodo")
    pyplot.bar(ids_acciones, pagos)
    pyplot.show()


#inserta_documentos("Acciones", "acciones.jsonl")
#inserta_documentos("Dividendos","dividendos.jsonl")

print(precio_promedio_accion("PEME1","2015-01-01","2016-01-01"))
print(precio_max_accion("PEME1","2015-01-01","2016-01-01"))
print(precio_min_accion("PEME1","2015-01-01","2016-01-01"))
print(mejor_accion_empresa("PEMEX","2016-05-20"))
print(pago_total_dividendo("PEME1","2015-01-01","2016-01-01"))
grafica_costo_acciones()
grafica_costo_accion("PEME1","2015-01-01","2016-01-01")
grafica_pago_dividendos(["PEME1", "PEME5"],"2015-01-01","2016-01-01")